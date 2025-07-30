#!/usr/bin/env python3
"""
Types example for IDA Domain API.

This example demonstrates how list all existing types from an IDA database.
"""

from pathlib import Path
import argparse
import ida_domain

parser = argparse.ArgumentParser(description="IDA Domain usage example, version {ida_domain.VersionInfo.api_version}")
parser.add_argument("-f", "--input-file", help="Binary input file to be loaded", type=str, required=True)
args = parser.parse_args()

example_til_path = (Path(__file__).parent.parent / "tests" / "resources" / "example.til").resolve()

db = ida_domain.Database()
if db.open(args.input_file):
    # Iterate names from external til
    for name in db.types.get_names(str(example_til_path)):
        print(name)

    # Iterate names from local til
    for name in db.types.get_names():
        print(name)

    #FIXME, why these are not working
    # Iterate named types from external til
    # for type_info in db.types.get_all(ida_domain.types.TypeKind.NAMED, str(example_til_path)):
    #     print(f"{type_info.name}")

    # Iterate named types from local til
    # for type_info in db.types.get_types():
    #     print(f"{type_info.name}")

    # Iterate ordinal types
    # for type_info in db.types.get_types(ida_domain.types.TypeKind.NUMBERED):
    #     print(f"{type_info.name}")

    db.close(False)
