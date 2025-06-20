from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, model_validator


class KnowledgeRow(BaseModel):
    """Knowledge Row that is stored in the database"""

    # id for this knowledge, auto-generated if not provided
    id: Optional[str] = None
    name: str
    description: str
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def generate_id(self) -> "KnowledgeRow":
        if self.id is None:
            from uuid import uuid4

            self.id = str(uuid4())
        return self

    def to_dict(self) -> Dict[str, Any]:
        _dict = self.model_dump(exclude={"last_updated"})
        _dict["last_updated"] = self.last_updated.isoformat() if self.last_updated else None
        return _dict