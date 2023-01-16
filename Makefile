POETRY_PYTHON_PATH = $(shell cd backend && poetry env info --path)
POETRY_PYTHON_PATH := $(subst  ,,$(POETRY_PYTHON_PATH)) # remove spaces
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON = $(addsuffix \Scripts\python.exe,$(POETRY_PYTHON_PATH))
else
	# Linux
	PYTHON = $(addsuffix /bin/python,$(POETRY_PYTHON_PATH))
endif

install_dep_backend:
	cd backend
	poetry install

install_dep_frontend:
	cd frontend
	npm install

install_dep: install_dep_backend install_dep_frontend

run_backend:
	cd backend
	$(PYTHON) -m uvicorn backend.main:app --reload

build_frontend:
	cd frontend
	npm run build

