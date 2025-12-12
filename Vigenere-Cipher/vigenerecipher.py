def enkripsi_vigenere(plaintext, kunci):
    """Melakukan enkripsi Plain Text menggunakan Vigenere Cipher."""
    ciphertext = ""
    plaintext = plaintext.upper().replace(" ", "")
    kunci = kunci.upper().replace(" ", "")
    panjang_kunci = len(kunci)

    for i, char_pt in enumerate(plaintext):
        pt_val = ord(char_pt) - ord('A')
        key_char = kunci[i % panjang_kunci]
        key_val = ord(key_char) - ord('A')
        
        # Rumus Enkripsi: E = (PT + K) mod 26
        ct_val = (pt_val + key_val) % 26
        
        ciphertext += chr(ct_val + ord('A'))
        
    return ciphertext

def dekripsi_vigenere(ciphertext, kunci):
    """Melakukan dekripsi Cipher Text menggunakan Vigenere Cipher."""
    plaintext = ""
    ciphertext = ciphertext.upper().replace(" ", "")
    kunci = kunci.upper().replace(" ", "")
    panjang_kunci = len(kunci)

    for i, char_ct in enumerate(ciphertext):
        ct_val = ord(char_ct) - ord('A')
        key_char = kunci[i % panjang_kunci]
        key_val = ord(key_char) - ord('A')
        
        # Rumus Dekripsi: D = (CT - K) mod 26
        pt_val = (ct_val - key_val + 26) % 26
        
        plaintext += chr(pt_val + ord('A'))
        
    return plaintext

# --- Interaksi Vigenere Cipher ---
print("=== Vigenere Cipher (Input Pengguna) ===")
pt_vigenere = input("Masukkan Plain Text (hanya huruf): ")
kunci_vigenere = input("Masukkan Kunci (hanya huruf): ")

ct_vigenere = enkripsi_vigenere(pt_vigenere, kunci_vigenere)
dt_vigenere = dekripsi_vigenere(ct_vigenere, kunci_vigenere)

print("\n--- Hasil ---")
print(f"Plain Text Input: {pt_vigenere.upper().replace(' ', '')}")
print(f"Kunci:            {kunci_vigenere.upper().replace(' ', '')}")
print(f"Cipher Text:      {ct_vigenere}")
print(f"Dekripsi:         {dt_vigenere}")