from PIL import Image
import os

# Get user input
print("This is the LSB steganography technique, please enter your name.")
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

def lsb_hide_image1(text, image_path, output_image_path, start_pixel=0):
    binary_i = 0 #pointer for the current position in the binary version of the name
    pixel_c = 0  #count the pixels that have been modified (length)
   
    # Get the binary of the name
    binary_name = text_to_binary(text)
    
    # Construct the full path of the image file, we assume that the current path to the directory is where the script and the image are being held
    current_path = os.path.join(os.getcwd(), image_path)
    
    # Open the image
    image = Image.open(current_path)
    #we get the pixel data
    pixels = list(image.getdata())

    #first we need to check if the image is rgb, if it is we need to convert it into binary instead of three binary values
    pixel_values = []
    if image.mode == 'RGB':
        for pixel in pixels:
            pixel_values.extend(pixel)
    else: # otherwise it is graayscale and just one set of binary
        pixel_values = pixels
    max_bits = len(binary_name) #max bitrs is how much text is being embded
    pixel_l = len(pixel_values) #total num of pixels so we dont go over

    for i in range(start_pixel, pixel_l):  # Loop through the pixel values starting from the start until the end of the image
        if binary_i < max_bits:  # dont do more than the message is necessary
            pixel_b = bin(pixel_values[i])[2:].zfill(8)  # Make the pixel into a binary, removing the 0b and make it a byte long
            pixel_b_new = pixel_b[:-1] + binary_name[binary_i]  # Replace LSB and make it our name
            pixel_values[i] = int(pixel_b_new, 2)  # Convert thestring back to an integer and update the pixel 
            binary_i += 1  # Move to the next bit in the binary name string
            pixel_c += 1  # Increment the pixel count, 
        else:
            break  # Stop 


    new_pixels = []
    for i in range(0, len(pixel_values), 3):
        pixel_group = pixel_values[i:i + 3]  # Get a group of three pixel values
        pixel_tuple = tuple(pixel_group)     # Convert the list to a tuple
        new_pixels.append(pixel_tuple)       # Append the tuple to the new_pixels list
    #we save the image as lsb_Stego_image
    cover_img = Image.new(image.mode, image.size)
    cover_img.putdata(new_pixels)
    cover_img.save(output_image_path)
    print(f"Image saved as {output_image_path}")

    # Generate the stego key
    stego_key = {
        "start_pixel": start_pixel,
        "bit_position": "LSB",
        "num_pixels_used": pixel_c,
        "channels": ['R', 'G', 'B']
    }

    return stego_key

# Embed name into an image and generate the stego key
stego_key = lsb_hide_image1(name, "pic.jpg", "lsb_stego_image.bmp", start_pixel=1000)

# Print the stego key for reference
print("Stego Key:", stego_key)
