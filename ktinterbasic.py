from tkinter import Tk, Label, Button, Entry, messagebox
 
def on_login_click():
    instance = instance_entry.get()
    username = username_entry.get()
    password = password_entry.get()
 
    if username == "user" and password == "password":
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid credentials")
 
root = Tk()
root.geometry('680x200')
root.title('ServiceNow Instance Reader')
Label(root, text="Provide ServiceNow Admin User").pack

Label(root, text="Instance:").grid(row=2, column=0, sticky="W")
instance_entry = Entry(root)
instance_entry.grid(row=2, column=1)

Label(root, text="Username:").grid(row=3, column=0, sticky="W")
username_entry = Entry(root)
username_entry.grid(row=3, column=1,)
 
Label(root, text="Password:").grid(row=4, column=0,sticky="W")
password_entry = Entry(root, show="*")
password_entry.grid(row=4, column=1)


 
Button(root, text="Login", command=on_login_click).grid(row=5, column=0, sticky="E")
 
root.mainloop()