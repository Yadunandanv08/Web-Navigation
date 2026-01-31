import re
from dataclasses import dataclass


@dataclass
class TagContentResult:
    content: list[str]
    found: bool


def extract_tag_content(text: str, tag: str) -> TagContentResult:
    tag_pattern = rf"<{tag}>(.*?)</{tag}>"

    matched_contents = re.findall(tag_pattern, text, re.DOTALL)

    return TagContentResult(
        content=[content.strip() for content in matched_contents],
        found=bool(matched_contents),
    )