import sys

import click
from rich.console import Console
from rich.rule import Rule

from splat_llm import styles
from splat_llm.normalize import (
    highlight_invisibles,
    markdown_lint,
    remap_unusual_characters,
    remove_invisibles,
    remove_markdown_formatting,
)


@click.command()
@click.option(
    "-s",
    "--show-invisibles",
    is_flag=True,
    help="Highlight invisible/control characters instead of removing them.",
)
@click.option(
    "--remove-headings/--keep-headings",
    default=False,
    help="Remove/keep markdown headings.",
)
@click.option(
    "--remove-code-blocks/--keep-code-blocks",
    default=True,
    help="Remove/keep markdown code blocks.",
)
@click.option(
    "--remove-inline-code/--keep-inline-code",
    default=True,
    help="Remove/keep markdown inline code.",
)
@click.option(
    "--remove-bold/--keep-bold",
    default=True,
    help="Remove/keep markdown bold formatting.",
)
@click.option(
    "--remove-italics/--keep-italics",
    default=True,
    help="Remove/keep markdown italics formatting.",
)
@click.option(
    "--remove-strikethrough/--keep-strikethrough",
    default=True,
    help="Remove/keep markdown strikethrough formatting.",
)
@click.option(
    "--remove-images/--keep-images",
    default=True,
    help="Remove/keep markdown images.",
)
@click.option(
    "--remove-links/--keep-links",
    default=True,
    help="Remove/keep markdown links.",
)
@click.option(
    "--remove-blockquotes/--keep-blockquotes",
    default=True,
    help="Remove/keep markdown blockquotes.",
)
@click.option(
    "--remove-unordered-lists/--keep-unordered-lists",
    default=False,
    help="Remove/keep markdown unordered lists.",
)
@click.option(
    "--remove-ordered-lists/--keep-ordered-lists",
    default=False,
    help="Remove/keep markdown ordered lists.",
)
@click.option(
    "--remove-horizontal-rules/--keep-horizontal-rules",
    default=True,
    help="Remove/keep markdown horizontal rules.",
)
@click.option(
    "--remove-tables/--keep-tables",
    default=True,
    help="Remove/keep markdown tables.",
)
@click.option(
    "--lint/--no-lint", default=True, help="Enable/disable markdown linting."
)
def main(
    show_invisibles: bool = False,
    remove_headings: bool = False,
    remove_code_blocks: bool = True,
    remove_inline_code: bool = True,
    remove_bold: bool = True,
    remove_italics: bool = True,
    remove_strikethrough: bool = True,
    remove_images: bool = True,
    remove_links: bool = True,
    remove_blockquotes: bool = True,
    remove_unordered_lists: bool = False,
    remove_ordered_lists: bool = False,
    remove_horizontal_rules: bool = True,
    remove_tables: bool = True,
    lint: bool = True,
) -> None:
    """Read text from stdin, normalize or highlight invisibles, and print the result."""

    stderr_console = Console(force_terminal=True, file=sys.stderr)

    stderr_console.print(
        "Please paste your text and press Ctrl+D to process:",
        style=styles.SYSTEM_STYLE,
    )
    input_text = sys.stdin.read()

    if show_invisibles:
        highlight_invisibles(input_text)
    else:
        output = remove_invisibles(input_text)
        output = remap_unusual_characters(output)
        output = remove_markdown_formatting(
            output,
            remove_headings=remove_headings,
            remove_code_blocks=remove_code_blocks,
            remove_inline_code=remove_inline_code,
            remove_bold=remove_bold,
            remove_italics=remove_italics,
            remove_strikethrough=remove_strikethrough,
            remove_images=remove_images,
            remove_links=remove_links,
            remove_blockquotes=remove_blockquotes,
            remove_unordered_lists=remove_unordered_lists,
            remove_ordered_lists=remove_ordered_lists,
            remove_horizontal_rules=remove_horizontal_rules,
            remove_tables=remove_tables,
        )
        if lint:
            output = markdown_lint(output)

        stderr_console.print(Rule(style=styles.SYSTEM_STYLE))
        print(output)
        stderr_console.print(Rule(style=styles.SYSTEM_STYLE))


if __name__ == "__main__":
    main()
