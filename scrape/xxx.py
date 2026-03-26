from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

from figma_nodes import TextSegment, TextStyleName
from text_segments import TextSegments

_SOFT_LINE_BREAK = "\u2028"
_NEWLINE = "\u000A"
_NBSP = "\u00a0"
_TARGET_TAGS: set[str] = {"h1", "h2", "h3", "p", "ul"}


def _tag_to_text_style_name(tag: str) -> TextStyleName:
    match tag.lower():
        case "h1":
            return TextStyleName.H1
        case "h2":
            return TextStyleName.H2
        case "h3" | "p" | "ul":
            return TextStyleName.P
        case _:
            raise ValueError(f"Неизвестный тег для стиля: {tag!r}")


def _syntax_code_text(syntaxhighlighter_el: WebElement) -> str:
    td_code = syntaxhighlighter_el.find_element(By.CSS_SELECTOR, "td.code")
    line_divs = td_code.find_elements(By.CSS_SELECTOR, "div.line")
    lines: list[str] = []
    for line_div in line_divs:
        text = line_div.text.replace(_NBSP, " ")
        lines.append(text)
    return _SOFT_LINE_BREAK.join(lines)


def _process_element(
        el: WebElement,
        out: TextSegments,
        search_targets: bool = True,
) -> None:
    tag = el.tag_name.lower()

    if search_targets and tag in _TARGET_TAGS:
        text = el.text.strip().replace(_NEWLINE, "")
        if text:
            out.append(
                TextSegment(
                    characters=text,
                    textStyleName=_tag_to_text_style_name(tag),
                )
            )
        return

    if tag == "div":
        classes_attr: Optional[str] = el.get_attribute("class")
        classes = (classes_attr or "").split()
        if "syntaxhighlighter" in classes:
            code_text = _syntax_code_text(el).strip()
            if code_text:
                out.append(
                    TextSegment(
                        characters=code_text,
                        textStyleName=TextStyleName.CODE,
                    )
                )
            return

    for child in el.find_elements(By.XPATH, "./*"):
        _process_element(child, out, search_targets=False)


def scrape_xxx(
        url: str,
) -> TextSegments:
    driver: WebDriver = SafariWebDriver()
    try:
        driver.get(url)
        content_blocks = driver.find_elements(By.CSS_SELECTOR, "div.item.center.menC")
        text_segments = TextSegments()
        for block in content_blocks:
            for child in block.find_elements(By.XPATH, "./*"):
                _process_element(child, text_segments)
        return text_segments
    finally:
        driver.quit()
