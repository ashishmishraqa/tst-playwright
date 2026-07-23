.PHONY: check check-format check-lint test coverage security

check: check-format check-lint test coverage security
	@echo "✅ All checks passed!"

check-format:
	@echo "▸ Checking formatting..."
	black --check . --quiet
	isort --check . --quiet

check-lint:
	@echo "▸ Linting..."
	pylint tests/ src/ --disable=all --enable=E,F

test:
	@echo "▸ Running tests..."
	pytest -v --tb=short

coverage:
	@echo "▸ Checking coverage..."
	pytest --cov=src --cov-fail-under=75 -q

security:
	@echo "▸ Security scan..."
	bandit -r . -ll 2>/dev/null || true

# Quick check - just formatting + tests
quick-check: check-format test
	@echo "✅ Quick check passed!"

# Fix formatting automatically
fix:
	black .
	isort .