# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path
from typing import Any

from ddeutil.io import YamlEnvFl

from ....__types import DictData


def get_pipeline(name: str, path: Path) -> DictData:
    """Get Pipeline data that store on an input config path.

    :param name: A pipeline name that want to search and extract data from the
        config path.
    :param path: A config path.

    :rtype: DictData
    """
    d: Path
    for d in path.rglob("*"):
        if d.is_dir() and d.stem == name:
            cfile: Path = d / "config.yml"
            if not cfile.exists():
                raise FileNotFoundError(
                    f"Get pipeline file: {cfile.name} does not exist."
                )

            data: DictData = YamlEnvFl(path=cfile).read()
            if name not in data:
                raise ValueError(
                    f"Pipeline config does not set {name!r} config data."
                )
            elif "type" not in (pipeline_data := data[name]):
                raise ValueError(
                    "Pipeline config does not pass the `type` for validation."
                )

            nodes: dict[str, Any] = {}
            f: Path
            for f in d.rglob("*"):
                if not f.is_file():
                    continue

                if f.suffix not in (".yml", ".yaml"):
                    continue

                node_data = YamlEnvFl(path=f).read()
                if node_data:
                    for nn in node_data:

                        if not (t := node_data[nn].get("type")) or t != "Node":
                            continue

                        nodes[nn] = {
                            "name": nn,
                            "pipeline_name": name,
                            **node_data[nn],
                        }

            pipeline_data["nodes"] = nodes
            return pipeline_data

    raise FileNotFoundError(f"Does not found pipeline: {name!r} at {path}")


def get_node(name: str, path: Path) -> DictData:
    for file in path.rglob("*"):
        if file.is_file() and file.stem == name:
            if file.suffix in (".yml", ".yaml"):
                data = YamlEnvFl(path=file).read()
                if name not in data:
                    raise NotImplementedError

                return {
                    "name": name,
                    "pipeline_name": file.parent.name,
                    **data[name],
                }

            else:
                raise NotImplementedError(
                    f"Get node file: {file.name} does not support for file"
                    f"type: {file.suffix}."
                )
    raise FileNotFoundError(f"{path}/**/{name}.yml")
