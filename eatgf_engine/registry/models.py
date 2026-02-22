from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict

class LifecycleState(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    ACTIVE = "Active"
    DEPRECATED = "Deprecated"
    SUNSET = "Sunset"
    RETIRED = "Retired"

class AuthorityClass(str, Enum):
    ISO27001 = "ISO27001"
    ISO42001 = "ISO42001"
    COBIT = "COBIT"
    NIST = "NIST"
    OTHER = "Other"

@dataclass
class RelationshipSet:
    implements: List[str] = field(default_factory=list)
    enforces: List[str] = field(default_factory=list)
    requires: List[str] = field(default_factory=list)

@dataclass
class Decomposition:
    clause: str
    justification: str

@dataclass
class Applicability:
    environments: List[str]
    ai_usage: str  # "All", "Conditional", etc.
    mandatory: bool

@dataclass
class Control:
    control_id: str
    domain: str
    primary_authority: str
    authority_class: AuthorityClass
    atomic_objective: str
    lifecycle_state: LifecycleState
    applicability: Applicability
    relationships: RelationshipSet
    decomposition: Optional[Decomposition] = None

@dataclass
class Registry:
    version: str
    controls: Dict[str, Control]
