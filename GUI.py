#Main file for first window of GUI
import sys
from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QDateEdit, QTextEdit, QMessageBox, 
                             QComboBox, QRadioButton, QButtonGroup, QDialog)
from secondary_windows import IntegerInputPopupWindow, StringInputPopupWindow
from secondary_windows.components.helper_functions.import_experiment_data import experiments
from secondary_windows.plate_map_input_window import PlateMapWindow
from secondary_windows.popups import show_error_message, show_warning_message

app = QApplication(sys.argv)

#invalid date list can be removed?
date_list = ["240625", "240725", "240925"]

class MainWindow(QWidget):
    """
    Main window with all necessary inputs
    """
    def __init__ (self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)

        self.setWindowTitle("Experimental Upload App")
        self.setLayout(layout)

        title = QLabel("Experimental Data Upload")
        title.setStyleSheet("font-size: 18px;")
        layout.addWidget(title, 0, 0, 1, 5, Qt.AlignmentFlag.AlignCenter)

        #Experiment Name
        exp_nm = QLabel("Experiment Name")
        layout.addWidget(exp_nm, 1, 0, 1, 2)
        self.exp_nm_inp = QLineEdit()
        layout.addWidget(self.exp_nm_inp, 1, 2, 1, 3)

        #Experiment Date
            #Date selector
        exp_dt = QLabel("Experiment Date")
        layout.addWidget(exp_dt, 2, 0, 1, 2)
            #Date editor
        self.exp_dt_inp = QDateEdit()
        self.exp_dt_inp.setDate(QDate.currentDate())
        self.exp_dt_inp.setCalendarPopup(True)
        layout.addWidget(self.exp_dt_inp, 2, 2, 1, 3)

        #Replicate Count
        rplct_cnt = QLabel("Replicate Count")
        layout.addWidget(rplct_cnt, 3, 0, 1, 2)
        #Add the input for this still
        self.rpl_ct_bg = QButtonGroup(self)
        self.rpl_b1 = QRadioButton("High")
        self.rpl_b2 = QRadioButton("Low")
        self.rpl_b3 = QRadioButton("Other")

        self.rpl_ct_bg.addButton(self.rpl_b1)
        self.rpl_ct_bg.addButton(self.rpl_b2)
        self.rpl_ct_bg.addButton(self.rpl_b3)

        layout.addWidget(self.rpl_b1, 3, 2)
        layout.addWidget(self.rpl_b2, 3, 3)
        layout.addWidget(self.rpl_b3, 3, 4)

        #Handle Radio Button Clicks
        self.rpl_ct_bg.buttonClicked.connect(self.handle_rep_cnt_btns)

        # Line edit for "Other" option
        self.other_input = QLineEdit()
        self.other_input.setPlaceholderText("Enter value")
        self.other_input.setEnabled(False)
        layout.addWidget(self.other_input, 13, 0, 1, 4)

        #Lab Tech
        lb_tch = QLabel("Lab Tech (Initials)")
        layout.addWidget(lb_tch, 4, 0, 1, 2)
        self.lb_tch_inp = QLineEdit()
        layout.addWidget(self.lb_tch_inp, 4, 2, 1, 3)

        #Cell Type
        cll_typ = QLabel("Cell Type")
        layout.addWidget(cll_typ, 5, 0, 1, 2)
        self.cll_typ_inp = QComboBox()
        self.cll_typ_inp.addItems(["hndf", "hacat"])
        layout.addWidget(self.cll_typ_inp, 5, 2, 1, 3)

        #Layout Type
        lyt_typ = QLabel("Layout Type")
        layout.addWidget(lyt_typ, 6, 0, 1, 2)
        self.lyt_typ_inp = QComboBox()
        self.lyt_typ_inp.addItems(["Plate"])
        layout.addWidget(self.lyt_typ_inp, 6, 2, 1, 3)

        #Experiment Type
        exp_typ = QLabel("Experiment Type")
        layout.addWidget(exp_typ, 7, 0, 1, 2)
        #Add the input for this still
        self.exp_typ_bg = QButtonGroup(self)
        self.exp_b1 = QRadioButton("edu")
        self.exp_b2 = QRadioButton("mft")
        self.exp_b3 = QRadioButton("Other")

        self.exp_typ_bg.addButton(self.exp_b1)
        self.exp_typ_bg.addButton(self.exp_b2)
        self.exp_typ_bg.addButton(self.exp_b3)

        layout.addWidget(self.exp_b1, 7, 2)
        layout.addWidget(self.exp_b2, 7, 3)
        layout.addWidget(self.exp_b3, 7, 4)

        #Handle Radio Button Clicks
        self.exp_typ_bg.buttonClicked.connect(self.handle_exp_typ_btns)

        #Additional Data Textbox
        textbox = QLabel("Experiment Description:")
        layout.addWidget(textbox, 10, 0, 1, 4)
        self.datainput = QTextEdit()
        layout.addWidget(self.datainput, 11, 0, 3, 5)

        # Enter button
        self.enterButton = QPushButton("Enter")
        self.enterButton.clicked.connect(self.collect_data)
        layout.addWidget(self.enterButton, 15, 0, 1, 5)

        self.rep_other_value = None
        self.exp_other_value = None
    
    def handle_rep_cnt_btns(self):
        """
        Handles when the radio buttons for replicate count are interacted with. 
        If the other button is selected (b3) the popup window is activated and the value inputted is past back to the main window.
        If the cancel button on the window is selected the else statment resets the buttons so none are selected.
        """
        if self.rpl_b3.isChecked():
            dialog = IntegerInputPopupWindow(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.rep_other_value = dialog.get_value()

            else:
                self.rpl_ct_bg.setExclusive(False)  # Temporarily disable exclusivity
                self.rpl_b3.setChecked(False)
                self.rpl_ct_bg.setExclusive(True)  # Re-enable exclusivity
                self.rep_other_value = None

    def handle_exp_typ_btns(self):
        """
        Handles when the radio buttons for experiment are interacted with. 
        If the other button is selected (b3) the popup window is activated and the string inputted is past back to the main window.
        If the cancel button on the window is selected the else statment resets the buttons so none are selected.
        """
        if self.exp_b3.isChecked():
            dialog = StringInputPopupWindow(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.exp_other_value = dialog.get_value()
            else:
                self.exp_typ_bg.setExclusive(False)  # Temporarily disable exclusivity
                self.exp_b3.setChecked(False)
                self.exp_typ_bg.setExclusive(True)  # Re-enable exclusivity
                self.exp_other_value = None
    
    def get_other_val(self, buttonslist, otherbutton, otherval):
        """
        Handles retrieving the value from a group of radio buttons
        Args:
            buttonlist(list): list of buttons in button group
            otherbutton(QRadioButton): The third button that corresponds to other
            otherval(int/str/None): The value passed from the window that is opened when the other button is pressed 
        """
        for button in buttonslist:
            if button.isChecked():
                return button.text()
        if otherbutton.isChecked():
            return otherval

    def collect_data(self):
        """
        Collects all the data for all the different fields using all the helper functions. 
        Throws an error if a necessary field is not filled out by calling the error message and throws warning 
        if field is left blank that doesn't necesarily need an input.

        Returns:
            dict: The dictionary created from all the inputs and their corresponding input that was just gathered
        """
        #Gather Experiment Name
        exp_nm = self.exp_nm_inp.text()
        if exp_nm ==  "":
            show_error_message("No Experiment Name", "Please Enter an Experiment Name.")
            return
        
        #Gather Date
        exp_dt = self.exp_dt_inp.date().toString("yyMMdd")
        if exp_dt in date_list:
            show_error_message("Invalid Date", "Please Enter a valid date.")
            return
        
        #Gather Replicate Count
        dict_conv = {"High": "hr", "Low": "lr"}
        rep_ct = self.get_other_val([self.rpl_b1,self.rpl_b2], self.rpl_b3, self.rep_other_value)
        if rep_ct == None:
            show_error_message("No Replicate Count", "Please Enter a Replicate Count")
            return
        elif rep_ct in dict_conv:
            rep_ct = dict_conv.get(rep_ct)
        elif rep_ct >= 0:
            pass
        else:
            show_error_message("Invalid Replicate Count", f"Please Enter a Valid Replicate Count.\nYou Entered {rep_ct}")
            return
       
        #Gather Lab Tech
        lb_tech = self.lb_tch_inp.text()
        if lb_tech ==  "":
            show_error_message("No Lab Tech Entered", "Please Enter Lab Tech.")
            return
        
        #Gather Cell Type and Layout type
        cll_typ = self.cll_typ_inp.currentText()
        lyt_typ = self.lyt_typ_inp.currentText()
        
        #Gather Experiment Type
        exp_typ = self.get_other_val([self.exp_b1, self.exp_b2], self.exp_b3, self.exp_other_value)
        if exp_typ ==  None:
            show_error_message("No Experiment Type Entered", "Please Enter an Experiment Type.")
            return
        
        #Gather Experiment Description
        exp_desc = self.datainput.toPlainText()
        if exp_desc == "":
            exp_desc = "None"
            if not show_warning_message("No Experimental Description", "Do You Want to Leave Experimental Description Blank?"):
                return

        dict = {"experiment_name": exp_nm, "experiment_date": exp_dt, "replicate_count": rep_ct, 
                "lab_tech": lb_tech, "cell_type": cll_typ, "layout_type": lyt_typ, 
                "experiment_type": exp_typ, "experiment_description": exp_desc}
        
        #Create readme string
        readme_string=""
        for string in dict:
            readme_string += f"{string}: {dict[string]}\n"
        
        #Use dict to print out what the base path should be
        base_path = f"{dict.get("experiment_type")}_data/"
        path_keys = ["experiment_date", "experiment_name", "lab_tech", "replicate_count", "cell_type"]
        full_path = base_path
        exp_fldr_nm = ""
        i = 0
        while i < len(path_keys):
            full_path += f"{dict.get(path_keys[i])}"
            exp_fldr_nm +=f"{dict.get(path_keys[i])}"
            if i == len(path_keys) - 1:
                full_path += "/"
                exp_fldr_nm += "/"
                i +=1
            else:
                full_path += "_"
                exp_fldr_nm += "_"
                i+=1
        
        if full_path in experiments:
            show_error_message("Invalid Experiment Path", "Please Enter a Valid Experiment Path.\nA path already exisits for the data you entered.")
            return
        
        #Dictionary for better dealing with data
        self.data = {"metadata" : {"experiment_name": exp_nm, "lab_tech": lb_tech, "replicate": rep_ct, "cell_type": cll_typ, "experiment_date": exp_dt, "layout_type": lyt_typ,
                     "data_types" : [],  "experiment_description": exp_desc, "experiment_type": exp_typ, "plate_data": {}}, 
                     "helpdata" : {"base_path": base_path, "full_path": full_path, "experiment_folder_name" : exp_fldr_nm, 
                                   "readme_string": readme_string}} 

        #Delete base path and experiment_folder_name if not needed

        #Json
        #json_data = json.dumps(dict)
        
        #print(f"Data is: {self.data}")
        #Open next window and close this Window when done
        self.plate_map_window = PlateMapWindow(main_window, self.data)
        self.plate_map_window.show()
        self.hide()

        #print(dict)
    
if __name__ == "__main__":
    """
    Handles running the app and specifying css styles and icon image
    """
    app.setWindowIcon(QIcon('DataInput.png'))  # Set the application icon
    """Add CSS Styles
    app.setStyleSheet(""" """)
    with open("styles.css","r") as file:
        app.setStyleSheet(file.read())"""
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())