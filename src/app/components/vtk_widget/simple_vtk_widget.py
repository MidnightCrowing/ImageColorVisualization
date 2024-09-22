from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from src.point_cloud import VTKManager


class SimpleVTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super(SimpleVTKWidget, self).__init__(parent)

        self.vtk_manager = VTKManager(self)
