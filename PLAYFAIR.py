import tkinter as tk
from tkinter import ttk

def prepare_key(key):
    key = key.replace("J", "I")
    key_set = set(key)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in key_set:
        if char in alphabet:
            alphabet = alphabet.replace(char, "")
    key_matrix = list(key + alphabet)
    key_matrix = [key_matrix[i:i + 5] for i in range(0, len(key_matrix), 5)]
    return key_matrix

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None, None

def toLowerCase(plain):
    return plain.lower()


# Function to remove all spaces in a string
def removeSpaces(plain):
    return plain.replace(" ", "")


# Function to generate the 5x5 key square
def generateKeyTable(key):
    key = key.lower().replace(' ', '').replace('j', 'i')
    key_square = ''
    for letter in key + 'abcdefghiklmnopqrstuvwxyz':
        if letter not in key_square:
            key_square += letter
    return key_square


# Function to search for the characters of a digraph
# in the key square and return their position (for encryption)
def search_encrypt(key_square, a, b):
    if a == 'j':
        a = 'i'
    elif b == 'j':
        b = 'i'
    row_a, col_a = divmod(key_square.index(a), 5)
    row_b, col_b = divmod(key_square.index(b), 5)
    if row_a == row_b:
        col_a = (col_a + 1) % 5
        col_b = (col_b + 1) % 5
    elif col_a == col_b:
        row_a = (row_a + 1) % 5
        row_b = (row_b + 1) % 5
    else:
        col_a, col_b = col_b, col_a
    return key_square[row_a * 5 + col_a] + key_square[row_b * 5 + col_b]


# Function to search for the characters of a digraph
# in the key square and return their position (for decryption)
def search_decrypt(key_square, a, b):
    if a == 'j':
        a = 'i'
    elif b == 'j':
        b = 'i'
    row_a, col_a = divmod(key_square.index(a), 5)
    row_b, col_b = divmod(key_square.index(b), 5)
    if row_a == row_b:
        col_a = (col_a - 1) % 5  # Reverse the column movement
        col_b = (col_b - 1) % 5
    elif col_a == col_b:
        row_a = (row_a - 1) % 5  # Reverse the row movement
        row_b = (row_b - 1) % 5
    else:
        col_a, col_b = col_b, col_a
    return key_square[row_a * 5 + col_a] + key_square[row_b * 5 + col_b]


# Function for performing the encryption
def encrypt(plain, key_square):
    plain = removeSpaces(toLowerCase(plain))
    encrypted = ''
    i = 0
    while i < len(plain):
        if i == len(plain) - 1 or plain[i] == plain[i + 1]:
            encrypted += plain[i] + 'x'
        else:
            encrypted += plain[i] + plain[i + 1]
            i += 1
        i += 1
    result = ''
    for i in range(0, len(encrypted), 2):
        result += search_encrypt(key_square, encrypted[i], encrypted[i + 1])
    return result.upper()


# Function for performing the decryption
def decrypt(ciphertext, key_square):
    # Loại bỏ các khoảng trắng khỏi văn bản mã hóa
    ciphertext = ciphertext.replace(" ", "")

    decrypted = ''
    i = 0
    while i < len(ciphertext):
        a = ciphertext[i].lower()
        if i + 1 < len(ciphertext):
            b = ciphertext[i + 1].lower()
        else:
            # If there's only one character left in the ciphertext, add 'x' to form a digraph
            b = 'x'

        if a == b:  # Trường hợp có cặp ký tự trùng nhau
            b = 'x'
            i -= 1  # Lùi lại 1 vị trí để xử lý cặp ký tự tiếp theo
        decrypted += search_decrypt(key_square, a, b)
        i += 2

    # Kiểm tra xem chuỗi đã giải mã có độ dài lẻ không, nếu có thì thêm 'x' vào cuối
    if len(decrypted) % 2 != 0:
        decrypted += 'x'

    return decrypted.upper()
 



def on_encrypt_button_click():
    plaintext = plaintext_entry.get()
    key = key_entry.get().upper()
    key_square = generateKeyTable(key)
    ciphertext = encrypt(plaintext.upper(), key_square)
    result_label.config(text=f"Ciphertext: {ciphertext}")
    display_matrix(key_square)

def on_decrypt_button_click():
   
    ciphertext = ciphertext_entry.get().upper()
    key = key_entry.get().upper()
    key_square = generateKeyTable(key)
    decrypted_text = decrypt(ciphertext, key_square)
    result_label.config(text=f"Decrypted Text: {decrypted_text}")
    display_matrix(key_square)

def transform_to_unique_list(matrix):
    unique_chars = set()
    unique_list = []

    for row in matrix:
        for char in row:
            if char not in unique_chars:
                unique_list.append(char)
                unique_chars.add(char)

    return unique_list

def transform_to_matrix(unique_list):
    matrix = [unique_list[i:i + 5] for i in range(0, len(unique_list), 5)]
    return matrix

def display_matrix(matrix):
    global matrix_frame

    matrix_frame.grid_forget()
    matrix_frame.destroy()

    unique_list = transform_to_unique_list(matrix)
    matrix = transform_to_matrix(unique_list)

    matrix_frame = ttk.Frame(main_frame, padding="10")
    matrix_frame.grid(column=2, row=0, rowspan=6, sticky=(tk.W, tk.E, tk.N, tk.S))

    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            label = ttk.Label(matrix_frame, text=char)
            label.grid(column=j, row=i, padx=5, pady=5)

# Create the graphical interface
root = tk.Tk()
root.title("Playfair Cipher")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

matrix_frame = ttk.Frame(main_frame, padding="10")
matrix_frame.grid(column=2, row=0, rowspan=6, sticky=(tk.W, tk.E, tk.N, tk.S))

plaintext_label = ttk.Label(main_frame, text="Plaintext:")
plaintext_label.grid(column=0, row=0, sticky=tk.W)

plaintext_entry = ttk.Entry(main_frame, width=30)
plaintext_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))

key_label = ttk.Label(main_frame, text="Key:")
key_label.grid(column=0, row=1, sticky=tk.W)

key_entry = ttk.Entry(main_frame, width=30)
key_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))

encrypt_button = ttk.Button(main_frame, text="Encrypt", command=on_encrypt_button_click)
encrypt_button.grid(column=1, row=2, sticky=tk.E)

ciphertext_label = ttk.Label(main_frame, text="Ciphertext:")
ciphertext_label.grid(column=0, row=3, sticky=tk.W)

ciphertext_entry = ttk.Entry(main_frame, width=30)
ciphertext_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))

decrypt_button = ttk.Button(main_frame, text="Decrypt", command=on_decrypt_button_click)
decrypt_button.grid(column=1, row=4, sticky=tk.E)

result_label = ttk.Label(main_frame, text="")
result_label.grid(column=0, row=5, columnspan=2, sticky=tk.W)

root.mainloop()
