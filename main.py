from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfilename
from random import choice, randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError
from datetime import datetime
from security import Security
import sys

sec = Security()


def load_list_box():
    search_list.delete(0, END)
    search_list_del.delete(0, END)
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    else:
        for index, key in enumerate(data):
            search_list.insert(index, key)
            search_list_del.insert(index, key)


def delete_item():
    if search_list_del.size() != 0:
        del_item = search_list_del.get(ANCHOR)
        res = messagebox.askquestion(title="Confirm...", message=f"Are you sure you what to delete {del_item}")
        if res == "yes":
            if del_item == "":
                messagebox.showinfo(title="Selection required...", message="Please select from the list below")
            else:
                with open("data.json", mode="r") as file:
                    data = json.load(file)
                    del data[del_item]
                with open("data.json", mode="w") as file:
                    json.dump(data, file, indent=4)
                    messagebox.showinfo("Info", f"{del_item} deleted")
                load_list_box()


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
    encrypt_email = f"'{sec.encrypt(entry_email_uname.get())}"
    encrypt_password = f"'{sec.encrypt(entry_password.get())}"

    new_data = {
        website: {
            "email": encrypt_email,
            "password": encrypt_password
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
    if search_list.size() != 0:
        search_value = search_list.get(ANCHOR)
        search_value_lower = search_list.get(ANCHOR).lower()

        if search_value_lower == "":
            messagebox.showinfo(title="Selection required...", message="Please select from the list below")
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

                        email = sec.decrypt(result["email"])
                        password = sec.decrypt(result["password"])
                        entry_website_search.delete(0, END)
                        entry_website_search.insert(0, search_value)
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
        file_name = askopenfilename(title="Select Import File", filetypes=[("json files", '*.json')])
        if file_name:
            with open(file_name) as file:
                data = json.load(file)
            with open("data.json", mode="w") as file:
                json.dump(data, file)
                messagebox.showinfo(title="Success...", message="Import complete")
            load_list_box()


def clear_search():
    entry_website_search.delete(0, END)
    entry_password_search.delete(0, END)
    entry_email_uname_search.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #


def exit_script():
    sys.exit()


def check_password():
    password = password_entry.get()
    if password == "your_password_here":
        # Password is correct, open the application
        password_window.destroy()  # Close the password window
    else:
        # Password is incorrect, show an error message
        messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")


password_window = Tk()
password_window.title("Password")
password_window.geometry("300x100")
password_window.resizable(False, False)
password_window.protocol("WM_DELETE_WINDOW", exit_script)

password_label = Label(password_window, text="Enter Password:")
password_label.pack()

password_entry = Entry(password_window, show="*")  # Use "show" to hide the password
password_entry.pack()

password_button = Button(password_window, text="Submit", command=check_password)
password_button.pack()

password_window.mainloop()


# ====================================================================== #

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
my_notebook.add(my_frame3, text="Import/Export/Delete")

# ---------------------------- Frame/TAB1/ADD ------------------------------- #
canvas = Canvas(my_frame1, width=200, height=200)
icon_img = PhotoImage(file="logo.png")
canvas.create_image(120, 100, image=icon_img)
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
canvas2.create_image(120, 100, image=icon_img)
canvas2.grid(column=1, row=0, sticky="EW")

label_website_search = Label(my_frame2, text="Website:")
label_website_search.grid(column=0, row=1, sticky="E")

entry_website_search = Entry(my_frame2)
entry_website_search.grid(column=1, row=1, columnspan=2, sticky="EW")
entry_website_search.bind("<Key>", lambda e: "break")

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
clear_btn = Button(my_frame2, text="Clear", cursor="hand2", command=clear_search, width=44)
clear_btn.grid(column=1, row=5, sticky="EW", columnspan=2, pady=(0, 8))

scrollbar = Scrollbar(my_frame2)
scrollbar.grid(row=6, column=3, sticky="WNS")
search_list = Listbox(my_frame2, height=4, selectmode=SINGLE, yscrollcommand=True)
search_list.grid(row=6, column=1, sticky="EW", columnspan=2)
search_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=search_list.yview)


# ---------------------------- Frame/TAB3/IMPORT/EXPORT ------------------------------- #


canvas3 = Canvas(my_frame3, width=200, height=200)
tomato_img3 = PhotoImage(file="logo.png")
canvas3.create_image(150, 100, image=icon_img)
canvas3.grid(column=1, row=0, sticky="EW")

scrollbar_del = Scrollbar(my_frame3)
scrollbar_del.grid(row=2, column=2, sticky="wns", pady=20)
search_list_del = Listbox(my_frame3, height=4, selectmode=SINGLE, yscrollcommand=True, width=50)
search_list_del.grid(row=2, column=1, pady=20, sticky="EW")
search_list_del.config(yscrollcommand=scrollbar_del.set)
scrollbar_del.config(command=search_list_del.yview)

export_btn = Button(my_frame3, text="Export", cursor="hand2", command=export, width=8)
export_btn.grid(row=1, column=0, sticky="E")

import_btn = Button(my_frame3, text="Import", cursor="hand2", command=import_data, width=8)
import_btn.grid(row=1, column=1,)

del_btn = Button(my_frame3, text="Delete", cursor="hand2", command=delete_item, width=8)
del_btn.grid(row=1, column=2, sticky="W")

load_list_box()

window.resizable(False, False)

window.mainloop()
