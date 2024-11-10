.PHONY: install

install:
	@echo "Клонируем PyFlowOpenCv."
	cd Packages && git clone https://github.com/wonderworks-software/PyFlowOpenCv.git
	@echo "Создаём виртуальное окружение."
	python3 -m venv .venv
	@echo "Установка PyFlow и расширений"
	.venv/bin/python3 -m pip install -e .
	cp -r Packages/PyFlowImageFiltering .venv/lib/python*/site-packages/PyFlow/Packages/
	cp -r Packages/PyFlowOpenCv/PyFlow/Packages/PyFlowOpenCv .venv/lib/python*/site-packages/PyFlow/Packages/
	@echo "Установка завершена."