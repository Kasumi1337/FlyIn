NAME = main.py

PYTHON = python3

run:
	@$(PYTHON) $(NAME) maps/easy/01_linear_path.txt

lint:
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@echo "Cleaning cache..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +


fclean: clean
	@echo "Nothing else to clean"

debug: 
	@python3 -m pdb ${NAME}

install:
	@pip install -r requirements.txt

re: fclean run

.PHONY: clean run fclean re lint install debug