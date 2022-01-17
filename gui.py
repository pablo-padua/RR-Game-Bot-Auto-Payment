import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

from main import RRbot

root = tk.Tk()

canvas = tk.Canvas(root, height="600", width="800")
canvas.pack()

back_img = tk.Label(root, bg="light blue")
back_img.place(relwidth=1,relheight=1)

frame=tk.Frame(root, bg="light green")
frame.place(relx=0.25,rely=0.12,relwidth=0.5,relheight=0.8)

label1 = tk.Label(frame, text="Login:" , bg="light green" ,font=('Century',14))
label1.place(relx=0.36, rely=0.015, relwidth=0.25, relheight=0.065)

entry1 = tk.Entry(frame, show="*", font=('Century',17)) #LOGIN INPUT
entry1.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.065)

label2 = tk.Label(frame, text="Password:" ,bg="light green" ,font=('Century',14))
label2.place(relx=0.335, rely=0.17, relwidth=0.3, relheight=0.05)

entry2 = tk.Entry(frame, show="*", font=('Century',17)) #PASSWORD INPUT
entry2.place(relx=0.05, rely=0.22, relwidth=0.9, relheight=0.065)

label3 = tk.Label(frame, text="Wars ID... Eg: 00001,00002,00003" , bg="light green" ,font=('Century',14))
label3.place(relx=0.07, rely=0.30, relwidth=0.9, relheight=0.05)

entry3 = tk.Entry(frame,font=('Century',15)) #WARS ID INPUT
entry3.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.065)

label4 = tk.Label(frame, text="Price: eg: 17,18,19" , bg="light green" ,font=('Century',14))
label4.place(relx=0.062, rely=0.42, relwidth=0.9, relheight=0.065)

entry4 = tk.Entry(frame,font=('Century',15)) #PRICE INPUT
entry4.place(relx=0.05, rely=0.48, relwidth=0.9, relheight=0.065)

label5 = tk.Label(frame, text="Your party ID" , bg="light green" ,font=('Century',14))
label5.place(relx=0.042, rely=0.56, relwidth=0.9, relheight=0.065)

entry5 = tk.Entry(frame,font=('Century',15)) #PARTY ID INPUT
entry5.place(relx=0.05, rely=0.63, relwidth=0.9, relheight=0.065)

#############TODO##############
# options = tk.StringVar(root)
# options.set("One") # default value

# l3 = tk.Label(root,  text='Select One',)  

# om1 =tk.OptionMenu(root, options, "VK","Facebook", "Google")
# root.mainloop()

def execute():
    username = entry1.get()
    password= entry2.get()
    warsIds= entry3.get()
    price = entry4.get()
    partyId= entry5.get()
    RRbot(username, password, warsIds, price, partyId)
    root.destroy()

button = tk.Button(root, text="Confirm", bg="black", fg="white", font=('Century',12), command=execute)
button.place(relx=0.34,rely=0.8,relwidth=0.28,relheight=0.05)

label3 = tk.Label(root, text="RR Bot By Padua" , bg="light green" ,font=('Century',12), borderwidth=10)
label3.place(relx=0.01, rely=0.94, relwidth=0.35, relheight=0.05)

label4 = tk.Label(root, text="@PaduaRR on Telegram" , bg="light green" ,font=('Century',12), borderwidth=10)
label4.place(relx=0.58, rely=0.94, relwidth=0.42, relheight=0.05)

root.mainloop()