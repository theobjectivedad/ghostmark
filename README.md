# Ghostmark




## Setup

First, clone this repository:

```shell

```

Next, create a virtual environment. Note that ``uv`` will be installed if it isn't found in the environment:

```shell
make venv
```

Now install into the virtual environment:

```shell
uv pip install --user --editable .
```

Finally, create an alias for the script in the newly created virtual environment:

```shell
alias ghost=~/workspace/ghostmark/.venv/bin/ghost
```
