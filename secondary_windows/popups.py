#Popup Error Messages
from PyQt6.QtWidgets import QMessageBox

def show_error_message(title, message):
    """
    When there is an invalid input or no input when collecting data this creates a popup window that lets the user know
    Args:
        title(string): the title of the error message for the pop up window
        message(string): the text in the error window
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec()
    
def show_warning_message(title, message):
    """
    When there is no input in a field but it is not necassary it throws a warning message
    Args:
        title(string): the title of the warning message for the pop up window
        message(string): the text in the warning window
        """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    result = msg.exec()
    return result == QMessageBox.StandardButton.Ok