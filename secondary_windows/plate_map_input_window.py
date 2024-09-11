from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QFileDialog, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from .popups import show_error_message
from .components.helper_functions.export_data import *

class DataWindow(QDialog):
    """
    Plate Map input window with all necessary inputs
    """
    def __init__ (self, data):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)
        self.data = data
        self.setWindowTitle("Experimental Upload App")
        self.setLayout(layout)

        title = QLabel("Your experimental data has been uploaded to S3")
        title.setStyleSheet("font-size: 16px;")
        layout.addWidget(title, 0, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)

        self.data = upload_data(self.data)

        print(self.data)


class PlateMapWindow(QDialog):
    """
    Plate Map input window with all necessary inputs
    """
    def __init__ (self, Main_window, data):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)
        self.data = data
        
        self.main_window = Main_window

        self.setWindowTitle("Experimental Upload App")
        self.setLayout(layout)

        title = QLabel("Plate Map Upload")
        title.setStyleSheet("font-size: 18px;")
        layout.addWidget(title, 0, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)

        #Experiment Units
        exp_unit = QLabel("Experiment Units")
        layout.addWidget(exp_unit, 1, 0, 1, 3)
        self.exp_unit_inp = QComboBox()
        self.exp_unit_inp.addItems(["nM", "ng/ml"])
        layout.addWidget(self.exp_unit_inp, 1, 3, 1, 3)

       # File Upload
        uploadtitle = QLabel("Please Select an Excel File to upload")
        layout.addWidget(uploadtitle, 2, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)
        self.fileButton = QPushButton("Upload File")
        self.fileButton.clicked.connect(self.open_file_path)
        layout.addWidget(self.fileButton, 3, 0, 1, 6)
       
        # Label to display selected file path
        self.filePathLabel = QLabel("Selected file: None")
        layout.addWidget(self.filePathLabel, 6, 0, 1, 6, Qt.AlignmentFlag.AlignCenter)

        #Buttons
        self.backButton = QPushButton("Back")
        self.backButton.clicked.connect(self.go_back)
        layout.addWidget(self.backButton, 7, 0, 1, 3)

        self.nextButton = QPushButton("Next")

        # Go to next page
        self.nextButton.clicked.connect(self.go_forward)
        layout.addWidget(self.nextButton, 7, 3, 1, 3)

        # Store file path
        self.file_path = ""

    def open_file_path(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            self.file_path = file_dialog.selectedFiles()[0]
            #get end of file name
            self.file_name = self.file_path.split("/")[-1]
            self.filePathLabel.setText(f"Selected file:\n{self.file_name}")

    def go_back(self):
        self.main_window.show()
        self.close()
    
    def go_forward(self):
        if self.file_path == "":
            show_error_message("No Excel File Path", "Please choose a valid Excel File path")
            return
        self.data["helpdata"]["file_path"] = self.file_path
        self.data["helpdata"]["experiment_units"] = self.exp_unit_inp.currentText()
        self.data_window = DataWindow(self.data)
        self.data_window.show()
        self.close()

# Data Obtaining
        
        """try: 
            selected_file = self.selected_file
        except AttributeError:
            self.show_error_message("Invalid Folder", "Please select a valid folder.")
            return"""

