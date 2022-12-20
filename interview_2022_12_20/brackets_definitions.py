from dataclasses import dataclass


@dataclass(frozen=True)
class BracketsDefinition:
    opening: str
    closing: str
