import numpy as np

def mod_inverse(a, m):
    """Mencari inverse dari a (mod m)."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def text_to_numbers(text):
    text = text.replace(" ", "").upper()
    return [ord(c) - 65 for c in text]

def numbers_to_text(numbers):
    return ''.join(chr(n + 65) for n in numbers)

# ------------------------
# Enkripsi
# ------------------------

def hill_encrypt(plaintext, key):
    nums = text_to_numbers(plaintext)

    # padding jika ganjil
    if len(nums) % 2 != 0:
        nums.append(23)  # huruf X

    cipher = []

    for i in range(0, len(nums), 2):
        block = np.array(nums[i:i+2])
        enc = np.dot(key, block) % 26
        cipher.extend(enc)

    return numbers_to_text(cipher)

# ------------------------
# Dekripsi
# ------------------------

def hill_decrypt(ciphertext, key):
    det = int(round(np.linalg.det(key))) % 26
    det_inv = mod_inverse(det, 26)

    if det_inv is None:
        return None  # menandakan kunci tidak valid

    # matriks adjoin
    adj = np.array([
        [key[1][1], -key[0][1]],
        [-key[1][0], key[0][0]]
    ])

    inv_key = (det_inv * adj) % 26

    nums = text_to_numbers(ciphertext)
    plain = []

    for i in range(0, len(nums), 2):
        block = np.array(nums[i:i+2])
        dec = np.dot(inv_key, block) % 26
        plain.extend(dec)

    return numbers_to_text(plain)

# ------------------------
# Input Matrix
# ------------------------

def input_key_matrix():
    print("\nMasukkan key matrix 2x2:")
    a = int(input("a11: "))
    b = int(input("a12: "))
    c = int(input("a21: "))
    d = int(input("a22: "))
    return np.array([[a, b], [c, d]])

# ------------------------
# Menu Utama
# ------------------------

def main():
    while True:
        print("\n=== MENU HILL CIPHER ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")

        pilihan = input("Pilih menu (1/2/3): ")

        # ---------------- ENKRIPSI ----------------
        if pilihan == "1":
            plaintext = input("\nMasukkan plaintext: ")
            key = input_key_matrix()
            ciphertext = hill_encrypt(plaintext, key)
            print("\nCiphertext:", ciphertext)

        # ---------------- DEKRIPSI ----------------
        elif pilihan == "2":
            ciphertext = input("\nMasukkan ciphertext: ")
            key = input_key_matrix()

            hasil = hill_decrypt(ciphertext, key)
            if hasil is None:
                print("\nKunci TIDAK memiliki invers modulo 26. Dekripsi tidak bisa dilakukan.")
            else:
                print("\nPlaintext:", hasil)

        # ---------------- KELUAR ----------------
        elif pilihan == "3":
            print("Keluar...")
            break

        else:
            print("Pilihan tidak valid!")

# Jalankan program
main()
