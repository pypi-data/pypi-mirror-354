from typing import List, Optional

from filedata.file import FileInspection
from pydantic import BaseModel


class FileInfo(BaseModel):
    filename: Optional[str] = None
    md5: Optional[str] = None
    content: Optional[str] = None
    snapshots: Optional[List[str]] = None


class FileContentResult(BaseModel):
    meta: FileInspection
    content: str
    snapshots: List[str]
    filename: Optional[str] = None
    size: Optional[int] = None
