import os
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import spacy
import re
import reports
import time


class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def format(name):
    name = name.lower()
    name = name.replace("-", " ")
    name = name.replace('_', ' ')
    name = name.split('.')[0]
    return name
    

def create_token_list(nlp):
    token_list = []

    folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\downloaded_pdfs'
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for file_name in file_names:
        token_list.append([token.text.lower() for token in nlp(format(file_name))])

    if(len(token_list) == 0):
        token_list.append([token.text.lower() for token in nlp(format("-"))])
    return token_list


def create_simple_name_list():
    name_list = []
    folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\downloaded_pdfs'
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for file_name in file_names:
        name_list.append(format(file_name))

    if(len(name_list) == 0):
        name_list.append("-")

    return name_list


def check_dups(name_check, token_list,name_list, nlp,pdf_url):
    #print(token_list)
    name_check = format(name_check)

    token_1 = [token.text.lower() for token in nlp(name_check)]

    get_simple_name = 0

    for names in token_list:

        token_2 = names

        intersection = len(set(token_1).intersection(token_2))
        union = len(set(token_1).union(token_2))
        jaccard_similarity = intersection / union if union > 0 else 0.0

        levenshtein_distance = fuzz.ratio(name_check, name_list[get_simple_name]) / 100.0

        threshold = 0.55

        overall_similarity = (jaccard_similarity + levenshtein_distance) / 2.0

        if overall_similarity >= threshold:
            print(f"{Color.YELLOW}--Los archivos [{name_check}] y [{name_list[get_simple_name]}] son demasiado similares por lo que fueron descartados, {Color.CYAN}SCORE: {overall_similarity}--{Color.RESET}")
            reports.write_report('general_reports','general_reports', 'Archivos Duplicados', [name_check,name_list[get_simple_name],overall_similarity,pdf_url])
            get_simple_name += 1
            return True

        else:
            get_simple_name += 1
    return False

def scrape_books(url):

    nlp = spacy.load("es_core_news_sm")
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        download_links = soup.find_all('a')

        current_file_path = os.path.abspath(__file__)
        current_directory =  os.path.dirname(current_file_path)
        current_directory = current_directory.replace('scraper.py', '')
        prefix = current_directory + '\\downloaded_pdfs\\'
        if not os.path.exists(prefix):
            os.makedirs(prefix)
            print(f"{Color.MAGENTA}Se creo el folder downloaded_pdfs{Color.RESET}")

        os.makedirs(prefix, exist_ok=True)
        file_list = create_token_list(nlp)
        simple_name_list = create_simple_name_list()

        print("----------------------------------Inicio descargas------------------------------------")

        for link in download_links:
            
            pdf_url = link['href']
            pdf_name = os.path.basename(pdf_url)
            pdf_path = os.path.join(prefix, pdf_name)
            
            if pdf_url.endswith('.pdf'):

                time.sleep(3)
                #verifica que los nombres no sean similare
                if not check_dups(pdf_name, file_list,simple_name_list,nlp,pdf_url):
                    pdf_response = requests.get(pdf_url)
                    if pdf_response.status_code == 200:
                        file_list.append([token.text.lower() for token in nlp(format(pdf_name))])
                        simple_name_list.append(format(pdf_name))
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_response.content)
                        print(f"{Color.GREEN}Se ha descargado: [{pdf_name}]{Color.RESET}")
                        downloads_list = [pdf_name, pdf_url]
                        reports.write_report('general_reports','general_reports','Archivos Descargados', downloads_list)
                    else:
                        print(f"{Color.RED}Error de descarga: [{pdf_name}]{Color.RESET}")

            elif "drive.google.com" in pdf_url:

                time.sleep(3)

                #https://drive.google.com/open?id=134ogJz8Pub8GoZ9cTMD60plz0xQk5yhS
                if("/file/d/" in pdf_url):
                    file_id = pdf_url.split("/file/d/")[1].split("/")[0]
                    file_id = 'https://drive.google.com/uc?id=' + file_id
                    response = requests.get(file_id)
                elif("open?id=" in pdf_url):
                    file_id = pdf_url.split("id=")[1]
                    file_id = 'https://drive.google.com/uc?id=' + file_id
                    response = requests.get(file_id)
                else:
                    file_id = pdf_url
                    response = requests.get(pdf_url)

                if response.status_code == 200:

                    content_disposition = response.headers.get("Content-Disposition")
                    if content_disposition:
                       filename_match = re.search(r'filename="(.+)"', content_disposition)
                    if filename_match:
                        filename = filename_match.group(1)
                    else:
                        filename = "downloaded_file.pdf"

                    if not check_dups(filename, file_list,simple_name_list,nlp,pdf_url):
                        with open(prefix + filename , "wb") as pdf_file:
                            pdf_file.write(response.content)
                        print(f"{Color.GREEN}Se ha descargado: [{filename}]{Color.RESET}")
                        downloads_list = [filename, pdf_url]
                        reports.write_report('general_reports','general_reports','Archivos Descargados', downloads_list)
                        file_list.append([token.text.lower() for token in nlp(format(filename))])
                        simple_name_list.append(format(filename))
                else:
                    print(f"{Color.RED}Error de descarga:{pdf_url} | code:{response.status_code} {Color.RESET}")
                    report = 'Error de descarga: ' + pdf_url
                    reports.write_report('general_reports','general_reports','Errores Descargas',[pdf_url,response.status_code])

        print("Se han descargado todos los pdfs")
        print("-------------------------------------Fin descargas------------------------------------")
        #print("LSIT:" + str(file_list))
    else:
        print("Failed to fetch the web page.")

