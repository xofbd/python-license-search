SHELL := /bin/bash
VENV := venv
ACTIVATE_VENV := source $(VENV)/bin/activate
CACHE_DIR := cache

.PHONY: all
all: clean $(VENV)/bin/activate
	$(ACTIVATE_VENV) && python3 src/license.py

$(VENV)/bin/activate: requirements.txt
	rm -rf $(VENV)
	python3 -m venv $(VENV)
	$(ACTIVATE_VENV) && pip install -r $<

.PHONY: clean
clean:
	rm -rf $(VENV) $(CACHE_DIR)
	find . -type d | grep "__pycache__" | xargs rm -rf
