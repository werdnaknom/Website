import typing as t
from dataclasses import dataclass

@dataclass
class Page:
    title: str
    header: str
    processing_header: str


@dataclass
class PostProcessingPage(Page):
    task_urls: t.List[str]
    redirect_url: str
