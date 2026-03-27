from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias


class TextStyleName(str, Enum):
    H1 = "h1"
    H2 = "h2"
    P = "p"
    CODE = "code"


class FigmaNodeType(str, Enum):
    TEXT = "TEXT"
    FRAME = "FRAME"


@dataclass(frozen=True, slots=True)
class TextSegment:
    characters: str | list[str]
    textStyleName: TextStyleName

    def as_json_dict(self) -> dict[str, object]:
        return {
            "characters": self.characters,
            "textStyleName": self.textStyleName.value,
        }


@dataclass
class TextNode:
    text_segments: list[TextSegment] = field(default_factory=list)

    def append(self, segment: TextSegment) -> None:
        self.text_segments.append(segment)

    def as_json_dict(self) -> dict[str, object]:
        return {
            "type": FigmaNodeType.TEXT,
            "textSegments": [s.as_json_dict() for s in self.text_segments],
        }


@dataclass
class FrameNode:
    children: list[TextNode] = field(default_factory=list)

    def as_json_dict(self) -> dict[str, object]:
        return {
            "type": FigmaNodeType.FRAME,
            "name": "Code",
            "children": [c.as_json_dict() for c in self.children],
        }


def frame_node(*children: TextNode) -> FrameNode:
    return FrameNode(list(children))


SceneNode: TypeAlias = TextNode | FrameNode
