import os
import shutil
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib

def copy_plugins():
    # Путь к site-packages
    site_packages_path = get_python_lib()

    # Путь к директории PyFlow Packages в site-packages
    pyflow_packages_path = os.path.join(site_packages_path, "PyFlow", "Packages")

    # Проверка наличия директории PyFlow Packages
    if not os.path.exists(pyflow_packages_path):
        print("PyFlow Packages directory not found. Ensure PyFlow is installed correctly.")
        return

    # Определяем директорию, где находится setup.py
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Пути к папкам с плагинами
    image_filtering_source = os.path.join(current_dir, "Packages")
    opencv_source = os.path.join(current_dir, "PyFlowOpenCv", "PyFlow", "Packages")

    # Копируем PyFlowImageFiltering
    if os.path.exists(image_filtering_source):
        print(f"Copying PyFlowImageFiltering to {pyflow_packages_path}")
        shutil.copytree(
            image_filtering_source,
            pyflow_packages_path,
            dirs_exist_ok=True
        )
    else:
        print("PyFlowImageFiltering directory not found.")

    # Копируем PyFlowOpenCv
    if os.path.exists(opencv_source):
        print(f"Copying PyFlowOpenCv to {pyflow_packages_path}")
        shutil.copytree(
            opencv_source,
            pyflow_packages_path,
            dirs_exist_ok=True
        )
    else:
        print("PyFlowOpenCv directory not found.")

# Запускаем функцию копирования плагинов
copy_plugins()

# Стандартная функция setup
setup(
    packages=find_packages()
)

