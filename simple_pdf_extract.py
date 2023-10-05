import os
import fitz
import PyPDF2

def convert_pdfs_to_utf8_txt(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_document = fitz.open(input_folder+'\\'+filename, filetype="pdf")
            output_lines = ""

            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)

                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            if "spans" in line:
                                for span in line["spans"]:
                                    font_name = span.get("font", "Unknown")
                                    font_size = span.get("size", 0)
                                    text = span.get("text", "")
                                    output_lines += str(text)

            save_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\pdf_to_txt\\'
            with open(save_path + filename + ".txt", 'w', encoding='utf-8') as file:
                file.write(output_lines)
            print(f'Done with: {filename}')

            file.close()

# Example usage
input_folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\downloaded_pdfs'
output_folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\pdf_to_txt'
convert_pdfs_to_utf8_txt(input_folder_path, output_folder_path)
