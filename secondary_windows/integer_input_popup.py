#File for a new window with an integer input when other is selected with a radio button
from PyQt6.QtWidgets import QDialog, QGridLayout, QSpinBox, QDialogButtonBox
from PyQt6.QtCore import Qt

class IntegerInputPopupWindow(QDialog):
    """
    Pop up window for inputting a value when other is selected in a radio button
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)
        
        self.setWindowTitle("Enter an Integer")
        self.setLayout(layout)

        self.input_spinbox = QSpinBox()
        self.input_spinbox.setMinimum(-1000000)
        self.input_spinbox.setMaximum(1000000)

        layout.addWidget(self.input_spinbox, 0, 0)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box, 1, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

    def get_value(self):
        """
        Returns: 
            int: The value inputted in the spinbox so that it is usable in the main window
        """
        return self.input_spinbox.value()