import tkinter as tk
import tkinter.ttk as ttk
import mariadb # Assuming MariaDB connector is installed
from subprocess import call
from tkinter import ttk, Listbox
from tkinter import *
import pandastable as pdt  # Import the pandastable library
import pandas as pd
import sys


class DatabaseGUI:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Database Connection")
    self.root.geometry("600x500")


    # GUI elements
    self.username_label = ttk.Label(self.root, text="Database username:")
    self.username_entry = ttk.Entry(self.root)
    self.password_label = ttk.Label(self.root, text="Database Password:")
    self.password_entry = ttk.Entry(self.root, show="*") # Hide password characters
    self.connect_button = ttk.Button(self.root, text="Connect", command=self.connect)
    self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset)
    self.select_DB_button = ttk.Button(self.root, text="select_DB", command=lambda: self.select_DB_and_detect_tables())

    self.database_combobox = ttk.Combobox(self.root, values=[], state="disabled")
    self.database_combobox.grid(row=0, column=3, columnspan=2)
    

    # Layout using grid for better organization
    self.username_label.grid(row=0, column=0, sticky=tk.W,padx=20,pady=5)
    self.username_entry.grid(row=0, column=1)
    self.password_label.grid(row=1, column=0, sticky=tk.W,padx=20,pady=5)
    self.password_entry.grid(row=1, column=1)
    self.connect_button.grid(row=3, column=0,padx=30,pady=20)
    self.reset_button.grid(row=3, column=1,padx=30,pady=20)
    self.select_DB_button.grid(row=2,column=3  )

    self.root.mainloop()
    #connect to the data base
  def connect(self):
    url = "jdbc:mariadb://localhost:3306/" + self.database_combobox.get()
    username = self.username_entry.get()
    password = self.password_entry.get()

    try:
      with mariadb.connect(user=username, password=password, database="test") as conn:
        # Connection successful, perform database operations here
      	cursor = conn.cursor()
      	self.Database_tables(cursor)
      	
      	

    except mariadb.Error as e:
      print("Connection failed:", e)
#reset button
  def reset(self):
    self.username_entry.delete(0, tk.END)
    self.password_entry.delete(0, tk.END)
# the list to select the data base
  def select_DB(self):
    url = "jdbc:mariadb://localhost:3306/"
    username = self.username_entry.get()
    password = self.password_entry.get()
    selected_database=self.database_combobox.get()
    try:
   	 with mariadb.connect(user=username, password=password, database=selected_database) as conn:
   	   cursor = conn.cursor()
   	   cursor.execute("use "+selected_database)
   	   self.tables_page()
   	   
    except mariadb.Error as e:
        print("Unexpected error", e)
  def tables(self):
  	self.choose_Databases = ttk.Label(self.root, text="Choose Database:")
  def detect_tables(self):
    try:
        with mariadb.connect(user=self.username_entry.get(), password=self.password_entry.get(), database=self.database_combobox.get()) as conn:
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]  # Extract table names
            print("Available tables:", table_names)

    except mariadb.Error as e:
        print("Error detecting tables:", e)
  	
  def Database_tables(self, cursor):
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        database_names = [db[0] for db in databases]  # Extract database names

        # Populate the combobox with database names
        self.database_combobox["values"] = database_names
        self.database_combobox.state(["!disabled"])  # Enable the combobox
  def select_DB_and_detect_tables(self):
    username = self.username_entry.get()
    password = self.password_entry.get()
    database_name = self.database_combobox.get()

    # Pass the arguments as command-line arguments to project.py
    call(["python", "project.py", username, password, database_name])



if __name__ == "__main__":
  DatabaseGUI()

