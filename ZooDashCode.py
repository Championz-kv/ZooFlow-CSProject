import customtkinter as ctk     # main GUI module
import mysql.connector as msc     # MySQL connector

ctk.set_appearance_mode("dark")     # default colour schemes
ctk.set_default_color_theme("blue")

# variables to Store credentials globally after login to use later
logged_in_username = None
logged_in_password = None
logged_in_job = None

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
    global logged_in_username, logged_in_password, logged_in_job, root

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
        
        if result is None or result[0] not in ['Manager', 'Admin',]:
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
    logged_in_job = result[0]
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
    animal_win = ctk.CTk()
    animal_win.title("Animal Data Editor")
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

    def fetch_data(query="SELECT * FROM animal_dat"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM animal_dat"):
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
        cursor.execute(f"SELECT * FROM animal_dat WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE animal_dat SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
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
            f"INSERT INTO animal_dat ({', '.join(cols)}) VALUES ({placeholders})",
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
        cursor.execute(f"DELETE FROM animal_dat WHERE {cursor.description[0][0]}=%s", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM animal_dat")
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
        query = f"SELECT * FROM animal_dat WHERE {col} = %s"
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

def open_transaction_data():
    transaction_win = ctk.CTk()
    transaction_win.title("Transaction logs")
    screen_width = transaction_win.winfo_screenwidth()
    screen_height = transaction_win.winfo_screenheight()
    transaction_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        transaction_win.destroy()
        return

    cursor = conn.cursor()
    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(transaction_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(transaction_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(transaction_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(transaction_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM transactions ORDER BY transact_no desc"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM transactions ORDER BY transact_no desc"):
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
        cursor.execute(f"SELECT * FROM transactions WHERE {cursor.description[0][0]}=%s ORDER BY transact_no desc", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE transactions SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
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
            f"INSERT INTO transactions ({', '.join(cols)}) VALUES ({placeholders})",
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
        cursor.execute(f"DELETE FROM transactions WHERE {cursor.description[0][0]}=%s", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM transactions")
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
        query = f"SELECT * FROM transactions WHERE {col} = %s ORDER BY transact_no desc"
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
    close_button = ctk.CTkButton(button_frame, text="Close", command=transaction_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    add_button.grid(row=0, column=1, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()
    transaction_win.mainloop()

def open_staff_data():
    staff_win = ctk.CTk()
    staff_win.title("Staff Data Editor")
    screen_width = staff_win.winfo_screenwidth()
    screen_height = staff_win.winfo_screenheight()
    staff_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        staff_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(staff_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(staff_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(staff_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(staff_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM staff_dat"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM staff_dat"):
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
        record_id = vals[0]
        if not record_id:
            return
        cursor.execute(f"SELECT * FROM staff_dat WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE staff_dat SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
        conn.commit()
        input_frame.pack_forget()
        display_table()

    def delete_record():
        vals = [e.get().strip() for e in entries]
        record_id = vals[0]
        if not record_id:
            return
        cursor.execute(f"DELETE FROM staff_dat WHERE {cursor.description[0][0]}=%s", (record_id,))
        cursor.execute(f"DROP USER IF EXISTS %s@'%' ", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM staff_dat")
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
        query = f"SELECT * FROM staff_dat WHERE {col} = %s"
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
    delete_button = ctk.CTkButton(button_frame, text="Delete", command=show_delete_field)
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=staff_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    staff_win.mainloop()

def open_visitor_data():
    visitor_win = ctk.CTk()
    visitor_win.title("View Visitor History")
    screen_width = visitor_win.winfo_screenwidth()
    screen_height = visitor_win.winfo_screenheight()
    visitor_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        visitor_win.destroy()
        return

    cursor = conn.cursor()
    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)
    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(visitor_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(visitor_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(visitor_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(visitor_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM visitors ORDER BY ticketno desc"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM visitors ORDER BY ticketno desc"):
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM visitors")
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
        query = f"SELECT * FROM visitors WHERE {col} = %s ORDER BY ticketno desc"
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
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=visitor_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    visitor_win.mainloop()

def open_requests_data():
    request_win = ctk.CTk()
    request_win.title("View Staff Requests")
    screen_width = request_win.winfo_screenwidth()
    screen_height = request_win.winfo_screenheight()
    request_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        request_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(request_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(request_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(request_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(request_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM requests ORDER BY sno desc"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM requests ORDER BY sno desc"):
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

        # Entry for S.No (read-only reference)
        sno_label = ctk.CTkLabel(input_frame, text="S.No:")
        sno_label.grid(row=0, column=0, padx=8)
        sno_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter S.No")
        sno_entry.grid(row=0, column=1, padx=8, pady=5, sticky="ew")
        entries.append(sno_entry)

        # Entry for Status (editable field)
        status_label = ctk.CTkLabel(input_frame, text="Status:")
        status_label.grid(row=0, column=2, padx=8)
        status_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter New Status")
        status_entry.grid(row=0, column=3, padx=8, pady=5, sticky="ew")
        entries.append(status_entry)

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # Save Button
        btn = ctk.CTkButton(input_frame, text="Save Edit", command=save_edit)
        btn.grid(row=0, column=4, padx=8)

    def save_edit():
        sno_val = entries[0].get().strip()
        new_status = entries[1].get().strip()

        if not sno_val.isdigit() or not new_status:
            return

        record_id = int(sno_val)
        cursor.execute("SELECT * FROM requests WHERE sno = %s ORDER BY sno DESC", (record_id,))
        current = cursor.fetchone()

        if not current:
            return

        cursor.execute("UPDATE requests SET status = %s WHERE sno = %s", (new_status, record_id))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM requests")
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
        query = f"SELECT * FROM requests WHERE {col} = %s ORDER BY sno desc"
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
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=request_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    request_win.mainloop()

def open_reviews_data():
    reviews_win = ctk.CTk()
    reviews_win.title("reviews Data Editor")
    screen_width = reviews_win.winfo_screenwidth()
    screen_height = reviews_win.winfo_screenheight()
    reviews_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        reviews_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(reviews_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(reviews_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(reviews_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(reviews_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM reviews order by date_and_time desc"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM reviews order by date_and_time desc"):
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

    def show_add_fields():
        nonlocal mode
        mode = 'add'
        clear_inputs()
        input_frame.pack(fill="x", padx=10)
        cols = [desc[0] for desc in cursor.description if desc[0] != 'date_and_time']
        for j, col in enumerate(cols):
            ent = ctk.CTkEntry(input_frame, placeholder_text=col)
            ent.grid(row=0, column=j, padx=8, pady=5, sticky="ew")
            entries.append(ent)
            input_frame.grid_columnconfigure(j, weight=1)
        btn = ctk.CTkButton(input_frame, text="Save Add", command=save_add)
        btn.grid(row=0, column=len(cols), padx=8)

    def save_add():
        vals = [e.get().strip() for e in entries]
        if not all(vals):
            return
        cols = [desc[0] for desc in cursor.description if desc[0] != 'date_and_time']
        placeholders = ", ".join(["%s"] * len(cols))
        cursor.execute(
            f"INSERT INTO reviews ({', '.join(cols)}) VALUES ({placeholders})",
            vals
        )
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM reviews")
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
        query = f"SELECT * FROM reviews WHERE {col} = %s order by date_and_time desc"
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
    add_button = ctk.CTkButton(button_frame, text="Add", command=show_add_fields)
    filter_button = ctk.CTkButton(button_frame, text="Apply Filter", command=toggle_filter)
    close_button = ctk.CTkButton(button_frame, text="Close", command=reviews_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    add_button.grid(row=0, column=1, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    reviews_win.mainloop()

def open_shop_purchase_logs_data():
    shop_logs_win = ctk.CTk()
    shop_logs_win.title("Shop Purchase Data")
    screen_width = shop_logs_win.winfo_screenwidth()
    screen_height = shop_logs_win.winfo_screenheight()
    shop_logs_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        shop_logs_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(shop_logs_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(shop_logs_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(shop_logs_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(shop_logs_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM shop_purchase_logs order by date_and_time desc"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM shop_purchase_logs order by date_and_time desc"):
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
        cursor.execute(f"SELECT * FROM shop_purchase_logs WHERE {cursor.description[0][0]}=%s order by date_and_time desc", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE shop_purchase_logs SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
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
            f"INSERT INTO shop_purchase_logs ({', '.join(cols)}) VALUES ({placeholders})",
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
        cursor.execute(f"DELETE FROM shop_purchase_logs WHERE {cursor.description[0][0]}=%s", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM shop_purchase_logs")
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
        query = f"SELECT * FROM shop_purchase_logs WHERE {col} = %s order by date_and_time desc"
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
    close_button = ctk.CTkButton(button_frame, text="Close", command=shop_logs_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    add_button.grid(row=0, column=1, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    shop_logs_win.mainloop()

def open_food_data():
    food_win = ctk.CTk()
    food_win.title("Food Stocks Viewer")
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

    def fetch_data(query="SELECT * FROM food_dir"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM food_dir"):
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
        cursor.execute(f"SELECT * FROM food_dir WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE food_dir SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
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
            f"INSERT INTO food_dir ({', '.join(cols)}) VALUES ({placeholders})",
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
        cursor.execute(f"DELETE FROM food_dir WHERE {cursor.description[0][0]}=%s", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM food_dir")
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
        query = f"SELECT * FROM food_dir WHERE {col} = %s"
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

def open_shop_stocks_data():
    shop_stock_win = ctk.CTk()
    shop_stock_win.title("Shop Stocks Editor")
    screen_width = shop_stock_win.winfo_screenwidth()
    screen_height = shop_stock_win.winfo_screenheight()
    shop_stock_win.geometry(f"{screen_width}x{screen_height}+0+0")

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
        shop_stock_win.destroy()
        return

    cursor = conn.cursor()

    header_font = ctk.CTkFont(size=14, weight="bold")
    cell_font = ctk.CTkFont(size=13)

    def on_enter(event, text):
        status_label.configure(text=text)

    def on_leave(event):
        status_label.configure(text="")

    scrollable_frame = ctk.CTkScrollableFrame(shop_stock_win, width=980, height=450)
    scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

    button_frame = ctk.CTkFrame(shop_stock_win)
    button_frame.pack(pady=5)

    input_frame = ctk.CTkFrame(shop_stock_win)
    entries = []
    mode = None
    filter_active = False

    # --- FILTER FRAME AND WIDGETS ---
    filter_frame = ctk.CTkFrame(shop_stock_win)
    filter_col_dropdown = None
    filter_val_dropdown = None
    confirm_filter_btn = None

    def fetch_data(query="SELECT * FROM shop_stock"):
        cursor.execute(query)
        return cursor.fetchall(), [desc[0] for desc in cursor.description]

    def display_table(query="SELECT * FROM shop_stock"):
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
        cursor.execute(f"SELECT * FROM shop_stock WHERE {cursor.description[0][0]}=%s", (record_id,))
        current = cursor.fetchone()
        if not current:
            return
        updated = [vals[i] if vals[i] else str(current[i]) for i in range(len(cursor.description))]
        set_clause = ", ".join(f"{cursor.description[i][0]}=%s" for i in range(1, len(updated)))
        params = updated[1:] + [record_id]
        cursor.execute(f"UPDATE shop_stock SET {set_clause} WHERE {cursor.description[0][0]}=%s", params)
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
            f"INSERT INTO shop_stock ({', '.join(cols)}) VALUES ({placeholders})",
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
        cursor.execute(f"DELETE FROM shop_stock WHERE {cursor.description[0][0]}=%s", (record_id,))
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
                cursor.execute(f"SELECT DISTINCT {choice} FROM shop_stock")
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
        query = f"SELECT * FROM shop_stock WHERE {col} = %s"
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
    close_button = ctk.CTkButton(button_frame, text="Close", command=shop_stock_win.destroy)
    status_label = ctk.CTkLabel(button_frame, text="", text_color=("#2B2B2B","#BCBCBC"), width=275, anchor="w")

    edit_button.grid(row=0, column=0, padx=8)
    add_button.grid(row=0, column=1, padx=8)
    delete_button.grid(row=0, column=2, padx=8)
    filter_button.grid(row=0, column=3, padx=8)
    close_button.grid(row=0, column=4, padx=8)
    status_label.grid(row=0, column=5, padx=(20, 10))

    display_table()

    shop_stock_win.mainloop()

def open_add_ticket():
    # Connect to the database
    conn = msc.connect(
        host="localhost",
        user=logged_in_username,
        password=logged_in_password,
        database="pawcache",
        use_pure=True
    )
    cursor = conn.cursor()

    ticket_win = ctk.CTk()
    ticket_win.title("Add Ticket")
    ticket_win.geometry("600x500+400+150")

    from datetime import datetime
    font_main = ("Arial", 18)

    top_frame = ctk.CTkFrame(ticket_win)
    top_frame.pack(fill="x", pady=10, padx=10)

    left_label = ctk.CTkLabel(top_frame, text=f"User: {logged_in_username} - Adding Ticket", font=font_main)
    left_label.pack(side="left")

    def back_to_home():
        ticket_win.destroy()

    close_btn = ctk.CTkButton(top_frame, text="Close", command=back_to_home, font=font_main)
    close_btn.pack(side="right", padx=10)

    center_frame = ctk.CTkFrame(ticket_win)
    center_frame.pack(pady=20, padx=40, fill="both", expand=True)

    # Retrieve defaults
    cursor.execute("SELECT singleticketprice, ticketno FROM visitors ORDER BY ticketno DESC LIMIT 1")
    last_row = cursor.fetchone()
    default_price = last_row[0] if last_row else 35
    next_ticketno = int(last_row[1]) + 1 if last_row else 1

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

    ent_price = add_input_row("Single Ticket Price", default_value=default_price)
    ent_group = add_input_row("Visitors in Group")
    ent_extra = add_input_row("Extra Fee", default_value=0)

    row_total = ctk.CTkFrame(center_frame)
    row_total.pack(fill="x", pady=4)
    lbl_total = ctk.CTkLabel(row_total, text="Total Amount:", width=200, anchor="w", font=font_main)
    lbl_total.pack(side="left")
    ent_total = ctk.CTkEntry(row_total, state="readonly", font=font_main)
    ent_total.pack(side="left", fill="x", expand=True)

    def update_total(*args):
        try:
            price = int(ent_price.get())
            group = int(ent_group.get())
            extra = int(ent_extra.get())
            total = price * group + extra
        except:
            total = 0
        ent_total.configure(state="normal")
        ent_total.delete(0, "end")
        ent_total.insert(0, str(total))
        ent_total.configure(state="readonly")

    ent_price.bind("<KeyRelease>", update_total)
    ent_group.bind("<KeyRelease>", update_total)
    ent_extra.bind("<KeyRelease>", update_total)

    ent_donation = add_input_row("Donation", default_value=0)
    ent_phone = add_input_row("Phone Number")

    row_pay = ctk.CTkFrame(center_frame)
    row_pay.pack(fill="x", pady=4)
    lbl_pay = ctk.CTkLabel(row_pay, text="Payment Mode:", width=200, anchor="w", font=font_main)
    lbl_pay.pack(side="left")
    pay_mode = ctk.CTkOptionMenu(row_pay, values=["Web", "Cash", "UPI", "Card", "Other"], font=font_main)
    pay_mode.pack(side="left", fill="x", expand=True)
    pay_mode.set("Cash")

    cursor.execute("SELECT DISTINCT got_to_know_by FROM visitors")
    sources = sorted({row[0] for row in cursor.fetchall() if row[0]})
    row_src = ctk.CTkFrame(center_frame)
    row_src.pack(fill="x", pady=4)
    lbl_src = ctk.CTkLabel(row_src, text="Got to Know By:", width=200, anchor="w", font=font_main)
    lbl_src.pack(side="left")
    source_box = ctk.CTkComboBox(row_src, values=sources, font=font_main)
    source_box.pack(side="left", fill="x", expand=True)
    source_box.set("")

    row_ticketno = ctk.CTkFrame(center_frame)
    row_ticketno.pack(fill="x", pady=4)
    lbl_ticketno = ctk.CTkLabel(row_ticketno, text="Ticket No:", width=200, anchor="w", font=font_main)
    lbl_ticketno.pack(side="left")
    ent_ticketno = ctk.CTkEntry(row_ticketno, state="readonly", font=font_main)
    ent_ticketno.pack(side="left", fill="x", expand=True)
    ent_ticketno.configure(state="normal")
    ent_ticketno.insert(0, str(next_ticketno).zfill(8))
    ent_ticketno.configure(state="readonly")

    msg_label = ctk.CTkLabel(center_frame, text="", font=font_main)
    msg_label.pack()

    def reset_fields():
        ent_price.delete(0, 'end')
        ent_price.insert(0, str(default_price))
        ent_group.delete(0, 'end')
        ent_extra.delete(0, 'end')
        ent_extra.insert(0, '0')
        ent_total.configure(state="normal")
        ent_total.delete(0, 'end')
        ent_total.configure(state="readonly")
        ent_donation.delete(0, 'end')
        ent_donation.insert(0, '0')
        ent_phone.delete(0, 'end')
        pay_mode.set("Cash")
        source_box.set("")
        btn.configure(text="Add Ticket")
        msg_label.configure(text="")


    def handle_add_confirm():
        if btn.cget("text") == "Add Ticket":
            if not ent_group.get().strip():
                msg_label.configure(text="Enter Visitors in Group", text_color="orange")
                return
            for name, entry in [("Ticket Price", ent_price), ("Visitors", ent_group), ("Extra Fee", ent_extra), ("Donation", ent_donation), ("Phone Number", ent_phone)]:
                if entry.get().strip() and not entry.get().strip().isdigit():
                    msg_label.configure(text=f"{name} only supports integer input", text_color="red")
                    return
            msg_label.configure(text="", text_color="green")
            btn.configure(text="CONFIRM TICKET")
        else:
            source = source_box.get().strip()
            if source == "":
                source = None
            cursor.execute("INSERT INTO visitors (singleticketprice, visitorsingroup, extra_fee, ticketamount, donation, phoneno, paymentmode, got_to_know_by) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (int(ent_price.get()), int(ent_group.get()), int(ent_extra.get()), int(ent_total.get()), int(ent_donation.get()),
                            int(ent_phone.get()) if ent_phone.get().isdigit() else None, pay_mode.get(), source))
            conn.commit()
            msg_label.configure(text="Visitor Ticket successfully added", text_color="green")
            ticket_win.after(2000, lambda: msg_label.configure(text=""))
            # Refresh ticketno
            cursor.execute("SELECT ticketno FROM visitors ORDER BY ticketno DESC LIMIT 1")
            latest_ticket = cursor.fetchone()
            if latest_ticket:
                next_ticketno = int(latest_ticket[0]) + 1
                ent_ticketno.configure(state="normal")
                ent_ticketno.delete(0, 'end')
                ent_ticketno.insert(0, str(next_ticketno).zfill(8))
                ent_ticketno.configure(state="readonly")

            # Refresh "Got to Know By"
            cursor.execute("SELECT DISTINCT got_to_know_by FROM visitors")
            sources = sorted({row[0] for row in cursor.fetchall() if row[0]})
            source_box.configure(values=sources)
            msg_label.configure(text="Visitor Ticket successfully added", text_color="green")
            ticket_win.after(2000, lambda: msg_label.configure(text=""))
            reset_fields()

    btn = ctk.CTkButton(center_frame, text="Add Ticket", font=font_main, command=handle_add_confirm)
    btn.pack(pady=10)
    ticket_win.mainloop()

def open_add_staff():
    import mysql.connector as msc
    from datetime import date
    conn = msc.connect(
        host="localhost",
        user=logged_in_username,
        password=logged_in_password,
        database="pawcache",
        use_pure=True
    )
    cursor = conn.cursor()

    win = ctk.CTk()
    win.title("Add Staff")
    win.geometry("600x600+400+100")

    font_main = ("Arial", 18)

    def add_input_row(parent, label_text, default_value="", readonly=False):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", pady=5)
        lbl = ctk.CTkLabel(row, text=label_text + ":", width=160, anchor="w", font=font_main)
        lbl.pack(side="left")
        ent = ctk.CTkEntry(row, font=font_main)
        ent.insert(0, str(default_value))
        if readonly:
            ent.configure(state="readonly")
        ent.pack(side="left", fill="x", expand=True)
        return ent

    center_frame = ctk.CTkFrame(win)
    center_frame.pack(pady=20, padx=40, fill="both", expand=True)

    ent_name = add_input_row(center_frame, "Name")
    ent_staffid = add_input_row(center_frame, "Staff ID")
    ent_password = add_input_row(center_frame, "Password")

    # Job dropdown (editable)
    row_job = ctk.CTkFrame(center_frame)
    row_job.pack(fill="x", pady=5)
    ctk.CTkLabel(row_job, text="Job:", width=160, anchor="w", font=font_main).pack(side="left")
    cursor.execute("SELECT DISTINCT job FROM staff_dat")
    job_list = sorted([row[0] for row in cursor.fetchall() if row[0]])
    job_dropdown = ctk.CTkComboBox(row_job, values=job_list, font=font_main, width=200)
    job_dropdown.pack(side="left", fill="x", expand=True)
    job_dropdown.set("")

    # Job Type dropdown (fixed values)
    row_jobtype = ctk.CTkFrame(center_frame)
    row_jobtype.pack(fill="x", pady=5)
    ctk.CTkLabel(row_jobtype, text="Job Type:", width=160, anchor="w", font=font_main).pack(side="left")
    jobtype_dropdown = ctk.CTkComboBox(row_jobtype, values=["critterscribe_animal", "critterscribe_shop", "manager", "admin"], font=font_main, width=200)
    jobtype_dropdown.pack(side="left", fill="x", expand=True)
    jobtype_dropdown.set("")
    jobtype_dropdown.configure(state="readonly")

    ent_block = add_input_row(center_frame, "Block", default_value="NA")

    # Workdays checkboxes
    row_days = ctk.CTkFrame(center_frame)
    row_days.pack(fill="x", pady=5)
    ctk.CTkLabel(row_days, text="Workdays:", width=160, anchor="w", font=font_main).pack(side="left")
    day_vars = {}
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        var = ctk.BooleanVar()
        chk = ctk.CTkCheckBox(row_days, text=day, variable=var, font=("Arial", 14))
        chk.pack(side="left")
        day_vars[day] = var

    ent_shift = add_input_row(center_frame, "Work Shift")
    ent_salary = add_input_row(center_frame, "Salary")

    today_str = str(date.today())
    ent_joindate = add_input_row(center_frame, "Join Date", default_value=today_str)

    msg_label = ctk.CTkLabel(center_frame, text="", font=font_main)
    msg_label.pack(pady=10)

    def reset_fields():
        for widget in [ent_name, ent_staffid, ent_password, ent_block, ent_shift, ent_salary, ent_joindate]:
            widget.delete(0, 'end')
        job_dropdown.set("")
        jobtype_dropdown.set("")
        ent_block.insert(0, "NA")
        ent_joindate.insert(0, today_str)
        for var in day_vars.values():
            var.set(False)
        btn.configure(text="Add Staff")
        msg_label.configure(text="")

    def handle_confirm():
        if btn.cget("text") == "Add Staff":
            # Switch to confirm mode
            btn.configure(text="CONFIRM STAFF")
            msg_label.configure(text="", text_color="green")
        else:
            name = ent_name.get().strip()
            staffid = ent_staffid.get().strip()
            password = ent_password.get().strip()
            job = job_dropdown.get().strip()
            jobtype = jobtype_dropdown.get().strip()
            block = ent_block.get().strip()
            workdays = ",".join([day for day, var in day_vars.items() if var.get()])
            shift = ent_shift.get().strip()
            salary = ent_salary.get().strip()
            joindate = ent_joindate.get().strip()

            if not (name and staffid and job and jobtype and shift and salary and joindate):
                msg_label.configure(text="All fields must be filled", text_color="orange")
                return

            try:
                cursor.execute("INSERT INTO staff_dat (name, staffid, job, block, workdays, workshift, salary, joindate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (name, staffid, job, block, workdays, shift, salary, joindate))
                conn.commit()

                if jobtype == "critterscribe_animal":
                    cursor.execute(f"CREATE USER '{staffid}'@'%' IDENTIFIED BY '{password}'")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON pawcache.animal_dat TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON pawcache.food_dir TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT, UPDATE ON pawcache.notes_for_{staffid} TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT, INSERT ON pawcache.requests TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT ON pawcache.staff_dat TO '{staffid}'@'%'")

                elif jobtype == "critterscribe_shop":
                    cursor.execute(f"CREATE USER '{staffid}'@'%' IDENTIFIED BY '{password}'")
                    cursor.execute(f"GRANT SELECT, UPDATE ON pawcache.notes_for_{staffid} TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT INSERT ON pawcache.requests TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON pawcache.shop_purchase_logs TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT, INSERT, UPDATE, DELETE ON pawcache.shop_stock TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT SELECT ON pawcache.staff_dat TO '{staffid}'@'%'")

                elif jobtype == "manager":
                    cursor.execute(f"CREATE USER '{staffid}'@'%' IDENTIFIED BY '{password}'")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON pawcache.* TO '{staffid}'@'%'")

                elif jobtype == "admin":
                    cursor.execute(f"CREATE USER '{staffid}'@'%' IDENTIFIED BY '{password}'")
                    cursor.execute(f"GRANT CREATE USER ON *.* TO '{staffid}'@'%'")
                    cursor.execute(f"GRANT ALL PRIVILEGES ON pawcache.* TO '{staffid}'@'%' WITH GRANT OPTION")
                    
                conn.commit()
                msg_label.configure(text="Staff successfully added", text_color="green")
                win.after(2000, reset_fields)

            except Exception as e:
                msg_label.configure(text="Error: " + str(e), text_color="red")

    btn = ctk.CTkButton(center_frame, text="Add Staff", font=font_main, command=handle_confirm)
    btn.pack(pady=10)

    win.mainloop()

def open_main_app():
    import mysql.connector
    global logged_in_username, logged_in_password, logged_in_job

    new_win = ctk.CTk()
    new_win.title("ZooDash Homepage")
    screen_width = new_win.winfo_screenwidth()
    screen_height = new_win.winfo_screenheight()
    new_win.geometry(f"{screen_width}x{screen_height}+0+0")

    underline = ctk.CTkFrame(new_win, height=4, fg_color=("#000083", "#9BB6FF"))
    underline.place(relx=0.2, rely=0.16, relwidth=0.6)
    underline2 = ctk.CTkFrame(new_win, height=4, fg_color=("#10861A", "#97FFB5"))
    underline2.place(relx=0.24, rely=0.18, relwidth=0.52)

    heading_label = ctk.CTkLabel(new_win, text="ZooDash Homepage", font=ctk.CTkFont(size=30, weight="bold"))
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

    def noaccess():
        show_temp_message("No Access")
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

    # === 6x2 Button Grid Layout ===
    button_texts = [
        "Add Ticket", "Manage Staff",
        "View Animal\nData", "View Food\nStocks",
        "View Requests", "Visitor Records",
        "Add/Check Reviews", "Analytic Plots",
        "Transaction\nRecords", "Add Staff",
        "Shop Purchase logs","View Shop Stocks"]
    button_refs = []  # To store the created button objects if needed
    # Loop to place buttons in 5 rows x 2 cols
    for i in range(6):  # rows
        for j in range(2):  # cols
            index = i * 2 + j
            text = button_texts[index]

            # Assign correct function to the two working buttons
            if index == 0:
                command = open_add_ticket
            elif index == 1:
                command = open_staff_data
            elif index == 2:
                command = open_animal_data
            elif index == 3:
                command = open_food_data
            elif index == 4:
                command = open_requests_data
            elif index == 5:
                command = open_visitor_data
            elif index == 6:
                command = open_reviews_data
            elif index == 8:
                command = open_transaction_data
            elif index == 9 and logged_in_job == "Manager":
                command = noaccess
            elif index == 9 and logged_in_job != "Manager":
                command = open_add_staff
            elif index == 10:
                command = open_shop_purchase_logs_data
            elif index == 11:
                command = open_shop_stocks_data
            else:
                command = None  # Placeholder for now

            btn = ctk.CTkButton(
                new_win,
                text=text,
                width=200,
                height=72,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=command
            )
            btn.place(relx=0.1 + j * 0.22, rely=0.28 + i * 0.115, anchor="w")
            if logged_in_job != "Admin" and index == 9:
                btn.configure(fg_color="#343A3E", hover_color="#505152", text_color="white" )
            button_refs.append(btn)

    def save_note():
        updated_text = note_textbox.get("1.0", "end").strip()
        try:
            conn = msc.connect(
                host="localhost",
                user=logged_in_username,
                password=logged_in_password,
                database="pawcache",
                use_pure=True
            )
            cur = conn.cursor()
            cur.execute("UPDATE notes SET note = %s WHERE userid = %s", (updated_text, logged_in_username))
            conn.commit()
            cur.close()
            conn.close()
            show_temp_message("Notes saved successfully.")
        except msc.Error as err:
            note_textbox.delete("1.0", "end")
            note_textbox.insert("1.0", f"Error saving note: {err}")

    def load_saved_notes():
        try:
            conn = msc.connect(
                host="localhost",
                user=logged_in_username,
                password=logged_in_password,
                database="pawcache",
                use_pure=True
            )
            cur = conn.cursor()
            cur.execute("SELECT note FROM notes WHERE userid = %s", (logged_in_username,))
            result = cur.fetchone()
            if result:
                note_textbox.delete("1.0", "end")
                note_textbox.insert("1.0", result[0])
                show_temp_message("Notes retrieved.")
            cur.close()
            conn.close()
        except msc.Error as err:
            note_textbox.delete("1.0", "end")
            note_textbox.insert("1.0", f"Error loading note: {err}")

    def clear_note():
        note_textbox.delete("1.0", "end")

    # === Textbox on Right Side ===
    note_textbox = ctk.CTkTextbox(new_win, width=500, height=350, font=ctk.CTkFont(size=16))
    note_textbox.place(relx=0.75, rely=0.52, anchor="center")

    # === Buttons under Textbox ===
    clear_button = ctk.CTkButton(new_win, text="Clear Note", width=150, command=clear_note)
    clear_button.place(relx=0.60, rely=0.82, anchor="center")

    save_button = ctk.CTkButton(new_win, text="Save Note", width=150, command=save_note)
    save_button.place(relx=0.75, rely=0.82, anchor="center")

    load_button = ctk.CTkButton(new_win, text="Load Saved Notes", width=150, command=load_saved_notes)
    load_button.place(relx=0.90, rely=0.82, anchor="center")
    note_textbox.insert("1.0", "Welcome to ZooDash app!\nPress 'Load Saved Notes' to see your existing notes.")

    # === Temporary Message Label (initially empty) ===
    def show_temp_message(text):
        status_label.configure(text=text)
        status_label.after(2000, lambda: status_label.configure(text=""))  # Clear after 2 seconds

    status_label = ctk.CTkLabel(new_win, text="", text_color="green", font=ctk.CTkFont(size=14))
    status_label.place(relx=0.75, rely=0.88, anchor="center")

    new_win.mainloop()

def launch_login():
    global root, username_entry, password_entry, message_label
    root = ctk.CTk()     # main first login screen
    root.title("Login")
    root.geometry("400x360")

    login_label = ctk.CTkLabel(root, text="Login to ZooDash", font=ctk.CTkFont(size=20, weight="bold"))     # top label
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