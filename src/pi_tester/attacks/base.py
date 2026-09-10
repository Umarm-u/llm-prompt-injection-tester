"""Base attack module."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AttackPayload:
    """A single attack test case."""

    id: str
    name: str
    category: str
    owasp_llm_id: str
    system_prompt: str
    injection: str
    success_indicator: str
    description: str


class AttackLoader:
    """Loads attack payloads from JSON files."""

    def __init__(self, payload_dir: str | Path = "attack_payloads"):
        self.payload_dir = Path(payload_dir)

    def load(self, category: str) -> list[AttackPayload]:
        path = self.payload_dir / f"{category}.json"
        with open(path) as f:
            data = json.load(f)
        return [AttackPayload(**item) for item in data]

    def load_all(self) -> list[AttackPayload]:
        payloads: list[AttackPayload] = []
        for path in sorted(self.payload_dir.glob("*.json")):
            with open(path) as f:
                data = json.load(f)
            payloads.extend([AttackPayload(**item) for item in data])
        return payloads
