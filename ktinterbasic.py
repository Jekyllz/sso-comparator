from tkinter import Tk, Label, Button, Entry, messagebox
import tkinter as tk
from pysnc import ServiceNowClient
import collections
import os
ins = ""
username = ""
password = ""
client = ServiceNowClient(ins, (username, password))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

root = Tk()

class QBox:
    """ Class that is an object"""
    
    def on_login_click():
        global root
        global client
        global username
        global password
        global inst
        inst = instance_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        root.destroy()
        QBox.dashboard()

    def login_window(): 
        global instance_entry
        global username_entry
        global password_entry
        
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

        Button(root, text="Login", command=QBox.on_login_click).grid(row=5, column=0, sticky="E")
    
        root.mainloop()

    def dashboard():
        global bcolors
        client = ServiceNowClient(inst, (username, password))
        
        root = Tk()
        root.geometry('800x200')
        root.title('ServiceNow SSO')
        gr = client.GlideRecord('sso_properties')
        gr.add_encoded_query("active=true")
        gr.query()
        I = 0
        r = ()
        idpdict = {}
 #       idpdict[I] = {'Num': I, 'Name': r.name}

        for r in gr:
#            I = I+1
#            print(idpdict[2])
            w = tk.Label(root, text=r.name, bg="red", fg="white")
            w.pack(fill=tk.X, padx=50, pady=10)
            w = tk.Label(root, text=idpdict[2], bg="green", fg="black")
            w.pack(fill=tk.X, padx=50, pady=10)
            w = tk.Label(root, text=idpdict[3], bg="blue", fg="white")
            w.pack(fill=tk.X, padx=50, pady=10)
            tk.mainloop()
        

    def login_page(): 
        global instance_entry
        global username_entry
        global password_entry
        global root
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
        Button(root, text="Login", command=QBox.on_login_click).grid(row=5, column=0, sticky="E")
    
        root.mainloop()
        
QBox.login_page()
    
