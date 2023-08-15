from tkinter import *
import tkinter as tk
from pysnc import ServiceNowClient

client = ServiceNowClient(ins, (user, pass))
gr = client.GlideRecord('sso_properties')
gr.add_encoded_query("active=true")
gr.query()
y = 0
root = Tk()
root.geometry('1000x200')
root.title('ServiceNow SSO')
txt_output = Text(root, height=5, width=30)

txt_output.pack(fill=tk.X, padx=50, pady=10)
idp_list = []

for r in gr:
    y+=1
    idp_list.insert(y, r.name)

for idp in idp_list:
    txt_output.insert(tk.END, idp + "\n")
root.mainloop()
