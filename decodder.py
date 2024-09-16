#Lukas Mikulenas
#I pledge my honor that I have abided by the Stevens Honor System
from PIL import Image

def decode_lsb_image(image_path, stego_key):
    """Decode a message hidden in the LSB of an image."""
    
    # Load the image
    image = Image.open(image_path)
    pixels = list(image.getdata())
    
    pixel_values = []
    if image.mode == 'RGB':
        for pixel in pixels:
            pixel_values.extend(pixel)
    else:
        pixel_values = pixels
    
    # Stego key details
    start_pixel = stego_key['start_pixel']
    bit_position = stego_key['bit_position']
    num_pixels_used = stego_key['num_pixels_used']
    channels = stego_key['channels']  # Should be ['R', 'G', 'B'] for RGB images

    # Initialize variables
    binary_message = []
    byte = ''
    decoded_message = ''
    
    # Loop through the pixels to extract the hidden bits
    for i in range(start_pixel, start_pixel + num_pixels_used):
        pixel_binary = bin(pixel_values[i])[2:].zfill(8)  # Get the 8-bit binary value of the pixel

        # Extract the LSB and append it to the binary message
        if bit_position == 'LSB':
            bit = pixel_binary[-1]  # Get the LSB
        else:
            bit = pixel_binary[0]  # For MSB (if needed, but this key uses LSB)
        
        byte += bit
        
        # Once we've collected 8 bits, convert to a character
        if len(byte) == 8:
            character = chr(int(byte, 2))  # Convert from binary to character
            
            # Stop decoding if we encounter the null terminator ('\0')
            if character == '\0':
                break
            
            decoded_message += character
            byte = ''  # Reset byte for next 8 bits

    return decoded_message

# Get image path and stego key information from the user
image_path = input("Enter the stego image file name (e.g., 'lsb_stego_image.bmp'):\n")

# Ask for the stego key details from the user
start_pixel = int(input("Enter the starting pixel index (e.g., 1000):\n"))
bit_position = input("Enter the bit position (LSB or MSB):\n")
num_pixels_used = int(input("Enter the number of pixels used to hide the message (e.g., 200):\n"))
channels_input = input("Enter the channels used (e.g., 'R,G,B'):\n")
channels = channels_input.split(',')

# Create the stego key from user inputs
stego_key = {
    "start_pixel": start_pixel,
    "bit_position": bit_position.upper(),  # Ensure bit position is uppercase for consistency
    "num_pixels_used": num_pixels_used,
    "channels": channels
}

# Decode the hidden message
decoded_message = decode_lsb_image(image_path, stego_key)

# Output the decoded message
print("Decoded Message:", decoded_message)
