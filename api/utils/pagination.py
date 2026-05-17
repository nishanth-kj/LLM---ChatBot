from dataclasses import dataclass
from typing import List, Any
import math

@dataclass
class Page:
    content: List[Any]
    page_number: int
    page_size: int
    total_elements: int
    total_pages: int
    last: bool

    @staticmethod
    def create(content: List[Any], page_number: int, page_size: int, total_elements: int):
        total_pages = math.ceil(total_elements / page_size) if page_size > 0 else 0
        last = (page_number + 1) >= total_pages
        return Page(
            content=content,
            page_number=page_number,
            page_size=page_size,
            total_elements=total_elements,
            total_pages=total_pages,
            last=last
        )

    def to_dict(self):
        return {
            "content": self.content,
            "pageNumber": self.page_number,
            "pageSize": self.page_size,
            "totalElements": self.total_elements,
            "totalPages": self.total_pages,
            "last": self.last
        }
