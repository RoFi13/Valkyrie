# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Classes for snipping widget tool."""
# Can't find PySide2 modules pylint: disable=I1101

import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets

from Core import core_paths as cpath

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


class CustomPreviewButton(QtWidgets.QLabel):
    """Create a custom button widget with an image preview."""

    def __init__(self, parent_class, parent=None):
        """Initialize instance of tool.

        Set up the default image and icon.

        Args:
            parent_class (obj): Parent class to init from.
            parent (None, optional): Optional parent object to init from.
        """
        super().__init__(parent)
        LOG.info("Creating custom preview widget with snipping tool...")

        self.parent_class = parent_class
        self.setFixedSize(200, 200)
        self.setStyleSheet(
            "border-style: solid; border-width: 2px; border-color: black"
        )

        self.default_preview_icon = (
            f"{MAIN_PATHS['repo_resources']}/Placeholders/Snapshot_Default.png"
        )
        LOG.debug("DEFAULT PREVIEW ICON: %s", self.default_preview_icon)

        if os.path.exists(self.default_preview_icon) is False:
            LOG.error(
                "Failed to find default preview image at: %s", self.default_preview_icon
            )
            self.deleteLater()
            return

        # Set the qLabel's current image path as the default icon
        self.current_image_path = self.default_preview_icon
        # Set default image for qLabel
        self.image_pix = QtGui.QPixmap(self.default_preview_icon)
        # Resize to fit qLabel
        self.resized_pix = self.image_pix.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        # Set image
        self.setPixmap(self.resized_pix)
        # Set widget
        self.snipping_widget = None

    def grab_preview(self):
        """Grab the preview of widget."""
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.snipping_widget.start()

    def on_snipping_completed(self, frame):
        """Set the frame of the image."""
        self.setWindowState(QtCore.Qt.WindowActive)
        if frame is None:
            return

        preview_pix = frame
        # Scale keeping aspect ratio of preview image to size of qLabel widget
        resized_preview_pix = preview_pix.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        # Set pixmap for label
        self.setPixmap(resized_preview_pix)
        # Set the qLabel's current image path to the new playblasted image
        self.current_image_path = "CustomPreview"

    def set_preview_widget(self, preview_path):
        """Set the qLabel's image to the newly rendered image."""
        # Create pixmap for preview still image
        preview_pix = QtGui.QPixmap(preview_path)
        # Scale keeping aspect ratio of preview image to size of qLabel widget
        resized_preview_pix = preview_pix.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        # Set pixmap for label
        self.setPixmap(resized_preview_pix)
        # Set the qLabel's current image path to the new playblasted image
        self.current_image_path = preview_path

    def reset_preview_widget(self):
        """Set the label's image back to the default image."""
        # Set default image for qLabel
        self.image_pix = QtGui.QPixmap(self.default_preview_icon)
        # Resize to fit qLabel
        self.resized_pix = self.image_pix.scaled(
            200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        # Set image
        self.setPixmap(self.resized_pix)
        self.current_image_path = self.default_preview_icon

    def mousePressEvent(  # Overriden method. pylint: disable=invalid-name
        self,
        mouse_event,  # QtCore.Qt required arg for override pylint: disable=unused-argument
    ):
        """Mouse press event."""
        self.snipping_widget = SnippingWidget(app=QtWidgets.QApplication.instance())
        self.snipping_widget.on_snipping_completed = self.on_snipping_completed
        self.grab_preview()


# Refer to https://github.com/harupy/snipping-tool
class SnippingWidget(QtWidgets.QWidget):
    """Function to make snipping tool."""

    IS_SNIPPING = False

    def __init__(self, parent=None, app=None):
        """Create a program that works like the snipping tool in Windows.

        Args:
            parent (None, optional): Optional parent object to init from.
            app (None, optional): Optional app object to init from.
        """
        # Retain python2 style to deploy tools.
        # pylint: disable=R1725
        super(SnippingWidget, self).__init__()
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.screen = app.primaryScreen()
        self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.on_snipping_completed = None

    def start(self):
        """Start function of a show."""
        SnippingWidget.IS_SNIPPING = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(  # Overriden method. pylint: disable=invalid-name
        self, event
    ):  # QtCore.Qt required arg for override pylint: disable=unused-argument
        """Drawrect paint event."""
        if SnippingWidget.IS_SNIPPING:
            brush_color = (255, 128, 128, 100)
            line_width = 3
            opacity = 0.3
        else:
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            line_width = 0
            opacity = 0

        self.setWindowOpacity(opacity)
        q_point = QtGui.QPainter(self)
        q_point.setPen(QtGui.QPen(QtGui.QColor("black"), line_width))
        q_point.setBrush(QtGui.QColor(*brush_color))
        rect = QtCore.QRectF(self.begin, self.end)
        q_point.drawRect(rect)

    def mousePressEvent(self, event):  # Overriden method. pylint: disable=invalid-name
        """Mouse press event."""
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):  # Overriden method. pylint: disable=invalid-name
        """Mouse move event.

        Args:
            event (obj): An object with the mouse action
        """
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(  # Overriden method. pylint: disable=invalid-name
        self,
        event,  # QtCore.Qt required arg for override pylint: disable=unused-argument
    ):
        """Mouse release event."""
        SnippingWidget.IS_SNIPPING = False
        QtWidgets.QApplication.restoreOverrideCursor()
        min_x = min(self.begin.x(), self.end.x())
        min_y = min(self.begin.y(), self.end.y())
        max_x = max(self.begin.x(), self.end.x())
        max_y = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()

        img = QtGui.QPixmap.grabWindow(
            QtWidgets.QApplication.desktop().winId(),
            min_x,
            min_y,
            max_x - min_x,
            max_y - min_y,
        )

        if self.on_snipping_completed is not None:
            self.on_snipping_completed(img)
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.ArrowCursor)
            )

        self.deleteLater()
        self.close()
