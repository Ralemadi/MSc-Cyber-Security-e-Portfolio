from __future__ import annotations

import json
import threading
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from banking.services.audit_details import AuditDetails


#Represent one structured audit event after it is read from JSONL storage.
@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    actor: str
    action: str
    outcome: str
    details: dict[str, Any] = field(default_factory=dict)
    risk_score: int | None = None
    risk_reason: str | None = None


#Write structured JSONL audit events in a thread-safe
class AuditLogService:


    #Initialise this component with its required dependencies and local state.
    def __init__(self, audit_file: str | Path) -> None:
        self.audit_file = Path(audit_file)
        self._lock = threading.Lock()

    #Perform the internal normalise details step used by this workflow.
    @staticmethod
    def _normalise_details(
        details: AuditDetails | Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if details is None:
            return {}

        if isinstance(details, AuditDetails):
            return details.to_dict()

        return dict(details)


    def record(
        self,
        *,
        actor: str,
        action: str,
        outcome: str,
        details: AuditDetails | Mapping[str, Any] | None = None,
        risk_score: int | None = None,
        risk_reason: str | None = None,
    ) -> AuditRecord:
        record = AuditRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            actor=actor,
            action=action,
            outcome=outcome,
            details=self._normalise_details(details),
            risk_score=risk_score,
            risk_reason=risk_reason,
        )

        self.audit_file.parent.mkdir(parents=True, exist_ok=True)

        with self._lock:
            with self.audit_file.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        asdict(record),
                        ensure_ascii=False,
                        sort_keys=True,
                    )
                    + "\n"
                )

        return record

    def list_records(self, limit: int = 50) -> list[AuditRecord]:
        if limit <= 0 or not self.audit_file.exists():
            return []

        with self._lock:
            lines = self.audit_file.read_text(
                encoding="utf-8"
            ).splitlines()

        records: list[AuditRecord] = []

        for line in reversed(lines):
            if not line.strip():
                continue

            try:
                raw = json.loads(line)
                records.append(AuditRecord(**raw))
            except (json.JSONDecodeError, TypeError):
              
                continue

            if len(records) >= limit:
                break

        return records
