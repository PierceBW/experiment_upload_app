#File for a new window with a string input when other is selected with a radio button
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox
from PyQt6.QtCore import Qt

class StringInputPopupWindow(QDialog):
    """
    Pop up window for inputting a string when other is selected in a radio button
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)
        
        self.setWindowTitle("Enter an Experiment Type")
        self.setLayout(layout)

        inputlbl = QLabel("Experiment Type:")
        layout.addWidget(inputlbl, 1, 0)
        self.input = QLineEdit()
        layout.addWidget(self.input, 1, 1)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

    def get_value(self):
        """
        Returns: 
            str: The string inputted in the input line so that it is usable in the main window
        """
        return self.input.text()


