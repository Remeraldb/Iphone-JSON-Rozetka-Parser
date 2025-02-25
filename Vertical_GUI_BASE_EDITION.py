import json
import tkinter as tk
from tkinter import messagebox, ttk
import math
import sys
import subprocess
import re

def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return None

def save_json_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)




def validate_rgb_color(rgb_string):
    # Regular expression pattern for RGB color in the format (R, G, B)
    rgb_pattern = r"rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)"

    if re.match(rgb_pattern, rgb_string):
        return True
    else:
        return False

def update_json():
    selected_index = treeview.focus()
    if selected_index:
        item = treeview.item(selected_index)
        item_values = item['values']
        value = value_entry.get()
        if value:
            index = int(selected_index[1:]) - 1
            column_name = treeview['columns'][selected_column_index]

            # Validate the entered RGB color
            if column_name == "Кольори":
                if not validate_rgb_color(value):
                    messagebox.showerror("Error", "Invalid RGB color format. Please enter color in the format (R, G, B)")
                    return

                # Save the entered value as a single string inside a list
                new_colors = [value.strip()]  # Clean up whitespace and create a list
                item_values[selected_column_index] = ', '.join(
                    [rgb_to_name(color) for color in new_colors])  # Convert to color names
                data[index][column_name] = new_colors  # Update data structure
            else:
                item_values[selected_column_index] = str(value)
                data[index][column_name] = str(value)

            treeview.item(selected_index, values=item_values)
            save_json_file(filename, data)
            messagebox.showinfo("Success", "Data updated successfully")
            value_entry.delete(0, tk.END)

            # Close and reopen the script
            close_and_reopen_script()
        else:
            messagebox.showerror("Error", "Please enter a value")
    else:
        messagebox.showerror("Error", "Please select an item")


def close_and_reopen_script():
    python = sys.executable
    subprocess.Popen([python, sys.argv[0]])
    root.destroy()
def on_click(event):
    global selected_column_index
    column = treeview.identify_column(event.x)
    if column:
        clicked_column_index = int(column[1:]) - 1
        selected_column_index = clicked_column_index  # Always update the selected column index
        column_name = treeview.heading(column)['text']
        selected_index = treeview.selection()[0]
        selected_item = treeview.item(selected_index)
        selected_value = selected_item['values'][selected_column_index]

        value_entry.delete(0, tk.END)

        if column_name == "Кольори":
            rgb_values = get_original_colors(selected_index)
            value_entry.insert(0, rgb_values)
        else:
            value_entry.insert(0, selected_value)

        characteristic_entry.delete(0, tk.END)
        characteristic_entry.insert(0, column_name)

def get_original_colors(treeview_id):
    item = treeview.item(treeview_id)
    colors = data[int(treeview_id[1:]) - 1]["Кольори"]
    return ', '.join(colors)


def rgb_to_name(rgb_string):

    color_map = {
        (255, 0, 0): "Red",
        (0, 255, 0): "Green",
        (0, 0, 255): "Blue",
        (255, 255, 0): "Yellow",
        (255, 0, 255): "Magenta",
        (0, 255, 255): "Cyan",
        (128, 128, 128): "Gray",
        (255, 165, 0): "Orange",
        (128, 0, 128): "Purple",
        (0, 128, 128): "Teal",
        (255, 192, 203): "Pink",
        (255, 255, 255): "White",
        (0, 0, 0): "Black",
        (255, 215, 0): "Gold",
        (218, 112, 214): "Orchid",
        (0, 128, 0): "Dark Green",
        (255, 140, 0): "Dark Orange",
        (0, 0, 128): "Navy",
        (128, 0, 0): "Maroon",
        (0, 128, 0): "Green",
        (255, 0, 255): "Fuchsia",
        (0, 255, 255): "Aqua",
        (255, 215, 0): "Gold",
        (255, 20, 147): "Deep Pink",
        (255, 250, 250): "Starlight",
        (0, 191, 255): "Deep Sky Blue",
        (139, 69, 19): "Saddle Brown",
        (218, 165, 32): "Goldenrod",
        (255, 228, 181): "Moccasin",
        (34, 139, 34): "Green",
        #myyyAddtions:
        (204, 204, 204): "Silver",
        (24, 31, 39): "Midnight",
    }

    formatted_string = rgb_string.strip()[4:-1]
    rgb_values = formatted_string.split(',')
    rgb = tuple(int(value.strip()) for value in rgb_values if value.strip().isdigit())

    if rgb in color_map:
        return color_map[rgb]
    else:
        closest_match = min(color_map.keys(), key=lambda x: math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb, x))))
        return color_map[closest_match]

filename = 'iphones.json'
root = tk.Tk()
root.title("THE JSON View and Edit 2024 PRO EDITION")

data = read_json_file(filename)
if data is None:
    root.destroy()
    raise SystemExit("The JSON file was not found and the application will close.")

treeview = ttk.Treeview(root, columns=list(data[0].keys()), show="headings")
MIN_COLUMN_WIDTH = 100

for col in data[0].keys():
    column_width = MIN_COLUMN_WIDTH
    if col == 'Назва':
        column_width = 500
    elif col == "Вбудована пам'ять" or col == "Оперативна пам'ять":
        column_width = 120
    elif col == "Серія":
        column_width = 115
    elif col == "Основна камера":
        column_width = 140
    elif col == "Процесор":
        column_width = 110
    elif col == "Частота оновлення екрана":
        column_width = 160
    elif col == "Кольори":
        column_width = 100
    else:
        column_width = MIN_COLUMN_WIDTH

    treeview.heading(col, text=col)
    treeview.column(col, width=column_width, minwidth=column_width, anchor="center")

root.update_idletasks()

min_height = 20
min_width = sum(treeview.column(col, "minwidth") for col in data[0].keys())

root.minsize(min_width + 20, min_height + 120)

treeview.grid(row=0, column=0, columnspan=3, sticky="nsew")

def rgb_to_hex(rgb_string):
    try:
        rgb = tuple(map(int, rgb_string[4:-1].split(', ')))
        if len(rgb) != 3:
            raise ValueError("RGB string does not contain three components")
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    except Exception as e:
        print(f"Error converting RGB to hex: {e}")
        return "#000000"

def apply_color_tags(treeview_id, colors_hex):
    for i, color_hex in enumerate(colors_hex):
        tag_name = f"color{i}_{treeview_id}"
        treeview.tag_configure(tag_name, background=color_hex)
        rgb_color = tuple(int(color_hex[j:j + 2], 16) for j in (1, 3, 5))
        brightness = (0.2126 * rgb_color[0] + 0.7152 * rgb_color[1] + 0.0722 * rgb_color[2]) / 255
        if brightness < 0.5:
            treeview.tag_configure(tag_name, foreground="white")
        else:
            treeview.tag_configure(tag_name, foreground="black")
        treeview.item(treeview_id, tags=(tag_name,))


def display_colors(colors):
    if isinstance(colors, list):
        return ', '.join([rgb_to_name(color.strip()) for color in colors])
    else:
        return ', '.join([rgb_to_name(color.strip()) for color in colors.split(', ')])

for item in data:
    item_values = list(item.values())
    colors = item_values.pop()
    if isinstance(colors, list):
        colors_hex = [rgb_to_hex(color.strip()) for color in colors]
    else:
        colors_hex = [rgb_to_hex(color.strip()) for color in colors.split(', ')]
    treeview_id = treeview.insert('', 'end', values=item_values + [display_colors(colors)])

    apply_color_tags(treeview_id, colors_hex)

def on_scroll(event):
    if event.num == 5 or event.delta < 0:  # Scroll down
        if not scroll_to_top_button.winfo_viewable():
            scroll_to_top_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
    elif event.num == 4 or event.delta > 0:  # Scroll up
        if not treeview.yview()[0] == 0.0:
            if not scroll_to_top_button.winfo_viewable():
                scroll_to_top_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
        else:
            if scroll_to_top_button.winfo_viewable():
                scroll_to_top_button.place_forget()

def scroll_to_top():
    treeview.yview_moveto(0)
    scroll_to_top_button.place_forget()

def toggle_scroll_button(event):
    if treeview.yview()[0] == 0.0:  # Check if scrolled to the top
        if scroll_to_top_button.winfo_viewable():
            scroll_to_top_button.place_forget()
    else:
        if not scroll_to_top_button.winfo_viewable():
            scroll_to_top_button.place(in_=scrollbar_frame, relx=1.0, rely=1.0, anchor='se', x=-40, y=-20)


scroll_to_top_button = tk.Button(root, text="Scroll to Top", command=scroll_to_top, highlightthickness=10, borderwidth=5, highlightbackground="black")

treeview.bind("<MouseWheel>", toggle_scroll_button, lambda event: on_scroll(event))  # For Windows and Linux
treeview.bind("<Button-4>", toggle_scroll_button, on_scroll)  # For Linux
treeview.bind("<Button-5>", toggle_scroll_button, on_scroll)  # For Linux

characteristic_label = tk.Label(root, text="Characteristic:")
characteristic_label.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=(5, 0))
characteristic_entry = tk.Entry(root, highlightthickness=1,borderwidth=5, highlightbackground="gray")
characteristic_entry.grid(row=1, column=1, sticky='we', padx=(0, 10), pady=(5, 0))

value_label = tk.Label(root, text="Value:")
value_label.grid(row=2, column=0, sticky='e', padx=(10, 5))
value_entry = tk.Entry(root, highlightthickness=1,borderwidth=5, highlightbackground="gray")
value_entry.grid(row=2, column=1, sticky='we', padx=(0, 10))

update_button = tk.Button(root, text="Update", command=update_json,borderwidth=5, highlightthickness=1, highlightbackground="gray")
update_button.grid(row=3, column=1, columnspan=1, sticky='s', padx=(10, 0), pady=(0, 10))

selected_column_index = None
treeview.bind("<ButtonRelease-1>", on_click)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

scrollbar_frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray")
scrollbar_frame.grid(row=0, column=3, sticky="ns")

tree_scroll_y = tk.Scrollbar(scrollbar_frame, orient="vertical", command=treeview.yview)
tree_scroll_y.pack(side="right", fill="y")

treeview.configure(yscrollcommand=tree_scroll_y.set)

tree_scroll_y.bind("<Motion>", toggle_scroll_button)
tree_scroll_y.bind("<ButtonRelease-1>", toggle_scroll_button)

root.mainloop()
