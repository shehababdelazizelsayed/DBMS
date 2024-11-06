import tkinter as tk
from tkinter import ttk
import mariadb
import sys
import sv_ttk
class DatabaseGUI:
    def __init__(self):
        self.create = None
        self.tables_combobox = None
        self.table_entries = {}
        self.combobox_options = list(range(1, 11))
        self.combobox_entries = {}

    def create_db(self):
        self.create = tk.Tk()
        self.create.title("Create database")
        self.create.geometry("1920x1080")
        sv_ttk.set_theme("dark")
        # Main frame (pack with fill and expand for flexible resizing)
        main_frame = tk.Frame(self.create)
        main_frame.pack(fill="both", expand=True)

        # Label and combobox for number of tables
        num_of_tables_label = ttk.Label(main_frame, text="Number of tables")
        num_of_tables_label.pack(pady=5)

        self.tables_combobox = ttk.Combobox(main_frame, values=self.combobox_options, state="readonly")
        self.tables_combobox.pack(pady=5)
        self.tables_combobox.bind("<<ComboboxSelected>>", self.update_comboboxes)

        # Button to trigger table creation
        enter_button = ttk.Button(main_frame, text="Enter the number", command=self.attribute_tables)
        enter_button.pack(pady=5)

        # Button to print entered values
        print_button = ttk.Button(main_frame, text="Create The Database", command=self.open_popup)
        print_button.pack(pady=5)
        
        clear_button = ttk.Button(main_frame, text="Clear", command=self.clear_widgets)
        clear_button.pack(pady=5)

        # Canvas and scrollable frame (pack within a separate frame)
        self.container_frame = tk.Frame(main_frame)
        self.container_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.container_frame, width=800, height=400)
        self.canvas.pack(fill="both", expand=True)

        self.scrollbar_x = ttk.Scrollbar(self.container_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y = ttk.Scrollbar(self.container_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Bind an event to update scrollbars when frame content changes
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Rest of the code, place widgets within self.scrollable_frame using pack
        
    def clear_widgets(self):
        """Clears all widgets within the scrollable frame."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Reset dictionaries
        self.table_entries = {}
        self.combobox_entries = {}
        self.table_entry_containers = {} 

    def on_frame_configure(self, event):
        # Update the canvas and scrollbars to fit the frame content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_comboboxes(self, event):
        """Clears existing widgets (except entry boxes) and creates new comboboxes and entry boxes based on the selected number of tables."""

        # Clear existing widgets, but exclude entry boxes to preserve them
        for widget in self.scrollable_frame.winfo_children():
            if not isinstance(widget, ttk.Entry):
                widget.destroy()

        # Additional variable to track entry box containers
        self.table_entry_containers = {}

        # Get selected number of tables
        num_tables = int(self.tables_combobox.get())

        # Start creating widgets from row 2
        row = 2

        for i in range(num_tables):
            # Create label for table (pack with `side=tk.LEFT`, clear margins)
            table_label = ttk.Label(self.scrollable_frame, text=f"Table {i + 1}:")
            table_label.pack(side=tk.TOP, padx=5)

            # Create entry box for table (pack with `side=tk.RIGHT`)
            table_entry = ttk.Entry(self.scrollable_frame)
            table_entry.pack(side=tk.TOP, padx=5)
            self.table_entries[f"table_{i + 1}"] = table_entry

            # Create combobox with truncated options and initial display of 1
            combobox = ttk.Combobox(
                self.scrollable_frame,  # Parent frame changed to scrollable_frame
                values=self.combobox_options[:10],  # Truncate options to 10
                state="readonly",
            )
            combobox.pack(side=tk.TOP, padx=5)  # Pack with padding and clear margins
            combobox.config(textvariable=tk.StringVar(value=str(self.combobox_options[0])))
            combobox.bind("<<ComboboxSelected>>", lambda e, table_index=i: self.create_entry_boxes(table_index, e))
            self.combobox_entries[f"combobox_{i + 1}"] = combobox

            table_container = tk.Frame(self.scrollable_frame)  # Create container here
            table_container.pack(side=tk.TOP, pady=10)

            # Store the reference for the current table container
            self.table_entry_containers[f"table_{i + 1}"] = table_container


    def create_entry_boxes(self, table_index, event):
        """Creates entry boxes based on the selected number in the combobox."""
        num_entries = int(self.combobox_entries[f"combobox_{table_index + 1}"].get())

    # Clear existing entry boxes for this table, if any
        table_container = self.table_entry_containers.get(f"table_{table_index + 1}")
        if table_container:
            for widget in table_container.winfo_children():
                if isinstance(widget, (ttk.Entry,ttk.Label)):
                    widget.destroy()

    # Create a new container each time to avoid conflicts
        table_container = tk.Frame(self.scrollable_frame)
        table_container.pack(side=tk.TOP, pady=10)
        

    # Store the reference for the current table container
        self.table_entry_containers[f"table_{table_index + 1}"] = table_container
        table_name = self.table_entries[f"table_{table_index + 1}"].get()
        if not table_name:
            print("Please enter a table name in the entry box.")
            return


    # Create label and entry boxes within the container
        table_label = ttk.Label(table_container, text=f"Table {table_name} :")
        table_label.pack(side=tk.LEFT, padx=5)
        


        for i in range(num_entries):

            new_entry = ttk.Entry(table_container)
            new_entry.pack(side=tk.LEFT, padx=5)

            combobox_1 = ttk.Combobox(
                table_container,
                values=("int,", "varchar(255),"),  # Use correct options
                state="readonly",
            )
            combobox_1.pack(side=tk.LEFT, padx=5)
            

    def attribute_tables(self):
        # Placeholder for future database connection and table creation logic
        pass
    def popup_destroy(self):
        self.popup.destroy()
    def open_popup(self):
        self.popup = tk.Toplevel(self.create)  # Create top-level window for popup
        self.popup.title("Confirm Database Creation")
        self.popup.geometry("250x150")
        table_label = ttk.Label(self.popup, text="Are you sure?")
        table_label.pack(side=tk.TOP, padx=5)
        enter_button = ttk.Button(self.popup, text="NO", command=self.popup_destroy)
        enter_button.pack(side=tk.LEFT,pady=5,padx=50)
        enter_button = ttk.Button(self.popup, text="Yes", command=self.print_entered_values)
        enter_button.pack(side=tk.LEFT,pady=5)
        

    def print_entered_values(self):
        username = sys.argv[1]
        password = sys.argv[2]
        database_name = sys.argv[3]


        if not self.table_entries:
            print("No entries created yet.")
            return



        values_by_suffix = {}

        # Combine data collection in a single loop
        for key, value in self.table_entries.items():
            # Assuming 'value' is the entry box object
            table_name = value.get()  # Use the correct entry box reference here
            suffix = key[key.rfind("_") + 1:]

        # Include table name with the suffix key
            values_by_suffix.setdefault(suffix, []).append(f"Create Table {table_name}")

        # Process combobox and entry values
            combobox_key = key.replace("table", "combobox")
            if combobox_key in self.combobox_entries:
                selected_value = self.combobox_entries[combobox_key].get()
                table_container = self.table_entry_containers[key]
                entry_values = [entry_box.get() for entry_box in table_container.winfo_children() if isinstance(entry_box, ttk.Entry)]

            # Combine all values for this suffix
                combined_value = f" {' '.join(entry_values)});"
                
                values_by_suffix[suffix].append(combined_value)
        try:
            with mariadb.connect(user=username, password=password, database=database_name) as conn:
                cursor = conn.cursor()
                for suffix, group_values in values_by_suffix.items():
                    joined_values = "( ".join(group_values)
                    joined_values = joined_values.replace(",);", ");")
                    cursor.execute(joined_values)
                    print(joined_values)
        except mariadb.Error as e:
            print("Connection failed:", e)


# Create an instance and start the GUI
gui = DatabaseGUI()
gui.create_db()
gui.create.mainloop()
