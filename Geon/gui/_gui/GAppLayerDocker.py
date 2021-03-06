from PyQt4.Qt import QDockWidget, QWidget, QVBoxLayout
from PyQt4.QtCore import Qt, SIGNAL

from GAppLayerW import GAppLayerW
from GDocker import GDocker


# Class for layer storage
class GAppLayerDocker(GDocker):
    def __init__(self, parent=None, layerSet=None, linkedCanvas=None):
        GDocker.__init__(self, parent)

        maxDockerElem = 4
        if len(layerSet) < maxDockerElem:
            maxDockerElem = len(layerSet)

        widgetsWidth = parent.width() / maxDockerElem

        # Set dock parameters
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable)
        self.setMinimumWidth(widgetsWidth)

        # Set main container parameter
        self._container = QWidget(self)
        self._container.setMinimumWidth(widgetsWidth)
        self.setWidget(self._container)

        # Vertical layout for the container (vertical dock)
        self._layout = QVBoxLayout(self._container)

        # Store the canvas of layers
        self._layerPortfolio = []

        # For each layer in layer set :
        for i in range(0, len(layerSet)):
            # Create a new widget
            layerWidget = GAppLayerW(layerSet[i], layerSet.rawLayers[i], linkedCanvas, self)

            # Set its properties
            layerWidget.setMinimumWidth(widgetsWidth)

            # Connect its with main canvas
            self.connect(linkedCanvas, SIGNAL("mapCanvasRefreshed()"), layerWidget.refreshExtent)

            # Add it to portfolio and display it
            self._layerPortfolio.append(layerWidget)
            self._layout.addWidget(layerWidget)

    def moveWidgetUp(self, widget):
        newIndex = self._layout.indexOf(widget) - 1
        if newIndex >= 0:
            self._layout.removeWidget(widget)
            self._layout.insertWidget(newIndex, widget)

    def moveWidgetDown(self, widget):
        newIndex = self._layout.indexOf(widget) + 1
        if newIndex < len(self._layout):
            self._layout.removeWidget(widget)
            self._layout.insertWidget(newIndex, widget)

    def _getLayout(self):
        return self._layout

    layout = property(_getLayout)
