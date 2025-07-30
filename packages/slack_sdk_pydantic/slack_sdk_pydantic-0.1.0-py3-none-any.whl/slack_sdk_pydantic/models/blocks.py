from abc import ABCMeta, abstractmethod

from pydantic import ConfigDict
from pydantic_xml import BaseXmlModel, attr, element
from slack_sdk.models import blocks as slack


def replace_newlines(text: str) -> str:
    return text.replace(r"\n", "\n")


class Base(BaseXmlModel):
    model_config = ConfigDict(str_strip_whitespace=True)


# N.B. it'd be good to make this generic but pydantic_xml doesn't play well with generics :(
class BaseBlock(Base, metaclass=ABCMeta):
    id: str | None = attr(default=None)

    @abstractmethod
    def to_block(self) -> slack.Block:
        pass


class DividerBlock(BaseBlock, tag="divider"):
    def to_block(self) -> slack.Block:
        return slack.DividerBlock(block_id=self.id)


class HeaderBlock(BaseBlock, tag="header"):
    text: str

    def to_block(self) -> slack.Block:
        return slack.HeaderBlock(block_id=self.id, text=self.text)


# TODO: Implement RichTextObject too
class PlainTextObject(Base, tag="text"):
    text: str

    @property
    def sanitised(self) -> str:
        text = self.text.replace(r"\n", "\n")
        if len(text) >= 2000:
            text = text[:1999] + "…"

        return text


class SectionBlock(BaseBlock, tag="section"):
    alt: str | None = attr(default=None)
    fields: list[PlainTextObject] = element(default=[])

    def to_block(self) -> slack.Block:
        return slack.SectionBlock(
            block_id=self.id, fields=[f.sanitised for f in self.fields], text=self.alt
        )


type Block = HeaderBlock | DividerBlock | SectionBlock


class Message(Base, tag="message"):
    alt: str | None = attr(default=None)
    content: list[Block] = element()
