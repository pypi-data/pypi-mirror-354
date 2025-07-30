import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import tkinter as tk

class CopyableTableview(Tableview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.clicked_cell = None
        self.clicked_row = None
        self.clicked_column_index = None
        self.copied_label = None

        # Tag for highlighting
        self.view.tag_configure("copied", background="#d4edda")

        # Create context menu
        self.menu = tk.Menu(self.view, tearoff=0)
        self.menu.add_command(label="Copy Cell", command=self.copy_cell)

        # Bind right-click
        self.view.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        row_id = self.view.identify_row(event.y)
        col_id = self.view.identify_column(event.x)

        if row_id and col_id:
            values = self.view.item(row_id)["values"]
            col_index = int(col_id.replace('#', '')) - 1
            if 0 <= col_index < len(values):
                self.clicked_cell = str(values[col_index])
                self.clicked_row = row_id
                self.clicked_column_index = col_index
                self.menu.post(event.x_root, event.y_root)
            else:
                self.clear_selection()
        else:
            self.clear_selection()

    def copy_cell(self):
        if self.clicked_cell:
            self.clipboard_clear()
            self.clipboard_append(self.clicked_cell)

            # Highlight the row briefly
            self.view.item(self.clicked_row, tags=("copied",))
            self.after(500, lambda: self.view.item(self.clicked_row, tags=()))

            # Show 'Copied!' label
            if self.copied_label:
                self.copied_label.destroy()
            self.copied_label = tk.Label(self.view, text="Copied!", bg="lightyellow", fg="green")
            self.copied_label.place(x=5, y=5)
            self.view.after(1000, self.copied_label.destroy)

    def clear_selection(self):
        self.clicked_cell = None
        self.clicked_row = None
        self.clicked_column_index = None