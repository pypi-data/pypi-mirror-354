from slack_sdk.models import blocks as s

from slack_sdk_pydantic.models import blocks as m

content1 = m.Message.model_construct(
    alt="ALT TEXT",
    content=[
        m.HeaderBlock.model_construct(text="Test"),
        m.SectionBlock.model_construct(
            id="section1",
            fields=[
                m.PlainTextObject.model_construct(text="Test"),
                m.PlainTextObject.model_construct(
                    text="Test\\n\n        test\\n\n        test\xa0\xa0\xa0test"
                ),
            ],
        ),
        m.DividerBlock.model_construct(),
    ],
)

content1_slack = [
    s.HeaderBlock(text="Test"),
    s.SectionBlock(fields=["Test", "Test\ntest\ntest test"], block_id="section1"),
    s.DividerBlock(),
]

content2 = m.Message.model_construct(
    alt="Long message",
    content=[
        m.SectionBlock.model_construct(
            fields=[
                m.PlainTextObject.model_construct(text="Very long message ahead"),
                m.PlainTextObject.model_construct(text="." * 2500),
            ],
        ),
        m.DividerBlock.model_construct(),
    ],
)

content2_slack = [
    s.SectionBlock(fields=["Very long message ahead", "." * 1999 + "…"]),
    s.DividerBlock(),
]
