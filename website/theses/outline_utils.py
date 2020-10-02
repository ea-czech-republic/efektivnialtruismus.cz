from __future__ import annotations
import re
import logging
from typing import List, Type

from wagtail.core.rich_text import RichText

logger = logging.getLogger(__name__)


class _HeadingBlock:
    @staticmethod
    def _get_title(m):
        title = m.group("title")
        to_drop = ("<br/>", r"<h\d>", r"</h\d>", "<b>", r"</b>")
        for text in to_drop:
            title = re.sub(text, "", title)
        return title.strip()

    @staticmethod
    def _get_link(title):
        return title.lower().replace(" ", "-")

    @classmethod
    def _get_additional_context(cls, _value):
        if isinstance(_value, RichText):  # in case of using Preview
            _value = _value.source
        m = re.search("<h(?P<heading_size>\d)>(?P<title>.*)</h\d>", _value)
        if not m:
            return {}

        title = cls._get_title(m)
        return dict(
            title=title,
            link=cls._get_link(title),
            heading_size=m.group("heading_size"),
        )


class Heading:
    title: str
    link: str
    size: int

    def __init__(self, title, link, heading_size):
        self.title = title
        self.link = link
        self.size = int(heading_size)

    def _to_html(self):
        _html = (
            "<div class='row mb-1'><div class='col'>"
            f"<a href='#{self.link}'><b>{self.title}</b></a>"
            "</div></div>"
        )
        return _html

    @classmethod
    def get_outline_html(cls, headings: List[Heading]) -> str:
        return "".join(heading._to_html() for heading in headings)


class NestableHeading(Heading):
    size: int
    nested_headings: List[NestableHeading]

    def __init__(self, title, link, heading_size):
        super().__init__(title, link, heading_size)
        self.nested_headings = []

    @classmethod
    def _place_heading_into_structure(
        cls, heading: NestableHeading, structure: List[NestableHeading]
    ) -> List[NestableHeading]:
        if not structure:
            return [heading]

        if heading.size <= structure[-1].size:
            structure.append(heading)
            return structure

        _structure = cls._place_heading_into_structure(
            heading, structure[-1].nested_headings
        )
        structure[-1].nested_headings = _structure
        return structure

    @classmethod
    def _nest_headings(cls, headings: List[NestableHeading]) -> List[NestableHeading]:
        if not headings:
            return []

        structure = []
        for heading in headings:
            structure = cls._place_heading_into_structure(heading, structure)

        return structure

    def _to_html(self):
        nested_html = self.nested_to_html(self.nested_headings)
        _html = f"<li><a href='#{self.link}'>{self.title}</a>{nested_html}</li>"
        return _html

    @staticmethod
    def nested_to_html(nested_headings: List[NestableHeading]) -> str:
        _nested_htmls = "".join(_heading._to_html() for _heading in nested_headings)
        nested_html = (
            f'<ul style="list-style-type:disc;">{_nested_htmls}</ul>'
            if _nested_htmls
            else ""
        )
        return nested_html

    @classmethod
    def get_outline_html(cls, headings: List[NestableHeading]) -> str:
        headings_nested = cls._nest_headings(headings)
        return cls.nested_to_html(headings_nested)


class Outline:
    HEADING_TYPE: Type[Heading]

    @staticmethod
    def _get_raw_heading(_data):
        if isinstance(_data, tuple):
            keys = ("type", "value", "id")
            _data = dict(zip(keys, _data))

        if not isinstance(_data, dict):
            return None

        if _data["type"] == "heading_linkable":
            source = _data["value"]
            return _HeadingBlock._get_additional_context(source)
        return None

    def get_raw_headings(self, stream_data):
        return [self._get_raw_heading(data) for data in stream_data]

    def _get_headings(self, stream_data) -> List[Heading]:
        raw_headings = self.get_raw_headings(stream_data)
        return [self.HEADING_TYPE(**heading) for heading in raw_headings if heading]

    def get_outline(self, stream_data) -> str:
        headings = self._get_headings(stream_data)
        return self.HEADING_TYPE.get_outline_html(headings)


class FlatLinksOutline(Outline):
    HEADING_TYPE = Heading


class NestedOutline(Outline):
    HEADING_TYPE = NestableHeading
