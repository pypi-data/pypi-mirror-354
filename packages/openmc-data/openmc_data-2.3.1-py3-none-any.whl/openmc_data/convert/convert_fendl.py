#!/usr/bin/env python3

"""
Download FENDL ACE files from the IAEA and convert it to a HDF5 library for use with OpenMC..
"""

import argparse
import ssl
import subprocess
import warnings
from pathlib import Path
from shutil import rmtree
from textwrap import dedent
from urllib.parse import urljoin

import openmc.data
from openmc_data import download, all_release_details, calculate_download_size, get_file_types


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


parser = argparse.ArgumentParser(description=__doc__, formatter_class=CustomFormatter)
parser.add_argument(
    "-d",
    "--destination",
    type=Path,
    default=None,
    help="Directory to create new library in",
)
parser.add_argument(
    "--download", action="store_true", help="Download files from IAEA-NDS"
)
parser.add_argument(
    "--no-download",
    dest="download",
    action="store_false",
    help="Do not download files from IAEA-NDS",
)
parser.add_argument("--extract", action="store_true", help="Extract tar/zip files")
parser.add_argument(
    "--no-extract",
    dest="extract",
    action="store_false",
    help="Do not extract tar/zip files",
)
parser.add_argument(
    "--libver",
    choices=["earliest", "latest"],
    default="earliest",
    help="Output HDF5 versioning. Use "
    "'earliest' for backwards compatibility or 'latest' for "
    "performance",
)
parser.add_argument(
    "-r",
    "--release",
    choices=["3.2c", "3.2b", "3.2a", "3.2", "3.1d", "3.1a", "3.1", "3.0", "2.1"],
    default="3.2c",
    help="The nuclear data library release version. The currently supported "
    "options are 3.2c 3.2b, 3.2a, 3.2, 3.1d, 3.1a, 3.1, 3.0, and 2.1",
)
parser.add_argument(
    "-p",
    "--particles",
    choices=["neutron", "photon"],
    nargs="+",
    default=["neutron", "photon"],
    help="Incident particles to include",
)
parser.add_argument(
    "--cleanup",
    action="store_true",
    help="Remove download directories when data has been processed",
)
parser.add_argument(
    "--no-cleanup",
    dest="cleanup",
    action="store_false",
    help="Do not remove download directories when data has been processed",
)
parser.set_defaults(download=True, extract=True, cleanup=False)
args = parser.parse_args()


# =============================================================================
# FUNCTIONS FOR DEALING WITH SPECIAL CASES
#
# Each of these functions should take a Path object which points to the file
# The function should return a bool which determines whether the file should be
# ignored.


def fendl30_k39(file_path):
    """Function to check for k-39 error in FENDL-3.0"""
    if "Inf" in open(file_path, "r").read():
        ace_error_warning = """
        {} contains 'Inf' values within the XSS array
        which prevent conversion to a HDF5 file format. This is a known issue
        in FENDL-3.0. {} has not been added to the cross section library.
        """.format(
            file_path, file_path.name
        )
        err_msg = dedent(ace_error_warning)
        return {"skip_file": True, "err_msg": err_msg}
    else:
        return {"skip_file": False}


def check_special_case(particle_details, script_step):
    """
    Helper function for checking if there are any special cases defined:
    Returns the special Cases relevant to a specific part of the script.
    If there are no special cases, return an empty dict
    """
    if "special_cases" in particle_details:
        if script_step in particle_details["special_cases"]:
            return particle_details["special_cases"][script_step]
    return {}


def main():

    library_name = "fendl"
    file_types = get_file_types(args.particles)
    cwd = Path.cwd()

    ace_files_dir = cwd.joinpath("-".join([library_name, args.release, "ace"]))
    endf_files_dir = cwd.joinpath("-".join([library_name, args.release, "endf"]))

    download_path = cwd.joinpath("-".join([library_name, args.release, "download"]))
    # the destination is decided after the release is know to avoid putting
    # the release in a folder with a misleading name
    if args.destination is None:
        args.destination = Path("-".join([library_name, args.release, "hdf5"]))

    # This dictionary contains all the unique information about each release.
    # This can be extended to accommodate new releases
    release_details = all_release_details[library_name]

    # todo refactor this into the release dictionary
    if args.release == "3.0":
        release_details[args.release]["neutron"]['ace']["special_cases"] = {
            "process": {"19K_039.ace": fendl30_k39}
        }

    # Warnings to be printed at the end of the script.
    output_warnings = []

    # ==============================================================================
    # DOWNLOAD FILES FROM IAEA SITE

    if args.download:
        calculate_download_size(library_name, args.release, args.particles, file_types, 'GB')

        for particle in args.particles:
            particle_details = release_details[args.release][particle][file_types[particle]]
            for f in particle_details["compressed_files"]:
                download(
                    urljoin(particle_details["base_url"], f),
                    as_browser=True,
                    context=ssl._create_unverified_context(),
                    output_path=download_path / particle,
                )

    # ==============================================================================
    # EXTRACT FILES FROM ZIP
    if args.extract:
        for particle in args.particles:

            particle_details = release_details[args.release][particle][file_types[particle]]

            special_cases = check_special_case(particle_details, "extract")

            if file_types[particle] == "ace":
                extraction_dir = ace_files_dir
            elif file_types[particle] == "endf":
                extraction_dir = endf_files_dir

            for f in particle_details["compressed_files"]:
                # Check if file requires special handling
                if f in special_cases:
                    ret = special_cases[f](Path(f))
                    if "err_msg" in ret:
                        output_warnings.append(ret["err_msg"])
                    if ret["skip_file"]:
                        continue

                # Extract files, the fendl release was compressed using type 9 zip format
                # unfortunatly which is incompatible with the standard python zipfile library
                # therefore the following system command is used
                subprocess.call(
                    ["unzip", "-o", download_path / particle / f, "-d", extraction_dir]
                )

        if args.cleanup and download_path.exists():
            rmtree(download_path)

    # ==============================================================================
    # GENERATE HDF5 LIBRARY

    library = openmc.data.DataLibrary()

    for particle in args.particles:
        # Create output directories if it doesn't exist
        particle_destination = args.destination / particle
        particle_destination.mkdir(parents=True, exist_ok=True)

        particle_details = release_details[args.release][particle][file_types[particle]]

        # Get dictionary of special cases for particle
        special_cases = check_special_case(particle_details, "process")

        if particle == "neutron":
            # Get a list of all ACE files
            neutron_files = ace_files_dir.glob(
                release_details[args.release]["neutron"][file_types[particle]]["ace_files"]
            )

            # excluding files ending with _ that are
            # old incorrect files kept in the release for backwards compatability
            neutron_files = [
                f
                for f in neutron_files
                if not f.name.endswith("_") and not f.name.endswith(".xsd")
            ]

            for filename in sorted(neutron_files):
                # Handling for special cases
                if filename.name in special_cases:
                    ret = special_cases[filename.name](filename)
                    if "err_msg" in ret:
                        output_warnings.append(ret["err_msg"])
                    if ret["skip_file"]:
                        continue

                print(f"Converting: {filename}")
                data = openmc.data.IncidentNeutron.from_ace(filename)

                # Export HDF5 file
                h5_file = particle_destination / f"{data.name}.h5"
                print(f"Writing {h5_file}...")
                data.export_to_hdf5(h5_file, "w", libver=args.libver)

                # Register with library
                library.register_file(h5_file)

            # Remove the ace files if required
            if args.cleanup and ace_files_dir.exists():
                rmtree(ace_files_dir)

        elif particle == "photon":

            photon_files = endf_files_dir.glob(
                release_details[args.release]["photon"][file_types[particle]]["endf_files"]
            )

            for photo_path in sorted(photon_files):

                # Check if file requires special handling
                if photo_path.name in special_cases:
                    ret = special_cases[photo_path.name](photo_path)
                    if "err_msg" in ret:
                        output_warnings.append(ret["err_msg"])
                    if ret["skip_file"]:
                        continue

                print(f"Converting: {photo_path}")
                evaluations = openmc.data.endf.get_evaluations(photo_path)
                for ev in evaluations:
                    # Export HDF5 file
                    data = openmc.data.IncidentPhoton.from_endf(ev)
                    h5_file = particle_destination / f"{data.name}.h5"
                    print(f"Writing {h5_file}...")
                    data.export_to_hdf5(h5_file, "w", libver=args.libver)

                # Register with library
                library.register_file(h5_file)

            # Remove the ENDF files if required
            if args.cleanup and endf_files_dir.exists():
                rmtree(endf_files_dir)

    # Write cross_sections.xml
    print("Writing ", args.destination / "cross_sections.xml")
    library.export_to_xml(args.destination / "cross_sections.xml")

    # Print any warnings
    for warning in output_warnings:
        warnings.warn(warning)


if __name__ == "__main__":
    main()
