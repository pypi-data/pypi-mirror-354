# ruff: noqa: D100

# Standard
import datetime
import typing
from pathlib import Path

# Third party
import schema
import yaml
import networkx as nx

# First party
from .common import escape_chars
from .logger import logger

_TZ = datetime.timezone(datetime.timedelta()) # UTC

_YAML_SCHEMA = schema.Schema({
    "tasks": {
        str: {
            "cmd": str,
            schema.Optional("ncpu"): int,
            },
        },
    "deps": {
        str: str,
        },
})

class Workflow:
    """A class representing a workflow."""

    def __init__(self, tasks: dict[str, dict[str, str | int]],
                 deps: dict[str, str]) -> None:
        """Initialize the Workflow instance."""
        self._tasks = tasks
        self._deps = deps

    @property
    def sorted_task(self) -> list[str]:
        """Get the tasks sorted according to dependencies."""

        dag = nx.DiGraph()

        # Add nodes (tasks)
        dag.add_nodes_from(self._tasks.keys())

        # Add edges (dependencies)
        for task, dep in self._deps.items():
            if dep not in self._tasks:
                msg = f"Dependency '{dep}' for task '{task}' not found."
                raise ValueError(msg)
            dag.add_edge(dep, task)

        # Check for cycles
        if not nx.is_directed_acyclic_graph(dag):
            msg = "The workflow contains cycles."
            raise ValueError(msg)

        # Perform topological sort
        return list(nx.topological_sort(dag))

    @classmethod
    def from_dict(cls, data: dict[str, typing.Any]) -> "Workflow":
        """Create a Workflow instance from a dictionary."""

        # Validate the schema
        _YAML_SCHEMA.validate(data)

        # Create the Workflow instance
        return cls(**data)

    @classmethod
    def from_yaml(cls, yaml_file: Path) -> list["Workflow"]:
        """Load a workflow from a YAML file."""
        logger.debug(f"Loading workflow from {yaml_file}")

        # Load the YAML file
        with yaml_file.open(encoding="utf-8") as f:
            docs = list(yaml.safe_load_all(f))

        return [cls.from_dict(doc) for doc in docs if doc is not None]

    def to_bash(self, output_file: Path, *, tagline: bool = True) -> None:
        """Generate a bash script from the workflow."""
        logger.debug(f"Generating bash script into {output_file}")

        with output_file.open('w') as f:

            # Write shebang
            f.write("#!/bin/bash\n")

            # Write tag line
            if tagline:
                date = datetime.datetime.now(tz = _TZ)
                f.write(f"# Generated on {date} by HPC Wizard package.\n")

            # Write tasks
            for task in self.sorted_task:
                command = self._tasks[task]['cmd']
                f.write(f"{command}\n")

    def to_pegasus_dag(self, output_file:Path, *, tagline:bool=True) -> None:
        """Generate a DAG for Pegasus from the workflow."""
        logger.debug(f"Generating DAG into {output_file}")

        with output_file.open('w') as f:

            # Write tag line
            if tagline:
                date = datetime.datetime.now(tz = _TZ)
                f.write(f"# Generated on {date} by HPC Wizard package.\n")

            # Write tasks
            f.write("# Tasks\n")
            for name, task in self._tasks.items():
                ncpu = task.get('ncpu', 1)
                f.write(f"TASK {name} -c {ncpu} bash -c \"set -eo pipefail ; "
                        + escape_chars(str(task['cmd']), chars='"') + "\"\n")

            # Write dependencies
            f.write("\n")
            f.write("# Dependencies\n")
            for task1, task2 in self._deps.items():
                if task1 not in self._tasks:
                    msg = f"Dependency '{task2}' for task '{task1}' not found."
                    raise ValueError(msg)
                f.write(f"EDGE {task1} {task2}\n")
