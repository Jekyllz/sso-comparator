import tkinter as tk
from pysnc import ServiceNowClient

client = ServiceNowClient("insname", ("username","pass"))

gr = client.GlideRecord("sso_properties")
gr.add_encoded_query("active=true")
gr.query()

def on_item_select(event):
    selected_item = listbox.get(listbox.curselection())
    selected_label.config(text=f"Selected: {selected_item}")

n = []
Dict = {}
f = int(0)
y = int(1)
b = 0

for r in gr:
    n.insert(f, str(r.name))
    Dict[f] = {'name': str(r.name), 'active': str(r.active), 'sys_id' : str(r.sys_id), 'UserField' : str(r.user_field), 'Auto': str(r.auto_provision),'ssoscript' : str(r.sso_script)}
    f+=1

print(Dict[0])


# Create the main window
root = tk.Tk()
root.title("List Selection Example")
root.geometry('800x400')

# Create a Listbox widget
listbox = tk.Listbox(root)
listbox.pack(padx=10, pady=10)
for i in n:
    listbox.insert(tk.END,n[b])
    b+=1

listbox.bind("<<ListboxSelect>>", on_item_select)

# Label to display selected item
selected_label = tk.Label(root, text="Selected: ")
selected_label.pack()

# Run the Tkinter event loop
root.mainloop()
