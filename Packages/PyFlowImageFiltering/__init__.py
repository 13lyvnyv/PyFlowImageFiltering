PACKAGE_NAME = 'PyFlowImageFiltering'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage


# Function based nodes
from PyFlow.Packages.PyFlowImageFiltering.FunctionLibraries.ImageFilteringLib import ImageFilteringLib

# Factories
from PyFlow.Packages.PyFlowOpenCv.Factories.PinInputWidgetFactory import getInputWidget
from PyFlow.Packages.PyFlowImageFiltering.Factories.UINodeFactory import createUINode


from PyFlow.Packages.PyFlowImageFiltering.Nodes.ShowNumber import showNumber


_FOO_LIBS = {ImageFilteringLib.__name__: ImageFilteringLib(PACKAGE_NAME)}
_NODES = {showNumber.__name__: showNumber}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()




class PyFlowImageFiltering(IPackage):
	def __init__(self):
		super(PyFlowImageFiltering, self).__init__()

	@staticmethod
	def GetExporters():
		return _EXPORTERS

	@staticmethod
	def GetFunctionLibraries():
		return _FOO_LIBS

	@staticmethod
	def GetNodeClasses():
		return _NODES

	@staticmethod
	def GetPinClasses():
		return _PINS

	@staticmethod
	def GetToolClasses():
		return _TOOLS

	@staticmethod
	def UINodesFactory():
		return createUINode

	@staticmethod
	def PinsInputWidgetFactory():
		return getInputWidget

