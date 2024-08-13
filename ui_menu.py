from PyQt5.QtWidgets import QMenu, QAction, QInputDialog, QMessageBox

class Menu:
    def __init__(self, parent):
        self.parent = parent
        self.create_menu()

    def create_menu(self):
        menubar = self.parent.menuBar()
        
        # View menu
        view_menu = menubar.addMenu("View")

        zoom_in_action = QAction("Zoom In", self.parent)
        zoom_in_action.triggered.connect(self.parent.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self.parent)
        zoom_out_action.triggered.connect(self.parent.zoom_out)
        view_menu.addAction(zoom_out_action)

        zoom_default_action = QAction("Default Zoom", self.parent)
        zoom_default_action.triggered.connect(self.parent.zoom_default)
        view_menu.addAction(zoom_default_action)

        # Command menu
        command_menu = menubar.addMenu("Command")

        add_cmd_action = QAction("Add Command", self.parent)
        add_cmd_action.triggered.connect(self.add_custom_command)
        command_menu.addAction(add_cmd_action)

        edit_cmd_action = QAction("Edit Command", self.parent)
        edit_cmd_action.triggered.connect(self.edit_custom_command)
        command_menu.addAction(edit_cmd_action)

        delete_cmd_action = QAction("Delete Command", self.parent)
        delete_cmd_action.triggered.connect(self.delete_custom_command)
        command_menu.addAction(delete_cmd_action)

    def add_custom_command(self):
        if len(self.parent.custom_cmd_buttons) < 3:
            cmd, ok = QInputDialog.getText(self.parent, "Add Command", "Enter 3-character CMD:")
            if ok and len(cmd) == 3:
                if cmd in self.parent.cmd_buttons or cmd in self.parent.custom_cmd_buttons:
                    QMessageBox.warning(self.parent, "Input Error", "CMD already exists.")
                else:
                    self.parent.custom_cmd_buttons.append(cmd)
                    self.parent.ui_initializer.update_cmd_buttons_layout()  # No argument needed
            elif len(cmd) != 3:
                QMessageBox.warning(self.parent, "Input Error", "CMD must be 3 characters long.")
        else:
            QMessageBox.warning(self.parent, "Limit Reached", "You can only add up to 3 custom commands.")

    def edit_custom_command(self):
        """Edit an existing custom command."""
        if not self.parent.custom_cmd_buttons:
            QMessageBox.information(self.parent, "Info", "No custom commands to edit.")
            return

        cmd_to_edit, ok = QInputDialog.getItem(self.parent, "Edit Command", "Select command to edit:", self.parent.custom_cmd_buttons, 0, False)

        if ok and cmd_to_edit:
            new_cmd, ok = QInputDialog.getText(self.parent, "Edit Command", "Enter new 3-character CMD:")

            if ok and len(new_cmd) == 3:
                if new_cmd not in self.parent.cmd_buttons + self.parent.custom_cmd_buttons:
                    index = self.parent.custom_cmd_buttons.index(cmd_to_edit)
                    self.parent.custom_cmd_buttons[index] = new_cmd
                    self.parent.ui_initializer.update_cmd_buttons_layout()
                else:
                    QMessageBox.warning(self.parent, "Error", "New command already exists or is invalid.")
            else:
                QMessageBox.warning(self.parent, "Error", "Command must be exactly 3 characters.")

    def delete_custom_command(self):
        """Delete an existing custom command."""
        if not self.parent.custom_cmd_buttons:
            QMessageBox.information(self.parent, "Info", "No custom commands to delete.")
            return

        cmd_to_delete, ok = QInputDialog.getItem(self.parent, "Delete Command", "Select command to delete:", self.parent.custom_cmd_buttons, 0, False)

        if ok and cmd_to_delete:
            self.parent.custom_cmd_buttons.remove(cmd_to_delete)
            self.parent.ui_initializer.update_cmd_buttons_layout()
