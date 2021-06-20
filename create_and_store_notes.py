from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from tkinter.simpledialog import askstring
import tkinter.font as tkFont
import mysql.connector

conn = mysql.connector.connect(host="localhost",port=3306,user="Student123",passwd="4483",db="NOTES")

def Click(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

# root.bind('<Button-1>',Click)
notes = {}
last_one = ""
def close():
    if len(last_one)!=0:
        notes[last_one] = notes_area.get(1.0, END)
        sql_update(last_one,notes_area.get(1.0,END))
    root1.destroy()

def sql_create(name,content):
    obj = conn.cursor()
    obj.execute("INSERT INTO ALL_NOTES (NAME,CONTENT) VALUES (%s, %s)",(name,content))
    conn.commit()

def sql_update(name,content):
    obj = conn.cursor()
    obj.execute("UPDATE ALL_NOTES SET CONTENT = %s WHERE NAME = %s",(content,name))
    conn.commit()

def sql_delete(name):
    obj = conn.cursor()
    obj.execute("DELETE FROM ALL_NOTES WHERE NAME = %s",(name,))
    conn.commit()

def rename_sql(title,prev_title):
    obj = conn.cursor()
    obj.execute("UPDATE ALL_NOTES SET NAME = %s WHERE NAME = %s", (title,prev_title))
    conn.commit()

def update(ListButton):
    lst = set()
    # print("Inside Update")
    for k in notes.keys():
        lst.add(k)
        # print(k)
    items_list = sorted(list(lst))
    items_list.insert(0,"Select")
    # print("Items List")
    # print(items_list)
    ListButton['values'] = items_list
    return


def create(notes_area,ListButton):
    # print("INNNNNN CREATE")
    global last_one
    if len(last_one)!=0:
        notes[last_one] = notes_area.get(1.0, END)
        sql_update(last_one,notes_area.get(1.0,END))
        if (ListButton.get() != "Select"):
            ListButton.current(0)
    title.config(state=NORMAL)
    title.delete(1.0,END)
    title.config(state=DISABLED)
    notes_area.delete(1.0, END)
    notes_area.config(state=DISABLED)
    dialog = Tk()
    dialog.withdraw()
    name_file = askstring(title="New Note Name",prompt="Enter the name for new Note",parent=dialog)

    if name_file is not None and len(name_file)!=0 :
        tk.messagebox.showinfo(" ","Note created Successfully!",parent=dialog)
        last_one = name_file
        title.config(state=NORMAL)
        title.insert(END,name_file)
        title.config(state=DISABLED)
        notes[name_file] = ""
        update(ListButton)
        notes_area.config(state=NORMAL)
        notes_area.insert(END, notes[name_file])
        sql_create(name_file,notes[name_file])
        # print(notes)
    return


def delete(notes_area,ListButton):
    global last_one
    title.config(state=NORMAL)
    notes_area.config(state=NORMAL)
    if len(last_one)!=0:
        notes[last_one] = notes_area.get(1.0, END)
        sql_update(last_one, notes_area.get(1.0, END))
        if (ListButton.get() != "Select"):
            ListButton.current(0)
    notes_area.delete(1.0, END)
    notes_area.config(state=DISABLED)
    title.delete(1.0,END)
    title.config(state=DISABLED)
    dialog = Tk()
    dialog.withdraw()
    name_file = askstring(title="Delete Note",prompt="Enter the name for note to be deleted",parent=dialog)
    if name_file in notes.keys():
        title.config(state=NORMAL)
        title.insert(END,name_file)
        notes_area.config(state=NORMAL)
        notes_area.insert(END,notes[name_file])
        choice = messagebox.askyesno("Confirmation","Are you sure you want to delete "+name_file,parent=dialog)
        if(choice):
            notes.pop(name_file)
            title.delete(1.0,END)
            notes_area.delete(1.0, END)
            sql_delete(name_file)
            update(ListButton)
        title.config(state=DISABLED)
        notes_area.config(state=DISABLED)
    return


def display(event,notes_area):
    global last_one
    # print("In display")
    # print(last_one)
    update(event.widget)
    if len(last_one)!=0:
        # print(notes)
        notes[last_one] = notes_area.get(1.0, END)
        sql_update(last_one, notes_area.get(1.0, END))
        # print(notes_area.get(1.0,END))
        # print(notes)
    title.config(state=NORMAL)
    title.delete(1.0,END)
    notes_area.delete(1.0, END)
    if( event.widget.get() != "Select"):
        title.insert(END,event.widget.get())
        title.config(state=DISABLED)
        notes_area.config(state=NORMAL)
        last_one = event.widget.get()
        notes_area.insert(END,notes[event.widget.get()])
        sql_update(event.widget.get(),notes[event.widget.get()])
        # print(notes[event.widget.get()])
    else:
        title.config(state=DISABLED)
        notes_area.config(state=DISABLED)
        last_one=""

    return

def rename():
    prev_title = title.get(1.0,END).strip()
    dialog = Tk()
    dialog.withdraw()
    title.config(state=DISABLED)
    name_file = askstring(title="New Note Name", prompt="Enter the name for new Note", parent=dialog)
    if name_file is not None and len(name_file)!=0 :
        title.config(state=NORMAL)
        title.delete(1.0,END)
        title.insert(END,name_file)
        notes[name_file]=notes[prev_title]
        rename_sql(name_file,prev_title)
        notes.pop(prev_title)
        title.config(state=DISABLED)
        update(ListButton)

def create_table():
    obj = conn.cursor()
    obj.execute('''CREATE TABLE IF NOT EXISTS ALL_NOTES (
                NAME VARCHAR(100), 
                CONTENT TEXT(65535))''')

def load_data():
    obj = conn.cursor()
    obj.execute("SELECT * FROM ALL_NOTES")
    for entry in obj.fetchall():
        notes[entry[0]]=entry[1]

def work_as_constructor():
    create_table()
    load_data()

work_as_constructor()

root1=Tk()
root1.geometry("2000x1000")
start_frame = Frame(root1,width=2000,height=1000,bg="#141f2b")
start_frame.pack()
vertical_line = Frame(root1,width=1,height=800,bg="#bbbdbf")
vertical_line.place(x=251,y=157)
notes_area = Text(root1,width=1000,height=500,bg="#141f2b",highlightbackground="#bbbdbf", highlightcolor="#bbbdbf", highlightthickness=1,bd=0,fg="white",padx=3,pady=3,state=DISABLED)
notes_area.place(x=255,y=160)
title = Text(root1,width=60,height=2,bg="#141f2b",highlightbackground="#bbbdbf", highlightcolor="#bbbdbf", highlightthickness=1,bd=0,fg="white",padx=3,pady=3,state=DISABLED)
title.place(x=255,y=106)
fontExample = tkFont.Font(family="Arial", size=12, weight="bold", slant="italic")
title.configure(font=fontExample)
rename_button = tk.Button(root1,text="RENAME",width=20,height=2,command=lambda :rename())
rename_button.place(x=820,y=106)
MENU = Frame(root1,width=14,height=17,bg="#141f2b")
MENU.place(x=71,y=157)
ListButton = ttk.Combobox(MENU, width=26, height=3, textvariable=tk.StringVar())
create_Button = tk.Button(MENU,text="CREATE",width=24,height=2,command=lambda : create(notes_area,ListButton))
create_Button.pack()
Delete_Button = tk.Button(MENU,text="DELETE",width=24,height=2,command=lambda :delete(notes_area,ListButton))
Delete_Button.pack()
update(ListButton)
ListButton.pack()
ListButton.current(0)
root1.bind('<Button-1>', Click)
ListButton.bind("<<ComboboxSelected>>",lambda event, arg = notes_area : display(event,arg))
root1.protocol("WM_DELETE_WINDOW",close)
root1.mainloop()


