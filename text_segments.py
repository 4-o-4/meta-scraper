from __future__ import annotations

from figma_nodes import SceneNode, TextNode, TextSegment, TextStyleName, frame_node


class FigmaNodesIterator:
    __slots__ = ("_blocks", "_index")

    def __init__(self, blocks: list[TextSegment]) -> None:
        self._blocks = blocks
        self._index = 0

    def __iter__(self) -> FigmaNodesIterator:
        return self

    def __next__(self) -> SceneNode:
        if self._index >= len(self._blocks):
            raise StopIteration

        if self._blocks[self._index].textStyleName == TextStyleName.CODE:
            inner = TextNode()
            while (
                    self._index < len(self._blocks)
                    and self._blocks[self._index].textStyleName == TextStyleName.CODE
            ):
                inner.append(self._blocks[self._index])
                self._index += 1
            return frame_node(inner)

        text_node = TextNode()
        while (
                self._index < len(self._blocks)
                and self._blocks[self._index].textStyleName != TextStyleName.CODE
        ):
            text_node.append(self._blocks[self._index])
            self._index += 1
        return text_node


class TextSegments:

    def __init__(self, text_segments: list[TextSegment] | None = None) -> None:
        self.text_segments: list[TextSegment] = (
            text_segments if text_segments is not None else []
        )

    def __iter__(self) -> FigmaNodesIterator:
        return FigmaNodesIterator(self.text_segments)

    def append(self, text_segment: TextSegment) -> None:
        self.text_segments.append(text_segment)
