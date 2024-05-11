
from tkinter import Tk, Label, Entry, messagebox, Button
import os
import shutil
import threading



def register():
    # Get the user input from the form
    first_name = first_name_entry.get()
    last_name = Last_name_entry.get()
    email = email_entry.get()
    mobile = Mobile_entry.get()

    # Create a new row with the user input
    new_row = [first_name, last_name, email, mobile]
    print(new_row)

    # Append the new row to the Excel sheet
    # workbook = openpyxl.load_workbook("registration_data.xlsx")
    # sheet = workbook.active
    # sheet.append(new_row)
    # workbook.save("registration_data.xlsx")
    # messagebox.showinfo("Success", "Registration successful!")
    messagebox.showerror("Empty Field", "Nooooo")


root = Tk()

root.title("Registration Form")
root.geometry('300x300')

first_name_label = Label(root, text="First Name:")
first_name_label.pack()
first_name_entry = Entry(root)
first_name_entry.pack()

Last_name_label = Label(root, text="Last Name:")
Last_name_label.pack()
Last_name_entry = Entry(root)
Last_name_entry.pack()

email_label = Label(root, text="Email:")
email_label.pack()
email_entry = Entry(root)
email_entry.pack()

Mobile_label = Label(root, text="Mobile:")
Mobile_label.pack()
Mobile_entry = Entry(root)
Mobile_entry.pack()

register_button = Button(root, text="Register", command=register)
register_button.pack()

root.mainloop()

def backup_files(source, destination):
    # Function to copy files/folders
    # You can modify this to handle different file operations or customize the backup process
    for root, dirs, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination, source_path.split(source)[-1])
            shutil.copy2(source_path, destination_path)
            print(f"Copied {source_path} to {destination_path}")


def main():
    source_directory = input("Enter the source directory to back up: ")
    destination_directory = input("Enter the destination directory for backup: ")

    # Create threads for concurrent file copying
    num_threads = 4  # Define the number of threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=backup_files, args=(source_directory, destination_directory))
        threads.append(thread)

    # Start and join threads
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Backup completed successfully!")


if __name__ == "__main__":
    main()
