#!/usr/bin/env python3

import argparse
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


def main():
    parser = argparse.ArgumentParser(description="Create an environment.yml from several environment yaml files.")
    parser.add_argument("-n", "--name", type=str, dest="name", default="base")
    parser.add_argument("-o", "--output", type=str, dest="output", required=True)
    parser.add_argument("-f", "--files", type=str, dest="env_files", nargs="+", help="")
    args = parser.parse_args()

    yaml = YAML()
    yaml.indent(mapping=2, sequence=2, offset=2)
    yaml.width = 2**16  # very large to not wrap lines
    yaml.sort_keys = False

    env_specs = []
    for env_file in args.env_files:
        with open(env_file, "r") as env_f:
            env_specs.append(yaml.load(env_f))

    # build list of conda dependencies (str in the dependencies list)
    new_env_deps = [
        dep for env in env_specs if env["dependencies"] for dep in env["dependencies"] if isinstance(dep, str)
    ]
    # Add the "nested" dependencies: dependencies in a nested dictionary like {"pip": [dep1, dep2, ...]}
    # the nested dependencies dict are merged together so all "pip" dependencies are under a single entry
    new_env_deps.extend(
        list_of_dict_to_merged_list_of_unit_dict(
            [dep for env in env_specs if env["dependencies"] for dep in env["dependencies"] if isinstance(dep, dict)]
        )
    )

    new_env = {
        "name": args.name,
        # Dict from keys to build {channel: None} while preserving order. Dict is converted back to list to conserve only keys
        "channels": list(dict.fromkeys([channel for env in env_specs for channel in env["channels"]])),
        "dependencies": new_env_deps,
    }

    with open(args.output, "w") as new_env_f:
        yaml.dump(new_env, new_env_f)


if __name__ == "__main__":
    main()
