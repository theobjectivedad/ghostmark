import re

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from clean import styles
from clean.database import (
    INVISIBLE_CHAR_MAP,
    TRANSLATION_MAP,
    WHITESPACE_MAP,
)


def remove_invisibles(text: str) -> str:
    """This function removes all invisible characters from the input string,
    except for tab, newline, and carriage return characters. It also
    removes trailing whitespace characters from each line."""

    # Remove all invisible/control/format characters except tab, newline,
    # and carriage return
    # Remove all invisible/control/format characters except tab, newline, and carriage return
    filtered_chars = []
    for char in text:
        # Keep tab, newline, and carriage return
        if char in ("\t", "\n", "\r", " "):
            filtered_chars.append(char)
            continue
        # Remove if in INVISIBLE_CHAR_DATABASE or WHITESPACE_DATABASE
        if char in INVISIBLE_CHAR_MAP or char in WHITESPACE_MAP:
            continue
        filtered_chars.append(char)
    text = "".join(filtered_chars)

    # Remove trailing whitespace characters from each line
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def remove_markdown_formatting(
    text: str,
    *,
    remove_headings: bool = False,
    remove_code_blocks: bool = True,
    remove_inline_code: bool = True,
    remove_bold: bool = True,
    remove_italics: bool = True,
    remove_strikethrough: bool = True,
    remove_images: bool = True,
    remove_links: bool = True,
    remove_blockquotes: bool = True,
    remove_unordered_lists: bool = True,
    remove_ordered_lists: bool = True,
    remove_horizontal_rules: bool = True,
    remove_tables: bool = True,
) -> str:
    """This function removes markdown formatting from the input string, with flags to control each removal."""

    # Remove code blocks (```...```)
    if remove_code_blocks:
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # Remove inline code (`...`)
    if remove_inline_code:
        text = re.sub(r"`([^`]*)`", r"\1", text)

    # Remove bold (**text** or __text__)
    if remove_bold:
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"__(.*?)__", r"\1", text)

    # Remove italics (*text* or _text_)
    if remove_italics:
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"_(.*?)_", r"\1", text)

    # Remove strikethrough (~~text~~)
    if remove_strikethrough:
        text = re.sub(r"~~(.*?)~~", r"\1", text)

    # Remove images ![alt](url)
    if remove_images:
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    # Remove links [text](url)
    if remove_links:
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    # Remove blockquotes (> ...)
    if remove_blockquotes:
        text = re.sub(r"^> ?", "", text, flags=re.MULTILINE)

    # Remove unordered list markers (-, *, +)
    if remove_unordered_lists:
        text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)

    # Remove ordered list markers (1. 2. etc.)
    if remove_ordered_lists:
        text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    # Remove horizontal rules (---, ***, ___)
    if remove_horizontal_rules:
        text = re.sub(r"^\s*([-*_]){3,}\s*$", "", text, flags=re.MULTILINE)

    # Remove tables (| col | col |)
    if remove_tables:
        text = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.MULTILINE)

    # Remove headings if remove_headings is True
    if remove_headings:
        text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Remove trailing/leading whitespace and extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def markdown_lint(text: str) -> str:
    """Other markdown formatting

    - When a heading is detected with a number, remove the number.
      Example: '# 1. Heading' -> '# Heading'
    """
    # Remove leading numbers from markdown headings
    # Matches lines starting with #, optional whitespace, a number, a dot, and whitespace
    return re.sub(r"^(#+\s*)\d+\.\s+", r"\1", text, flags=re.MULTILINE)


def remap_unusual_characters(text: str) -> str:
    translation = str.maketrans(TRANSLATION_MAP)

    return text.translate(translation)


def highlight_invisibles(text: str) -> None:
    """
    Reveals and highlights invisible characters in a text string.
    """
    stdout_console = Console(force_terminal=True)

    result = Text()
    text_stats: dict[str, int] = {}

    # Process each character
    for char in text:
        validation: str | None = INVISIBLE_CHAR_MAP.get(char, None)
        if validation is not None:
            derived_style = (
                styles.WHITESPACE_STYLE
                if char in WHITESPACE_MAP
                else styles.INVISIBLE_STYLE
            )

            if validation in text_stats:
                text_stats[validation] += 1
            else:
                text_stats[validation] = 1

            if char == " ":
                # Add a dot for space
                result.append("\u00b7", style=derived_style)
            else:
                # Else pretty print the invisible character
                result.append(f"[{validation}]", style=derived_style)

            # Add real newlines after the invisible character
            if char == "\n":
                result.append("\n", style=derived_style)
        elif char in TRANSLATION_MAP:
            if "TRANSLATABLE" in text_stats:
                text_stats["TRANSLATABLE"] += 1
            else:
                text_stats["TRANSLATABLE"] = 1

            result.append(char, style=styles.TRANSLATION_STYLE)
        else:
            result.append(char, style=styles.NORMAL_STYLE)

    # Build the stats table
    stats_table = None
    if text_stats:
        stats_table = Table.grid(padding=(0, 1))
        stats_table.add_column("Character Type", style="white")
        stats_table.add_column("Count", style="bold white", justify="right")

        # Sort by count descending
        for char_type, count in sorted(
            text_stats.items(), key=lambda x: x[1], reverse=True
        ):
            if char_type in WHITESPACE_MAP.values():
                stats_style = styles.WHITESPACE_STYLE
            elif char_type in INVISIBLE_CHAR_MAP.values():
                stats_style = styles.INVISIBLE_STYLE
            elif char_type == "TRANSLATABLE":
                stats_style = styles.TRANSLATION_STYLE
            else:
                stats_style = styles.NORMAL_STYLE

            stats_table.add_row(char_type, str(count), style=stats_style)

    # Print the highlighted text
    result_panel = Panel(
        Align.left(result),
        border_style=styles.SYSTEM_COLOR,
        title="Highlighted Invisibles",
        padding=(0, 1),
    )
    stdout_console.print(result_panel)

    # Print the stats table
    if stats_table:
        stats_panel = Panel(
            stats_table,
            title="Statistics",
            border_style=styles.SYSTEM_COLOR,
            padding=(0, 1),
        )
        stdout_console.print(stats_panel)
