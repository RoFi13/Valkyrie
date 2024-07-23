# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Various Project utility functions."""

# Can't find PySide2 modules pylint: disable=I1101
# create_progress_bar
# update_progress_bar

import logging
import os

from Core import core_paths as cpath

from PySide6 import QtCore, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QBoxLayout,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressDialog,
    QPushButton,
    QSpacerItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

LOADER = QUiLoader()

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


def setup_class_ui(
    tool_object: QMainWindow,
    window_object_name: str,
    window_title: str,
    ui_details: dict,
):
    """Set default class UI settings for PySide tools.

    Args:
        tool_object (QMainWindow): Class object setting defaults for.
        window_object_name (str): Window object name in memory.
        window_title (str): Window title.
        ui_details (dict): UI details in dictionary as follows:
            'main_ui_file': 'String path to main class UI file.'
            'min_size': [x: int, y: int]
            'max_size': [x: int, y: int]

    Returns:
        QWidget: Main tool widget.
    """

    # Set object name and window title
    tool_object.setObjectName(window_object_name)
    tool_object.setWindowTitle(window_title)

    if len(ui_details["min_size"]) > 0:
        tool_object.setMinimumSize(ui_details["min_size"][0], ui_details["min_size"][1])
    if len(ui_details["max_size"]) > 0:
        tool_object.setMaximumSize(ui_details["max_size"][0], ui_details["max_size"][1])

    # Window type
    tool_object.setWindowFlags(QtCore.Qt.Window)

    # Makes Maya perform magic which makes the window stay
    # on top in OS X and Linux. As an added bonus, it'll
    # make Maya remember the window position
    tool_object.setProperty("saveWindowPref", True)

    # Load UI file for class object
    LOG.info("Loading UI file: %s", ui_details["main_ui_file"])
    main_tool_widget = LOADER.load(ui_details["main_ui_file"], tool_object)

    # Set the main widget
    tool_object.setCentralWidget(main_tool_widget.root_widget)

    # Set common shared icons directory
    QtCore.QDir.addSearchPath("shared_icons", MAIN_PATHS["shared_icons"])

    # Set main stylesheet
    LOG.info("Setting style sheet: %s", MAIN_PATHS["stylesheet"])
    with open(MAIN_PATHS["stylesheet"], "r", encoding="utf-8") as style_sheet_file:
        main_tool_widget.root_widget.setStyleSheet(style_sheet_file.read())

    return main_tool_widget


def update_combobox(
    combobox: QComboBox,
    new_options: list,
    sort_options=False,
    reverse_sort=False,
    clear=True,
):
    """_summary_

    Args:
        combobox (QComboBox): _description_
        new_options (list): _description_
        sort_options (bool, optional): _description_. fdaf da fdaf dafda fdaf daf daf d.
            Defaults to False.
        reverse_sort (bool, optional): _description_. Defaults to False.
        clear (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """

    if len(new_options) == 0:
        LOG.warning("List of new options is empty.")
        return False

    if clear is True:
        combobox.clear()

    if sort_options is True:
        new_options.sort(reverse=reverse_sort)

    for option in new_options:
        combobox.addItem(option)

    return True


def set_label_pixmap(label: QLabel, image_path: str):
    """Set a QLabel object's pixmap image.

    Args:
        label (qLabel): QLabel object to change image for.
        image_path (str): Image file path.
    """

    new_pixmap = QtGui.QPixmap(image_path)
    label.setScaledContents(True)
    label.setPixmap(
        new_pixmap.scaled(label.width(), label.height(), QtCore.Qt.KeepAspectRatio)
    )


def create_progress_bar(
    title: str, initial_label: str, number_of_operations: int, parent_ui_object: QWidget
):
    """Create a progress bar.

    Args:
        title (str): Title of progress bar window.
        initial_label (str): Initial starting progress bar label.
        number_of_operations (int): Number of operations to reach 100%.
        parent_ui_object (QWidget): parent widget of this progress bar.

    Returns:
        QWidget of newly create progress bar.
    """

    progress_bar = QProgressDialog(
        title, None, 0, number_of_operations, parent_ui_object
    )
    progress_bar.setWindowTitle(title)
    progress_bar.setValue(0)
    progress_bar.setWindowModality(QtCore.Qt.WindowModal)
    progress_bar.show()
    QtCore.QCoreApplication.processEvents()
    progress_bar.setLabelText(initial_label)
    return progress_bar


def update_progress_bar(progress_bar: QProgressDialog, new_label: str = None):
    """Update Progress bar.

    Args:
        progress_bar (QProgressDialo): Object of progress bar.
        new_label (str): New value for the progress bar.
    """

    progress_bar.setValue(progress_bar.value() + 1)

    if new_label is not None:
        progress_bar.setLabelText(new_label)

    QtCore.QCoreApplication.processEvents()


def create_new_button(
    text: str = "",
    icon_path: str = "",
    icon_size: QtCore.QSize = None,
    minimum_size: QtCore.QSize = None,
    maximum_size: QtCore.QSize = None,
):
    """Create new Pyside Button.

    Args:
        text (str, optional): Button text. Defaults to "".
        icon_path (str, optional): Button icon path. Defaults to "".
        icon_size (QtCore.QSize, optional): Icon size. Defaults to None.
        minimum_size (QtCore.QSize, optional): Minimum x and y size. Defaults to None.
        maximum_size (QtCore.QSize, optional): Maximum x and y size. Defaults to None.

    Returns:
        QPushButton: Returns newly created Button widget.
    """

    new_button = QPushButton(text)

    if minimum_size is not None:
        new_button.setMinimumSize(minimum_size)

    if maximum_size is not None:
        new_button.setMaximumSize(maximum_size)

    if len(icon_path) > 0:
        new_button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))

    if icon_size is not None:
        new_button.setIconSize(icon_size)

    return new_button


def clear_grid_layout(grid_layout: QGridLayout):
    """Clear all widgets from a grid layout.

    Args:
        grid_layout (QGridLayout): Grid to clear of widgets.
    """
    # Loop backwards to avoid indexing issues while removing items
    for i in reversed(range(grid_layout.count())):
        item = grid_layout.itemAt(i)
        widget = item.widget()
        if widget:
            grid_layout.removeWidget(widget)
            widget.deleteLater()  # Safely delete the widget


def clear_box_layout(box_layout: QBoxLayout):
    """Clear the Box Layout of all items and widgets.

    Args:
        box_layout (QBoxLayout): Box layout to clear of items and widgets.
    """
    # Iterate backwards to avoid indexing issues after removal
    for i in range(box_layout.count() - 1, -1, -1):
        item = box_layout.takeAt(i)
        if item.widget():
            # If the item is a widget, remove and delete it
            widget = item.widget()
            widget.deleteLater()
        elif item.layout():
            # If the item is a layout, recursively clear the layout and then delete it
            clear_box_layout(item.layout())
            item.layout().deleteLater()
        elif item.spacerItem():
            # For spacer items, the takeAt() already removes the spacer item
            pass


def create_line(create_horizontal: bool = True) -> QFrame:
    """Create either horizontal or vertical line widget."""
    new_line = QFrame()
    if create_horizontal:
        new_line.setFrameShape(QFrame.HLine)
    else:
        new_line.setFrameShape(QFrame.VLine)

    new_line.setFrameShadow(QFrame.Sunken)
    return new_line


def move_children_to_parent(
    new_parent_item: QTreeWidgetItem, old_parent_item: QTreeWidgetItem
):
    """Move item's child items to a new parent."""
    new_parent_item.addChildren(old_parent_item.takeChildren())


def get_tree_item_children(parent_item: QTreeWidgetItem):
    """Get QTreeWidgetItem's children item widgets."""
    return [parent_item.child(i) for i in range(parent_item.childCount())]


def remove_tree_item(tree_widget: QTreeWidget, tree_item: QTreeWidgetItem):
    """Remove QTreeWidgetItem from QTreeWidget."""
    parent = tree_item.parent()
    if parent is None:
        # Item is a top-level item
        index = tree_widget.indexOfTopLevelItem(tree_item)
        if index != -1:
            tree_widget.takeTopLevelItem(index)
    else:
        # Item is a child item
        parent.removeChild(tree_item)


def add_line_edit_regex(line_widget: QLineEdit, regex_pattern: str) -> None:
    line_regex_obj = QtCore.QRegularExpression(regex_pattern)
    line_regex_validator = QtGui.QRegularExpressionValidator(line_regex_obj)
    # Assign text validators
    line_widget.setValidator(line_regex_validator)


if __name__ == "__main__":
    pass
