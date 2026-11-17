import tkinter as tk
from tkinter import messagebox


from books import (
    open_add_book_window,
    view_books,
    search_books
)

from members import (
    open_add_member_window,
    view_members,
    search_members
)

from issue_return import (
    open_issue_book_window,
    open_return_book_window,
    view_issue_records
)

from database import connect_database


def get_dashboard_data():

    connection = connect_database()
    cursor = connection.cursor()

    # Total books
    cursor.execute(
        "SELECT COUNT(*) FROM books"
    )

    total_books = cursor.fetchone()[0]

    # Available books
    cursor.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM books"
    )

    available_books = cursor.fetchone()[0]

    # Total members
    cursor.execute(
        "SELECT COUNT(*) FROM members"
    )

    total_members = cursor.fetchone()[0]

    # Issued books
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM issue_return
        WHERE return_date IS NULL
        """
    )

    issued_books = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return (
        total_books,
        available_books,
        total_members,
        issued_books
    )


def update_dashboard():

    total_books, available_books, total_members, issued_books = (
        get_dashboard_data()
    )

    total_books_label.config(
        text=str(total_books)
    )

    available_books_label.config(
        text=str(available_books)
    )

    total_members_label.config(
        text=str(total_members)
    )

    issued_books_label.config(
        text=str(issued_books)
    )


# Main Window

window = tk.Tk()

window.title(
    "Library Management System"
)

window.geometry(
    "1000x700"
)

window.configure(bg="#2D68C4")
# Heading

heading = tk.Label(
    window,
    text="Library Management System",
    font=("Arial", 28)
)

heading.pack(pady=25)


subtitle = tk.Label(
    window,
    text="Library Dashboard",
    font=("Arial", 16)
)

subtitle.pack()


# Dashboard frame

dashboard_frame = tk.Frame(window)

dashboard_frame.pack(pady=30)


# Total Books

total_books_frame = tk.Frame(
    dashboard_frame,
    width=200,
    height=120,
    relief=tk.RIDGE,
    borderwidth=2
)

total_books_frame.grid(
    row=0,
    column=0,
    padx=15
)

tk.Label(
    total_books_frame,
    text="Total Books",
    font=("Arial", 14)
).pack(pady=10)

total_books_label = tk.Label(
    total_books_frame,
    text="0",
    font=("Arial", 24)
)

total_books_label.pack(pady=10)


# Available Books

available_books_frame = tk.Frame(
    dashboard_frame,
    width=200,
    height=120,
    relief=tk.RIDGE,
    borderwidth=2
)

available_books_frame.grid(
    row=0,
    column=1,
    padx=15
)

tk.Label(
    available_books_frame,
    text="Available Books",
    font=("Arial", 14)
).pack(pady=10)

available_books_label = tk.Label(
    available_books_frame,
    text="0",
    font=("Arial", 24)
)

available_books_label.pack(pady=10)


# Total Members

total_members_frame = tk.Frame(
    dashboard_frame,
    width=200,
    height=120,
    relief=tk.RIDGE,
    borderwidth=2
)

total_members_frame.grid(
    row=0,
    column=2,
    padx=15
)

tk.Label(
    total_members_frame,
    text="Total Members",
    font=("Arial", 14)
).pack(pady=10)

total_members_label = tk.Label(
    total_members_frame,
    text="0",
    font=("Arial", 24)
)

total_members_label.pack(pady=10)


# Issued Books

issued_books_frame = tk.Frame(
    dashboard_frame,
    width=200,
    height=120,
    relief=tk.RIDGE,
    borderwidth=2
)

issued_books_frame.grid(
    row=0,
    column=3,
    padx=15
)

tk.Label(
    issued_books_frame,
    text="Issued Books",
    font=("Arial", 14)
).pack(pady=10)

issued_books_label = tk.Label(
    issued_books_frame,
    text="0",
    font=("Arial", 24)
)

issued_books_label.pack(pady=10)


# Buttons section

buttons_frame = tk.Frame(window)

buttons_frame.pack(pady=20)



# Book buttons

tk.Label(
    buttons_frame,
    text="Book Management",
    font=("Arial", 16)
).grid(
    row=0,
    column=0,
    columnspan=3,
    pady=10
)


tk.Button(
    buttons_frame,
    text="Add Book",
    width=20,
    command=open_add_book_window
).grid(
    row=1,
    column=0,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="View Books",
    width=20,
    command=view_books
).grid(
    row=1,
    column=1,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="Search Books",
    width=20,
    command=search_books
).grid(
    row=1,
    column=2,
    padx=10,
    pady=5
)


# Member buttons

tk.Label(
    buttons_frame,
    text="Member Management",
    font=("Arial", 16)
).grid(
    row=2,
    column=0,
    columnspan=3,
    pady=10
)


tk.Button(
    buttons_frame,
    text="Add Member",
    width=20,
    command=open_add_member_window
).grid(
    row=3,
    column=0,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="View Members",
    width=20,
    command=view_members
).grid(
    row=3,
    column=1,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="Search Members",
    width=20,
    command=search_members
).grid(
    row=3,
    column=2,
    padx=10,
    pady=5
)


# Transaction buttons

tk.Label(
    buttons_frame,
    text="Transactions",
    font=("Arial", 16)
).grid(
    row=4,
    column=0,
    columnspan=3,
    pady=10
)


tk.Button(
    buttons_frame,
    text="Issue Book",
    width=20,
    command=open_issue_book_window
).grid(
    row=5,
    column=0,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="Return Book",
    width=20,
    command=open_return_book_window
).grid(
    row=5,
    column=1,
    padx=10,
    pady=5
)


tk.Button(
    buttons_frame,
    text="Issue Records",
    width=20,
    command=view_issue_records
).grid(
    row=5,
    column=2,
    padx=10,
    pady=5
)


# Update dashboard initially


def logout():

    confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if confirm:

        window.destroy()

        import login

logout_button = tk.Button(
    window,
    text="Logout",
    width=20,
    command=logout
)

logout_button.pack(pady=10)

refresh_button = tk.Button(
    window,
    text="Refresh Dashboard",
    width=20,
    command=update_dashboard
)

refresh_button.pack(pady=5)

footer = tk.Label(
    window,
    text="Library Management System | Python + Tkinter + MySQL",
    font=("Arial", 10)
)

footer.pack(
    side=tk.BOTTOM,
    pady=10
)
update_dashboard()


window.mainloop()