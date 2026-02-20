from typing import Dict, Set
from .models import Registry, Control

class RegistryValidationError(Exception):
    pass

def validate_unique_control_ids(registry: Registry):
    ids = registry.controls.keys()
    if len(ids) != len(set(ids)):
        raise RegistryValidationError("Duplicate control_id detected.")

def validate_single_primary_authority(registry: Registry):
    for control in registry.controls.values():
        if not control.primary_authority:
            raise RegistryValidationError(
                f"{control.control_id} missing primary_authority."
            )

def validate_decomposition_limits(registry: Registry):
    clause_map: Dict[str, Dict[str, int]] = {}

    for control in registry.controls.values():
        if control.decomposition:
            clause = control.decomposition.clause
            domain = control.domain

            clause_map.setdefault(clause, {})
            clause_map[clause].setdefault(domain, 0)
            clause_map[clause][domain] += 1

    for clause, domain_counts in clause_map.items():
        for domain, count in domain_counts.items():
            if count > 2:
                raise RegistryValidationError(
                    f"Clause {clause} decomposed into {count} controls in domain {domain} (limit=2)."
                )

def validate_relationship_targets_exist(registry: Registry):
    all_ids: Set[str] = set(registry.controls.keys())

    for control in registry.controls.values():
        for target in (
            control.relationships.requires
            + control.relationships.implements
            + control.relationships.enforces
        ):
            if target not in all_ids:
                raise RegistryValidationError(
                    f"{control.control_id} references unknown control {target}"
                )

def validate_no_self_dependency(registry: Registry):
    for control in registry.controls.values():
        if control.control_id in control.relationships.requires:
            raise RegistryValidationError(
                f"{control.control_id} cannot require itself."
            )

def detect_requires_cycles(registry: Registry):
    """
    Detect cycles in the requires dependency graph (across all domains).
    Fail-fast if any cycle is found.
    """
    from enum import Enum

    class VisitState(Enum):
        UNVISITED = 0
        VISITING = 1
        VISITED = 2

    graph = {ctrl.control_id: ctrl.relationships.requires for ctrl in registry.controls.values()}
    state = {ctrl_id: VisitState.UNVISITED for ctrl_id in graph}
    path = []

    def dfs(node):
        state[node] = VisitState.VISITING
        path.append(node)
        for neighbor in graph[node]:
            if state[neighbor] == VisitState.UNVISITED:
                if dfs(neighbor):
                    return True
            elif state[neighbor] == VisitState.VISITING:
                # Cycle found
                cycle_start = path.index(neighbor)
                cycle_path = path[cycle_start:] + [neighbor]
                raise RegistryValidationError(
                    f"Cycle detected: {' → '.join(cycle_path)}"
                )
        state[node] = VisitState.VISITED
        path.pop()
        return False

    for node in graph:
        if state[node] == VisitState.UNVISITED:
            dfs(node)

def run_all_validations(registry: Registry):
    validate_unique_control_ids(registry)
    validate_single_primary_authority(registry)
    validate_decomposition_limits(registry)
    validate_relationship_targets_exist(registry)
    validate_no_self_dependency(registry)
    detect_requires_cycles(registry)
