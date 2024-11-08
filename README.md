# PyFlowImageFiltering

**PyFlowImageFiltering** — это расширение для фреймворка [PyFlow](https://github.com/wonderworks-software/PyFlow), которое добавляет набор фильтров для обработки изображений с использованием OpenCV.

## Требования

Для работы **PyFlowImageFiltering** необходимо установить расширение [PyFlowOpenCV](https://github.com/wonderworks-software/PyFlowOpenCv).

## Установка и запуск
### 1. Установка PyFlow
Устанавливаем PyFlow:
```
pip install git+https://github.com/wonderworks-software/PyFlow.git@master
```
### 2. Установка PyFlowOpenCv
Копируем репозиторий PyFlowOpenCv:
```
git clone https://github.com/wonderworks-software/PyFlowOpenCv
```
Переходим в PyFlowOpenCv и устанавливаем `requirements.txt`:
```
cd PyFlowOpenCv
pip install -r requirements.txt
```
Копируем PyFlowOpenCv из .PyFlow/Packages в дирректорию `.venv/lib/python/site-packages/PyFlow/Packages`.
### 3. Установка PyFlowImageFiltering
Копируем репозиторий PyFlowImageFiltering:
```
git clone https://github.com/13lyvnyv/PyFlowImageFiltering
```
Переходим в PyFlowImageFiltering и копируем расширение PyFlowImageFiltering в `.PyFlow/Packages`.

### 4. Запуск
Для запуска вводим `pyflow` в терминале.  
В приложении для удобства добавляем инструменты **NodeBox** (`Tools -> PyFlowBase -> NodeBox`) и **Properties** (`Tools -> PyFlowBase -> Properties`).  
#### Замечания
- При использовании инструмента **ImageViewerTool** из библиотеки PyFlowOpenCv могут возникнуть проблемы с функциональностью меню File. Это может привести к нестабильной работе PyFlow.  
- Для использования инструмента **Logger** необходимо зайти в `Edit -> Preferences -> General` и активировать опцию **Redirect output**.
## Описание функций

**PyFlowImageFiltering** включает в себя следующие ноды:

### 1. cv_Sharpen
Применяет фильтр резкости.



### 2. cv_Brightness
Регулирует яркость изображения и возвращает его среднюю яркость.



### 3. cv_Contrast
Настраивает контраст изображения.



### 4. cv_GaussianBlur
Применяет гауссово размытие к изображению.



### 5. cv_MedianBlur
Применяет медианное размытие для уменьшения шума.



### 6. cv_Saturation
Регулирует насыщенность изображения.



### 7. calcPixels
Считает общее количество пикселей на изображении.



### 8. showNumber
Отображает переданное число.



## Добавление нодов


Ниже приведён пример добавления узла `cv_Sharpen` в библиотеке `ImageFilteringLib.py`

```python
@staticmethod
@IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
def cv_Sharpen(input=('ImagePin', None), intensity=('FloatPin', 1.0), img=(REF, ('ImagePin', None))):
    """
    Применяет фильтр резкости к изображению с возможностью регулировки интенсивности.

    :param input: Входное изображение.
    :type input: numpy.ndarray
    :param intensity: Интенсивность резкости.
    :type intensity: float
    :param img: Выходной пин для передачи обработанного изображения.
    """

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(input, -1, kernel)
    blended_image = cv2.addWeighted(input, 1.0 - intensity * 0.5, sharpened_image, intensity * 0.5, 0)
    
    img(blended_image)
```
Этого достаточно для добавления фильтров.  
Все ноды, объявленные в `ImageFilteringLib.py`, используют графический интерфейс `UIOpenCvBaseNode.py` из расширения **PyFlowOpenCv**.   
Однако если требуется дополнительный вывод информации в ноде, нужно подключить соответствующий класс.
Так, например, нод `showNumber` реализован отдельным файлом `showNumber.py` и использует `UIShowNumber.py`.  
Чтобы связать нод с его интерфейсом, необходимо внести изменения в файл `UINodeFactory.py`
```python
#UINodeFactory.py
def createUINode(raw_instance):
	if raw_instance.__class__.__name__ == "showNumber":
		return UIShowNumber(raw_instance)
	return UIOpenCvBaseNode(raw_instance)
```
### Инициализация нодов
В PyFlowImageFiltering/__init__.py нужно зарегистрировать библиотеки и узлы:
```python
#PyFlowImageFiltering/__init__.py
from PyFlow.Packages.PyFlowImageFiltering.FunctionLibraries.ImageFilteringLib import ImageFilteringLib
from PyFlow.Packages.PyFlowImageFiltering.Factories.UINodeFactory import createUINode
from PyFlow.Packages.PyFlowImageFiltering.Nodes.ShowNumber import showNumber

...

_FOO_LIBS = {ImageFilteringLib.__name__: ImageFilteringLib(PACKAGE_NAME)}
_NODES = {showNumber.__name__: showNumber}

...

@staticmethod
def UINodesFactory():
	return createUINode
```


