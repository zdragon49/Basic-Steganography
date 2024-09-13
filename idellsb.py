from PIL import Image
import os

# Get user input
print("This is the LSB steganography technique, please enter your name.")
name = input("Enter your full name: ")
image_path = input("Enter your image file name. This program assumes that you have the image and the current script running in the same folder:\n")


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
    #we get the name of the person first wrote
    binary_name = text_to_binary(name)
    #this gets the current path of the image assuming its in the same directory
    current_path = os.getcwd()
    current_path = current_path + image_path
    #open the image
    image = Image.open(current_path);
    #we get the pixels
    pixels = list(image.getdata())  

    #array to hold the vlaues of the rgb pixesl
    pixel_values = []

    #check what kind of image it is, if its RGB we add it to the array 
    if image.mode == 'RGB':  
        for pixel in pixels:
            pixel_values.extend(pixel)
    else:
        # no need to do it for grayscale
        pixel_values = pixels

    
lsb_hide_image1(name)
