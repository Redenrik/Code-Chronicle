#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QCheckBox)

from file_explorer_summary import get_ignore_patterns, list_files, create_output_file, get_file_paths

def get_main_folder():
    # Assuming gui.py is located in src folder in the main project folder
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class ProjectExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Project Explorer')

        self.label = QLabel('Select a project folder:', self)
        self.label.move(20, 20)

        self.folder_edit = QLineEdit(self)
        self.folder_edit.textChanged.connect(self.set_folder_name)
        self.folder_edit.move(20, 50)

        self.folder_button = QPushButton('Browse', self)
        self.folder_button.move(250, 50)
        self.folder_button.clicked.connect(self.show_folder_dialog)

        self.summary_checkbox = QCheckBox('Generate script summary', self)
        self.summary_checkbox.move(20, 100)

        self.index_checkbox = QCheckBox('Generate file index', self)
        self.index_checkbox.move(20, 150)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.move(20, 200)
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_files)

        self.history_button = QPushButton('History', self)
        self.history_button.move(250, 200)
        self.history_button.clicked.connect(self.open_history_folder)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.move(20, 250)
        self.quit_button.clicked.connect(QApplication.instance().quit)

        self.show()

    def set_folder_name(self, text):
        self.folder_name = text.strip()
        if self.folder_name:
            self.generate_button.setEnabled(True)
        else:
            self.generate_button.setEnabled(False)

    def show_folder_dialog(self):
        folder_name = QFileDialog.getExistingDirectory(self, "Select project folder")
        if folder_name:
            self.folder_name = folder_name
            self.folder_edit.setText(self.folder_name)
            self.generate_button.setEnabled(True)

    def generate_files(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        main_folder = get_main_folder()
        history_folder = os.path.join(main_folder, "chronicle-history")
        os.makedirs(history_folder, exist_ok=True)

        ignore_patterns = get_ignore_patterns(self.folder_name)  # Pass the folder_name as the selected_folder

        if self.summary_checkbox.isChecked():
            output_file_name = f"{os.path.basename(self.folder_name)}_scripts-list_{timestamp}.txt"
            output_file_path = os.path.join(history_folder, output_file_name)
            file_paths = get_file_paths(self.folder_name, ignore_patterns)
            create_output_file(file_paths, output_file_path)
            subprocess.Popen(['notepad.exe', output_file_path], close_fds=True)

        if self.index_checkbox.isChecked():
            output_file_name = f"{os.path.basename(self.folder_name)}_file-index_{timestamp}.txt"
            output_file_path = os.path.join(history_folder, output_file_name)
            list_files(self.folder_name, ignore_patterns, output_file_path)
            subprocess.Popen(['notepad.exe', output_file_path], close_fds=True)


    def open_history_folder(self):
        main_folder = get_main_folder()
        history_folder = os.path.join(main_folder, "chronicle-history")
        os.startfile(history_folder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectExplorer()
    sys.exit(app.exec_())