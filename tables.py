import pandas as pd
import tkinter as tk
from tkinter import ttk  # Import ttk for styled buttons
import mariadb
import sys
import sv_ttk


def db_tables():
    """Fetches table names from the database and returns them."""
    try:
        # Replace with your database details
        conn = mariadb.connect(
            user="black",
            password="Ss1234567890",
            host="localhost",
            database="test"
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)  # Exit if connection fails

    finally:
        cursor.close()
        conn.close()  # Close connection and cursor

def on_frame_configure(event):
    # Update the canvas and scrollbars to fit the frame content
    canvas.configure(scrollregion=canvas.bbox("all"))


app = tk.Tk()
app.title("Alter Tab")
app.geometry("1920x1080")


sv_ttk.set_theme("dark")

# Get table names from the database
table_names = db_tables()

main_frame = tk.Frame(app)
main_frame.pack(fill="both", expand=True)

lable = ttk.Label(main_frame, text="Select table")
lable.pack(side=tk.TOP)

# Create combobox with retrieved table names
comb = ttk.Combobox(main_frame, values=table_names)
comb.pack(side=tk.TOP)

canvas = tk.Canvas(app, scrollregion=(0, 0, 2000, 5000))
canvas.pack(expand=True, fill="both")


scrollbar = ttk.Scrollbar(app, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

scrollbar_bottom = ttk.Scrollbar(app, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar_bottom.set)
scrollbar_bottom.place(relx=0, rely=1, relwidth=1, anchor="sw")

scrollableframe = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollableframe, anchor="nw")
scrollableframe.bind("<Configure>", on_frame_configure)

app.mainloop()
