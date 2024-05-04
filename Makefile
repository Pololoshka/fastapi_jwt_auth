install_pre_commit:
	pre-commit install
	pre-commit install --hook-type commit-msg
	pre-commit autoupdate

fix:
	ruff format src tests preload_data
	ruff check --fix --show-fixes src tests preload_data

check:
	ruff format --check src tests preload_data
	ruff check src tests preload_data
	mypy src tests preload_data
	pytest tests
