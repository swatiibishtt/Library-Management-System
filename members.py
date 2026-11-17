import tkinter as tk
from tkinter import messagebox
from database import connect_database


def add_member():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if name == "" or email == "" or phone == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        INSERT INTO members (name, email, phone)
        VALUES (%s, %s, %s)
    """

    values = (name, email, phone)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Member added successfully!"
    )

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def open_add_member_window():

    global name_entry
    global email_entry
    global phone_entry

    window = tk.Toplevel()

    window.title("Add Member")
    window.geometry("500x400")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Add New Member",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    tk.Label(
        window,
        text="Member Name"
    ).pack()

    name_entry = tk.Entry(
        window,
        width=40
    )

    name_entry.pack(pady=5)

    tk.Label(
        window,
        text="Email"
    ).pack()

    email_entry = tk.Entry(
        window,
        width=40
    )

    email_entry.pack(pady=5)

    tk.Label(
        window,
        text="Phone"
    ).pack()

    phone_entry = tk.Entry(
        window,
        width=40
    )

    phone_entry.pack(pady=5)

    tk.Button(
        window,
        text="Add Member",
        command=add_member
    ).pack(pady=20)

    #view
def view_members():

    global tree
    global window

    window = tk.Toplevel()

    window.title("Member Management")
    window.geometry("900x550")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Member Management",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    from tkinter import ttk

    columns = (
        "ID",
        "Name",
        "Email",
        "Phone"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")

    tree.column("ID", width=60)
    tree.column("Name", width=200)
    tree.column("Email", width=250)
    tree.column("Phone", width=150)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM members")

    members = cursor.fetchall()

    cursor.close()
    connection.close()

    for member in members:

        tree.insert(
            "",
            tk.END,
            values=member
        )

    update_button = tk.Button(
        window,
        text="Update Selected Member",
        command=update_member
    )

    update_button.pack(pady=5)

    delete_button = tk.Button(
        window,
        text="Delete Selected Member",
        command=delete_member
    )

    delete_button.pack(pady=5)

    #update
def update_member():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a member to update."
        )
        return

    member = tree.item(selected[0])["values"]

    member_id = member[0]

    update_window = tk.Toplevel()

    update_window.title("Update Member")
    update_window.geometry("500x400")
    update_window.configure(bg="#2D68C4")
    tk.Label(
        update_window,
        text="Update Member",
        font=("Arial", 20)
    ).pack(pady=20)

    tk.Label(
        update_window,
        text="Name"
    ).pack()

    name_update = tk.Entry(
        update_window,
        width=40
    )

    name_update.pack(pady=5)

    name_update.insert(
        0,
        member[1]
    )

    tk.Label(
        update_window,
        text="Email"
    ).pack()

    email_update = tk.Entry(
        update_window,
        width=40
    )

    email_update.pack(pady=5)

    email_update.insert(
        0,
        member[2]
    )

    tk.Label(
        update_window,
        text="Phone"
    ).pack()

    phone_update = tk.Entry(
        update_window,
        width=40
    )

    phone_update.pack(pady=5)

    phone_update.insert(
        0,
        member[3]
    )

    def save_update():

        name = name_update.get()
        email = email_update.get()
        phone = phone_update.get()

        if name == "" or email == "" or phone == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        connection = connect_database()
        cursor = connection.cursor()

        query = """
            UPDATE members
            SET name = %s,
                email = %s,
                phone = %s
            WHERE member_id = %s
        """

        values = (
            name,
            email,
            phone,
            member_id
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Member updated successfully!"
        )

        update_window.destroy()

        window.destroy()

        view_members()

    tk.Button(
        update_window,
        text="Save Changes",
        command=save_update
    ).pack(pady=20)

    #delete
def delete_member():

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a member to delete."
        )
        return

    member = tree.item(selected[0])["values"]

    member_id = member[0]

    confirmation = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this member?"
    )

    if not confirmation:
        return

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        DELETE FROM members
        WHERE member_id = %s
    """

    cursor.execute(
        query,
        (member_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Member deleted successfully!"
    )

    window.destroy()

    view_members()
#search 
def search_members():

    search_window = tk.Toplevel()

    search_window.title("Search Members")
    search_window.geometry("900x550")
    search_window.configure(bg="#2D68C4")

    heading = tk.Label(
        search_window,
        text="Search Members",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    search_frame = tk.Frame(search_window)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search:"
    ).pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(
        search_frame,
        width=40
    )

    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=lambda: perform_member_search()
    )

    search_button.pack(side=tk.LEFT, padx=5)

    from tkinter import ttk

    columns = (
        "ID",
        "Name",
        "Email",
        "Phone"
    )

    search_tree = ttk.Treeview(
        search_window,
        columns=columns,
        show="headings"
    )

    search_tree.heading("ID", text="ID")
    search_tree.heading("Name", text="Name")
    search_tree.heading("Email", text="Email")
    search_tree.heading("Phone", text="Phone")

    search_tree.column("ID", width=60)
    search_tree.column("Name", width=200)
    search_tree.column("Email", width=250)
    search_tree.column("Phone", width=150)

    search_tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    def perform_member_search():

        search_text = search_entry.get()

        for item in search_tree.get_children():
            search_tree.delete(item)

        connection = connect_database()
        cursor = connection.cursor()

        query = """
            SELECT *
            FROM members
            WHERE name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
        """

        search_value = "%" + search_text + "%"

        cursor.execute(
            query,
            (
                search_value,
                search_value,
                search_value
            )
        )

        members = cursor.fetchall()

        cursor.close()
        connection.close()

        for member in members:

            search_tree.insert(
                "",
                tk.END,
                values=member
            )