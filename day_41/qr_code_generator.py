import qrcode
from PIL import Image
import os

def add_logo_to_qr(qr_image, logo_path, output_path):
    """
    Add a logo to the center of the QR code and save the result.
    """
    try:
        # Open the QR code and logo images
        qr = Image.open(qr_image)
        logo = Image.open(logo_path)

        # Convert images to RGBA if not already
        qr = qr.convert("RGBA")
        logo = logo.convert("RGBA")

        # Calculate the size of the logo (1/4th of QR code size)
        qr_width, qr_height = qr.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Calculate position to place the logo (center)
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        # Paste the logo onto the QR code
        qr.paste(logo, logo_position, logo)

        # Save the final image
        qr.save(output_path, "PNG")
        print(f"✅ QR code with logo saved as '{output_path}'")
    except Exception as e:
        print(f"❌ Error adding logo: {e}")

def generate_qr_code(text, output_path="qr_code.png", logo_path=None):
    """
    Generate a QR code from the given text and save it as an image.
    Optionally add a logo in the center.
    """
    try:
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
            box_size=10,
            border=4,
        )

        # Add the text/URL to the QR code
        qr.add_data(text)
        qr.make(fit=True)

        # Create the QR code image
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Save the initial QR code
        temp_path = "temp_qr_code.png"
        img.save(temp_path, "PNG")

        if logo_path and os.path.exists(logo_path):
            # Add logo to the QR code
            add_logo_to_qr(temp_path, logo_path, output_path)
            # Remove the temporary file
            os.remove(temp_path)
        else:
            # Save the QR code without a logo
            img.save(output_path, "PNG")
            print(f"✅ QR code saved as '{output_path}'")

    except Exception as e:
        print(f"❌ Error generating QR code: {e}")

def main():
    print("🎯 Day 41: QR Code Generator")
    # Get user input
    text = input("Enter text or URL to generate QR code: ").strip()
    output_path = input("Enter output file name (default: qr_code.png): ").strip() or "qr_code.png"
    logo_choice = input("Do you want to add a logo to the QR code? (y/n): ").strip().lower()
    
    logo_path = None
    if logo_choice == 'y':
        logo_path = input("Enter path to logo image (PNG format): ").strip()
        if not os.path.exists(logo_path):
            print(f"⚠️ Logo file '{logo_path}' not found. Proceeding without logo.")
            logo_path = None

    # Generate the QR code
    generate_qr_code(text, output_path, logo_path)

if __name__ == "__main__":
    main()