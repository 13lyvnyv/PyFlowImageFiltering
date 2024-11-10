.PHONY: install

install:
	@echo "Клонируем PyFlowOpenCv..."
	git clone https://github.com/wonderworks-software/PyFlowOpenCv.git
	@echo "Создаём виртуальное окружение..."
	python3 -m venv .venv
	@echo "Установка PyFlow и расширений"
	.venv/bin/python3 -m pip install -e .
	.venv/bin/python3 -m pip install .
	@echo "Установка завершена."
