from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


# Password Generator Project


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    entry_password.delete(0, END)
    entry_password.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def append_data_to_file():
    website = entry_website.get()
    email = entry_email_uname.get()
    password = entry_password.get()
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Missing data", message="One or more fields blank")
    else:
        confirm = messagebox.askquestion(title="Confirm", message=f"You have entered website {website},\n"
                                                                  f"Email/Username {email},\n"
                                                                  f"Password {password},\n"
                                                                  f"Are these correct.")

        if confirm == "yes":
            data = f"{website} | {email} | {password}\n"
            with open("data.txt", mode="a") as file:
                file.write(data)
            entry_website.delete(0, END)
            entry_password.delete(0, END)
            entry_website.focus()
            messagebox.showinfo("Info", "Password Saved")
        else:
            messagebox.showinfo(title="Canceled", message="Save canceled")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
tomato_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=tomato_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:")
label_website.grid(column=0, row=1, sticky="E")

entry_website = Entry()
entry_website.focus()
entry_website.grid(column=1, row=1, columnspan=2, sticky="E W")

label_email_uname = Label(text="Email/Username:")
label_email_uname.grid(column=0, row=2, sticky="E")

entry_email_uname = Entry()
entry_email_uname.insert(0, "tommy_kelly@icloud.com")
entry_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")

label_password = Label(text="Password:")
label_password.grid(column=0, row=3, sticky="E")

entry_password = Entry()
entry_password.grid(column=1, row=3, sticky="EW")

generate_btn = Button(text="Generate Password", cursor="hand2", command=generate_password)
generate_btn.grid(column=2, row=3, sticky="EW", padx=(4, 0), pady=2)

add_btn = Button(text="Add", width=35, cursor="hand2", command=append_data_to_file)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

window.resizable(False, False)

mainloop()
