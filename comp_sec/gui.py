import tkinter as tk
import sec


window = tk.Tk()
window.title("Encryption Methods")


encryption_types = [
    "Caesar Cipher",
    "MonoAlphabetic Cipher",
    "One-Time Pad",
    "Hill Cipher",
    "Rail Fence",
    "Playfair Cipher",
]


is_encryption: bool = True

def on_encrypt_var_change(_, __, ___):
    global is_encryption
    is_encryption = not is_encryption

def put_space(widget, width=0, height=0):
    spacer = tk.Frame(widget)
    spacer.pack(padx=width/2, pady=height/2)

def on_encrypt_decrypt(*_):
    selected_type = encryption_type_var.get()

    encryption_method: sec.EncryptionMethod

    if selected_type == encryption_types[0]:
        encryption_method = sec.CaesarCipher()
    elif selected_type == encryption_types[1]:
        encryption_method = sec.MonoAlphabetic()
    elif selected_type == encryption_types[2]:
        encryption_method = sec.OnTimePad()
    elif selected_type == encryption_types[3]:
        encryption_method = sec.Hill()
    elif selected_type == encryption_types[4]:
        encryption_method = sec.RailFence()
    else:
        encryption_method = sec.PlayFair()

    text: str
    if is_encryption:
        text = encryption_method.encrypt(cipher_text_field.get(), key_text_field.get())
    else:
        text = encryption_method.decrypt(cipher_text_field.get(), key_text_field.get())

    return text



label_title = tk.Label(window, text="Encryption Methods", font=("Arial", 16), pady=10)
label_title.config(fg="purple")
label_title.pack(pady=20)


frame = tk.Frame(window)
frame.pack()

label_key = tk.Label(frame, text="Choose The Algorithm")
label_key.config(fg="purple")
label_key.pack()

encryption_type_var = tk.StringVar(frame)
encryption_type_var.set(encryption_types[0])
encryption_type_dropdown = tk.OptionMenu(window, encryption_type_var, *encryption_types)
encryption_type_dropdown.pack()

put_space(window, height=10)

label_key = tk.Label(window, text="Plain/Cipher Text", font=("Arial", 12))
label_key.config(fg="purple")
label_key.pack()

cipher_text_field = tk.Entry(window, width=40)
cipher_text_field.config(fg="blue")
cipher_text_field.pack(padx=20)

put_space(window, height=10)

label_key = tk.Label(window, text="Key", font=("Arial", 12))
label_key.config(fg="purple")
label_key.pack()

key_text_field = tk.Entry(window, width=40)
key_text_field.config(fg="blue")
key_text_field.pack()

put_space(window, height=10)

encrypt_var = tk.IntVar()
encrypt_var.trace("w", on_encrypt_var_change)
encrypt_checkbox = tk.Checkbutton(window, text="Encrypt (Check for decryption)", variable=encrypt_var)
encrypt_checkbox.pack()


def add_result():
    global result_title_label
    global result_label

    result_title = "Plain Text"

    if is_encryption:
        result_title = "Cipher Text"

    result_title_label.config(text=result_title, fg="green")
    result_label.config(text=on_encrypt_decrypt(), fg="green")


encryption_button = tk.Button(window, text="Encrypt/Decrypt", width=20)
encryption_button.pack(pady=10)
encryption_button["command"] = add_result

put_space(window, height=20)

result_frame = tk.Frame(window)
result_frame.pack()

result_title_label: tk.Label = tk.Label(result_frame, text="Result", font=("Arial", 15))
result_title_label.pack()

result_label = tk.Label(result_frame, text="", font=("Arial", 13))
result_label.pack()

put_space(window, height=20)

window.mainloop()

