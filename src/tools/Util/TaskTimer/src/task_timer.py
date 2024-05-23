import sys
import time
import json
import os
import logging
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QInputDialog,
    QMessageBox,
    QTextEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QComboBox,
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QClipboard

logging.basicConfig(
    filename="task_timer.log", level=logging.DEBUG, format="%(asctime)s %(message)s"
)


class TaskTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.tasks = {}
        self.current_task_name = None
        self.tasks_folder = "tasks"

        if not os.path.exists(self.tasks_folder):
            os.makedirs(self.tasks_folder)

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def init_ui(self):
        logging.debug("Initializing UI")
        self.setWindowTitle("Task Timer")

        main_layout = QVBoxLayout()

        task_layout = QHBoxLayout()

        self.label = QLabel("Elapsed Time: 0h 0m 0s")
        main_layout.addWidget(self.label)

        self.category_combobox = QComboBox()
        self.category_combobox.addItems(
            [
                "Administrative",
                "Research",
                "Planning",
                "UI Design",
                "UI Implementation",
                "Functional Coding",
                "Testing",
                "Meetings",
            ]
        )
        task_layout.addWidget(self.category_combobox)

        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name here")
        task_layout.addWidget(self.task_name_input)

        main_layout.addLayout(task_layout)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_timer)
        button_layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume")
        self.resume_button.clicked.connect(self.resume_timer)
        button_layout.addWidget(self.resume_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

        self.save_button = QPushButton("Save Tasks")
        self.save_button.clicked.connect(self.save_tasks)
        main_layout.addWidget(self.save_button)

        self.clear_display_button = QPushButton("Clear Display")
        self.clear_display_button.clicked.connect(self.clear_task_display)
        main_layout.addWidget(self.clear_display_button)

        self.copy_to_clipboard_button = QPushButton("Copy to Clipboard")
        self.copy_to_clipboard_button.clicked.connect(self.copy_to_clipboard)
        main_layout.addWidget(self.copy_to_clipboard_button)

        self.task_files_list = QListWidget()
        self.task_files_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_files_list.customContextMenuRequested.connect(self.show_context_menu)
        self.task_files_list.itemClicked.connect(self.load_tasks_from_file)
        main_layout.addWidget(self.task_files_list)

        self.task_display = QTextEdit()
        self.task_display.setReadOnly(True)
        main_layout.addWidget(self.task_display)

        self.setLayout(main_layout)

        self.update_task_files_list()

    def start_timer(self):
        task_name = self.task_name_input.text()
        if task_name == "":
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter a task name before starting the timer.",
            )
            return

        category = self.category_combobox.currentText()
        self.current_task_name = task_name

        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.timer.start(100)
            self.label.setText("Timer started")
            self.start_button.setEnabled(False)

    def pause_timer(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            self.timer.stop()
            self.label.setText("Timer paused")
            self.start_button.setEnabled(True)

    def resume_timer(self):
        task_name = self.task_name_input.text()
        category = self.category_combobox.currentText()
        self.current_task_name = task_name

        if not self.running:
            if self.current_task_name in self.tasks:
                self.elapsed_time = self.tasks[self.current_task_name]["duration"]
            else:
                self.elapsed_time = 0

            self.start_time = time.time()
            self.running = True
            self.timer.start(100)
            self.label.setText("Timer resumed")
            self.start_button.setEnabled(False)

    def stop_timer(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            self.timer.stop()
            self.start_button.setEnabled(True)
        if self.current_task_name:
            self.tasks[self.current_task_name] = {
                "duration": self.elapsed_time,
                "task_type": self.category_combobox.currentText(),
            }
            self.current_task_name = None
            self.elapsed_time = 0
            self.update_task_display()
            self.label.setText("Timer stopped")

    def save_tasks(self):
        if not self.tasks:
            QMessageBox.warning(self, "Save Tasks", "No tasks to save.")
            return

        filename, ok = QInputDialog.getText(self, "Save Tasks", "Enter filename:")
        if ok:
            filepath = os.path.join(self.tasks_folder, filename + ".json")
            with open(filepath, "w") as f:
                json.dump(self.tasks, f)
            self.update_task_files_list()
            QMessageBox.information(self, "Save Tasks", "Tasks saved successfully")

    def load_tasks_from_file(self, item):
        filename = item.text()
        filepath = os.path.join(self.tasks_folder, filename)
        try:
            with open(filepath, "r") as f:
                self.tasks = json.load(f)
            self.update_task_display()
        except FileNotFoundError:
            QMessageBox.warning(self, "Load Tasks", "No saved tasks found")

    def delete_task_file(self):
        selected_items = self.task_files_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            filename = item.text()
            filepath = os.path.join(self.tasks_folder, filename)
            os.remove(filepath)
            self.update_task_files_list()
            QMessageBox.information(
                self, "Delete Task File", "Task file deleted successfully"
            )

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_task_file)
        menu.exec(self.task_files_list.mapToGlobal(position))

    def update_timer(self):
        if self.running:
            elapsed = self.elapsed_time + (time.time() - self.start_time)
            self.label.setText(f"Elapsed Time: {self.format_time(elapsed)}")

    def update_task_display(self):
        self.task_display.clear()
        for task_name, details in self.tasks.items():
            elapsed = details["duration"]
            self.task_display.append(
                f"Task: {task_name}, Duration: {self.format_time(elapsed)}"
            )

    def clear_task_display(self):
        self.task_display.clear()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        tasks_text = ""
        for task_name, details in self.tasks.items():
            # Remove the category from the task name
            hours = details["duration"] / 3600
            tasks_text += f"{task_name}\t{hours:.2f}\n"
        clipboard.setText(tasks_text)
        QMessageBox.information(
            self, "Copy to Clipboard", "Tasks copied to clipboard in spreadsheet format"
        )

    def update_task_files_list(self):
        self.task_files_list.clear()
        task_files = [f for f in os.listdir(self.tasks_folder) if f.endswith(".json")]
        for task_file in task_files:
            self.task_files_list.addItem(QListWidgetItem(task_file))

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"


if __name__ == "__main__":
    logging.debug("Starting application")
    app = QApplication(sys.argv)

    window = TaskTimer()
    window.show()

    sys.exit(app.exec())
