from PyFlow.Packages.PyFlowOpenCv.UI.UIOpenCvBaseNode import UIOpenCvBaseNode
from PyFlow.Packages.PyFlowImageFiltering.UI.UIShowNumber import UIShowNumber

def createUINode(raw_instance):
	if raw_instance.__class__.__name__ == "showNumber":
		return UIShowNumber(raw_instance)
	return UIOpenCvBaseNode(raw_instance)
