from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QAction, QMainWindow
from qgis.gui import *
from geon.layer import LayerSet



class MainWindow(QMainWindow):
    def __init__(self, layerSet=None, extent=None):
        QMainWindow.__init__(self)
        self._canvas = QgsMapCanvas()
        self._canvas.setCanvasColor(Qt.white)
        self.setCentralWidget(self._canvas)
        self._layerSet = LayerSet()

        if layerSet:
            self._layerSet = layerSet
            self._canvas.setLayerSet(layerSet)

            if extent:
                self._extent = extent
            else:
                self._extent = self._layerSet.rawLayers[len(self._layerSet.rawLayers) - 1].extent()

            self._canvas.setExtent(self._extent)

        actionZoomIn = QAction("Zoom in", self)
        actionZoomOut = QAction("Zoom out", self)
        actionPan = QAction("Pan", self)

        actionZoomIn.setCheckable(True)
        actionZoomOut.setCheckable(True)
        actionPan.setCheckable(True)

        self.connect(actionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        self.connect(actionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        self.connect(actionPan, SIGNAL("triggered()"), self.pan)

        self.toolbar = self.addToolBar("_canvas actions")
        self.toolbar.addAction(actionZoomIn)
        self.toolbar.addAction(actionZoomOut)
        self.toolbar.addAction(actionPan)

        # create the map tools
        self.toolPan = QgsMapToolPan(self._canvas)
        self.toolPan.setAction(actionPan)
        self.toolZoomIn = QgsMapToolZoom(self._canvas, False)  # false = in
        self.toolZoomIn.setAction(actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self._canvas, True)  # true = out
        self.toolZoomOut.setAction(actionZoomOut)

        self.pan()

    def setLayerSet(self, layerSet, extent=None):
        self._layerSet = layerSet
        self._canvas.setLayerSet(layerSet)

        if extent:
            self._extent = extent
        else:
            self._extent = self._layerSet.rawLayers[len(self._layerSet.rawLayers) - 1].extent()

        self._canvas.setExtent(self._extent)

    def addLayerSet(self, layerSet):
        self._layerSet.appendLayerSet(layerSet)

    def zoomIn(self):
        self._canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self._canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self._canvas.setMapTool(self.toolPan)

    def _getCanvas(self):
        return self._canvas

    def _getLayerSet(self):
        return self._layerSet

    def _setLayerSet(self, newLayerSet):
        self._layerSet = newLayerSet

    def _getExtent(self):
        return self._extent

    def _setExtent(self, newExtent):
        self._extent = newExtent

    canvas = property(_getCanvas)
    extent = property(_getExtent, _setExtent)
    layerSet = property(_getLayerSet, _setLayerSet)

