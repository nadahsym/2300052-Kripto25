from PIL import Image
import numpy as np

def extract_lsb(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    data = np.array(img)

    # Ambil LSB dari semua channel RGB
    bits = (data & 1).flatten()
    bytes_ = [bits[i:i+8] for i in range(0, len(bits), 8)]

    message = ""
    for byte in bytes_:
        char = chr(int("".join(map(str, byte)), 2))
        # hentikan jika karakter tidak masuk akal
        if not 32 <= ord(char) <= 126:  
            continue
        message += char

    print(message[:25])  # tampilkan sebagian
    return message

extract_lsb("stego.png")
