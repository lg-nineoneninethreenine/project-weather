# import sys
# import time

# import requests

# import modules
import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x400")
app.resizable(False, False)

def search():
    print(f"Searchbar: {searchbar.get()}")
def tempunit_change(value):
    print(f"Tempunit: {value}")

heading_label = ctk.CTkLabel(app, text = "Weather", font = ("Consolas", 30)).pack(pady = 5)

searchframe = ctk.CTkFrame(app, width = 179, height = 28)
searchframe.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

searchbar = ctk.CTkEntry(searchframe, width=113, placeholder_text = "Enter City Name")
searchbar.place(relx=0.33, rely=0.5, anchor=ctk.CENTER)

searchbutton = ctk.CTkButton(searchframe, text="Search", command=search, width = 40)
searchbutton.place(relx=0.84, rely=0.5, anchor=ctk.CENTER)
app.bind("<Return>", lambda event: searchbutton.invoke())

tempbutton = ctk.CTkSegmentedButton(app, values=["C", "F"], command = tempunit_change)
tempbutton.place(relx=0.85, rely=0.15, anchor=ctk.CENTER)
tempbutton.set("C")

app.mainloop()
