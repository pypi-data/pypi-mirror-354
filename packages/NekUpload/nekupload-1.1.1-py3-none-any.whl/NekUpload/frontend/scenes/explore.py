import logging
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
from NekUpload.frontend.components.copyable_table import CopyableTableview
from NekUpload.frontend.components.settings_manager import SettingsManager
from NekUpload.manager import NekManager,RecordMetadata

from NekUpload.frontend.config import DB_AVAILABLE_COMMUNITIES,DB_COMMUNITY_NAMES

class ExploreScene(ttk.Frame):
    def __init__(self,parent,setting_manager: SettingsManager):
        super().__init__(parent)

        self.setting_manager = setting_manager#contains settings data
        self.data: list[tuple[str]] = []#format for table

        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=1)

        self.about_description = ttk.Label(
            master=self,
            text=("Use this page to explore what records you have uploaded and what records exist in a certain community."
            "This tool is designed to complement the Upload page by providing users with a method for "
            "identifying which record IDs they may want to link with. html link is also provided if you wish to view this"
            " natively on the online repository.\n"
            "\n"
            "To load in data, please select either User Records or Community Records. For User Records, you must have"
            " completed the Settings page and provided your API key. The records of the user associated with this API key "
            "will be loaded. For community records, no API key is required, but a target community must be specified."),
            font=("TKDefaultFont", 12),
            anchor="w",
            justify="left",
        )
        self.about_description.grid(row=0,column=0,sticky=NSEW,columnspan=3) 

        self.user_record_info: ttk.Frame = self.info_frame(self)
        self.user_record_info.grid(row=1,column=0,sticky=(NSEW))

        self.get_user_records_button = ttk.Button(
            master=self,
            text="Get User Records",
            command=self.get_user_records,
            bootstyle=(PRIMARY,OUTLINE)
        )
        self.get_user_records_button.grid(row=2, column=0, sticky=(EW))

        get_community_record_frame: ttk.Frame = self.get_community_record_frame(self)
        get_community_record_frame.grid(row=3,column=0,sticky=NSEW)

        #for updating text on window change
        self.bind("<Configure>", self.update_wraplength)

    def get_community_record_frame(self,parent) -> ttk.Frame:
        frame = ttk.Frame(parent)
        frame.rowconfigure(0,weight=1)
        frame.rowconfigure(1,weight=1)
        frame.columnconfigure(0,weight=1)
        frame.columnconfigure(1,weight=1)
        frame.columnconfigure(2,weight=1)

        self.get_community_records_button = ttk.Button(
            master=frame,
            text="Get Community Records",
            command=self.get_community_records,
            bootstyle=(PRIMARY,OUTLINE)
        )
        self.get_community_records_button.grid(row=1, column=0, columnspan=3, sticky=(EW))

        #######SETTING PRESETS FOR COMMUNITY TARGET
        self.presets = ttk.Combobox(
            master=frame,
            state="readonly"
        )
        self.presets.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        self.presets.bind("<<ComboboxSelected>>",self._update_community_slug_value)
        self.setting_manager.add_callbacks_on_update_host_name(self._update_community_slug_value)

        community_slug_label = ttk.Label(
            master=frame,
            text="Community Slug: ",
            bootstyle=PRIMARY
        )
        community_slug_label.grid(row=0,column=0,sticky=W)

        self._community_slug = tk.StringVar()
        self.community_slug_entry = ttk.Entry(
            master=frame,
            textvariable=self._community_slug
        )
        self.community_slug_entry.grid(row=0,column=2,padx=5,pady=5,sticky=EW)

        #update final value of combobox
        self._update_community_slug_value()

        return frame

    def info_frame(self,parent) -> ttk.Frame:
        frame = ttk.Frame(master=parent)
        
        frame.rowconfigure(0,weight=1)
        frame.columnconfigure(0,weight=1)

        self.user_records_table = self._build_table(frame,self.data)
        self.user_records_table.grid(row=0,column=0,sticky=NSEW)

        return frame

    def get_user_records(self):
        URL: str = self.setting_manager.database_url
        TOKEN: str = self.setting_manager.token

        logging.info("Retrieving data, this may take some time.")
        data: list[RecordMetadata] = NekManager.get_all_uploaded_user_records(URL,TOKEN)
        
        formatted_data:list[tuple[str]] = []
        for record in data:
            status = "Draft" if record.is_draft else "Published"
            formatted_data.append(
                (record.record_id,record.title,record.resource_type,record.record_link,status)
            )

        self.data = formatted_data#update new information

        logging.info(f"Information retrieved successfully")
        
        #destroy and recreate frame and table
        #table created correctly as calls self.data, so formatted data must be stored there
        self.user_record_info.destroy()
        self.user_record_info: ttk.Frame = self.info_frame(self)
        self.user_record_info.grid(row=1,column=0,sticky=(NSEW))

    def get_community_records(self):
        URL: str = self.setting_manager.database_url
        COMMUNITY: str = self.community_slug

        logging.info("Retrieving data, this may take some time.")
        data: list[RecordMetadata] = NekManager.get_all_community_records(URL,COMMUNITY)
        
        formatted_data:list[tuple[str]] = []
        for record in data:
            status = "Draft" if record.is_draft else "Published"
            formatted_data.append(
                (record.record_id,record.title,record.resource_type,record.record_link,status)
            )

        self.data = formatted_data#update new information

        logging.info(f"Information retrieved successfully")
        
        #destroy and recreate frame and table
        #table created correctly as calls self.data, so formatted data must be stored there
        self.user_record_info.destroy()
        self.user_record_info: ttk.Frame = self.info_frame(self)
        self.user_record_info.grid(row=1,column=0,sticky=(NSEW))

    def _build_table(self,parent,row_data: list[tuple[str]]) -> Tableview:
        coldata = [
            "Record ID",
            "Title",
            "Resource Type",
            {"text": "Link", "stretch": False},
            "Status"
        ]

        table = CopyableTableview(
            master=parent,
            coldata=coldata,
            rowdata=row_data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
        )

        return table
    
    def _update_community_slug_value(self, event: tk.Event = None):
        """Callback for combobox selection, sets default values in some fields"""
        database_name: str = self.setting_manager.database_name
        
        # Safely get available communities with fallback to empty list
        available_communities = DB_COMMUNITY_NAMES.get(database_name, [])
        self.presets.configure(values=available_communities)

        # Determine selected community with proper fallbacks
        selected_community_value = ""
        if event and hasattr(event, 'widget'):
            selected_community_value = event.widget.get()
        else:
            selected_community_value = self.presets.get() if self.presets.get() else ""
        
        if not selected_community_value and available_communities:
            selected_community_value = available_communities[0]

        # Safely get community slugs with fallback to empty dict
        communities_in_db = DB_AVAILABLE_COMMUNITIES.get(database_name, {})
        community_slug = communities_in_db.get(selected_community_value, "")
        
        # Update UI state
        self._community_slug.set(community_slug)

        # If no event triggered the change, apply default settings
        if event is None:
            self._set_default_community(database_name)

    def _set_default_community(self, database_name: str):
        """Sets the default community selection and slug."""
        default_community = DB_COMMUNITY_NAMES.get(database_name, [""])[0]  # Default to first or empty
        self.presets.set(default_community)

        community_slug = DB_AVAILABLE_COMMUNITIES.get(database_name, {}).get(default_community, "")
        self._community_slug.set(community_slug)

    @property
    def community_slug(self) -> str:
        return self._community_slug.get()
    
    def update_wraplength(self, event):
        # Dynamically set the wraplength based on the width of the parent frame
        # Subtract a little for padding and margin
        self.about_description.config(wraplength=event.width - 20)
