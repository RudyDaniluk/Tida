import sys
import os
import shutil
import subprocess  
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QMimeData
from PyQt5.uic import loadUi

class ClipClapApp(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('clip_clap.ui', self)  
        
        self.browseButton.clicked.connect(self.browse_files)
        self.saveButton.clicked.connect(self.save_txt)
        self.useCopyButton.clicked.connect(self.copy_file_to_clipboard)
        self.openDirectoryButton.clicked.connect(self.open_directory)
        self.removeButton.clicked.connect(self.remove_file)
        
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.add_file_to_list(file_path)

    def add_file_to_list(self, file_path):
        row_position = self.fileTable.rowCount()
        self.fileTable.insertRow(row_position)

        icon = QIcon(file_path)
        
        icon_item = QTableWidgetItem()
        icon_item.setIcon(icon)  
        file_item = QTableWidgetItem(file_path)

        self.fileTable.setItem(row_position, 0, icon_item)
        self.fileTable.setItem(row_position, 1, file_item)

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Wybierz pliki", "", "All Files (*)")
        for file in files:
            self.add_file_to_list(file)

    def save_txt(self):
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Wybierz katalog", "", options=options)
        if directory:
            file_path = os.path.join(directory, "file_list.txt")
            with open(file_path, 'w') as f:
                for row in range(self.fileTable.rowCount()):
                    file_item = self.fileTable.item(row, 1)
                    f.write(file_item.text() + '\n')
            QMessageBox.information(self, "Sukces", f"Zapisano listę plików do {file_path}")

    def copy_file_to_clipboard(self):
        selected_row = self.fileTable.currentRow()
        if selected_row != -1:
            file_item = self.fileTable.item(selected_row, 1)
            file_path = file_item.text()

            if os.path.exists(file_path):
                try:
                    
                    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'application/octet-stream', file_path], check=True)
                    QMessageBox.information(self, "Sukces", "Plik skopiowany do schowka.")
                except subprocess.CalledProcessError:
                    QMessageBox.warning(self, "Błąd", "Nie udało się skopiować pliku do schowka.")
            else:
                QMessageBox.warning(self, "Błąd", "Plik nie istnieje.")
        else:
            QMessageBox.warning(self, "Błąd", "Nie wybrano pliku.")



    def open_directory(self):
        selected_row = self.fileTable.currentRow()
        if selected_row != -1:
            file_item = self.fileTable.item(selected_row, 1)
            file_path = file_item.text()
            directory = os.path.dirname(file_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(directory))
        else:
            QMessageBox.warning(self, "Błąd", "Nie wybrano pliku.")

    def remove_file(self):
        selected_row = self.fileTable.currentRow()
        if selected_row != -1:
            self.fileTable.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Błąd", "Nie wybrano pliku.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClipClapApp()
    window.show()
    sys.exit(app.exec_())
