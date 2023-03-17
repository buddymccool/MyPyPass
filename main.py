from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    pw_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    p_nums = [choice(numbers) for _ in range(randint(2, 4))]
    p_lets = [choice(letters) for _ in range(randint(8, 10))]
    p_syms = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = p_syms + p_lets + p_nums
    shuffle(password_list)
    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    w = website_entry.get()
    e = email_entry.get()
    p = pw_entry.get()
    new_data = {
        w: {
            "email": e,
            "password": p,
        }
    }
    if w == "" or e == "" or p == "":
        messagebox.showerror(title="Error: Empty Field(s)", message="Please fill out all fields before saving :^)")
    else:
        try:
            with open("data.json", "r") as f:
                # read data
                data = json.load(f)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            # update data
            data.update(new_data)

            with open("data.json", "w") as f:
                # save updated data
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, END)
            pw_entry.delete(0, END)

# ---------------------------- FIND SAVED DATA ------------------------------- #


def search():
    w = website_entry.get().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(message="No Data", detail="No Data File Found :(")
    else:
        if w in data:
            messagebox.showinfo(message=f"Saved data for {w.capitalize()}",
                                detail=f"Email: {data[w]['email']}\nPassword: {data[w]['password']}")
        else:
            messagebox.showerror(message="No Match", detail="No details for the website exist.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("PyPassMyPass")
window.config(padx=50, pady=50)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username: ")
email_label.grid(column=0, row=2)
pw_label = Label(text="Password: ")
pw_label.grid(column=0, row=3)

website_entry = Entry(width=22)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "example@email.com")
pw_entry = Entry(width=22)
pw_entry.grid(column=1, row=3)

gen_pass = Button(text="Generate Password", command=generate_password)
gen_pass.grid(column=2, row=3)
add_butt = Button(text="Add to Saved Passwords", width=36, command=save)
add_butt.grid(column=1, row=4, columnspan=2)
search_butt = Button(text="Search", command=search, width=13)
search_butt.grid(column=2, row=1)


window.mainloop()

