.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "  %-28s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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
