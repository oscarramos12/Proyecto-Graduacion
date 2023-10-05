import fitz
import re
import os
import PyPDF2
import scraper
import reports
import time

'''
RETOS:
    -la font liberation seriff no la puede leer fitz que es la libreria que me deja acceder a los datos de la font
    por lo que tuve que usar Py2PDF lo cual hace que se tarde mas

    -los archivos de google drive no se pueden descargar solo asi por lo que se tiene que editar el link para que sea directo

    -aparte de que sea directo se necesitan los headers para obtener el nombre del archivo

    -se tuvieron que hacer similaridad de jaccard y distancia de levenshtein para evaluar que no se descargue el mismo libro 2 veces
'''

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def is_number(line):
    number_pattern = r'^[1-9][0-9]*$'  
    return bool(re.match(number_pattern, line))

def is_capitulo(line):

    toLower = line.lower()
    toLower = toLower.replace(" ", "")
    if((toLower.find("capitulo") or toLower.find("capítulo")) and (len(toLower) < 20) and not('.' in toLower)):
        return True
    return False


def extract_and_append_lines(pdf_file, target_font_name, target_font_size, output_file):
    pdf_document = fitz.open(pdf_file, filetype="pdf")
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




                            if (font_name == target_font_name and font_size == target_font_size and not is_number(text) and not is_capitulo(text)):
                                if(len(text) > 0 and text[len(text) - 1] == '.'):
                                    text += '\n'
                                output_lines += str(text) + ' '

    save_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_files\\'
    output_file = output_file.split('.pdf')[0]
    with open(save_path + output_file + ".txt", 'w', encoding='utf-8') as file:
        file.write(output_lines)

    file.close()

def do_folder(folder_path):
      

    all_files_and_folders = os.listdir(folder_path)

    file_names = [item for item in all_files_and_folders if os.path.isfile(os.path.join(folder_path, item))]
    return file_names

def check_txt_duplicates(txt_folder):
    all_files_and_folders = os.listdir(txt_folder)

    file_names = [scraper.format(item) for item in all_files_and_folders if os.path.isfile(os.path.join(txt_folder, item))]
    return file_names


def bad_font_file(file,target_font,target_size):
    print(f"{Color.BLUE}La font de este archivo no se puede descifrar, se tendran que tomar pasos extra{Color.RESET}")
    pdf_file = "C:\\Users\\Oscar\\Desktop\\LIBROS\\downloaded_pdfs\\" + file
    docx_file_name = file.split(".")[0]
    txt_directory = "C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_files\\" + docx_file_name + ".txt"
    
    pdf_document = PyPDF2.PdfReader(open(pdf_file, "rb"))
    pdf_document_font_check = fitz.open(pdf_file, filetype="pdf")

    font_sizes_count = {}
    font_types_count = {}

    whole_text = ""

    with open(txt_directory, "w", encoding="utf-8") as txt_output_file:
        for page_number in range(len(pdf_document.pages)):
            page = pdf_document.pages[page_number]
            page_font_check = pdf_document_font_check.load_page(page_number)
            clean_text = page.extract_text()
            clean_text = clean_text.split('\n')
            total_words = 0
            for block in page_font_check.get_text("dict")["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        if "spans" in line:
                            for span in line["spans"]:
                                font_size = span.get("size", 0)
                                font_name = span.get("font", "Unknown")
                                ugly_text = span.get("text", "")
                                total_words += + 1

                                if font_size in font_sizes_count:
                                    font_sizes_count[font_size] += 1
                                else:
                                    font_sizes_count[font_size] = 1

                                if font_name in font_types_count:
                                    font_types_count[font_name] += 1
                                else:
                                    font_types_count[font_name] = 1

            font_sizes_count = dict(sorted(font_sizes_count.items(), key=lambda item: item[1], reverse=True))
            font_types_count = dict(sorted(font_types_count.items(), key=lambda item: item[1], reverse=True))

            
            get_font_size = next(iter(font_sizes_count))
            get_font_types = next(iter(font_types_count))
            get_count = next(iter(font_sizes_count.values()))
            if(total_words != 0):
                prescence = get_count / total_words
            else:
                prescence = 0
            '''
            print(ugly_text)

            print(get_font_size)
            print(get_font_types)
            '''
            if(get_font_size == target_size and get_font_types == target_font and prescence > 0.7):
                new_text =  page.extract_text()

                #if('	' in new_text):
                    #new_text = new_text.replace("	", " ")

                new_text_split = new_text.split('\n')
                edit_text = ""
                for line in new_text_split:
                    line_toLower = line.lower()
                    if(len(line_toLower) > 0 and not(is_number(line_toLower))):
                        if(("capitulo" or "capítulo" in line_toLower) and (len(line_toLower) < 18) and not(line_toLower[len(line_toLower) - 1] == '.')):
                            pass
                        elif(line[len(line) - 1] == '.'):
                            edit_text += line + '\n'
                        else:
                            edit_text += line + ' '
                whole_text += edit_text
        txt_output_file.write(whole_text)
    txt_output_file.close()    
    print("DONE")
    print("-------------------------------------------------------------------------------")


def convert_to_txt(folder_path):
    
    bad_fonts = ['LiberationSerif']
    file_names = do_folder(folder_path)
    txt_dups = check_txt_duplicates('C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_files\\')
    for file in file_names:
        if('.pdf' in file):
            clean_file_name = scraper.format(file.split('.')[0])
            if(clean_file_name not in txt_dups):
                pdf_file = folder_path + file
                font_sizes_count, font_types_count = reports.extract_font_info(pdf_file)

                print("-------------------------------------------------------------------------------")
                print("FILE: " + file)
                print("Estadisticas tamaños de font:")
                print(font_sizes_count)            
                print("Estadisticas tipos de font:")
                print(font_types_count)

                top_font_size = next(iter(font_sizes_count))
                top_font_name = next(iter(font_types_count))
                
                
                if(top_font_name in bad_fonts):
                    bad_font_file(file,top_font_name,top_font_size)
                else:
                    extract_and_append_lines(pdf_file, top_font_name, top_font_size, file)
            else:
                print(f"{Color.YELLOW}El archivo [{clean_file_name}] ya habia sido procesado{Color.RESET}")


def get_links_from_file(file_path):
    split_contents = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            split_contents = file.read().split('\n')
    except FileNotFoundError:
        print(f"No se encontro el archivo: {file_path}")
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")

    return split_contents

def main():
    #all_links = get_links_from_file('C:\\Users\\Oscar\\Desktop\\LIBROS\\download_links.txt')
    #for link in all_links:
        #if(not(link == '\n') or not(link == ' ')):
            #time.sleep(10)
            #scraper.scrape_books(link)
            #print(f'Se completaron las descargas de {link}')
            #reports.write_report('general_reports','general_reports','Links Recorridos',[link])
    #folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\downloaded_pdfs\\'
    #convert_to_txt(folder_path)
    pass
    
    

if __name__ == "__main__":
    main()
