from PIL import Image

def text_to_bits(text):
    """Mengubah string teks menjadi string bit (0s dan 1s)"""
    bits = bin(len(text))[2:].zfill(16)  
    for char in text:
        bits += bin(ord(char))[2:].zfill(8)
    return bits

def bits_to_text(bits):
    """Mengubah string bit menjadi string teks"""
    text = ""
    length_bits = bits[:16]
    message_length = int(length_bits, 2)
    
    message_bits = bits[16:]
    
    if len(message_bits) < message_length * 8:
        print("Error: Panjang bit yang diekstrak tidak sesuai dengan header.")
        return ""

    for i in range(0, message_length * 8, 8):
        byte = message_bits[i:i+8]
        if byte:
            text += chr(int(byte, 2))
    return text

# ENCODE

def encode_image(image_path, secret_message, output_path):
    """Menyisipkan pesan rahasia ke dalam citra menggunakan LSB."""
    try:
        img = Image.open(image_path).convert("RGB")
        width, height = img.size
        
        binary_message = text_to_bits(secret_message)
        data_len = len(binary_message)

        max_capacity = width * height * 3
        if data_len > max_capacity:
            print("Error: Pesan terlalu panjang untuk disembunyikan di dalam gambar ini.")
            return

        print(f"Pesan (termasuk header panjang) memiliki {data_len} bit.")
        print(f"Kapasitas gambar: {max_capacity} bit.")

        message_index = 0
        for x in range(width):
            for y in range(height):
                pixel = list(img.getpixel((x, y)))
                
                for i in range(3):
                    if message_index < data_len:
                        bit_to_hide = int(binary_message[message_index])
                        
                        pixel[i] = (pixel[i] & 254) | bit_to_hide
                        
                        message_index += 1
                
                img.putpixel((x, y), tuple(pixel))
                
                if message_index >= data_len:
                    break
            if message_index >= data_len:
                break
            
        img.save(output_path)
        print(f"\nSukses menyisipkan pesan! Stego-Image tersimpan di: {output_path}")

    except FileNotFoundError:
        print(f"\nError: File gambar tidak ditemukan di {image_path}")
    except Exception as e:
        print(f"\nTerjadi error saat encoding: {e}")

# DECODE

def decode_image(stego_image_path):
    """Mengekstrak pesan rahasia dari citra stego-object."""
    try:
        img = Image.open(stego_image_path).convert("RGB")
        width, height = img.size
        
        extracted_bits = ""
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                
                for i in range(3):
                    extracted_bits += str(pixel[i] & 1)

                    if len(extracted_bits) == 16:
                        message_length = int(extracted_bits, 2)
                        
                        total_bits_to_extract = 16 + message_length * 8
                        print(f"Panjang pesan (dari header): {message_length} karakter.")
                        
                        if total_bits_to_extract > width * height * 3:
                            print("Error: Header menunjukkan pesan lebih panjang dari kapasitas gambar.")
                            return "Pesan tidak valid atau gambar rusak."
                            
                    if 'total_bits_to_extract' in locals() and len(extracted_bits) >= total_bits_to_extract:
                        break
            
            if 'total_bits_to_extract' in locals() and len(extracted_bits) >= total_bits_to_extract:
                break

        if 'total_bits_to_extract' in locals():
            final_bits = extracted_bits[:total_bits_to_extract]
            secret_text = bits_to_text(final_bits)
            return secret_text
        else:
            return "Tidak ada header panjang pesan yang terdeteksi."


    except FileNotFoundError:
        return f"Error: File gambar tidak ditemukan di {stego_image_path}"
    except Exception as e:
        return f"Terjadi error saat decoding: {e}"

if __name__ == "__main__":
    COVER_IMAGE = "input.png" 
    SECRET_MESSAGE = "rora cakep bgt gile"
    STEGO_IMAGE = "output.png"

    print("--- Proses ENCODING (Menyisipkan Pesan) ---")
    encode_image(COVER_IMAGE, SECRET_MESSAGE, STEGO_IMAGE)
    
    print("\n" + "="*50 + "\n")

    print("--- Proses DECODING (Mengekstrak Pesan) ---")
    extracted_message = decode_image(STEGO_IMAGE)
    print(f"Pesan yang Diekstrak: {extracted_message}")