import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, GENDER TEXT, DOB TEXT)"
)

# Creating the functions


def reset_fields():
    global name_strvar, gender_strvar, dob

    for i in ['name_strvar', 'gender_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


def reset_form():
    global tree
    tree.delete(*tree.get_children())

    reset_fields()


def display_records():
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)


def add_record():
    global name_strvar, gender_strvar, dob

    name = name_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()

    if not name or not gender or not DOB:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        connector.execute(
            'INSERT INTO SCHOOL_MANAGEMENT (NAME, GENDER, DOB) VALUES (?,?,?)', (
                name, gender, DOB)
        )
        connector.commit()
        mb.showinfo('Record added', f"Record of {name} was successfully added")
        reset_fields()
        display_records()


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute(
            'DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo(
            'Done', 'The record you wanted deleted was successfully deleted.')

        display_records()


# Initializing the GUI window
main = Tk()
main.title('DataFlair School Management System')
main.geometry('1500x900')

# Creating the background and foreground color variables
lf_bg = 'red'  # bg color for the left_frame
cf_bg = 'white'  # bg color for the center_frame

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
gender_strvar = StringVar()
dob_strvar = StringVar()

# Placing the components in the main window
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont,
      bg='black').pack(side=TOP, fill=X)

# Creating a frame and placing it in the main window.
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

# Creating a frame and placing it in the main window.
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

# Creating a frame and placing it in the main window.
right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
# Placing the labels in the left frame.
Label(left_frame, text="Name", font=labelfont,
      bg=lf_bg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Gender", font=labelfont,
      bg=lf_bg).place(relx=0.375, rely=0.15)
Label(left_frame, text="Date of Birth (DOB)",
      font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.25)
# Creating an entry widget with a width of 19 characters, a textvariable of name_strvar, and a font of
# entryfont. It is then placing it at x=50 and rely=0.1.
Entry(left_frame, width=19, textvariable=name_strvar,
      font=entryfont).place(x=50, rely=0.1)

# Creating a dropdown menu with the options 'Male' and 'Female' and placing it in the left_frame.
OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(
    x=75, rely=0.2, relwidth=0.5)

# Creating a DateEntry widget and placing it in the left_frame.
dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=75, rely=0.3)

# Creating a button with the text 'Submit and Add Record', a font of labelfont, a command of
# add_record, and a width of 18. It is then placing it at relx=0.075 and rely=0.85.
Button(left_frame, text='Submit and Add Record', font=labelfont,
       command=add_record, width=18).place(relx=0.075, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont,
       command=remove_record, width=15).place(relx=0.15, rely=0.3)
Button(center_frame, text='Reset Fields', font=labelfont,
       command=reset_fields, width=15).place(relx=0.15, rely=0.4)
Button(center_frame, text='Delete database', font=labelfont,
       command=reset_form, width=15).place(relx=0.15, rely=0.5)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont,
      bg='red', fg='white').pack(side=TOP, fill=X)

# Creating a treeview widget with the height of 100, a selectmode of BROWSE, and the columns of
# Student ID, Name, Gender, and Date of Birth.
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Gender", "Date of Birth"))

# Creating a scrollbar for the treeview widget.
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

# Creating the headers for the treeview widget.
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)

# Setting the width of the columns.
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=100, stretch=NO)
tree.column('#2', width=300, stretch=NO)

# Placing the tree widget in the right frame.
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
