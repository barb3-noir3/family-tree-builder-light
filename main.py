"""
This program creates a family tree with a user interface to add, edit end delete family members.
It can be use for your won family, for monarchs/family you want to study, or for fictional characters.
For now I don't know how many generations it can handle, but I think it can handle a lot of them.
The export format is in svg, so you can print it in a large format and it stays clear.
This version is a standalone version, I called it the light version because I won't update it. It works as it is.

I'm currently working on a more advanced version that will not be free, but will have more features and will be updated regularly.
"""


"""
Author : Barb3 Noire3
Date : 02/02/2025
Version : 1.0
Licence : GNU General Public License v3.0 
"""

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime
from tkcalendar import DateEntry
import os
import tree_generation as ga

# UI setup
root = tk.Tk()
root.title("Family Tree Builder (light)")

# Variables 
entries = {
    'ID': tk.StringVar(),
    'No Gen': tk.StringVar(),
    'Surname': tk.StringVar(),
    'Name': tk.StringVar(),
    'Gender': tk.StringVar(),
    'Date of Birth': tk.StringVar(),
    'Date of Death': tk.StringVar(),
    'Birthplace': tk.StringVar(),
    'Job': tk.StringVar(),
    'ID Spouse': tk.StringVar(),
    'ID Mother': tk.StringVar(),
    'ID Father': tk.StringVar()
}

# Variable to store the status of the person
is_alive = tk.BooleanVar()

# Variable to save the selected ID
selected_id = None

# Validate the dates
def validate_dates(dob, dod):
    if dod.lower() == 'unknown':
        return True  # Skip validation if the person is alive
    try:
        dob_date = datetime.strptime(dob, '%d/%m/%Y')
        dod_date = datetime.strptime(dod, '%d/%m/%Y')
        return dod_date > dob_date
    except ValueError:
        return False

# Save the data to the CSV file
def save_to_csv():
    global selected_id
    dob = entries['Date of Birth'].get()
    dod = entries['Date of Death'].get()

    if is_alive.get():
        dod = 'Unknown'  # Set Date of Death to "Unknown" if the person is alive

    if not validate_dates(dob, dod):
        messagebox.showerror("Error", "The date of death must be greater than the date of birth or 'Unknown' if the person is alive.")
        return

    # Verification of the IDs
    id = entries['ID'].get()
    idepoux = entries['ID Spouse'].get()
    fid = entries['ID Father'].get()
    mid = entries['ID Mother'].get()

    if id == idepoux:
        messagebox.showerror("Error", "The ID is the same as the spouse's, please change it.")
        return
    elif id == fid:
        messagebox.showerror("Error", "The ID is the same as the father's, please change it.")
        return
    elif id == mid:
        messagebox.showerror("Error", "The ID is the same as the mother's, please change it.")
        return

    data = {key: [entries[key].get()] for key in entries}
    data['Date of Death'] = [dod]  # Update the date of death
    df = pd.DataFrame(data)

    gender = entries['Gender'].get()
    if gender not in ["Male", "Female"]:
        messagebox.showerror("Error", "Please gender must be Male or Female.")
        return

    try:
        if selected_id:
            # Update the existing row
            existing_df = pd.read_csv('family_tree.csv', sep=';')
            if 'ID' not in existing_df.columns:
                raise KeyError("The 'ID' column does not exist in the CSV file.")
            # Convert ID columns to string to ensure consistent comparison
            for col in existing_df.columns:
                if col in ['ID', 'ID Mother', 'ID Father', 'No Gen']:
                    existing_df[col] = existing_df[col].astype(str)
            existing_df.loc[existing_df['ID'] == selected_id, entries.keys()] = df.values[0]
            existing_df.to_csv('family_tree.csv', index=False, sep=';')
            selected_id = None  # Deselect the ID 
        else:
            #  Add a new row
            if not os.path.exists('family_tree.csv'):
                df.to_csv('family_tree.csv', mode='w', index=False, sep=';')
            else:
                df.to_csv('family_tree.csv', mode='a', header=False, index=False, sep=';')
        messagebox.showinfo("Success", "Data saved successfully!")
        load_csv_data()  # Load the data after saving
        clear_entries()  # Clear the entry fields
    except Exception as e:
        messagebox.showerror("Error", f"Error while the data saved: {e}")

# Function to load the CSV data into the Treeview
def load_csv_data():
    try:
        df = pd.read_csv('family_tree.csv', sep=';')
        for i in tree.get_children():
            tree.delete(i)
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))
    except FileNotFoundError:
        messagebox.showinfo("Information", "No CSV file found. Please add data.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while the data loaded: {e}")

# Function to select an item in the Treeview
def select_item(event):
    global selected_id
    selected_items = tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        selected_id = tree.item(selected_item, 'values')[0]  # Set selected_id to the ID of the selected row
        for key, var in entries.items():
            var.set(tree.item(selected_item, 'values')[list(entries.keys()).index(key)])
        is_alive.set(entries['Date of Death'].get().lower() == 'unknown')

# Function to clear the entry fields
def clear_entries():
    for var in entries.values():
        var.set('')
    is_alive.set(False)

# Function to delete the selected item
def delete_selected_item():
    selected_id = entries['ID'].get()  # Get the ID from the entry field
    if not selected_id:
        messagebox.showerror("Error", "Please select a row to delete.")
        return
        
    try:
        # Load the CSV and print initial state
        df = pd.read_csv("family_tree.csv", sep=';')
        
        # Convert ID column to string to ensure consistent comparison
        df['ID'] = df['ID'].astype(str)
        selected_id = str(selected_id)
        
        # Print matching rows before deletion
        matching_rows = df[df['ID'] == selected_id]
        print(f"Found {len(matching_rows)} matching rows")
        
        if len(matching_rows) == 0:
            messagebox.showerror("Error", f"No row found with this ID: {selected_id}")
            return
            
        # Perform the deletion
        df = df[df['ID'] != selected_id]
        
        # Save and verify
        df.to_csv('family_tree.csv', index=False, sep=';')
        
        # Verify the save worked
        verification_df = pd.read_csv('family_tree.csv', sep=';')
        
        messagebox.showinfo("Success", "Row deleted successfully!")
        load_csv_data()  # Reload the data after deletion
        clear_entries()  # Clear the entry fields
    except Exception as e:
        print(f"Full error details: {str(e)}")
        messagebox.showerror("Error", f"Error while the deletion: {e}")

# Configure root window
root.configure(bg='#f0f0f0')  # Light gray background

# Create a style for widgets
style = ttk.Style()
style.configure('TLabel', background='#f0f0f0')
style.configure('TEntry', background='white')
style.configure('Custom.TButton', padding=5)

# Create frames to organize the layout
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
input_frame.configure(style='Custom.TFrame')

# Function to create labeled entry with consistent styling
def create_labeled_entry(parent, row, column, label_text, variable, is_date=False):
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=column, padx=5, pady=2, sticky=tk.W)
    
    if is_date:
        entry = DateEntry(parent, textvariable=variable, date_pattern='dd/mm/yyyy',
                         background='white', foreground='black', borderwidth=2)
    else:
        entry = ttk.Entry(parent, textvariable=variable)
    entry.grid(row=row, column=column+1, padx=5, pady=2, sticky=(tk.W, tk.E))
    return entry

# Create the input fields with improved layout
row_index = 0
for key, var in entries.items():
    if key == 'Date of Death':
        # Create date of death field aligned with other fields
        label = ttk.Label(input_frame, text=key)
        label.grid(row=row_index, column=0, padx=5, pady=2, sticky=tk.W)
        
        # Add date field
        death_date = DateEntry(input_frame, textvariable=var, date_pattern='dd/mm/yyyy',
                             background='white', foreground='black', borderwidth=2)
        death_date.grid(row=row_index, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Add "Is Alive" checkbox to the right
        alive_check = ttk.Checkbutton(input_frame, text="Is Alive", variable=is_alive)
        alive_check.grid(row=row_index, column=2, padx=(20, 0), pady=2, sticky=tk.W)
    
    elif key in ['Date of Birth']:
        create_labeled_entry(input_frame, row_index, 0, key, var, is_date=True)
    else:
        create_labeled_entry(input_frame, row_index, 0, key, var)
    row_index += 1

# Function to generate the family tree
def generate_tree():
    ga.generate_tree()
    messagebox.showinfo("Success", "Family tree successfully generated, please wait!")

# Create a frame for buttons
button_frame = ttk.Frame(input_frame, padding="5")
button_frame.grid(row=row_index+1, column=0, columnspan=2, pady=10)

# Add buttons with consistent styling
save_button = ttk.Button(button_frame, text="Save", command=save_to_csv, style='Custom.TButton')
save_button.grid(row=0, column=0, padx=5)

delete_button = ttk.Button(button_frame, text="Delete", command=delete_selected_item, style='Custom.TButton')
delete_button.grid(row=0, column=1, padx=5)

gen_tree_button = ttk.Button(button_frame, text="Family Tree Generation", command=generate_tree, style='Custom.TButton')
gen_tree_button.grid(row=0, column=2, padx=5)

# Configure the Treeview with improved styling
tree_frame = ttk.Frame(root, padding="10")
tree_frame.grid(row=row_index+2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

tree = ttk.Treeview(tree_frame, columns=list(entries.keys()), show='headings', style='Custom.Treeview')
for col in entries.keys():
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Add scrollbars to Treeview
y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

# Grid the Treeview and scrollbars
tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
y_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
x_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Configure grid weights for resizing
root.grid_columnconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)
tree_frame.grid_rowconfigure(0, weight=1)

# Bind the selection event
tree.bind('<ButtonRelease-1>', select_item)
if not os.path.exists('family_tree.csv'):
    columns = ['ID', 'No Gen', 'Surname', 'Name', 'Gender', 'Date of Birth', 'Date of Death', 'Birthplace', 'Job', 'ID Spouse', 'ID Mother', 'ID Father']
    pd.DataFrame(columns=columns).to_csv('family_tree.csv', index=False, sep=';')

# Load the CSV data
load_csv_data()

# Launch the application
root.mainloop()