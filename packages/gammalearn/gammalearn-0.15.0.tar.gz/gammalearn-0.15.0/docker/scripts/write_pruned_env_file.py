#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict

from ruamel.yaml import YAML


def list_of_dict_to_merged_list_of_unit_dict(list_of_dict):
    """[{"a": [1, 2], "b": [3]}, {"a": [4, 5]}] -> [{"a": [1, 2, 4, 5]}, {"b": [3]}]"""
    # from a list of dicts, first create a dictionary with all keys, and all values merged together in a list
    new_env_dict_deps = defaultdict(list)
    for dict_dep in [d for d in list_of_dict if d]:  # filter out empty lists
        for dep_key, deps in dict_dep.items():
            new_env_dict_deps[dep_key].extend(deps if isinstance(deps, list) else [deps])

    # now split the dict to a list of dicts that only have a single key
    return [{dep_key: deps} for dep_key, deps in new_env_dict_deps.items()]


def prune_pinned_specs(pinned_specs, specs):
    pruned_specs = []

    # handle conda dependencies that are just string in the list
    for dep in [dep for dep in specs if isinstance(dep, str)]:
        search_dep = (
            re.split("[><=]", dep)[0].lower().replace(" ", "")
        )  # lower to ignore case, conda and pip are case insensitive, replace to remove whitespaces
        for pinned_dep in pinned_specs:
            if (
                # only search in the "same level" in the specifications
                # pip dependencies for instance are at a "lower level" than conda dependencies
                # because they are in a nested dictionary, handled in next section
                isinstance(pinned_dep, str) and search_dep == pinned_dep.split("=")[0].lower().replace(" ", "")
            ):
                if pinned_dep not in pruned_specs:
                    pruned_specs.append(pinned_dep)
                break
        else:
            raise ValueError("Could not find dependency {} in pinned dependencies {}".format(dep, pinned_specs))

    # now handle "lower level" dependencies: dependencies that are in a dictionary
    # eg "pip" dependencies are in a dict {"pip": [pip_dep_1, pip_dep_2, ...]}
    for dep_dict in [dep for dep in specs if isinstance(dep, dict)]:
        # Search through the pinned specs for the same dependency section
        dep_key = list(dep_dict.keys())[0]  # this should only be "pip"
        for pinned_dep_dict in [spec for spec in pinned_specs if isinstance(spec, dict)]:
            # compare dict keys (take 1st key as there should be only one!) to make sure we get the same dependency
            # There should be only 1 key: "pip"
            if list(pinned_dep_dict.keys())[0] == dep_key:
                pruned_specs.append(
                    {
                        dep_key: prune_pinned_specs(
                            pinned_dep_dict[dep_key],
                            dep_dict[dep_key],
                        )
                    }
                )
                break
        else:
            raise ValueError("Could not find {} in pinned_spec {}".format(dep, pinned_specs))

    return pruned_specs


def main():
    parser = argparse.ArgumentParser(
        description="Create an environment.yml file with dependencies in `old_env`, "
        "pruned to those specified in the input files."
    )
    parser.add_argument(
        "--old_env",
        "-e",
        dest="old_env_file",
        required=True,
        help='Old environment files with pinned versions, obtained with "micromamba env export"',
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        dest="new_env_file",
        help="Path to a file where to write the pruned environment",
        default="pruned_env.yml",
    )
    parser.add_argument("-f", "--files", type=str, dest="env_files", nargs="+", help="")
    parser.add_argument(
        "-n",
        "--nodefaults",
        action=argparse.BooleanOptionalAction,
        dest="nodefaults",
        help="If --nodefaults is passed, then the nodefaults channel is set in the new environment channels",
    )
    args = parser.parse_args()

    yaml = YAML()
    yaml.indent(mapping=4, sequence=4, offset=2)
    yaml.width = 2**16  # very large to not wrap lines
    yaml.sort_keys = False

    with open(args.old_env_file, "r") as old_f:
        pinned_env = yaml.load(old_f)

    env_specs = []
    for env_file in args.env_files:
        with open(env_file, "r") as env_f:
            env_specs.append(yaml.load(env_f))

    # gather all conda dependencies
    # It doesn't matter if env1 and env2 have a specification for a particular "dep", eg numpy<1.9 and numpy<1.8
    # mamba will find a version that satisfies all specification, or make an error
    specs = [dep for specs in env_specs for dep in specs["dependencies"] if isinstance(dep, str)]
    # gather all pip (or other dependencies defined in a nested dict) dependencies
    nested_specs = [dep for specs in env_specs for dep in specs["dependencies"] if isinstance(dep, dict)]
    # re-order merged pip deps in a single list as expected in env.yaml, and add them to specs
    specs.extend(list_of_dict_to_merged_list_of_unit_dict(nested_specs))

    # environment name will be the one from initial environment
    pruned_env_specs = {
        "name": pinned_env["name"],
        "channels": pinned_env["channels"],
        "dependencies": prune_pinned_specs(
            pinned_env["dependencies"],
            specs,
        ),
    }

    # Check that specs do not contain channels missing from pinned specs
    for env in env_specs:
        for channel in env["channels"]:
            if channel != "nodefaults":
                assert (
                    channel in pinned_env["channels"]
                ), "Channel {} in new environment file not present in old environment channels {}".format(
                    channel, pinned_env["channels"]
                )

    # add nodefaults last
    if args.nodefaults:
        pruned_env_specs["channels"].append("nodefaults")
    with open(args.new_env_file, "w") as new_env_f:
        yaml.dump(pruned_env_specs, new_env_f)


if __name__ == "__main__":
    main()
