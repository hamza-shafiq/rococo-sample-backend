from dataclasses import dataclass, field
from typing import ClassVar, Optional
from rococo.models import VersionedModel


@dataclass
class Task(VersionedModel):
    use_type_checking: ClassVar[bool] = True
    person_id: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    completed: bool = field(default=False)
