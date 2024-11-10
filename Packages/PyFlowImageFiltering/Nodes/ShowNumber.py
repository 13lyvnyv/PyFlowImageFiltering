from qtpy import QtCore, QtGui
from PyFlow.Core.NodeBase import NodeBase, NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class showNumber(NodeBase):
    """
    Узел, отображающий значение типа float, переданное на вход.

    Этот узел предназначен для получения значения на входе
    и последующего отображения его в интерфейсе.
    """

    def __init__(self, name):
        """
        Инициализирует узел showNumber и создаёт входной пин для передачи числа.

        :param name: Имя узла для идентификации в графе.
        :type name: str
        """
        super(showNumber, self).__init__(name)

        self.floatInput = self.createInputPin('number', 'FloatPin')

    def compute(self, *args, **kwargs):
        """
        Логика исполнения узла, выполняющаяся при активации.

        Этот метод вызывается для получения значения из входного пина
        и дальнейшей обработки, если это необходимо.

        :param args: Дополнительные аргументы для выполнения.
        :param kwargs: Дополнительные именованные аргументы.
        """

        number = self.intInput.getData()

    @staticmethod
    def pinTypeHints():
        """
        Предоставляет рекомендации по типам пинов для этого узла.

        Возвращает объект, содержащий допустимые типы данных и структуры,
        которые можно подключать к пину узла.

        :return: Объект NodePinsSuggestionsHelper с допустимыми типами.
        :rtype: NodePinsSuggestionsHelper
        """
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('FloatPin')
        helper.addInputStruct(StructureType.Single)

        return helper

    @staticmethod
    def category():
        """
        Возвращает категорию узла для организации в интерфейсе.

        :return: Строка, указывающая категорию узла.
        :rtype: str
        """
        return "Display"

    @staticmethod
    def description():
        """
        Описание узла для отображения в интерфейсе или документации.

        :return: Строка с описанием узла.
        :rtype: str
        """
        return "A node that displays a float passed as input."
