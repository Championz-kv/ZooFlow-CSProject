import customtkinter as ctk     # main GUI module
import mysql.connector as msc     # MySQL connector
import ast

ctk.set_appearance_mode("dark")     # default colour schemes
ctk.set_default_color_theme("blue")

# variables to Store credentials globally after login to use later
logged_in_username = None
logged_in_password = None
shop = False

# for info page
global txt
txt = ''' 
This computer science project is collective set of two applications interfaces connected through a database, the PawCache🐾, that are-\n
CritterScribe: Animal Record Management for Zoo Workers 🔍
ZooDash: One Dashboard, Efficient Tracking, and Piles of Zoo Data 👨🏽‍💻\n
Description-\n
The ZooFlow project involves two python based applications working together for the smart and efficient management of the zoo, to take care of all the animals, updating their data and requirements for food, health and cleanliness, on the common SQL database, containing all the necessary informations required, like the food stock, visitors, staff, animals, their info and so on. \n
The first application, CritterScribe lets the workers of the zoo and caretakers of the various species to update and check the data regarding the meals of every animal in the area, their health check or cleanliness records, gender and age. This serves easy recording of data without making any mess or chance to forget about  anything, in an perfect and efficient manner.\n
What works alongside it is the multipurpose dashboard, ZooDash, letting the owners, admins or managers of the zoo to have a check on all the records updated by the workers, and on the stock amount of food resources and medicines they have for their animals, so that they dont find themselves in the corner at the last moment. It helps track the visiting patterns too, while registering the entries and ticket with the time and money records.\n
The database, PawCache as we call it, with its structure built on MySQL, is connected with the above applications through the well known language of python, having a clean set of separated tables for staff details, visitor tickets, animals and their info and the resources available in stock. It is designed in a way to create maximum and efficient outputs, while being easily modifiable and upgradable.'''

def attempt_login():
    global logged_in_username, logged_in_password, shop, root
    usern = username_entry.get()
    passw = password_entry.get()

    try:
        # First, try logging in with entered credentials
        conn = msc.connect(
            host="localhost",
            user=usern,
            passwd=passw,
            database="pawcache",
            use_pure=True
        )
    except:
        message_label.configure(text="Login invalid. Try again.", text_color="red")
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        return

    try:
        # Now check if the user's job is allowed
        cursor = conn.cursor()
        cursor.execute("SELECT job FROM staff_dat WHERE staffid = %s", (usern,))
        result = cursor.fetchone()

        if result is None or result[0] not in ['Keeper', 'Veterinarian','Shopkeeper']:
            message_label.configure(text="Login invalid. No access", text_color="red")
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            conn.close()
            return

        conn.close()

    except:
        message_label.configure(text="Error checking user role.", text_color="red")
        conn.close()
        return

    logged_in_username = usern
    logged_in_password = passw
    if result[0] == 'Shopkeeper':
        shop = True
    root.destroy()
    open_main_app()

def toggle_theme():
    current = ctk.get_appearance_mode()
    new_mode = "dark" if current == "Light" else "light"
    ctk.set_appearance_mode(new_mode)

def logout(main_win):
    global logged_in_username, logged_in_password
    logged_in_username = None
    logged_in_password = None
    main_win.destroy()
    launch_login()

def open_animal_data():
    global shop
    if not shop:
        table = "animal_dat"
    else:
        table = "shop_stock"
    animal_win = ctk.CTk()
    if not shop:
        animal_win.title("Animal Data Editor")
    if shop:
        animal_win.title("Shop Stocks Editor")
    screen_width = animal_win.winfo_screenwidth()
    screen_height = animal_win.winfo_screenheight()
    animal_win.geometry(f"{screen_width}x{screen_height}+0+0")

    try:
        conn = msc.connect(
            host="localhost",
            user=logged_in_username,
            passwd=logged_in_password,
            database="pawcache",
            use_pure=True
        )
    except Exception as e:
        print("DB connection failed:", e)
        animal_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(animal_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(animal_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(animal_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(animal_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query=f"SELECT * FROM {table}"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query=f"SELECT * FROM {table}"):
        for w in scrollable_frame.winfo_children():
            w.destroy()
        rows, cols = fetch_data(query)
        for j, col in enumerate(cols):
            lbl = ctk.CTkLabel(scrollable_frame, text=col, font=header_font, anchor="w")
            lbl.grid(row=0, column=j, sticky="w", padx=10, pady=6)
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell_text = str(val)
                lbl = ctk.CTkLabel(scrollable_frame, text=cell_text, font=cell_font, anchor="w")
                lbl.grid(row=i+1, column=j, sticky="w", padx=10, pady=4)
                lbl.bind("<Enter>", lambda e, t=cell_text: on_enter(e, t))
                lbl.bind("<Leave>", on_leave)
        for j in range(len(cols)):
            scrollable_frame.grid_columnconfigure(j, weight=1)

    def clear_inputs():
        for w in input_frame.winfo_children():
            w.destroy()
        entries.clear()

    def show_edit_fields():
        nonlocal mode
        mode = 'edit'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        cols = [desc[0] for desc in cursor.description]
        for j, col in enumerate(cols):
            ent = ctk.CTkEntry(input_frame, placeholder_text=col)
            ent.grid(row=0, column=j, padx=8, pady=5, sticky="ew")
            entries.append(ent)
            input_frame.grid_columnconfigure(j, weight=1)
        btn = ctk.CTkButton(input_frame, text="Save Edit", command=save_edit)
        btn.grid(row=0, column=len(cols), padx=8)

    def show_add_fields():
        nonlocal mode
        mode = 'add'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        cols = [desc[0] for desc in cursor.description][1:]
        for j, col in enumerate(cols):
            ent = ctk.CTkEntry(input_frame, placeholder_text=col)
            ent.grid(row=0, column=j, padx=8, pady=5, sticky="ew")
            entries.append(ent)
            input_frame.grid_columnconfigure(j, weight=1)
        btn = ctk.CTkButton(input_frame, text="Save Add", command=save_add)
        btn.grid(row=0, column=len(cols), padx=8)

    def show_delete_field():
        nonlocal mode
        mode = 'delete'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        ent = ctk.CTkEntry(input_frame, placeholder_text='ID (primary key)')
        ent.grid(row=0, column=0, padx=8, pady=5, sticky="ew")
        entries.append(ent)
        btn = ctk.CTkButton(input_frame, text="Confirm Delete", command=delete_record)
        btn.grid(row=0, column=1, padx=8)

    def save_edit():
        vals = [e.get().strip() for e in entries]
        if not vals[0].isdigit():
            return
        record_id = int(vals[0])
        cursor.execute(f"SELECT * FROM {table} WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def save_add():
        vals = [e.get().strip() for e in entries]
        if not all(vals):
            return
        cols = [desc[0] for desc in cursor.description][1:]
        placeholders = ", ".join(["%s"] * len(cols))
        cursor.execute(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
            vals
        )
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def delete_record():
        vals = [e.get().strip() for e in entries]
        if not vals[0].isdigit():
            return
        record_id = int(vals[0])
        cursor.execute(f"DELETE FROM {table} WHERE {cursor.description[0][0]}=%s", (record_id,))
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def toggle_filter():
        nonlocal filter_active, filter_col_dropdown, filter_val_dropdown, confirm_filter_btn

        if not filter_active:
            filter_frame.pack(pady=5)
            clear_inputs()
            cols = [desc[0] for desc in cursor.description]
            filter_col_dropdown = ctk.CTkOptionMenu(filter_frame, values=cols)
            filter_col_dropdown.set("Select Column")
            filter_col_dropdown.grid(row=0, column=0, padx=8)

            def update_value_dropdown(choice):
                cursor.execute(f"SELECT DISTINCT {choice} FROM {table}")
                values = [str(row[0]) for row in cursor.fetchall()]
                filter_val_dropdown.configure(values=values)
                if values:
                    filter_val_dropdown.set(values[0])
                else:
                    filter_val_dropdown.set("")

            filter_val_dropdown = ctk.CTkOptionMenu(filter_frame, values=["Select Column First"])
            filter_val_dropdown.set("Select Value")
            filter_val_dropdown.grid(row=0, column=1, padx=8)

            filter_col_dropdown.configure(command=update_value_dropdown)

            confirm_filter_btn = ctk.CTkButton(filter_frame, text="Confirm Selection", command=apply_filter)
            confirm_filter_btn.grid(row=0, column=2, padx=8)

            filter_button.configure(text="Remove Filter")
            filter_active = True
        else:
            filter_frame.pack_forget()
            display_table()
            filter_button.configure(text="Apply Filter")
            filter_active = False

    def apply_filter():
        col = filter_col_dropdown.get()
        val = filter_val_dropdown.get()
        query = f"SELECT * FROM {table} WHERE {col} = %s"
        cursor.execute(query, (val,))
        rows = cursor.fetchall()
        if rows:
            for w in scrollable_frame.winfo_children():
                w.destroy()
            cols = [desc[0] for desc in cursor.description]
            for j, colname in enumerate(cols):
                lbl = ctk.CTkLabel(scrollable_frame, text=colname, font=header_font, anchor="w")
                lbl.grid(row=0, column=j, sticky="w", padx=10, pady=6)
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    cell_text = str(val)
                    lbl = ctk.CTkLabel(scrollable_frame, text=cell_text, font=cell_font, anchor="w")
                    lbl.grid(row=i+1, column=j, sticky="w", padx=10, pady=4)
                    lbl.bind("<Enter>", lambda e, t=cell_text: on_enter(e, t))
                    lbl.bind("<Leave>", on_leave)

    # BUTTONS
    edit_button = ctk.CTkButton(button_frame, text="Edit", command=show_edit_fields)
    add_button = ctk.CTkButton(button_frame, text="Add", command=show_add_fields)
    delete_button = ctk.CTkButton(button_frame, text="Delete", command=show_delete_field)
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=animal_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    add_button.grid(row=0, column=1, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    animal_win.mainloop()

def open_food_data():
    global shop
    if not shop:
        table = "food_dir"
    else:
        table = "shop_purchase_logs"
    food_win = ctk.CTk()
    if not shop:
        food_win.title("Food Stocks Viewer")
    if shop:
        food_win.title("Shop Purchase Logs")
    screen_width = food_win.winfo_screenwidth()
    screen_height = food_win.winfo_screenheight()
    food_win.geometry(f"{screen_width}x{screen_height}+0+0")

    try:
        conn = msc.connect(
            host="localhost",
            user=logged_in_username,
            passwd=logged_in_password,
            database="pawcache",
            use_pure=True
        )
    except Exception as e:
        print("DB connection failed:", e)
        food_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    scrollable_frame = ctk.CTkScrollableFrame(food_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(food_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(food_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME ---
    filter_frame = ctk.CTkFrame(food_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")
    status_label.grid(row=0, column=5, padx=(20, 10))

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    def fetch_data(query=f"SELECT * FROM {table}"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query=f"SELECT * FROM {table}"):
        for w in scrollable_frame.winfo_children():
            w.destroy()
        rows, cols = fetch_data(query)
        for j, col in enumerate(cols):
            lbl = ctk.CTkLabel(scrollable_frame, text=col, font=header_font, anchor="w")
            lbl.grid(row=0, column=j, sticky="w", padx=10, pady=6)
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell_text = str(val)
                lbl = ctk.CTkLabel(scrollable_frame, text=cell_text, font=cell_font, anchor="w")
                lbl.grid(row=i+1, column=j, sticky="w", padx=10, pady=4)
                lbl.bind("<Enter>", lambda e, t=cell_text: on_enter(e, t))
                lbl.bind("<Leave>", on_leave)
        for j in range(len(cols)):
            scrollable_frame.grid_columnconfigure(j, weight=1)

    def clear_inputs():
        for w in input_frame.winfo_children():
            w.destroy()
        entries.clear()

    def show_edit_fields():
        nonlocal mode
        mode = 'edit'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        cols = [desc[0] for desc in cursor.description]
        for j, col in enumerate(cols):
            ent = ctk.CTkEntry(input_frame, placeholder_text=col)
            ent.grid(row=0, column=j, padx=8, pady=5, sticky="ew")
            entries.append(ent)
            input_frame.grid_columnconfigure(j, weight=1)
        btn = ctk.CTkButton(input_frame, text="Save Edit", command=save_edit)
        btn.grid(row=0, column=len(cols), padx=8)

    def show_add_fields():
        nonlocal mode
        mode = 'add'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        cols = [desc[0] for desc in cursor.description][1:]
        for j, col in enumerate(cols):
            ent = ctk.CTkEntry(input_frame, placeholder_text=col)
            ent.grid(row=0, column=j, padx=8, pady=5, sticky="ew")
            entries.append(ent)
            input_frame.grid_columnconfigure(j, weight=1)
        btn = ctk.CTkButton(input_frame, text="Save Add", command=save_add)
        btn.grid(row=0, column=len(cols), padx=8)

    def show_delete_field():
        nonlocal mode
        mode = 'delete'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        ent = ctk.CTkEntry(input_frame, placeholder_text='ID (primary key)')
        ent.grid(row=0, column=0, padx=8, pady=5, sticky="ew")
        entries.append(ent)
        btn = ctk.CTkButton(input_frame, text="Confirm Delete", command=delete_record)
        btn.grid(row=0, column=1, padx=8)

    def save_edit():
        vals = [e.get().strip() for e in entries]
        if not vals[0].isdigit():
            return
        record_id = int(vals[0])
        cursor.execute(f"SELECT * FROM {table} WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def save_add():
        vals = [e.get().strip() for e in entries]
        if not all(vals):
            return
        cols = [desc[0] for desc in cursor.description][1:]
        placeholders = ", ".join(["%s"] * len(cols))
        cursor.execute(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
            vals
        )
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def delete_record():
        vals = [e.get().strip() for e in entries]
        if not vals[0].isdigit():
            return
        record_id = int(vals[0])
        cursor.execute(f"DELETE FROM {table} WHERE {cursor.description[0][0]}=%s", (record_id,))
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def toggle_filter():
        nonlocal filter_active, filter_col_dropdown, filter_val_dropdown, confirm_filter_btn

        if not filter_active:
            filter_frame.pack(pady=5)
            clear_inputs()
            cols = [desc[0] for desc in cursor.description]
            filter_col_dropdown = ctk.CTkOptionMenu(filter_frame, values=cols)
            filter_col_dropdown.set("Select Column")
            filter_col_dropdown.grid(row=0, column=0, padx=8)

            def update_value_dropdown(choice):
                cursor.execute(f"SELECT DISTINCT {choice} FROM {table}")
                values = [str(row[0]) for row in cursor.fetchall()]
                filter_val_dropdown.configure(values=values)
                if values:
                    filter_val_dropdown.set(values[0])
                else:
                    filter_val_dropdown.set("")

            filter_val_dropdown = ctk.CTkOptionMenu(filter_frame, values=["Select Column First"])
            filter_val_dropdown.set("Select Value")
            filter_val_dropdown.grid(row=0, column=1, padx=8)

            filter_col_dropdown.configure(command=update_value_dropdown)

            confirm_filter_btn = ctk.CTkButton(filter_frame, text="Confirm Selection", command=apply_filter)
            confirm_filter_btn.grid(row=0, column=2, padx=8)

            filter_button.configure(text="Remove Filter")
            filter_active = True
        else:
            filter_frame.pack_forget()
            display_table()
            filter_button.configure(text="Apply Filter")
            filter_active = False

    def apply_filter():
        col = filter_col_dropdown.get()
        val = filter_val_dropdown.get()
        query = f"SELECT * FROM {table} WHERE {col} = %s"
        cursor.execute(query, (val,))
        rows = cursor.fetchall()
        if rows:
            for w in scrollable_frame.winfo_children():
                w.destroy()
            cols = [desc[0] for desc in cursor.description]
            for j, colname in enumerate(cols):
                lbl = ctk.CTkLabel(scrollable_frame, text=colname, font=header_font, anchor="w")
                lbl.grid(row=0, column=j, sticky="w", padx=10, pady=6)
            for i, row in enumerate(rows):
                for j, val in enumerate(row):
                    cell_text = str(val)
                    lbl = ctk.CTkLabel(scrollable_frame, text=cell_text, font=cell_font, anchor="w")
                    lbl.grid(row=i+1, column=j, sticky="w", padx=10, pady=4)
                    lbl.bind("<Enter>", lambda e, t=cell_text: on_enter(e, t))
                    lbl.bind("<Leave>", on_leave)

    edit_button = ctk.CTkButton(button_frame, text="Edit", command=show_edit_fields)
    add_button = ctk.CTkButton(button_frame, text="Add", command=show_add_fields)
    delete_button = ctk.CTkButton(button_frame, text="Delete", command=show_delete_field)
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=food_win.destroy)

    edit_button.grid(row=0, column=0, padx=8)
    add_button.grid(row=0, column=1, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)

    display_table()
    food_win.mainloop()

def make_new_bill():
    import mysql.connector as msc
    from datetime import datetime

    conn = msc.connect(
        host="localhost",
        user=logged_in_username,
        password=logged_in_password,
        database="pawcache",
        use_pure=True
    )
    cursor = conn.cursor()

    bill_win = ctk.CTk()
    bill_win.title("Create Purchase Bill")
    bill_win.geometry("600x520+400+150")

    font_main = ("Arial", 18)
    item_qty_dict = {}
    amount_sum = [0]  # Using list to make it mutable in nested functions

    top_frame = ctk.CTkFrame(bill_win)
    top_frame.pack(fill="x", pady=10, padx=10)

    left_label = ctk.CTkLabel(top_frame, text=f"User: {logged_in_username} - New Bill", font=font_main)
    left_label.pack(side="left")

    def close_bill():
        bill_win.destroy()

    close_btn = ctk.CTkButton(top_frame, text="Close", command=close_bill, font=font_main)
    close_btn.pack(side="right", padx=10)

    center_frame = ctk.CTkFrame(bill_win)
    center_frame.pack(pady=20, padx=40, fill="both", expand=True)

    def add_input_row(label_text, default_value="", readonly=False):
        row = ctk.CTkFrame(center_frame)
        row.pack(fill="x", pady=4)

        lbl = ctk.CTkLabel(row, text=label_text + ":", width=200, anchor="w", font=font_main)
        lbl.pack(side="left")

        ent = ctk.CTkEntry(row, font=font_main)
        ent.insert(0, str(default_value))
        if readonly:
            ent.configure(state="readonly")
        ent.pack(side="left", fill="x", expand=True)
        return ent

    ent_ticketno = add_input_row("Ticket No")

    cursor.execute("SELECT block FROM staff_dat where staffid = %s", (logged_in_username,))
    block_row = cursor.fetchone()
    block_val = block_row[0] if block_row else ""
    ent_shop_no = add_input_row("Shop No", default_value=block_val)

    def update_dropdown_on_enter(event=None):
        shopno_str = ent_shop_no.get().strip()
        if not shopno_str.isdigit():
            return
        shopno = int(shopno_str)
        cursor.execute("SELECT itemname FROM shop_stock WHERE in_stock > 0 AND shop_no = %s", (shopno,))
        item_list = sorted({row[0] for row in cursor.fetchall()})
        item_dropdown.configure(values=item_list)

    ent_shop_no.bind("<Return>", update_dropdown_on_enter)
    row_item_input = ctk.CTkFrame(center_frame)
    row_item_input.pack(fill="x", pady=4)

    lbl_items = ctk.CTkLabel(row_item_input, text="Add Item:", width=200, anchor="w", font=font_main)
    lbl_items.pack(side="left")

    shopno = int(ent_shop_no.get().strip())
    cursor.execute("SELECT itemname FROM shop_stock WHERE in_stock > 0 AND shop_no = %s", (shopno,))
    item_list = sorted([row[0] for row in cursor.fetchall()])

    item_dropdown = ctk.CTkComboBox(row_item_input, values=item_list, font=font_main, width=140, state="readonly")
    item_dropdown.pack(side="left", padx=5)
    item_dropdown.set("")

    qty_entry = ctk.CTkEntry(row_item_input, width=50, font=font_main)
    qty_entry.pack(side="left", padx=5)

    row_items = ctk.CTkFrame(center_frame)
    row_items.pack(fill="x", pady=4)
    lbl_items_full = ctk.CTkLabel(row_items, text="Items Tuple:", width=200, anchor="w", font=font_main)
    lbl_items_full.pack(side="left")
    items_text = ctk.CTkEntry(row_items, font=font_main, state="readonly")
    items_text.pack(side="left", fill="x", expand=True)

    def calculate_total():
        amount_sum[0] = 0
        try:
            for item, qty in item_qty_dict.items():
                cursor.execute("SELECT price FROM shop_stock WHERE itemname = %s", (item,))
                result = cursor.fetchall()  # <-- Use fetchall() to consume result fully
                if result:
                    price = int(result[0][0])
                    amount_sum[0] += price * qty
            ent_amount.configure(state="normal")
            ent_amount.delete(0, 'end')
            ent_amount.insert(0, str(amount_sum[0]))
            ent_amount.configure(state="readonly")
        except Exception as e:
            print("Calculation error:", e)
            amount_sum[0] = 0

    row_amount = ctk.CTkFrame(center_frame)
    row_amount.pack(fill="x", pady=4)

    lbl_amount = ctk.CTkLabel(row_amount, text="Total Amount:", width=200, anchor="w", font=font_main)
    lbl_amount.pack(side="left")

    ent_amount = ctk.CTkEntry(row_amount, state="readonly", font=font_main, width=100)
    ent_amount.pack(side="left", padx=(0, 10))

    calc_btn = ctk.CTkButton(row_amount, text="Calculate", font=font_main, command=calculate_total, width=120)
    calc_btn.pack(side="left")

    msg_label = ctk.CTkLabel(center_frame, text="", font=font_main)
    msg_label.pack()

    def add_item_tuple():
        item = item_dropdown.get().strip()
        qty = qty_entry.get().strip()
        if item and qty.isdigit():
            qty = int(qty)
            item_qty_dict[item] = item_qty_dict.get(item, 0) + qty
            current_text = items_text.get()
            if current_text and not current_text.endswith(","):
                current_text += ","
            new_tuple = f"('{item}',{qty})"
            updated = current_text + new_tuple + ","
            items_text.configure(state="normal")
            items_text.delete(0, 'end')
            items_text.insert(0, updated)
            items_text.configure(state="readonly")
            item_dropdown.set("")
            qty_entry.delete(0, 'end')

    plus_btn = ctk.CTkButton(row_item_input, text="+", command=add_item_tuple, width=40, font=font_main)
    plus_btn.pack(side="left", padx=5)

    def reset_fields():
        ent_ticketno.delete(0, 'end')
        ent_shop_no.delete(0, 'end')
        ent_shop_no.insert(0, block_val)
        items_text.configure(state="normal")
        items_text.delete(0, 'end')
        items_text.configure(state="readonly")
        ent_amount.configure(state="normal")
        ent_amount.delete(0, 'end')
        ent_amount.configure(state="readonly")
        item_dropdown.set("")
        qty_entry.delete(0, 'end')
        item_qty_dict.clear()
        amount_sum[0] = 0
        btn.configure(text="Create Bill")

    def handle_bill_confirm():
        nonlocal amount_sum, item_qty_dict  # Access the outer variables

        ticket_val = ent_ticketno.get().strip()
        shop_val = ent_shop_no.get().strip()
        item_str_raw = items_text.get().strip()

        if btn.cget("text") == "Create Bill":
            # Validate all required fields
            if not ticket_val or not shop_val or not item_str_raw:
                msg_label.configure(text="All fields (Ticket, Shop No, Items) must be filled", text_color="orange")
                bill_win.after(2000, lambda: msg_label.configure(text=""))
                return
            if ticket_val and not ticket_val.isdigit():
                msg_label.configure(text="Ticket No must be numeric", text_color="red")
                bill_win.after(2000, lambda: msg_label.configure(text=""))
                return
            if shop_val and not shop_val.isdigit():
                msg_label.configure(text="Shop No must be numeric", text_color="red")
                bill_win.after(2000, lambda: msg_label.configure(text=""))
                return
            # Ensure total is calculated once before moving to confirm stage
            calculate_total()

            msg_label.configure(text="", text_color="green")
            btn.configure(text="CONFIRM BILL")

        else:
            ticket = int(ticket_val) if ticket_val.isdigit() else None
            shopno = int(shop_val)
            items_str = item_str_raw.rstrip(",")
            formatted_items = f"({items_str})" if items_str else None
            amount = int(ent_amount.get()) if ent_amount.get().strip().isdigit() else None

            cursor.execute(
                "INSERT INTO shop_purchase_logs (ticketno, shop_no, items, amount) VALUES (%s, %s, %s, %s)",
                (ticket, shopno, formatted_items, amount)
            )
            conn.commit()

            msg_label.configure(text="Bill successfully added", text_color="green")
            bill_win.after(2000, lambda: msg_label.configure(text=""))  # Show message for 2 sec

            reset_fields()
            item_qty_dict.clear()
            amount_sum = 0
            btn.configure(text="Create Bill")  # Reset button label

    btn = ctk.CTkButton(center_frame, text="Create Bill", font=font_main, command=handle_bill_confirm)
    btn.pack(pady=10)

    bill_win.mainloop()

def open_main_app():
    import mysql.connector
    global logged_in_username, logged_in_password, shop
    request_view_mode = {"previous": False}  # Tracks if we're in previous requests view

    new_win = ctk.CTk()
    new_win.title("CritterScribe Homepage")
    screen_width = new_win.winfo_screenwidth()
    screen_height = new_win.winfo_screenheight()
    new_win.geometry(f"{screen_width}x{screen_height}+0+0")

    underline = ctk.CTkFrame(new_win, height=4, fg_color=("#000083", "#9BB6FF"))
    underline.place(relx=0.2, rely=0.16, relwidth=0.6)
    underline2 = ctk.CTkFrame(new_win, height=4, fg_color=("#10861A", "#97FFB5"))
    underline2.place(relx=0.24, rely=0.18, relwidth=0.52)

    heading_label = ctk.CTkLabel(new_win, text="CritterScribe Homepage", font=ctk.CTkFont(size=30, weight="bold"))
    heading_label.place(relx=0.5, rely=0.1, anchor="center")

    logout_button = ctk.CTkButton(new_win, text="Logout", command=lambda: logout(new_win),
                                  fg_color="red", hover_color="#aa0000")
    logout_button.place(relx=0.98, rely=0.02, anchor="ne")

    def toggle_password_entry():
        if password_entry.winfo_ismapped():
            password_entry.place_forget()
        else:
            password_entry.place(x=10, y=60)

    def change_password():
        global logged_in_username, logged_in_password
        new_password = password_entry.get()
        if not new_password:
            status_label.configure(text="Please enter a new password.", text_color="orange")
            new_win.after(2000, lambda: status_label.configure(text=""))
            return
        try:
            db = mysql.connector.connect(host="localhost", user=logged_in_username,
                                         password=logged_in_password, use_pure=True)
            cursor = db.cursor()
            cursor.execute(f"ALTER USER CURRENT_USER() IDENTIFIED BY '{new_password}'")
            db.commit()
            password_entry.delete(0, "end")
            password_entry.place_forget()
            status_label.configure(text="Password changed successfully.", text_color="green")
            new_win.after(2000, lambda: status_label.configure(text=""))
            logged_in_password = new_password
        except Exception as e:
            status_label.configure(text=f"Password change unsuccessful.", text_color="red")
            new_win.after(2000, lambda: status_label.configure(text=""))
            print("Error:", e)
        finally:
            try:
                cursor.close()
                db.close()
            except:
                pass

    def open_about_page():
        about_win = ctk.CTk()
        about_win.title("About ZooFlow")
        about_win.geometry(f"{about_win.winfo_screenwidth()}x{about_win.winfo_screenheight()}+0+0")
        heading = ctk.CTkLabel(about_win, text="About ZooFlow", font=ctk.CTkFont(size=32, weight="bold"))
        heading.place(relx=0.5, rely=0.1, anchor="center")
        underline1 = ctk.CTkFrame(about_win, height=4, fg_color=("#000083", "#9BB6FF"))
        underline1.place(relx=0.2, rely=0.16, relwidth=0.6)
        underline2 = ctk.CTkFrame(about_win, height=4, fg_color=("#10861A", "#97FFB5"))
        underline2.place(relx=0.24, rely=0.18, relwidth=0.52)
        
        info_textbox = ctk.CTkTextbox(about_win, width=1200, height=460, font=ctk.CTkFont(size=16), wrap="word")
        info_textbox.place(relx=0.5, rely=0.22, anchor="n")
        info_textbox.insert("1.0", txt)
        info_textbox.configure(state="disabled")
        close_button = ctk.CTkButton(about_win, text="Close", command=about_win.destroy)
        close_button.place(relx=0.98, rely=0.02, anchor="ne")
        about_win.mainloop()

    change_pass_button = ctk.CTkButton(new_win, text="Change Password", command=toggle_password_entry, width=130)
    change_pass_button.place(x=10, y=20)

    password_entry = ctk.CTkEntry(new_win, placeholder_text="New Password", show="*")
    password_entry.bind("<Return>", lambda e: change_password())

    status_label = ctk.CTkLabel(new_win, text="", font=ctk.CTkFont(size=12))
    status_label.place(x=10, y=90)

    user_label = ctk.CTkLabel(new_win, text=f"User: {logged_in_username}", font=ctk.CTkFont(size=14))
    user_label.place(x=160, y=25)

    toggle_button = ctk.CTkButton(new_win, text="Toggle Theme", command=toggle_theme)
    toggle_button.place(relx=0.86, rely=0.02, anchor="ne")

    about_button = ctk.CTkButton(new_win, text="About ZooFlow Project", command=open_about_page)
    about_button.place(relx=0.74, rely=0.02, anchor="ne")

    if not shop:
        btntxt = ["View Animal\nData","View Food\nStocks"]
    else :
        btntxt = ["View Shop\nStocks","View Purchase\nLogs"]

    animal_button = ctk.CTkButton(new_win, text=btntxt[0], width=200, height=90,
                                  font=ctk.CTkFont(size=20, weight="bold"), command=open_animal_data)
    animal_button.place(relx=0.1, rely=0.4, anchor="w")

    food_button = ctk.CTkButton(new_win, text=btntxt[1], width=200, height=90,
                                font=ctk.CTkFont(size=20, weight="bold"), command=open_food_data)
    food_button.place(relx=0.1, rely=0.55, anchor="w")

    if shop:
        makebill_button = ctk.CTkButton(new_win, text="Make bill", width=200, height=90,
                                    font=ctk.CTkFont(size=20, weight="bold"), command=make_new_bill) 
        makebill_button.place(relx=0.1, rely=0.85, anchor="w")
    mode = {"request": False}

    def load_text():
        try:
            conn = mysql.connector.connect(host="localhost", user=logged_in_username,
                                           password=logged_in_password, database="pawcache", use_pure=True)
            cur = conn.cursor()
            column = "request" if mode["request"] else "note"
            cur.execute(f"SELECT {column} FROM notes_for_{logged_in_username}")
            result = cur.fetchone()
            notes_box.delete("1.0", "end")
            if result and result[0]:
                notes_box.insert("1.0", result[0])
            cur.close()
            conn.close()
        except Exception as e:
            print("Load error:", e)

    def save_text():
        try:
            text = notes_box.get("1.0", "end-1c")
            column = "request" if mode["request"] else "note"
            conn = mysql.connector.connect(host="localhost", user=logged_in_username,
                                           password=logged_in_password, database="pawcache", use_pure=True)
            cur = conn.cursor()
            cur.execute(f"UPDATE notes_for_{logged_in_username} SET {column} = %s", (text,))
            conn.commit()
            cur.close()
            conn.close()
            msg = "Request successfully made." if mode["request"] else "Notes saved."
            status_message_label.configure(text=msg, text_color="green")
            new_win.after(2000, lambda: status_message_label.configure(text=""))
        except Exception as e:
            print("Save error:", e)
            status_message_label.configure(text="Save failed.", text_color="red")
            new_win.after(2000, lambda: status_message_label.configure(text=""))

    def clear_and_save():
        notes_box.delete("1.0", "end")
        notes_box.insert("1.0", "NA")
        save_text()

    def toggle_request_view():
        if not mode["request"]:
            return
        request_view_mode["previous"] = not request_view_mode["previous"]

        try:
            conn = mysql.connector.connect(host="localhost", user=logged_in_username,
                                           password=logged_in_password, database="pawcache", use_pure=True)
            cur = conn.cursor()

            notes_box.configure(state="normal")
            notes_box.delete("1.0", "end")

            if request_view_mode["previous"]:
                cur.execute("SELECT request, status FROM requests WHERE username = %s", (logged_in_username,))
                results = cur.fetchall()
                for req, stat in results:
                    notes_box.insert("end", f"{req} -- {stat}\n\n")
                notes_box.configure(state="disabled")
                see_requests_button.configure(text="Current Request")
            else:
                cur.execute(f"SELECT request FROM notes_for_{logged_in_username}")
                result = cur.fetchone()
                if result and result[0]:
                    notes_box.insert("1.0", result[0])
                notes_box.configure(state="normal")
                see_requests_button.configure(text="See Previous Requests")

            cur.close()
            conn.close()
        except Exception as e:
            print("Error in request view toggle:", e)

    def confirm_and_send_request():
        try:
            request_text = notes_box.get("1.0", "end-1c").strip()
            if not request_text:
                return

            conn = mysql.connector.connect(host="localhost", user=logged_in_username,
                                           password=logged_in_password, database="pawcache", use_pure=True)
            cur = conn.cursor()
            cur.execute("INSERT INTO requests (username, request, status) VALUES (%s, %s, 'not read')",
                        (logged_in_username, request_text))
            cur.execute(f"UPDATE notes_for_{logged_in_username} SET request = %s", (request_text,))
            conn.commit()
            cur.close()
            conn.close()
            status_message_label.configure(text="Request sent successfully.", text_color="green")
            new_win.after(2000, lambda: status_message_label.configure(text=""))
        except Exception as e:
            print("Send request error:", e)
            status_message_label.configure(text="Failed to send request.", text_color="red")
            new_win.after(2000, lambda: status_message_label.configure(text=""))

    notes_box = ctk.CTkTextbox(new_win, width=750, height=335, font=ctk.CTkFont(size=14),
                               fg_color=("#d5d5d5", "#464646"))
    clear_save_button = ctk.CTkButton(new_win, text="Clear & Save", width=120, command=clear_and_save)
    save_button = ctk.CTkButton(new_win, text="Save Notes", width=120, command=save_text)
    status_message_label = ctk.CTkLabel(new_win, text="", font=ctk.CTkFont(size=14))
    toggle_request_button = ctk.CTkButton(new_win, text="Make Request", width=200, height=90,
                                          font=ctk.CTkFont(size=20, weight="bold"), command=lambda: show_notes_ui(not mode["request"]))
    see_requests_button = ctk.CTkButton(new_win, text="See Previous Requests", width=180, command=toggle_request_view)
    send_request_button = ctk.CTkButton(new_win, text="Confirm & Send Request", width=180,
                                        command=confirm_and_send_request)

    see_requests_button.place_forget()
    send_request_button.place_forget()

    def show_notes_ui(request_mode):
        mode["request"] = request_mode

        # Exit "Previous Requests" view if user switches to Edit Notes
        if not request_mode and request_view_mode["previous"]:
            request_view_mode["previous"] = False
            see_requests_button.configure(text="See Previous Requests")
            notes_box.configure(state="normal")

        load_text()
        edit_notes_starter.place_forget()
        make_request_starter.place_forget()
        notes_box.place(relx=0.30, rely=0.25, anchor="nw")
        clear_save_button.place(relx=0.30, rely=0.78, anchor="nw")
        save_button.place(relx=0.88, rely=0.78, anchor="ne")
        status_message_label.place(relx=0.65, rely=0.78, anchor="ne")
        toggle_request_button.place(relx=0.1, rely=0.7, anchor="w")

        if request_mode:
            toggle_request_button.configure(text="Edit Notes")
            save_button.configure(text="Save Request")
            see_requests_button.place(relx=0.30, rely=0.83, anchor="nw")
            send_request_button.place(relx=0.88, rely=0.83, anchor="ne")
        else:
            toggle_request_button.configure(text="Make Request")
            save_button.configure(text="Save Notes")
            see_requests_button.place_forget()
            send_request_button.place_forget()

    edit_notes_starter = ctk.CTkButton(new_win, text="Edit Notes", width=200, height=90,
                                       font=ctk.CTkFont(size=20, weight="bold"), command=lambda: show_notes_ui(False))
    make_request_starter = ctk.CTkButton(new_win, text="Make Request", width=200, height=90,
                                         font=ctk.CTkFont(size=20, weight="bold"), command=lambda: show_notes_ui(True))
    edit_notes_starter.place(relx=0.42, rely=0.45, anchor="w")
    make_request_starter.place(relx=0.6, rely=0.45, anchor="w")

    new_win.mainloop()

def launch_login():
    global root, username_entry, password_entry, message_label

    root = ctk.CTk()     # main first login screen
    root.title("Login")
    root.geometry("400x360")
    login_label = ctk.CTkLabel(root, text="Login to CritterScribe", font=ctk.CTkFont(size=20, weight="bold"))     # top label
    login_label.pack(pady=20)

    username_entry = ctk.CTkEntry(root, placeholder_text="Username")     # username box
    username_entry.pack(pady=10)
    username_entry.bind("<Return>", lambda e: attempt_login())

    password_entry = ctk.CTkEntry(root, placeholder_text="Password", show="*")     # password box
    password_entry.pack(pady=10)
    password_entry.bind("<Return>", lambda e: attempt_login())

    login_button = ctk.CTkButton(root, text="Login", command=attempt_login, text_color="black",     # login button
                                 fg_color="lightgreen", hover_color="#77dd77")
    login_button.pack(pady=10)

    def open_about_from_login():
        root.destroy()
        about_win = ctk.CTk()
        about_win.title("About ZooFlow")
        about_win.geometry(f"{about_win.winfo_screenwidth()}x{about_win.winfo_screenheight()}+0+0")

        # Heading
        heading = ctk.CTkLabel(about_win, text="About ZooFlow", font=ctk.CTkFont(size=32, weight="bold"))
        heading.place(relx=0.5, rely=0.1, anchor="center")

        # Decorative lines
        underline1 = ctk.CTkFrame(about_win, height=4, fg_color=("#000083", "#9BB6FF"), corner_radius=0)
        underline1.place(relx=0.2, rely=0.16, relwidth=0.6)

        underline2 = ctk.CTkFrame(about_win, height=4, fg_color=("#10861A", "#97FFB5"), corner_radius=0)
        underline2.place(relx=0.24, rely=0.18, relwidth=0.52)

        # Scrollable info textbox (read-only)
        info_textbox = ctk.CTkTextbox(about_win, width=1200, height=460, font=ctk.CTkFont(size=16), wrap="word")
        info_textbox.place(relx=0.5, rely=0.22, anchor="n")
        info_textbox.insert("1.0", txt)  # Replace with your actual text
        info_textbox.configure(state="disabled")  # Make it read-only

        def close_and_reopen_login():
            about_win.destroy()
            launch_login()  # reopen login page

        close_button = ctk.CTkButton(about_win, text="Close", width=30, height=25, command=close_and_reopen_login,
                                    fg_color="red", hover_color="#aa0000")
        close_button.place(relx=0.98, rely=0.02, anchor="ne")

        about_win.mainloop()

    #toggle_bg = "#f0f0f0" if ctk.get_appearance_mode() == "Dark" else "#2b2b2b"
    toggle_button = ctk.CTkButton(root, text="Toggle Theme", command=toggle_theme)     # toggle button
    toggle_button.pack(pady=5)

    about_button = ctk.CTkButton(root, text="About ZooFlow Project", command=open_about_from_login)
    about_button.pack(pady=5)

    message_label = ctk.CTkLabel(root, text="", font=ctk.CTkFont(size=12))     # for displaying invalid msg
    message_label.pack()

    root.mainloop()

launch_login()