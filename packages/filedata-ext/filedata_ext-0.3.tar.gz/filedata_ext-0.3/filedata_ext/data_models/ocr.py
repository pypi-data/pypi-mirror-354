from typing import List, Optional

from filedata.image import OCRRegion
from pydantic import BaseModel


class OCRMeta(BaseModel):
    file_link: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class OCRCache(BaseModel):
    filename: Optional[str] = None
    md5: Optional[str] = None
    meta: Optional[List[OCRMeta]] = None
    ocr_result: Optional[List[List[OCRRegion]]] = None
    file_link: Optional[str] = None
