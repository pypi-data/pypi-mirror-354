import sqlite3
import sys
import os
from tkinter import StringVar, Tk, Frame, Label
from datetime import datetime
import tkinter as tk
from ui_components.dropdown import create_dropdown
from ui_components.error_msg import display_message

final_uid_callback = None


import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


dropdown_widgets = []
def on_category_change(*args, category, cat_mapped_value, property_frame, root, on_final_uid=None, clear_uid_table=None):
    global final_uid_callback
    final_uid_callback = on_final_uid
    
    for widget in property_frame.winfo_children():
        widget.destroy()
    dropdown_widgets.clear()
    for child in root.winfo_children():
        if isinstance(child, tk.Entry):
            child.destroy()
    db_path = resource_path("databases/"+category+".db")
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        display_message(property_frame, f"Database file not found: {db_path}", msg_type="error")
        return
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()
    if category is None or cat_mapped_value is None:
        print("Invalid category selected.")
        display_message(property_frame, f"Invalid Category Selected", msg_type="error")
        return
   
    
    table_names= cursor.execute(f'''SELECT Properties
    FROM Headers ''').fetchall()
    properties = [name[0] for name in table_names if name[0] != 'sqlite_sequence']
    uid_parts = [""] * len(properties)
    prop_values = ["-1"] * len(properties)
    uid_var = StringVar(value="B"+cat_mapped_value)
    def create_property_dropdown(header_index, prop_values):
        if header_index >= len(properties):
            return
        header = properties[header_index]
        prop_var = StringVar(value=f"Select {header}")
        current_prop = header
        column_to_check = 'Filter'
        table_name = current_prop

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]

        if column_to_check in columns:
            results = []
            for item in prop_values:
                if item == "-1":
                    continue
                query = f''' 
                SELECT id, {table_name}_key, {table_name}_value, Filter FROM {table_name} WHERE Filter = ?
                '''
                cursor.execute(query, (item,))
                results = cursor.fetchall()
                if results:
                    break
        else:
            query = f'''
                   SELECT id, {table_name}_key, {table_name}_value FROM {table_name}
             '''
            cursor.execute(query)
            results = cursor.fetchall()
        options = [item[1] for item in results]

        def on_property_change(*args, prop_var=prop_var, header_index=header_index):
            if clear_uid_table:
                clear_uid_table()  # Clear table when any property changes
            prop_values[header_index] = prop_var.get()
           
            for i in range(header_index + 1, len(prop_values)):
                 prop_values[i] = "-1"
                 uid_parts[i] = ""
                
            for i in range(header_index + 1, len(dropdown_widgets)):
                 widget = dropdown_widgets[i]
                 if hasattr(widget, "destroy"):
                  widget.destroy()
            dropdown_widgets[:] = dropdown_widgets[:header_index + 1]
            value = None
            for row in results:
                if row[1] == prop_values[header_index]:
                    value = row[2]
                    break

            if value not in (None, "-1"):
                uid_parts[header_index] = value
                full_uid = "B" + cat_mapped_value + "".join(uid_parts)
                uid_var.set(full_uid)
                if all(uid_parts):
                    # Pass property names and their selected values as a list of tuples
                    selected_props = [(properties[i], prop_values[i]) for i in range(len(properties))]
                    if final_uid_callback:
                        final_uid_callback(full_uid, selected_props)
            create_property_dropdown(header_index + 1, prop_values)

        prop_var.trace_add("write", on_property_change)

        dropdown, prop_var = create_dropdown(property_frame, f"{header}:", options, row=header_index+1, var=prop_var)
        dropdown_widget = dropdown[0] if isinstance(dropdown, (tuple, list)) else dropdown
        dropdown_widgets.append(dropdown_widget)
    create_property_dropdown(0, prop_values)

