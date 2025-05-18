# SplatLLM

SplatLLM is a tool designed for post-formatting text from large language models (LLMs). Broadly this involves:

* Removal of [invisible characters](https://invisible-characters.com/) that can be used for watermarking and/or hiding information in plain text.
* Remapping of unusual characters typically produced my LLMs but not typically used by human writers, for example Unicode dash punctuation commonly output by LLMs are be remapped to an ASCII hyphen.
* Removal of certain markdown formatting characteristically used by LLMs.

Additionally SplatLLM can be used to inspect text for the presence of invisible characters and other unusual formatting via the ``splat --show-invisibles`` / ``splat -s`` command:

![SplatLLM text analysis sample](https://raw.githubusercontent.com/theobjectivedad/splat-llm/refs/heads/master/images/splat_llm_dump.webp)

*Coming soon will be an MCP version that will expose SplatLLM as a callable tool for agent-driven post-formatting.*

## Quickstart

```shell
uvx splatllm
```

## Development Setup

First, clone this repository:

```shell
git clone https://github.com/theobjectivedad/splat-llm.git
```

Change directory to the cloned repository:

```shell
cd splat-llm
```

Next, setup your local virtual environment. Note that [uv](https://github.com/astral-sh/uv) will be installed if it isn't found in the environment:

```shell
make venv
```

Finally, create an alias for the script in the newly created virtual environment in your shell resource file, ex: ``~/.bashrc``, ``~/.zshrc``, etc.:

```shell
alias splat=PATH_TO_SPLAT_LLM/.venv/bin/splat
```

You can now use the ``splat`` command via the CLI (note that you may need to re-read your shell rc file for the alias to be recognized):

```shell
splat 
```

Access CLI help via:

```shell
splat --help
```
