import os
import cv2
import easyocr
import matplotlib.pyplot as plt
from PIL import ImageOps

# Function to flip the image horizontally
def flip_image_horizontally(image_path):
    image = cv2.imread(image_path)
    return cv2.flip(image, 1)

# Function to save extracted text to a file with UTF-8 encoding
def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

# Function to process images in a folder
def process_images_with_easyocr(source_folder, output_folder, text_folder):
    # Ensure the output and text folders exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
    
    # Initialize easyocr Reader
    reader = easyocr.Reader(['en'])  # You can add more languages if needed
    
    # Get a list of image files in the source folder
    image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    
    # Process each image
    for image_file in image_files:
        image_path = os.path.join(source_folder, image_file)
        output_image_path = os.path.join(output_folder, f"out_{image_file}")
        text_file_path = os.path.join(text_folder, f"{os.path.splitext(image_file)[0]}.txt")
        
        # Flip the image horizontally
        flipped_image = flip_image_horizontally(image_path)
        
        # Perform OCR on the flipped image
        result = reader.readtext(flipped_image)
        
        # Save the extracted text to a file
        extracted_text = "\n".join([text for _, text, _ in result])
        save_text_to_file(extracted_text, text_file_path)
        
        # Draw bounding boxes and OCR text on the image
        for (bbox, text, prob) in result:
            # Unpack the bounding box
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            # Draw the bounding box on the image
            cv2.rectangle(flipped_image, top_left, bottom_right, (0, 255, 0), 2)
            # Put the OCR result text
            cv2.putText(flipped_image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save the output image with annotations
        cv2.imwrite(output_image_path, flipped_image)
        
        print(f"Processed {image_file}, extracted text saved to {text_file_path}, image saved to {output_image_path}")

# Define the source and output folders
source_folder = r'C:\Users\prana\Desktop\TechnoGems\Ocr\pix\frames'
output_image_folder = r'C:\Users\prana\Desktop\TechnoGems\Ocr\pix\final2'
text_output_folder = r'C:\Users\prana\Desktop\TechnoGems\Ocr\pix\text2'

# Process the images
process_images_with_easyocr(source_folder, output_image_folder, text_output_folder)
