import copy
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field
from typing_extensions import Self

from ....__types import DictData
from .utils import get_node, get_pipeline


class NodeDeps(BaseModel):
    name: str
    trigger_rule: Optional[str] = Field(default=None)


class Node(BaseModel):
    """Node model."""

    name: str = Field(description="A node name.")
    pipeline_name: Optional[str] = Field(
        default=None, description="A pipeline name of this node."
    )
    desc: Optional[str] = Field(default=None)
    upstream: list[NodeDeps] = Field(default_factory=list)
    operator: str = Field(description="An node operator.")
    task: str = Field(description="A node task.")
    params: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_conf(cls, name: str, path: Path) -> Self:
        """Construct Node model from an input node name and config path."""
        data: DictData = get_node(name=name, path=path)

        if (t := data.pop("type")) != cls.__name__:
            raise ValueError(f"Type {t!r} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(data)
        return cls.model_validate(obj=loader_data)


class Lineage(BaseModel):
    inlets: list[NodeDeps] = Field(default_factory=list)
    outlets: list[NodeDeps] = Field(default_factory=list)


class Pipeline(BaseModel):
    """Pipeline model."""

    name: str = Field(description="A pipeline.")
    desc: Optional[str] = Field(
        default=None,
        description=(
            "A pipeline description that allow to write with markdown syntax."
        ),
    )
    nodes: dict[str, Node] = Field(
        default_factory=list, description="A list of Node model."
    )
    tags: list[str] = Field(default_factory=list)

    @classmethod
    def from_conf(cls, name: str, path: Path) -> Self:
        """Construct Pipeline model from an input pipeline name and config path.

        :param name: (str) A pipeline name that want to search from config path.
        :param path: (Path) A config path.

        :rtype: Self
        """
        data: DictData = get_pipeline(name=name, path=path)

        if (t := data.pop("type")) != cls.__name__:
            raise ValueError(f"Type {t!r} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(data)
        loader_data["name"] = name

        return cls.model_validate(obj=loader_data)

    def node(self, name: str) -> Node:
        """Get the Node model with pass the specific node name."""
        return self.nodes[name]

    def lineage(self) -> list[list[str]]:
        """Generate the Node lineage with its upstream field."""

        if not self.nodes:
            return []

        # Build reverse adjacency list and in-degree count in one pass
        in_degree = {}
        dependents = {}  # node -> [nodes that depend on it]

        # Initialize
        for node in self.nodes:
            in_degree[node] = 0
            dependents[node] = []

        # Build graph
        for node, config in self.nodes.items():
            if config.upstream:
                for upstream in config.upstream:
                    upstream_name = upstream.name

                    # Add upstream node if not seen before
                    if upstream_name not in in_degree:
                        in_degree[upstream_name] = 0
                        dependents[upstream_name] = []

                    # Update relationships
                    in_degree[node] += 1
                    dependents[upstream_name].append(node)

        # Kahn's algorithm with level-by-level processing
        result = []
        current_level = [
            node for node, degree in in_degree.items() if degree == 0
        ]

        while current_level:
            current_level.sort()  # For consistent output
            result.append(current_level[:])  # Shallow copy

            next_level = []
            for node in current_level:
                # Decrease in-degree for all dependents
                for dependent in dependents[node]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_level.append(dependent)

            current_level = next_level

        # Cycle detection
        if sum(in_degree.values()) > 0:
            raise ValueError("Circular dependency detected")

        return result
