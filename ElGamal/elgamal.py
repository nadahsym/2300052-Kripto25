def generate_key_elgamal(p, g, x):
    """Menghitung kunci publik y = g^x mod p"""
    y = pow(g, x, p)
    return y

def enkripsi_elgamal(plaintext, p, g, y, k):
    """Melakukan enkripsi Plain Text."""
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = []
    
    # C1 = g^k mod p
    C1 = pow(g, k, p) 
    
    # y_k = y^k mod p
    y_k = pow(y, k, p)

    for char_pt in plaintext:
        M = ord(char_pt) - ord('A')
        
        # C2 = M * y^k mod p
        C2 = (M * y_k) % p
        
        ciphertext.append((C1, C2))
        
    return ciphertext

def dekripsi_elgamal(ciphertext, p, x):
    """Melakukan dekripsi Cipher Text."""
    plaintext = ""
    
    for C1, C2 in ciphertext:
        # Menghitung invers modular (C1^x)^-1 mod p
        # Rumus: a^-1 = a^(p-1-x) mod p
        # Pengecekan: Pastikan C1^x dan p saling prima, yang diasumsikan valid.
        C1_x_inv = pow(C1, p - 1 - x, p) 
        
        # M = C2 * (C1^x)^-1 mod p
        M = (C2 * C1_x_inv) % p
        
        plaintext += chr(M + ord('A'))
        
    return plaintext

# --- Interaksi ElGamal Algorithm ---
print("\n=== ElGamal Algorithm (Input Pengguna) ===")
try:
    p = int(input("Masukkan p (Bilangan Prima): "))
    g = int(input("Masukkan g (Akar Primitif): "))
    x = int(input("Masukkan x (Kunci Privat): "))
    k = int(input("Masukkan k (Kunci Sementara): "))
    pt_elgamal = input("Masukkan Plain Text (hanya huruf): ")
except ValueError:
    print("Input harus berupa angka atau teks yang valid.")
    exit()

# 1. Kunci Publik
y = generate_key_elgamal(p, g, x)

# 2. Enkripsi
ct_elgamal = enkripsi_elgamal(pt_elgamal, p, g, y, k)

# 3. Dekripsi
dt_elgamal = dekripsi_elgamal(ct_elgamal, p, x)

print("\n--- Hasil ---")
print(f"Parameter: p={p}, g={g}, x={x}, k={k}")
print(f"Kunci Publik (y): {y}")
print(f"Plain Text Input: {pt_elgamal.upper().replace(' ', '')}")
print(f"Cipher Text (pasangan C1, C2): \n{ct_elgamal}")
print(f"Dekripsi: {dt_elgamal}")