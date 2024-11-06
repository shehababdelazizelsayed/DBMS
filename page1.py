import pandastable as pdt  # Import the pandastable library
import pandas as pd
import tkinter as tk
from tkinter import ttk  # Import ttk for styled buttons
import mariadb
import sys
import sv_ttk
username = sys.argv[1]
password = sys.argv[2]
database_name = sys.argv[3]

dataframes = []  # Create an empty list to store DataFrames



try:
    with mariadb.connect(user=username, password=password, database=database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]  # Extract table names


        for table_name in table_names:
            cursor.execute(f"SELECT * FROM {table_name}")
            table_description = cursor.description  # Get column descriptions
            column_names = [col[0] for col in table_description]  # Extract column names
            table_data = cursor.fetchall()

    # Create DataFrame and assign name (compatibility fix)
            df = pd.DataFrame(table_data, columns=column_names)  # Create DataFrame without `name`
            df.name = table_name  # Assign name after creation
            dataframes.append(df)
except mariadb.Error as e:
    print("Connection failed:", e)

# Create the main window
root = tk.Tk()
root.title("Database Tables Viewer")  # Add a title
sv_ttk.set_theme("dark")
# Create frames for each page
table_frames = []
for df in dataframes:
    table_frame = tk.Frame(root)
    table = pdt.Table(table_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

    # Store table name for button text
    table_frame.table_name = df.name
    table_frames.append(table_frame)

# Display the first page initially
table_frames[0].pack(fill=tk.BOTH, expand=True)

# Create buttons for switching pages (horizontal layout)
button_frame = ttk.Frame(root)  # Use ttk for styled buttons
button_frame.pack(pady=10)  # Add some padding above the buttons
page_buttons = []
for i in range(len(table_frames)):
    button_text = table_frames[i].table_name  # Retrieve stored table name

    # Create styled button with white text and black background
    style = ttk.Style()
    style.configure("my.TButton", foreground="white", background="black")
    button = ttk.Button(button_frame, text=button_text, style="my.TButton", command=lambda i=i: switch_page(i))
    button.pack(side=tk.LEFT, padx=5)
    page_buttons.append(button)

def switch_page(index):
    """Switches to the specified page."""
    for i in range(len(table_frames)):
        table_frames[i].pack_forget()
    table_frames[index].pack(fill=tk.BOTH, expand=True)

root.mainloop()

