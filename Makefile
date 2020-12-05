PYTHONPATH='./:./modules/metarepo-to-json'
SHELL=/bin/bash

export PYTHONPATH

.PHONY: all submodules-info sync get-latest-modules help

all: help

submodules-info:
	@echo getting refs for all submodules ...
	@echo
	git submodule foreach 'git config --get remote.origin.url && \
		git status && \
		echo'

sync: submodules-info
	@echo synchronizing repo with remote ...
	git config --get remote.origin.url
	@echo
	git pull
	@echo
	git submodule init
	git submodule sync
	git submodule update --init

get-latest-modules:
	@echo getting lates git submodules from remotes ...
	@echo
	git submodule update --remote

help:
	@echo Metarepo CPE tag
	@echo
	@echo "For available targets type: 'make ' and hit TAB"
	@echo
