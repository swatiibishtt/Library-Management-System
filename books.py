import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import connect_database


def add_book():
    title = title_entry.get()
    author = author_entry.get()
    category = category_entry.get()
    quantity = quantity_entry.get()

    if title == "" or author == "" or category == "" or quantity == "":
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")
        return

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        INSERT INTO books (title, author, category, quantity)
        VALUES (%s, %s, %s, %s)
    """

    values = (title, author, category, quantity)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    messagebox.showinfo("Success", "Book added successfully!")

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


def open_add_book_window():
    global title_entry
    global author_entry
    global category_entry
    global quantity_entry

    window = tk.Toplevel()

    window.title("Add Book")
    window.geometry("500x400")
    window.configure(bg="#2D68C4")
    heading = tk.Label(
        window,
        text="Add New Book",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    title_label = tk.Label(
        window,
        text="Book Title"
    )

    title_label.pack()

    title_entry = tk.Entry(
        window,
        width=40
    )

    title_entry.pack(pady=5)

    author_label = tk.Label(
        window,
        text="Author"
    )

    author_label.pack()

    author_entry = tk.Entry(
        window,
        width=40
    )

    author_entry.pack(pady=5)

    category_label = tk.Label(
        window,
        text="Category"
    )

    category_label.pack()

    category_entry = tk.Entry(
        window,
        width=40
    )

    category_entry.pack(pady=5)

    quantity_label = tk.Label(
        window,
        text="Quantity"
    )

    quantity_label.pack()

    quantity_entry = tk.Entry(
        window,
        width=40
    )

    quantity_entry.pack(pady=5)

    add_button = tk.Button(
        window,
        text="Add Book",
        command=add_book
    )

    add_button.pack(pady=20)

#delete
    
def delete_book():
    
        selected = tree.selection()
    
        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a book to delete."
            )
            return
    
        book = tree.item(selected[0])["values"]
    
        book_id = book[0]
    
        confirmation = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        )
    
        if not confirmation:
            return
    
        connection = connect_database()
        cursor = connection.cursor()
    
        query = "DELETE FROM books WHERE book_id = %s"
    
        cursor.execute(
            query,
            (book_id,)
        )
    
        connection.commit()
    
        cursor.close()
        connection.close()
    
        messagebox.showinfo(
            "Success",
            "Book deleted successfully!"
        )
    
        window.destroy()
    
        view_books()

#view

def view_books():
    global tree
    global window
    window = tk.Toplevel()

    window.title("Book Management")
    window.geometry("1000x600")
    window.configure(bg="#2D68C4")

    heading = tk.Label(
        window,
        text="Book Management",
        font=("Arial", 20)
    )

    heading.pack(pady=20)

    # Table
    from tkinter import ttk

    columns = ("ID", "Title", "Author", "Category", "Quantity")

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Category", text="Category")
    tree.heading("Quantity", text="Quantity")

    tree.column("ID", width=50)
    tree.column("Title", width=200)
    tree.column("Author", width=180)
    tree.column("Category", width=150)
    tree.column("Quantity", width=80)

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # Get books from database
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    # Display books
    for book in books:
        tree.insert(
            "",
            tk.END,
            values=book
        )
        update_button = tk.Button(
        window,
        text="Update Selected Book",
        command=update_book
    )

    update_button.pack(pady=10)

    delete_button = tk.Button(
        window,
        text="Delete Selected Book",
        command=delete_book
    )

    delete_button.pack(pady=5)

#update

def update_book():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book to update."
        )
        return

    book = tree.item(selected[0])["values"]

    book_id = book[0]

    update_window = tk.Toplevel()

    update_window.title("Update Book")
    update_window.geometry("500x450")

    tk.Label(
        update_window,
        text="Update Book",
        font=("Arial", 20)
    ).pack(pady=20)

    tk.Label(
        update_window,
        text="Book Title"
    ).pack()

    title_update = tk.Entry(
        update_window,
        width=40
    )

    title_update.pack(pady=5)
    title_update.insert(0, book[1])

    tk.Label(
        update_window,
        text="Author"
    ).pack()

    author_update = tk.Entry(
        update_window,
        width=40
    )

    author_update.pack(pady=5)
    author_update.insert(0, book[2])

    tk.Label(
        update_window,
        text="Category"
    ).pack()

    category_update = tk.Entry(
        update_window,
        width=40
    )

    category_update.pack(pady=5)
    category_update.insert(0, book[3])

    tk.Label(
        update_window,
        text="Quantity"
    ).pack()

    quantity_update = tk.Entry(
        update_window,
        width=40
    )

    quantity_update.pack(pady=5)
    quantity_update.insert(0, book[4])

    def save_update():

        title = title_update.get()
        author = author_update.get()
        category = category_update.get()
        quantity = quantity_update.get()

        if title == "" or author == "" or category == "" or quantity == "":
            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantity must be a number."
            )
            return

        connection = connect_database()
        cursor = connection.cursor()

        query = """
            UPDATE books
            SET title = %s,
                author = %s,
                category = %s,
                quantity = %s
            WHERE book_id = %s
        """

        values = (
            title,
            author,
            category,
            quantity,
            book_id
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Book updated successfully!"
        )

        update_window.destroy()

        window.destroy()

        view_books()

    tk.Button(
        update_window,
        text="Save Changes",
        command=save_update
    ).pack(pady=20)

   #search
def search_books():

    global search_tree

    search_window = tk.Toplevel()

    search_window.title("Search Books")
    search_window.geometry("1000x550")
    search_window.configure(bg="#2D68C4")

    heading = tk.Label(
        search_window,
        text="Search Books",
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

    columns = (
        "ID",
        "Title",
        "Author",
        "Category",
        "Quantity"
    )

    search_tree = ttk.Treeview(
        search_window,
        columns=columns,
        show="headings"
    )

    search_tree.heading("ID", text="ID")
    search_tree.heading("Title", text="Title")
    search_tree.heading("Author", text="Author")
    search_tree.heading("Category", text="Category")
    search_tree.heading("Quantity", text="Quantity")

    search_tree.column("ID", width=60)
    search_tree.column("Title", width=220)
    search_tree.column("Author", width=180)
    search_tree.column("Category", width=150)
    search_tree.column("Quantity", width=100)

    search_tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    def perform_search():

        search_text = search_entry.get()

        for item in search_tree.get_children():
            search_tree.delete(item)

        connection = connect_database()
        cursor = connection.cursor()

        query = """
            SELECT *
            FROM books
            WHERE title LIKE %s
               OR author LIKE %s
               OR category LIKE %s
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

        books = cursor.fetchall()

        cursor.close()
        connection.close()

        for book in books:

            search_tree.insert(
                "",
                tk.END,
                values=book
            )

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=perform_search
    )

    search_button.pack(side=tk.LEFT, padx=5)