from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, List

from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Mailable(ABC):
    _to_email: Optional[str] = None
    _to_cc: List[str] = field(default_factory=list)
    _to_bcc: List[str] = field(default_factory=list)

    _subject_line: str = ""
    _template_path: str = ""

    _context: Dict[str, any] = field(default_factory=dict)
    _attachments: List[str] = field(default_factory=list)

    def to(self, recipient_email: str):
        self._to_email = recipient_email
        return self

    def cc(self, *emails: str):
        self._to_cc.extend(emails)
        return self

    def bcc(self, *emails: str):
        self._to_bcc.extend(emails)
        return self

    def subject(self, subject_line: str):
        self._subject_line = subject_line
        return self

    def template(self, path: str):
        self._template_path = path
        return self

    def with_context(self, context_dict: Dict[str, any]):
        self._context.update(context_dict)
        return self

    def attach(self, file_path: str):
        self._attachments.append(file_path)
        return self

    @abstractmethod
    def build(self):
        """Subclasses define how the email is built."""
        pass

    def render(self, project_root: Optional[str] = PROJECT_ROOT) -> str:
        environment = Environment(
            loader=FileSystemLoader(project_root),
            autoescape=True,
        )

        template = environment.get_template(self._template_path)

        return template.render(**self._context)
