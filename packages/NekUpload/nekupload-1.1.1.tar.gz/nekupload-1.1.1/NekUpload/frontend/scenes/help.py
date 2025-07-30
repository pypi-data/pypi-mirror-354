import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from NekUpload.frontend.components.settings_manager import SettingsManager

class HelpScene(ttk.Frame):
    def __init__(self,parent,setting_manager: SettingsManager):
        super().__init__(parent)
        self.setting_manager = setting_manager#contains settings data
        self.columnconfigure(0,weight=1)

        self.LEFT_MARGIN = 5
        self._question_1_frame()

        self.bind("<Configure>", self.update_wraplength)

    def update_wraplength(self, event):
        # Dynamically set the wraplength based on the width of the parent frame
        # Subtract a little for padding and margin
        self.question_1.config(wraplength=event.width - 20)

    def _question_1_frame(self):
        # Create the label for the title
        about_label = ttk.Label(
            master=self,
            text="Incorrect Number of Checkpoint Files (One too many or one too few)?",
            font=("TkDefaultFont", 20, "bold", "underline"),
            anchor="center",
            bootstyle=PRIMARY
        )
        about_label.grid(row=0, column=0, pady=5, padx=self.LEFT_MARGIN, sticky=W)

        # Create the description label
        self.question_1 = ttk.Label(
            master=self,
            text=(f"If you believe that you have submitted the correct number of checkpoint files, "
                "but NekUpload is telling you that you are missing one or have one too many. "
                "This is likely due to a floating point issue in either the Nektar++ solver or in NekUpload, "
                "causing a discrepancy of one checkpoint file. "
                "If NekUpload expects N+1 files where you only have N, then go to the session file and increment"
                "<IO_Checksteps> by 1. If NekUpload expects N-1 files where you have N, then go to the session file "
                "and decrement <IO_Checksteps> by 1. If this still does not work, and you are adamant you are correct "
                "please submit the issue to NekUpload."),
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        self.question_1.grid(row=1, column=0, padx=self.LEFT_MARGIN, pady=10, sticky="nsew")
