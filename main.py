from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from random import choice, randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError
from datetime import datetime


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
    website = entry_website.get().lower()
    email = entry_email_uname.get()
    password = entry_password.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Missing data", message="One or more fields blank")
    else:
        confirm = messagebox.askquestion(title="Confirm", message=f"You have entered website - {website},\n"
                                                                  f"Email/Username - {email},\n"
                                                                  f"Password - {password},\n"
                                                                  f"Are these correct.")

        if confirm == "yes":
            # data = f"{website} | {email} | {password}\n"
            try:
                with open("data.json", mode="r") as file:
                    data = json.load(file)

            except (JSONDecodeError, FileNotFoundError):
                with open("data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
                    messagebox.showinfo("Info", "Password Saved")

            else:

                if website in data:
                    res = messagebox.askokcancel(message="This website is all ready saved.\n"
                                                         "Click Yes to overwrite.\n"
                                                         "Or Cancel to cancel.")
                    if res == FALSE:
                        print(res)
                        return
                data.update(new_data)
                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)
                    messagebox.showinfo("Info", "Password Saved")

            finally:
                entry_website.delete(0, END)
                entry_password.delete(0, END)
                entry_website.focus()

        else:
            messagebox.showinfo(title="Canceled", message="Save canceled")
# ---------------------------- GET DATA ------------------------------- #


def get_data():
    search_value = entry_website.get()
    search_value_lower = entry_website.get().lower()
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
            try:
                conversion = {x.lower(): y for x, y in data.items()}
                result = conversion[search_value_lower]
            except KeyError:
                messagebox.showerror("Not Found", message=f"{search_value} not found")
            else:
                email = result["email"]
                password = result["password"]
                entry_email_uname.delete(0, END)
                entry_email_uname.insert(0, email)
                entry_password.delete(0, END)
                entry_password.insert(0, password)
                pyperclip.copy(password)
    except FileNotFoundError:
        messagebox.showerror(title="Data file Err", message="Data file not found")

# ---------------------------- EXPORT DATA ------------------------------- #


def export():
    folder_name = askdirectory()
    file_name = datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace("/", ".").replace(":", ".")
    export_name = f"{folder_name}/{file_name}.json"

    if folder_name:
        with open("data.json") as file:
            data = json.load(file)
        with open(export_name, mode="w") as file:
            json.dump(data, file, indent=4)
            messagebox.showinfo(title="Success", message="Export Complete")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")
window.config(padx=30, pady=30)
window.option_add('*Dialog.msg.font', 'Helvetica 30')

canvas = Canvas(width=200, height=200)
tomato_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=tomato_img)
canvas.grid(column=1, row=0)

label_website = Label(text="Website:")
label_website.grid(column=0, row=1, sticky="E")

entry_website = Entry()
entry_website.focus()
entry_website.grid(column=1, row=1, sticky="EW")

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

search_btn = Button(text="Search", cursor="hand2", command=get_data)
search_btn.grid(column=2, row=1, sticky="EW", padx=(4, 0), pady=2)

add_btn = Button(text="Add", width=35, cursor="hand2", command=append_data_to_file)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

export_btn = Button(text="Export", cursor="hand2", command=export)
export_btn.place(x=0, y=0)

window.resizable(False, False)

mainloop()
