import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from NekUpload.frontend.components.settings_manager import SettingsManager

class ReviewScene(ttk.Frame):
    def __init__(self,parent,setting_manager: SettingsManager):
        super().__init__(parent)
        self.setting_manager = setting_manager#contains settings data

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)

        self.placeholder = ttk.Label(
            master=self,
            text="REVIEW HERE",
            font=("TkDefaultFont", 20),
            anchor="center"
        )

        self.placeholder.grid(row=1,column=1,sticky=(NSEW))
        