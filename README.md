# SplatLLM

SplatLLM is a tool designed for post-formatting text from large language models (LLMs). Broadly this involves:

* Removal of [invisible characters](https://invisible-characters.com/) that can be used for watermarking and/or hiding information in plain text.
* Remapping of unusual characters typically produced my LLMs but not typically used by human writers, for example En/Em dashes and horizontal bars are be remapped to a single hyphen.
* Removal of certain markdown formatting characteristically used by LLMs.

Additionally SplatLLM can be used to inspect text for the presence of invisible characters and other unusual formatting via the ``splat --show-invisibles`` command:

![SplatLLM text analysis sample](https://raw.githubusercontent.com/theobjectivedad/splat-llm/refs/heads/master/images/splat_llm_dump.webp)

Coming soon will be an MCP version that will expose SplatLLM as a callable tool for agent-driven post-formatting.

## Setup

Ahead of getting this project up and running you can run locally via the commands below.

First, clone this repository:

```shell
git clone https://github.com/theobjectivedad/splat-llm.git
```

Change directory to the cloned repository:

```shell
cd splat-llm
```

Next, create a virtual environment. Note that ``uv`` will be installed if it isn't found in the environment:

```shell
make venv
```

Now install into the virtual environment:

```shell
uv pip install --user --editable .
```

Finally, create an alias for the script in the newly created virtual environment, this can be in ``~/.bashrc``, ``~/.zshrc``, etc. depending on your shell:

```shell
alias splat=PATH_TO_SPLAT_LLM/.venv/bin/splat
```

You can now use SplatLLM via the CLI:

```shell
splat 
```

Access CLI help via:

```shell
splat --help
```
