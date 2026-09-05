# import sys
# import time

# import requests

# import modules
import tkinter as tk

app = tk.Tk()
app.config(height=400, width=400)


def search():
    print(f"Searchbar: {searchbar.get()}")


searchbar = tk.Entry(app, width=15)
searchbar.place(relx=0.46, rely=0.1225, anchor=tk.CENTER)

testbutton = tk.Button(app, text="Search", command=search)
testbutton.place(relx=0.66, rely=0.1225, anchor=tk.CENTER)
app.bind("<Return>", lambda event: testbutton.invoke())


app.mainloop()
