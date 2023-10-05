
import re
import os

def remove_single_capital_letters(input_folder):
    # Iterate through text files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            txt_path = os.path.join(input_folder, filename)

            # Read the text content from the input text file
            with open(txt_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()

            # Remove consecutive single capital letters
            cleaned_text = re.sub(r'\b[A-Z](?: [A-Z])+\b', lambda x: x.group().replace(' ', ''), text)

            # Create a txt file for the cleaned text in the same folder
            cleaned_filename = f"cleaned_{filename}"
            cleaned_txt_path = os.path.join(input_folder, cleaned_filename)

            # Write cleaned text to the output txt file
            with open(cleaned_txt_path, 'w', encoding='utf-8') as cleaned_txt_file:
                cleaned_txt_file.write(cleaned_text)

# Example usage
input_folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\temp\\'
remove_single_capital_letters(input_folder_path)