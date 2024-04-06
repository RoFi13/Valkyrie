# Copyright (C) 2023 Robert Wiese - All Rights Reserved.
"""Build Pipeline File Menu within Maya."""

import logging
import os
import sys

from maya import cmds
from maya import mel

import yaml


PY_VERSION = sys.version

LOG = logging.getLogger(os.path.basename(__file__))


class BuildPipeMenu:
    """Class representing menu."""

    def __init__(self, menu_id="Pipe_menu", menu_label="Pipe Tools"):
        """Initiate build for menu."""
        self.menu_tracker = []
        self.current_menu_level = 0
        self.menu_id = menu_id
        self.menu_label = menu_label
        self.main_maya_window = mel.eval("$tempMelVar=$gMainWindow")
        self.yaml_menu_path = f"{os.path.split(__file__)[0]}\\pipe_menu_commands.yaml"

        if os.path.exists(self.yaml_menu_path) is False:
            raise RuntimeError(
                f"Failed to find menu commands yaml file at: {self.yaml_menu_path}"
            )

        self.verify_menu_exists()

        self.create_menu()

    def verify_menu_exists(self):
        """Verify the menu exists."""
        if cmds.menu(self.menu_id, query=True, exists=True):
            LOG.info("Menu exists. Deleting menu...")
            cmds.deleteUI(self.menu_id, menu=True)
            return

        LOG.info("Menu doesn't exist.")

    def create_menu(self):
        """Create menu."""
        self.menu_tracker.append(
            cmds.menu(
                self.menu_id,
                label=self.menu_label,
                tearOff=True,
                parent=self.main_maya_window,
            )
        )

        # Get custom menu data from yaml file
        with open(self.yaml_menu_path, encoding="utf-8") as menu_yaml:
            data = yaml.safe_load(menu_yaml)

        # Build custom menu recursively
        self.recursively_create_menu(data)

        LOG.info("Pipe Menu successfully built!")

    def recursively_create_menu(self, yaml_data):
        """Recursively creates menu."""
        # For each dictionary in list...
        for menu_dict in yaml_data:
            # For each key in dictionary...
            for key in menu_dict:
                # If key's value == list... i.e. list = new sub-menu...
                if isinstance(menu_dict[key], list):
                    # Create sub menu and then call itself (recurse)
                    self.menu_tracker.append(
                        self.create_sub_menu(
                            key, self.menu_tracker[self.current_menu_level]
                        )
                    )
                    self.current_menu_level += 1
                    self.recursively_create_menu(menu_dict[key])

                # If key's value != list... i.e. a string = new command button
                else:
                    # Create new button
                    if self.current_menu_level == 0:
                        self.create_menu_item(menu_dict, self.menu_tracker[0])
                    else:
                        self.create_menu_item(
                            menu_dict, self.menu_tracker[self.current_menu_level]
                        )
                    break

        # Go back one level deep and remove the last sub menu from list
        self.current_menu_level -= 1
        self.menu_tracker.pop()

    def create_sub_menu(self, current_menu, menu_parent):
        """Create the sub_menu."""
        new_menu = cmds.menuItem(
            current_menu,
            label=current_menu,
            parent=menu_parent,
            subMenu=True,
            tearOff=True,
        )
        return new_menu

    def create_menu_item(self, menu_dict, menu_parent):
        """Create items within the menu."""
        if "icon" in menu_dict:
            LOG.debug("Added menu item with icon.")
            new_menu_item = cmds.menuItem(
                menu_dict["label"],
                label=menu_dict["label"],
                image=menu_dict["icon"],
                command=menu_dict["command"],
                sourceType=menu_dict["lang"],
                parent=menu_parent,
            )

        elif "divider" in menu_dict:
            LOG.debug("Added divider.")
            if "None" in menu_dict["divider"]:
                new_menu_item = cmds.menuItem(divider=True, parent=menu_parent)
            else:
                new_menu_item = cmds.menuItem(
                    divider=True, label=menu_dict["divider"], parent=menu_parent
                )

        else:
            LOG.debug("Added menu item without icon.")
            new_menu_item = cmds.menuItem(
                menu_dict["label"],
                label=menu_dict["label"],
                command=menu_dict["command"],
                sourceType=menu_dict["lang"],
                parent=menu_parent,
            )

        return new_menu_item


def reload_menu():
    """Rebuild the menu."""
    # Build a menu and parent under the Maya Window
    menu_id = "Pipe_menu"

    if cmds.menu(menu_id, query=True, exists=True):
        cmds.deleteUI(menu_id, menu=True)

    BuildPipeMenu()
