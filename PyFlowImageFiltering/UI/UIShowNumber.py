from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QGraphicsTextItem, QSizePolicy
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.NodeActionButton import NodeActionButtonBase
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.Core.Common import *
import os


class UIShowNumber(UINodeBase):
    """
    Класс UIShowNumber представляет графический интерфейс для отображения числового значения в PyFlow.
    Этот узел отображает текущее числовое значение и поддерживает изменение размеров, а также
    функцию обновления для получения актуальных данных.
    """

    def __init__(self, raw_node):
        """
        Инициализирует графический узел и настраивает текстовый элемент для отображения значения.

        :param raw_node: Ссылка на основной узел данных.
        """
        super(UIShowNumber, self).__init__(raw_node)

        self.displayItem = QGraphicsTextItem("0", self)
        self.displayItem.setDefaultTextColor(QtCore.Qt.white)

        font = QtGui.QFont("Consolas", 12)
        self.displayItem.setFont(font)

        self.actionOnRefresh = self._menu.addAction("RefreshCurrentNode")
        self.actionOnRefresh.triggered.connect(self.onRefresh)
        self.actionOnRefresh.setData(NodeActionButtonInfo(
            os.path.dirname(__file__) + "/resources/reload.svg", NodeActionButtonBase))

        self.resizable = True

    @property
    def collapsed(self):
        """
        Свойство, указывающее, свёрнут ли узел.
        """
        return self._collapsed

    @collapsed.setter
    def collapsed(self, bCollapsed):
        """
        Устанавливает новое состояние узла (свёрнут или развернут).
        Обновляет видимость текста и входов/выходов.

        :param bCollapsed: Состояние узла.
        """
        if bCollapsed != self._collapsed:
            self._collapsed = bCollapsed
            self.updateNodeShape()

            self.displayItem.setVisible(not bCollapsed)

            for i in range(self.inputsLayout.count()):
                inp = self.inputsLayout.itemAt(i)
                inp.setVisible(not bCollapsed)
            for o in range(self.outputsLayout.count()):
                out = self.outputsLayout.itemAt(o)
                out.setVisible(not bCollapsed)

    def updateNodeShape(self):
        """
        Обновляет форму узла и отображаемое значение в соответствии с текущим значением узла данных.
        """
        super(UIShowNumber, self).updateNodeShape()

        input_value = self._rawNode.floatInput.getData()

        if input_value is not None:
            self.displayItem.setPlainText(str(input_value))
        else:
            self.displayItem.setPlainText("0")

        self.updateGeometry()
        self.updateTextPosition()
        self.update()

        self.headerLayout.setPreferredWidth(self.getNodeWidth() - self.nodeLayout.spacing())

    def updateTextPosition(self):
        """
        Обновляет позицию текстового элемента, чтобы центрировать его в нижней части узла.
        """

        node_rect = self.boundingRect()
        text_rect = self.displayItem.boundingRect()

        x_pos = (node_rect.width() - text_rect.width()) / 2  # Центрирование по горизонтали
        y_pos = node_rect.height() - text_rect.height() - 5  # Отступ снизу
        self.displayItem.setPos(x_pos, y_pos)

    def getNodeWidthText(self):
        """
        Вычисляет и возвращает минимальную ширину узла с учётом ширины отображаемого текста.

        :return: Ширина узла.
        """
        text_width = self.displayItem.boundingRect().width()
        width = max(text_width, 100)

        if self.resizable:
            width = max(width, self._rect.width())

        return width

    def getNodeHeightText(self):
        """
        Вычисляет и возвращает минимальную высоту узла с учётом высоты отображаемого текста.

        :return: Высота узла.
        """
        text_height = self.displayItem.boundingRect().height()
        height = max(text_height, 75)

        if self.resizable:
            height = max(height, self._rect.height())

        if self.collapsed:
            height = min(self.minHeight, self.labelHeight + self.nodeLayout.spacing() * 2)

        return height

    def getNodeWidth(self):
        """
        Возвращает текущую ширину узла.

        :return: Ширина узла.
        """
        return self.getNodeWidthText()

    def getNodeHeight(self):
        """
        Возвращает текущую высоту узла.

        :return: Высота узла.
        """
        return self.getNodeHeightText()

    def onRefresh(self):
        """
        Обновляет форму и отображаемое значение узла при нажатии кнопки обновления.
        """
        return self.updateNodeShape()
