import json
import tkinter as tk
from tkinter import messagebox, ttk
import math

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

def update_json():
    selected_index = treeview.selection()
    if selected_index:
        item = treeview.item(selected_index)
        item_values = item['values']
        value = value_entry.get()
        if value:
            index = int(selected_index[0][1:]) - 1
            column_name = treeview['columns'][selected_column_index]

            if column_name == "Кольори":
                new_colors = [rgb_to_name(color.strip()) for color in value.split(',')]
                item_values[selected_column_index] = ', '.join(new_colors)
                data[index][column_name] = new_colors
            else:
                item_values[selected_column_index] = str(value)
                data[index][column_name] = str(value)

            treeview.item(selected_index, values=item_values)
            save_json_file(filename, data)
            messagebox.showinfo("Success", "Data updated successfully")
            value_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a value")
    else:
        messagebox.showerror("Error", "Please select an item")
def on_click(event):
    global selected_column_index
    column = treeview.identify_column(event.y)
    if column:
        clicked_column_index = int(column[1:]) - 1
        selected_column_index = clicked_column_index  # Always update the selected column index
        column_name = treeview.heading(column)['text']
        selected_index = treeview.focus()
        selected_item = treeview.item(selected_index)
        selected_value = selected_item['values'][selected_column_index]
        value_entry.delete(0, tk.END)
        value_entry.insert(0, selected_value)
        characteristic_entry.delete(0, tk.END)
        characteristic_entry.insert(0, column_name)

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

    rgb = tuple(map(int, rgb_string[4:-1].split(', ')))

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

treeview = ttk.Treeview(root, columns=["Characteristic"] + list(data[0].keys()), show="headings", height=20)
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

treeview.grid(row=0, column=0, sticky="nsew")

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
    treeview_id = treeview.insert('', 'end', values=[""] + item_values + [display_colors(colors)])

    apply_color_tags(treeview_id, colors_hex)

def on_scroll(event):
    if event.num == 5 or event.delta < 0:  # Scroll right
        if not scroll_to_left_button.winfo_viewable():
            scroll_to_left_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
    elif event.num == 4 or event.delta > 0:  # Scroll left
        if not treeview.xview()[0] == 0.0:
            if not scroll_to_left_button.winfo_viewable():
                scroll_to_left_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
        else:
            if scroll_to_left_button.winfo_viewable():
                scroll_to_left_button.place_forget()

def scroll_to_left():
    treeview.xview_moveto(0)
    scroll_to_left_button.place_forget()

def toggle_scroll_button(event):
    if event.num == 5 or event.delta < 0:  # Scroll right
        if not scroll_to_left_button.winfo_viewable():
            scroll_to_left_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
    elif event.num == 4 or event.delta > 0:  # Scroll left
        if not treeview.xview()[0] == 0.0:
            if not scroll_to_left_button.winfo_viewable():
                scroll_to_left_button.place(in_=treeview, relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)
        else:
            if scroll_to_left_button.winfo_viewable():
                scroll_to_left_button.place_forget()


def display_rows(start_index, end_index):
    for item in data[start_index:end_index]:
        item_values = list(item.values())
        colors = item_values.pop()
        if isinstance(colors, list):
            colors_hex = [rgb_to_hex(color.strip()) for color in colors]
        else:
            colors_hex = [rgb_to_hex(color.strip()) for color in colors.split(', ')]
        treeview_id = treeview.insert('', 'end', values=[""] + item_values + [display_colors(colors)])

        apply_color_tags(treeview_id, colors_hex)

# Define start and end indices for displayed rows
start_index = 0
end_index = 10

# Function to update the displayed rows based on the scrollbar position
def on_scroll(event):
    if event.num == 5 or event.delta < 0:  # Scroll down
        if end_index < len(data):
            start_index += 1
            end_index += 1
            treeview.delete(*treeview.get_children())
            display_rows(start_index, end_index)
    elif event.num == 4 or event.delta > 0:  # Scroll up
        if start_index > 0:
            start_index -= 1
            end_index -= 1
            treeview.delete(*treeview.get_children())
            display_rows(start_index, end_index)

# Function to handle mouse wheel events for scrolling
def toggle_scroll_button(event):
    if event.num == 5 or event.delta < 0:  # Scroll down
        if end_index < len(data):
            start_index += 1
            end_index += 1
            treeview.delete(*treeview.get_children())
            display_rows(start_index, end_index)
    elif event.num == 4 or event.delta > 0:  # Scroll up
        if start_index > 0:
            start_index -= 1
            end_index -= 1
            treeview.delete(*treeview.get_children())
            display_rows(start_index, end_index)

display_rows(start_index, end_index)

treeview.bind("<MouseWheel>", on_scroll)  # For Windows and Linux
treeview.bind("<Button-4>", on_scroll)  # For Linux
treeview.bind("<Button-5>", on_scroll)  # For Linux

scroll_to_left_button = tk.Button(root, text="Scroll to Left", command=scroll_to_left, highlightthickness=1, highlightbackground="gray")

treeview.bind("<MouseWheel>", toggle_scroll_button)  # For Windows and Linux
treeview.bind("<Button-4>", toggle_scroll_button)  # For Linux
treeview.bind("<Button-5>", toggle_scroll_button)  # For Linux

characteristic_label = tk.Label(root, text="Characteristic:")
characteristic_label.grid(row=1, column=0, sticky='e', padx=(10, 5), pady=(5, 0))
characteristic_entry = tk.Entry(root, highlightthickness=1, highlightbackground="gray")
characteristic_entry.grid(row=1, column=1, sticky='we', padx=(0, 10), pady=(5, 0))

value_label = tk.Label(root, text="Value:")
value_label.grid(row=2, column=0, sticky='e', padx=(10, 5))
value_entry = tk.Entry(root, highlightthickness=1, highlightbackground="gray")
value_entry.grid(row=2, column=1, sticky='we', padx=(0, 10))

update_button = tk.Button(root, text="Update", command=update_json, highlightthickness=1, highlightbackground="gray")
update_button.grid(row=3, column=1, columnspan=1, sticky='s', padx=(10, 0), pady=(0, 10))

selected_column_index = None
treeview.bind("<ButtonRelease-1>", on_click)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

scrollbar_frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray")
scrollbar_frame.grid(row=1, column=0, sticky="ew")

tree_scroll_x = tk.Scrollbar(scrollbar_frame, orient="horizontal", command=treeview.xview)
tree_scroll_x.pack(side="bottom", fill="x")

treeview.configure(xscrollcommand=tree_scroll_x.set)


def transpose_data(data):
    transposed_data = []
    num_rows = len(data)
    num_cols = len(data[0])

    for j in range(num_cols):
        transposed_row = {}
        for i in range(num_rows):
            transposed_row[f"Column {i+1}"] = data[i][list(data[i].keys())[j]]
        transposed_data.append(transposed_row)

    return transposed_data

transposed_data = transpose_data(data)

# Now update the treeview with transposed columns
treeview.config(columns=list(transposed_data[0].keys()))

for col in transposed_data[0].keys():
    column_width = MIN_COLUMN_WIDTH
    treeview.heading(col, text=col)
    treeview.column(col, width=column_width, minwidth=column_width, anchor="center")

# Remove existing items from the treeview
for item in treeview.get_children():
    treeview.delete(item)

# Insert transposed data into the treeview
for item in transposed_data:
    item_values = list(item.values())
    treeview.insert('', 'end', values=item_values)

# Update scrollbar
root.update_idletasks()
min_width = sum(treeview.column(col, "minwidth") for col in transposed_data[0].keys())
root.minsize(min_width + 20, min_height + 120)


root.mainloop()
