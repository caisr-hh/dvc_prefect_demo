.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##### Documentation tools
# sudo npm install -g @mermaid-js/mermaid-cli
# sudo npx puppeteer browsers install chrome-headless-shell
MMDC ?= mmdc
MERMAID_OUT_EXT ?= png

.PHONY: render-all-mermaids
render-all-mermaids: ## generate images from all mermaid files in this repo (find them recursively)
	@find . -type f -name '*.mermaid' -exec sh -c '\
		for f do \
			out="$${f%.mermaid}.$(MERMAID_OUT_EXT)"; \
			$(MMDC) -i "$$f" -o "$$out"; \
		done' sh {} +

##### Dev Targets
.PHONY: formatter
formatter: ## Check code formatting.
	@echo "\n=== Checking code formatting ==="
	@black --check .

.PHONY: linter
linter: ## Run the linter.
	@echo "\n=== Linting Python files (all) ==="
	@pylint $(shell git ls-files '*.py')

MYPY_OPTS = --install-types --non-interactive --explicit-package-bases --config-file=pyproject.toml --show-error-codes

.PHONY: type-check
type-check: ## Run static type checking.
	@echo "\n=== Running type checks (all) ==="
	@mypy $(MYPY_OPTS) .

.PHONY: code-quality
code-quality: ## Run the main code-quality checks (formatting, linting, typing).
	-@$(MAKE) formatter
	-@$(MAKE) type-check
	-@$(MAKE) linter

#### Prefect
# IMPORTANT NOTE: These server configs must match config in 'prefect_server_utils.py,'
PREFECT_HOST ?= 127.0.0.1
PREFECT_PORT ?= 4200
PREFECT_HOME_DIR ?= $(PWD)/prefect
PREFECT_DB := $(PREFECT_HOME_DIR)/prefect.db
PREFECT_STORAGE := $(PREFECT_HOME_DIR)/storage

.PHONY: prefect-start
prefect-start: ## Start Prefect server with project-local state (blocks).
	@mkdir -p "$(PREFECT_STORAGE)"
	@echo "Starting Prefect server on port $(PREFECT_PORT) with PREFECT_HOME=$(PREFECT_HOME_DIR)"
	@PREFECT_HOME="$(PREFECT_HOME_DIR)" \
	 PREFECT_RESULTS_PERSIST_BY_DEFAULT="true" \
	 PREFECT_LOCAL_STORAGE_PATH="$(PREFECT_STORAGE)" \
	 PREFECT_API_DATABASE_CONNECTION_URL="sqlite+aiosqlite:///$$(realpath $(PREFECT_DB))" \
	 nohup prefect server start --host $(PREFECT_HOST) --port $(PREFECT_PORT) >/dev/null 2>&1 &

.PHONY: prefect-stop
prefect-stop: ## Stop Prefect server
	@echo "Stopping Prefect server on port $(PREFECT_PORT)"
	@fuser -k $(PREFECT_PORT)/tcp || true

.PHONY: prefect-status
prefect-status:  ## Check whether the Prefect server is reachable.
	@curl -fsS "http://$(PREFECT_HOST):$(PREFECT_PORT)/api/health" >/dev/null && \
	  echo "Prefect server is UP at http://$(PREFECT_HOST):$(PREFECT_PORT)" || \
	  echo "Prefect server is DOWN"

.PHONY: prefect-reset-soft
prefect-reset-soft: ## Soft reset Prefect server: delete results, keep but reset db
	@echo "Soft-resetting Prefect: clearing local results and resetting DB schema"
	@rm -rf "$(PREFECT_STORAGE)" && mkdir -p "$(PREFECT_STORAGE)"
	@PREFECT_HOME="$(PREFECT_HOME_DIR)" \
	 PREFECT_API_DATABASE_CONNECTION_URL="sqlite+aiosqlite:///$$(realpath $(PREFECT_DB))" \
	 prefect server database reset -y

.PHONY: prefect-reset-hard
prefect-reset-hard: prefect-stop # Hard reset Prefect server: stop server, delete (DB + results), re-start server clean
	@echo "Hard-resetting Prefect: deleting DB and local results"
	@rm -f "$(PREFECT_DB)"
	@rm -rf "$(PREFECT_STORAGE)" && mkdir -p "$(PREFECT_STORAGE)"
	@echo "Recreating empty database schema"
	@PREFECT_HOME="$(PREFECT_HOME_DIR)" \
	 PREFECT_API_DATABASE_CONNECTION_URL="sqlite+aiosqlite:///$$(realpath $(PREFECT_DB))" \
	 prefect server database reset -y
	@$(MAKE) prefect-start
