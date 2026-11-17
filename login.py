import tkinter as tk
from tkinter import messagebox

from database import connect_database


def check_login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password."
        )
        return

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM users
        WHERE username = %s
        AND password = %s
    """

    cursor.execute(
        query,
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:

        messagebox.showinfo(
            "Login Successful",
            "Welcome to Library Management System!"
        )

        login_window.destroy()

        import main

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


login_window = tk.Tk()

login_window.title(
    "Library Management System - Login"
)

login_window.geometry(
    "500x400"
)
login_window.configure(bg="#2D68C4")

heading = tk.Label(
    login_window,
    text="Library Management System",
    font=("Arial", 22)
)

heading.pack(pady=30)

login_label = tk.Label(
    login_window,
    text="Login",
    font=("Arial", 18)
)

login_label.pack(pady=10)


tk.Label(
    login_window,
    text="Username"
).pack()

username_entry = tk.Entry(
    login_window,
    width=35
)

username_entry.pack(pady=5)


tk.Label(
    login_window,
    text="Password"
).pack()

password_entry = tk.Entry(
    login_window,
    width=35,
    show="*"
)

password_entry.pack(pady=5)


login_button = tk.Button(
    login_window,
    text="Login",
    width=20,
    command=check_login
)

login_button.pack(pady=25)


login_window.mainloop()