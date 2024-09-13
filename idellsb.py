from PIL import Image
import os

# Get user input
print("This is the LSB steganography technique, please enter your name.")
name = input("Enter your full name: ")
image_path = input("Enter your image file name\n")


def text_to_binary(text):
    """Convert text to binary string representation."""
    ascii_value_array = []
    for i in name:
        ascii_value = ord(i)
        ascii_value_array.append(ascii_value)

    binary_value_array = []
    for i in ascii_value_array:
        binary_value = bin(i)[2:].zfill(8)  
        binary_value_array.append(binary_value)

    binary_value_array.append("00000000")
    result_string = ''.join(binary_value_array)
    return (result_string)


#def lsb_hide_image(image_path, text, output_image_path, start_pixel=0, channels=['R', 'G', 'B']):

def lsb_hide_image1(text):
    binary_name = text_to_binary(name)
    
    image = Image.open(image_path);

    
lsb_hide_image1(name)
