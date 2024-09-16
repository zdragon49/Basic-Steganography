# Lukas Mikulenas
# I pledge my honor that I have abided by the Stevens Honor System
from PIL import Image
import os

# Get user input
print("This is the MSB steganography technique, please enter your name.")
name = input("Enter your full name: ")
image_path = input("Enter your image file name. This program assumes that you have the image and the current script running in the same folder:\n")

def text_to_binary(text):
    """Convert text to binary string representation."""
    
    #char to ascii
    ascii_value_array = []
    for i in name:
        ascii_value = ord(i)
        ascii_value_array.append(ascii_value)
    #ascii to binary
    binary_value_array = []
    for i in ascii_value_array:
        binary_value = bin(i)[2:].zfill(8)  
        binary_value_array.append(binary_value)
    #add a null terminator and then append to single string
    binary_value_array.append("00000000")
    result_string = ''.join(binary_value_array)
    return (result_string)

def msb_hide_image(text, image_path, output_image_path, start_pixel=0):
    binary_i = 0  # Pointer for the current position in the binary version of the name
    pixel_c = 0   # Count the pixels that have been modified (length)
    
    # Get the binary of the name
    binary_name = text_to_binary(text)
    
    # Construct the full path of the image file
    current_path = os.path.join(os.getcwd(), image_path)
    
    # Open the image
    image = Image.open(current_path)
    # Get the pixel data
    pixels = list(image.getdata())

    #first we need to check if the image is rgb, if it is we need to convert it
    pixel_values = []
    if image.mode == 'RGB':
        for pixel in pixels:
            pixel_values.extend(pixel)
    else:  # Grayscale image
        pixel_values = pixels
    
    max_bits = len(binary_name)  # Number of bits to be embedded
    pixel_l = len(pixel_values)  # Total number of pixel values

    for i in range(start_pixel, pixel_l):
        if binary_i < max_bits:
            pixel_b = bin(pixel_values[i])[2:].zfill(8)  # Convert pixel value to 8-bit binary string
            # Replace MSB and keep the rest of the bits unchanged
            pixel_b_new = binary_name[binary_i] + pixel_b[1:]# this is the main difference between LSB and MSB
            pixel_values[i] = int(pixel_b_new, 2)  # Convert binary string back to integer
            binary_i += 1
            pixel_c += 1
        else:
            break

    # Reconstruct the image from the modified pixel values
    new_pixels = []
    for i in range(0, len(pixel_values), 3):
        pixel_group = pixel_values[i:i + 3]  # Get a group of three pixel values
        pixel_tuple = tuple(pixel_group)     # Convert the list to a tuple
        new_pixels.append(pixel_tuple)       # Append the tuple to the new_pixels list
    
    # Save the image with embedded data
    cover_img = Image.new(image.mode, image.size)
    cover_img.putdata(new_pixels)
    cover_img.save(output_image_path)
    print(f"Image saved as {output_image_path}")

    # Generate the stego key
    stego_key = [start_pixel, "MSB", pixel_c, ["RGB"]]

    return stego_key

# Embed name into an image and generate the stego key
stego_key = msb_hide_image(name, "pic.jpg", "msb_stego_image.bmp", start_pixel=1000)

# Print the stego key for reference
print("Stego Key:", stego_key)
