from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from random import choice, randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError
from datetime import datetime


def load_list_box():
    search_list.delete(0, END)
    with open("data.json", mode="r") as file:
        data = json.load(file)
        for index, key in enumerate(data):
            search_list.insert(index, key)
            print(index)


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
                load_list_box()
        else:
            messagebox.showinfo(title="Canceled", message="Save canceled")
# ---------------------------- GET DATA ------------------------------- #


def get_data():
    search_value = search_list.get(ANCHOR)
    search_value_lower = search_list.get(ANCHOR).lower()

    if search_value_lower == "":
        messagebox.showinfo(title="Selection required...", message="Please from the list below")
    else:
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
                    entry_email_uname_search.delete(0, END)
                    entry_email_uname_search.insert(0, email)
                    entry_password_search.config(state='normal')
                    entry_password_search.delete(0, END)
                    entry_password_search.insert(0, password)
                    pyperclip.copy(password)

        except FileNotFoundError:
            messagebox.showerror(title="Data file Err", message="Data file not found")

# ---------------------------- EXPORT DATA ------------------------------- #


def export():
    confirm = messagebox.askyesno(title="Confirm", message="Are you sure you want to export")

    if confirm:
        folder_name = askdirectory()
        file_name = datetime.now().strftime("%d/%m/%Y %H:%M:%S").replace("/", ".").replace(":", ".")
        export_name = f"{folder_name}/{file_name}.json"

        if folder_name:
            with open("data.json") as file:
                data = json.load(file)
            with open(export_name, mode="w") as file:
                json.dump(data, file, indent=4)
                messagebox.showinfo(title="Success", message="Export Complete")

# ---------------------------- IMPORT DATA ------------------------------- #


def import_data():

    res = messagebox.askokcancel(title="Confirm", message="This action will overwrite all previous data")
    if res:
        print("ok")
        file_name = askopenfilename(title="Select Import File", filetypes=[("json files", '*.json')])
        if file_name:
            with open(file_name) as file:
                data = json.load(file)
            with open("data.json", mode="w") as file:
                json.dump(data, file)
                messagebox.showinfo(title="Success...", message="Import complete")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Generator")

my_notebook = ttk.Notebook(window)
my_notebook.grid(row=0, column=0, padx=20, pady=20)

my_frame1 = Frame(my_notebook, padx=40, pady=40)
my_frame1.grid(row=0, column=0, sticky="nsew")
my_frame2 = Frame(my_notebook, padx=40, pady=40)
my_frame2.grid(row=0, column=0, sticky="nsew")
my_frame3 = Frame(my_notebook, padx=40, pady=40)
my_frame3.grid(row=0, column=0, sticky="nsew")

my_notebook.add(my_frame1, text="Add")
my_notebook.add(my_frame2, text="Search")
my_notebook.add(my_frame3, text="Import/Export")

# ---------------------------- Frame/TAB1/ADD ------------------------------- #
canvas = Canvas(my_frame1, width=200, height=200)
icon_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=icon_img)
canvas.grid(column=1, row=0, sticky="EW")

label_website = Label(my_frame1, text="Website:")
label_website.grid(column=0, row=1, sticky="E")

entry_website = Entry(my_frame1)
entry_website.focus()
entry_website.grid(column=1, row=1, columnspan=2, sticky="EW")

label_email_uname = Label(my_frame1, text="Email/Username:")
label_email_uname.grid(column=0, row=2, sticky="E")

entry_email_uname = Entry(my_frame1)
entry_email_uname.insert(0, "tommy_kelly@icloud.com")
entry_email_uname.grid(column=1, row=2, columnspan=2, sticky="EW")

label_password = Label(my_frame1, text="Password:")
label_password.grid(column=0, row=3, sticky="E")

entry_password = Entry(my_frame1)
entry_password.grid(column=1, row=3, sticky="EW")

generate_btn = Button(my_frame1, text="Generate Password", cursor="hand2", command=generate_password)
generate_btn.grid(column=2, row=3, sticky="EW", padx=(4, 0), pady=2)

add_btn = Button(my_frame1, text="Add", width=35, cursor="hand2", command=append_data_to_file)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

# ---------------------------- Frame/TAB2/SEARCH ------------------------------- #
canvas2 = Canvas(my_frame2, width=200, height=200)
tomato_img2 = PhotoImage(file="logo.png")
canvas2.create_image(100, 100, image=icon_img)
canvas2.grid(column=1, row=0, sticky="EW")

label_website_search = Label(my_frame2, text="Website:")
label_website_search.grid(column=0, row=1, sticky="E")

entry_website_search = Entry(my_frame2)
entry_website_search.focus()
entry_website_search.grid(column=1, row=1, columnspan=2, sticky="EW")

label_email_uname_search = Label(my_frame2, text="Email/Username:")
label_email_uname_search.grid(column=0, row=2, sticky="E")

entry_email_uname_search = Entry(my_frame2)
entry_email_uname_search.grid(column=1, row=2, columnspan=2, sticky="EW")
entry_email_uname_search.bind("<Key>", lambda e: "break")

label_password_search = Label(my_frame2, text="Password:")
label_password_search.grid(column=0, row=3, sticky="E")

entry_password_search = Entry(my_frame2)
entry_password_search.grid(column=1, row=3, columnspan=2, sticky="EW")
entry_password_search.bind("<Key>", lambda e: "break")

search_btn = Button(my_frame2, text="Search", cursor="hand2", command=get_data, width=44)
search_btn.grid(column=1, row=4, sticky="EW", columnspan=2, pady=8)

scrollbar = Scrollbar(my_frame2)
scrollbar.grid(row=5, column=2, sticky="W")
search_list = Listbox(my_frame2, height=4, selectmode=SINGLE, yscrollcommand=True)
search_list.grid(row=5, column=1, sticky="EW")
search_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=search_list.yview)

load_list_box()

# ---------------------------- Frame/TAB3/IMPORT/EXPORT ------------------------------- #

canvas3 = Canvas(my_frame3, width=200, height=200)
tomato_img3 = PhotoImage(file="logo.png")
canvas3.create_image(100, 100, image=icon_img)
canvas3.place(x=95, y=1)


export_btn = Button(my_frame3, text="Export", cursor="hand2", command=export, width=8)
export_btn.grid(row=1, column=0, pady=10)

import_btn = Button(my_frame3, text="Import", cursor="hand2", command=import_data, width=8)
import_btn.grid(row=2, column=0)

window.resizable(False, False)

mainloop()
