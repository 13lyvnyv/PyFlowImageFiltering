import cv2
import numpy as np
from PyFlow.Core import (
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

from qtpy.QtWidgets import QApplication, QWidget
from qtpy.QtGui import QPainter, QColor

def clamp(value, minV, maxV):
    """
    Ограничивает значение в пределах заданного диапазона.

    :param value: Значение для ограничения.
    :param minV: Минимально допустимое значение.
    :param maxV: Максимально допустимое значение.
    :return: Ограниченное значение.
    :rtype: float
    """
    return min(max(minV, value), maxV)

def oddify(value):
    """
    Преобразует значение в нечётное путём прибавления единицы, если значение чётное.

    :param value: Входное значение.
    :return: Нечётное значение.
    :rtype: int
    """
    return max(0, value + (value - 1))

class ImageFilteringLib(FunctionLibraryBase):
    """
    Библиотека функций для фильтрации изображений с использованием OpenCV.
    Содержит функции для применения различных фильтров, изменения яркости, насыщенности и контраста изображения.
    """

    def __init__(self, packageName):
        """
        Инициализирует библиотеку функций для обработки изображений.

        :param packageName: Имя пакета.
        :type packageName: str
        """
        super(ImageFilteringLib, self).__init__(packageName)

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

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
    def cv_Brightness(input=('ImagePin', None), value=('FloatPin', 0), img=(REF, ('ImagePin', None)),
                      mean_brightness=(REF, ('FloatPin', 0))):
        """
        Регулирует яркость изображения и вычисляет его среднюю яркость.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param value: Значение яркости для добавления.
        :type value: float
        :param img: Выходной пин для передачи обработанного изображения.
        :param mean_brightness: Выходной пин для средней яркости изображения.
        """
        image = cv2.convertScaleAbs(input, alpha=1, beta=value)
        img(image)
        mean_brightness_value = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        mean_brightness(mean_brightness_value)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
    def cv_Contrast(input=('ImagePin', None), alpha=('FloatPin', 1), img=(REF, ('ImagePin', None))):
        """
        Регулирует контраст изображения.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param alpha: Коэффициент контраста.
        :type alpha: float
        :param img: Выходной пин для передачи обработанного изображения.
        """
        image = cv2.convertScaleAbs(input, alpha=alpha, beta=0)
        img(image)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
    def cv_GaussianBlur(input=('ImagePin', None), ksize=('IntPin', 5), sigmaX=('FloatPin', 0), img=(REF, ('ImagePin', None))):
        """
        Применяет гауссово размытие к изображению.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param ksize: Размер ядра свёртки (нечётное значение).
        :type ksize: int
        :param sigmaX: Сигма по оси X.
        :type sigmaX: float
        :param img: Выходной пин для передачи обработанного изображения.
        """
        image = cv2.GaussianBlur(input, (oddify(ksize), oddify(ksize)), sigmaX)
        img(image)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
    def cv_MedianBlur(input=('ImagePin', None), ksize=('IntPin', 5), img=(REF, ('ImagePin', None))):
        """
        Применяет медианное размытие к изображению.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param ksize: Размер ядра свёртки (нечётное значение).
        :type ksize: int
        :param img: Выходной пин для передачи обработанного изображения.
        """
        image = cv2.medianBlur(input, oddify(ksize))
        img(image)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'ImageFiltering', NodeMeta.KEYWORDS: []})
    def cv_Saturation(input=('ImagePin', None), saturation=('FloatPin', 1.0), img=(REF, ('ImagePin', None))):
        """
        Регулирует насыщенность изображения с регулируемой интенсивностью.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param saturation: Интенсивность насыщенности.
        :type saturation: float
        :param img: Выходной пин для передачи обработанного изображения.
        """
        if input is not None:
            hsv_image = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 1] = cv2.multiply(hsv_image[:, :, 1], saturation)
            adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
            img(adjusted_image)

    @staticmethod
    @IMPLEMENT_NODE(returns=None, meta={NodeMeta.CATEGORY: 'Сalculating', NodeMeta.KEYWORDS: []})
    def calcPixels(input=('ImagePin', None), count=(REF, ('IntPin', 0))):
        """
        Считает общее количество пикселей на изображении.

        :param input: Входное изображение.
        :type input: numpy.ndarray
        :param count: Выходной пин для общего количества пикселей.
        """
        height, width = input.shape[:2]
        pixelCount = height * width
        count(pixelCount)


