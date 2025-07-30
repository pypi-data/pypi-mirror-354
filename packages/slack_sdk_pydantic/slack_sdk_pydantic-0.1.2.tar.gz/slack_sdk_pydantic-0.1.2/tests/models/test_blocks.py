import pytest
from slack_sdk.models.blocks import Block

from slack_sdk_pydantic.models import blocks as m
from tests import fixtures, utils


@pytest.mark.parametrize(
    ("fx", "expected"),
    [
        ("blocks/content1.xml", fixtures.content1),
        ("blocks/content2.xml", fixtures.content2),
    ],
)
def test_read_mixed_content(fx: str, expected: m.Message) -> None:
    fixture = utils.read_fixture_raw(fx)
    actual = m.Message.from_xml(fixture)

    assert actual == expected


@pytest.mark.parametrize(
    ("fx", "expected"),
    [
        (fixtures.content1, fixtures.content1_slack),
        (fixtures.content2, fixtures.content2_slack),
    ],
)
def test_slack_blocks(fx: m.Message, expected: list[Block]) -> None:
    actual = [c.to_block() for c in fx.content]
    assert actual == expected
