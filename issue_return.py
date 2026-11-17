import tkinter as tk
from tkinter import messagebox
from database import connect_database


def issue_book():

    book_id = book_id_entry.get()
    member_id = member_id_entry.get()

    if book_id == "" or member_id == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Book ID and Member ID."
        )
        return

    try:
        book_id = int(book_id)
        member_id = int(member_id)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Book ID and Member ID must be numbers."
        )
        return

    connection = connect_database()
    cursor = connection.cursor()

    # Check whether book exists and has available quantity
    query = """
        SELECT quantity
        FROM books
        WHERE book_id = %s
    """

    cursor.execute(
        query,
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        messagebox.showerror(
            "Error",
            "Book not found."
        )

        cursor.close()
        connection.close()
        return

    if book[0] <= 0:
        messagebox.showerror(
            "Error",
            "Book is not available."
        )

        cursor.close()
        connection.close()
        return

    # Check whether member exists
    query = """
        SELECT member_id
        FROM members
        WHERE member_id = %s
    """

    cursor.execute(
        query,
        (member_id,)
    )

    member = cursor.fetchone()

    if member is None:
        messagebox.showerror(
            "Error",
            "Member not found."
        )

        cursor.close()
        connection.close()
        return

    # Add issue record
    query = """
        INSERT INTO issue_return
        (book_id, member_id, issue_date)
        VALUES (%s, %s, CURDATE())
    """

    cursor.execute(
        query,
        (book_id, member_id)
    )

    # Decrease book quantity
    query = """
        UPDATE books
        SET quantity = quantity - 1
        WHERE book_id = %s
    """

    cursor.execute(
        query,
        (book_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Book issued successfully!"
    )

    book_id_entry.delete(0, tk.END)
    member_id_entry.delete(0, tk.END)


def open_issue_book_window():

    global book_id_entry
    global member_id_entry

    window = tk.Toplevel()

    window.title("Issue Book")
    window.geometry("500x350")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Issue Book",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    tk.Label(
        window,
        text="Book ID"
    ).pack()

    book_id_entry = tk.Entry(
        window,
        width=30
    )

    book_id_entry.pack(pady=5)

    tk.Label(
        window,
        text="Member ID"
    ).pack()

    member_id_entry = tk.Entry(
        window,
        width=30
    )

    member_id_entry.pack(pady=5)

    tk.Button(
        window,
        text="Issue Book",
        command=issue_book
    ).pack(pady=20)

    #return
def return_book():

    issue_id = issue_id_entry.get()

    if issue_id == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Issue ID."
        )
        return

    try:
        issue_id = int(issue_id)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Issue ID must be a number."
        )
        return

    connection = connect_database()
    cursor = connection.cursor()

    # Find the issued book
    query = """
        SELECT book_id, return_date
        FROM issue_return
        WHERE issue_id = %s
    """

    cursor.execute(
        query,
        (issue_id,)
    )

    issue = cursor.fetchone()

    if issue is None:
        messagebox.showerror(
            "Error",
            "Issue record not found."
        )

        cursor.close()
        connection.close()
        return

    book_id = issue[0]
    return_date = issue[1]

    if return_date is not None:
        messagebox.showwarning(
            "Warning",
            "This book has already been returned."
        )

        cursor.close()
        connection.close()
        return

    # Set return date
    query = """
        UPDATE issue_return
        SET return_date = CURDATE()
        WHERE issue_id = %s
    """

    cursor.execute(
        query,
        (issue_id,)
    )

    # Increase book quantity
    query = """
        UPDATE books
        SET quantity = quantity + 1
        WHERE book_id = %s
    """

    cursor.execute(
        query,
        (book_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Book returned successfully!"
    )

    issue_id_entry.delete(
        0,
        tk.END
    )


def open_return_book_window():

    global issue_id_entry

    window = tk.Toplevel()

    window.title("Return Book")
    window.geometry("500x300")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Return Book",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    tk.Label(
        window,
        text="Issue ID"
    ).pack()

    issue_id_entry = tk.Entry(
        window,
        width=30
    )

    issue_id_entry.pack(pady=10)

    tk.Button(
        window,
        text="Return Book",
        command=return_book
    ).pack(pady=20)

#view issue records
def view_issue_records():

    global window

    window = tk.Toplevel()

    window.title("Issue / Return Records")
    window.geometry("1000x550")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Issue / Return Records",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    from tkinter import ttk

    columns = (
    "Issue ID",
    "Book",
    "Member",
    "Issue Date",
    "Return Date"
)
    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    tree.heading("Issue ID", text="Issue ID")
    tree.heading("Book", text="Book")
    tree.heading("Member", text="Member")
    tree.heading("Issue Date", text="Issue Date")
    tree.heading("Return Date", text="Return Date")

    tree.column("Issue ID", width=100)
    tree.column("Book", width=250)
    tree.column("Member", width=200)
    tree.column("Issue Date", width=180)
    tree.column("Return Date", width=180)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
        issue_return.issue_id,
        books.title,
        members.name,
        issue_return.issue_date,
        issue_return.return_date
        FROM issue_return
        JOIN books
        ON issue_return.book_id = books.book_id
        JOIN members
        ON issue_return.member_id = members.member_id
"""

    cursor.execute(query)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    for record in records:

        tree.insert(
            "",
            tk.END,
            values=record
        )