###############################################################################
# Makefile Configuration
###############################################################################

.ONESHELL:
SHELL:=/bin/bash
.SHELLFLAGS=-o errexit -o allexport -o pipefail -o nounset -c

.SILENT:
MAKEFLAGS+=--no-print-directory

.PHONY: default
default: dev

###############################################################################
# Global Variables
###############################################################################

WORKSPACE_DIR:=$(CURDIR)
SRC_DIR:=$(WORKSPACE_DIR)/src
AGENTS_DIR:=$(WORKSPACE_DIR)/agents
VENV_DIR:=$(WORKSPACE_DIR)/.venv
VENV_PYTHON:=$(VENV_DIR)/bin/python
SUBMODULES_DIR:=$(WORKSPACE_DIR)/submodules
PYTHON_VERSION:=3.12

###############################################################################
# Environment & Build
###############################################################################

.PHONY: venv
venv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "INFO: Installing uv package manager..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		if [ $$? -ne 0 ]; then \
			echo "ERROR: Failed to install uv."; \
			exit 1; \
		fi; \
	fi
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "ERROR: Virtual environment '$(VENV_DIR)' already exists."; \
		exit 1; \
	fi
	uv venv \
		--python $(PYTHON_VERSION) \
		--prompt "clean" \
		$(VENV_DIR)
	uv add --python=$(VENV_PYTHON) --dev --editable .
	echo "Virtual environment created at '$(VENV_DIR)'. Activate with: source $(VENV_DIR)/bin/activate"


