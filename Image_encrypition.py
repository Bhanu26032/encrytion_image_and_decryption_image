from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os

root = Tk()
root.title("Image Encryption")

# Variables to store the image path and encryption key
image_path = ""
key = None

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

def encrypt_image():
    global image_path, key
    
    if not image_path:
        return
    
    image = Image.open(image_path)
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    image_bytes = image.tobytes()
    encrypted_bytes = bytes([byte ^ key[i % len(key)] for i, byte in enumerate(image_bytes)])
    
    save_path = os.path.splitext(image_path)[0] + "_encrypted.png"
    with open(save_path, 'wb') as f:
        f.write(encrypted_bytes)
    
    key_label = Label(root, text="Encryption Key: " + key.decode('utf-8'))
    key_label.pack()
    
    # Show the encrypted image in the tkinter window
    encrypted_image = ImageTk.PhotoImage(Image.open(save_path))
    image_label = Label(root, image=encrypted_image)
    image_label.image = encrypted_image  # Store a reference to prevent image garbage collection
    image_label.pack()

def decrypt_image():
    global image_path, key
    
    if not image_path or not key:
        return
    
    encrypted_image = Image.open(image_path)
    image_bytes = encrypted_image.tobytes()
    
    decrypted_bytes = bytes([byte ^ key[i % len(key)] for i, byte in enumerate(image_bytes)])
    
    save_path = os.path.splitext(image_path)[0] + "_decrypted.png"
    with open(save_path, 'wb') as f:
        f.write(decrypted_bytes)
    
    decrypted_image = ImageTk.PhotoImage(Image.open(save_path))
    decrypted_label = Label(root, image=decrypted_image)
    decrypted_label.image = decrypted_image  # Store a reference to prevent image garbage collection
    decrypted_label.pack()

select_button = Button(root, text="Select Image", command=select_image)
select_button.pack()

encrypt_button = Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.pack()

decrypt_button = Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.pack()

root.mainloop()
