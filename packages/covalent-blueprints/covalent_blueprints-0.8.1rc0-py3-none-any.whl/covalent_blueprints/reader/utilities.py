# Copyright 2024 Agnostiq Inc.
"""Utilities for processing Covalent scripts."""

from pprint import pformat
from typing import Callable, Dict

import covalent as ct
from covalent._workflow.lattice import Lattice

from covalent_blueprints.logger import bp_log

# pylint: disable=protected-access


def custom_build_graph(
    lattice_obj: Lattice, electrons: Dict[str, Callable], *args, **kwargs
) -> None:
    """Override the usual `build_graph` method of a lattice to update
    metadata.

    Args:
        lattice_: The lattice object to update.
    """
    bp_log.debug(
        "Running native build_graph on lattice\n\n%s",
        lattice_obj.workflow_function_string,
    )

    # Need task_packing "context" lke in `cc.dispatch`.
    old_task_packing = ct.get_config("sdk.task_packing")
    ct.set_config("sdk.task_packing", "true")

    # Calling via class avoids recursion errors in sublattice case.
    Lattice.build_graph(lattice_obj, *args, **kwargs)

    ct.set_config("sdk.task_packing", old_task_packing)

    # Update the transport graph created by original build_graph.
    _update_executor_data(lattice_obj, electrons)

    # Graph is already built. Avoid rebuilding during dispatch.
    _disable_build_graph(lattice_obj)


def _collect_executor_data(
    lattice_obj: Lattice, electrons: Dict[str, Callable]
) -> Dict[int, Dict]:
    """Create new executor data using states of script electrons."""
    # Map of electron names to updated metadata.
    electron_metadata_dict = {
        name: electron.electron_object.metadata.copy()  # type: ignore
        for name, electron in electrons.items()
    }

    bp_log.debug(
        "Script electron metadata dict:\n%s",
        pformat(electron_metadata_dict),
    )

    executor_data_all = {}

    # Strictly for debugging.
    task_groups_to_modify = {}  # type: ignore

    # Identify electron task groups and prepare metadata for them.
    for node_id in lattice_obj.transport_graph._graph.nodes:
        node_dict = lattice_obj.transport_graph._graph.nodes[node_id]

        name = node_dict["name"]
        bp_log.debug("Inspecting node %s ('%s')", node_id, name)

        # Clear leading ":sublattice:" prefix e.g.
        _name = name.split(":")[-1]
        if new_metadata := electron_metadata_dict.get(_name):
            bp_log.debug("Creating new metadata for node %s ('%s')", node_id, name)

            # Prepare metadata for the electron's task group.
            task_group_id = node_dict["task_group_id"]
            executor_data_all[task_group_id] = new_metadata["executor_data"]

            # Record the task group ID-name list for debugging.
            if node_id in task_groups_to_modify:
                task_groups_to_modify[node_id].append(name)
            else:
                task_groups_to_modify[node_id] = [name]

    bp_log.debug(
        "Collected executor data for task groups %s:\n%s",
        list(executor_data_all),
        pformat(executor_data_all),
    )
    bp_log.debug(
        "Task groups correspond to tasks: %s",
        task_groups_to_modify,
    )

    return executor_data_all


def _update_executor_data(lattice_obj: Lattice, electrons: Dict[str, Callable]) -> None:
    """Obtain new executor data and apply to transport graph."""
    executor_data_all = _collect_executor_data(lattice_obj, electrons)

    # Loop again to set metadata for task groups.
    for node_id in lattice_obj.transport_graph._graph.nodes:
        node_dict = lattice_obj.transport_graph._graph.nodes[node_id]

        tg_id = node_dict["task_group_id"]
        bp_log.debug("Checking task group %s", tg_id)

        if (executor_data := executor_data_all.get(tg_id)) is not None:
            # Update node's executor data according to its task group.
            bp_log.debug(
                "Setting 'metadata.executor_data' for task group %s ('%s'):\n%s\n",
                tg_id,
                node_dict["name"],
                executor_data,
            )
            node_dict["metadata"]["executor_data"] = executor_data


def _disable_build_graph(lattice_obj: Lattice) -> None:
    """Disable the build_graph method of a lattice object."""
    bp_log.debug(
        "Disabling build_graph on lattice %s ('%s') to prevent overwrite.",
        lattice_obj,
        lattice_obj.__name__,
    )
    setattr(lattice_obj, "build_graph", lambda *_, **__: None)
