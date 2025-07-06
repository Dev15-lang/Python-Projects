import qrcode

def main():
    # Prompt user for input
    data = input("Enter the text or URL to encode in the QR code: ")
    if not data.strip():
        print("No input provided. Exiting.")
        return

    # Generate QR code
    img = qrcode.make(data)

    # Save the image
    filename = "qrcode.png"
    img.save(filename)
    print(f"QR code saved as {filename}")

if __name__ == "__main__":
    main() 