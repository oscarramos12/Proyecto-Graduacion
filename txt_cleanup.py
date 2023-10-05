import os
from langdetect import detect
import re
import reports
import nltk
import shutil
import glob
from fuzzywuzzy import fuzz
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_files'
new_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_clean\\'

def all_unique_characters(folder_path):
    data = ""
    folder_path += '\\*.txt'
    for file_path in glob.glob(folder_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            temp_data = file.read()
            data += temp_data
    chars = sorted(list(set(data)))
    report = []
    report.append(str(chars))
    reports.write_report('general_reports','general_reports','Todos los Caracteres',report)
    print("Todos los caracteres en los archivos son: ", ''.join(chars))

def copy_files(folder_path, new_path):
    files_to_move = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    if not os.path.exists(new_path):
        os.makedirs(new_path)
        print(f"{Color.MAGENTA}Se creo el folder: '{new_path}'{Color.RESET}")

    for file_name in files_to_move:
        source_file_path = os.path.join(folder_path, file_name)
        destination_file_path = os.path.join(new_path, file_name)

        shutil.copy(source_file_path, destination_file_path)
    print(f"Se han copiado los archivos")

def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum()]

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    return ' '.join(tokens)

def calculate_cosine_similarity(text1, text2):
    preprocessed_text1 = preprocess_text(text1)
    preprocessed_text2 = preprocess_text(text2)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([preprocessed_text1, preprocessed_text2])

    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return similarity_score

def check_text_similarity(folder_path):
    text_content_list = []

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    txt_files = [f for f in files if f.lower().endswith('.txt')]

    for txt_file in txt_files:
        sinlge_book = []
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
            if(len(text_content) > 2500):
                sinlge_book.append(txt_file)
                sinlge_book.append(text_content[0:2500])
            else:
                sinlge_book.append(txt_file)
                sinlge_book.append(text_content)
            text_content_list.append(sinlge_book)

    if(text_content == ''):
        print('here')

    general_counter = 0
    individual_counter = 0

    duplicate_names = []
    to_be_deleted = []

    while (general_counter < len(text_content_list)):
        individual_counter = 0
        while (individual_counter < len(text_content_list)):
            if(not(individual_counter == general_counter)):
                cosine_similarity = calculate_cosine_similarity(text_content_list[general_counter][1], text_content_list[individual_counter][1])
                levenshtein_distance = fuzz.ratio(text_content_list[general_counter][1], text_content_list[individual_counter][1]) / 100.0
                similarity_score = (cosine_similarity + levenshtein_distance)/2
                similarity_score_string = "{:.3f}".format(similarity_score)
                if(similarity_score >= 0.8 and text_content_list[general_counter][0] not in to_be_deleted):
                    duplicate_names.append([text_content_list[general_counter][0],text_content_list[individual_counter][0],similarity_score_string])
                    to_be_deleted.append(text_content_list[general_counter][0])
                    to_be_deleted.append(text_content_list[individual_counter][0])
            individual_counter += 1
        general_counter += 1

    for duplicate in duplicate_names:
        #os.remove(folder_path + '\\' +  duplicate[0])
        move_file = folder_path + '\\' + duplicate[0]

        destination_folder = folder_path.replace('txt_clean\\','') + 'txt_similar_content'

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            print(f'{Color.MAGENTA} Se ha credo el folder txt_similar_content')

        destination_file = destination_folder + '\\' + duplicate[0]

        shutil.move(move_file, destination_file)

        print(f'{Color.RED}Se ha movido el archivo {Color.BLUE}{duplicate[0]}{Color.RED} ya que el contenido era muy similar a {Color.BLUE}{duplicate[1]} {Color.RED} con una score de {Color.YELLOW}{duplicate[2]}{Color.RESET}')
        reports.write_report('general_reports','general_reports','Contenidos Similares',duplicate)

    

def clean_special_characters(folder_path,new_path):
    special_characters = ['«', '»', '<', '°', '*', '„', '“', '…', '~', '§', '=', '•', ']', '[', '>', '—', '/', '`', '^','-','{','}','‘','’','”','›','¬','ª','´','%','$', '‐', '–', '―', '−','	','_','©','£', 'Æ', '¼', '½', '®', 'µ', '×', 'Ø', '˛', '†', '‹', '⁄', '∫', 'Λ', 'Μ', 'Σ', 'ά', 'έ', 'ή', 'ί', 'α', 'γ', 'ε', 'ι', 'κ', 'λ', 'ν', 'ο', 'π', 'ρ', 'ς', 'σ', 'υ', 'φ', 'χ', 'ω','¢','¨','­·']
    try:
        if not (os.path.exists(new_path) or os.path.exists(folder_path)):
            print("Alguno de los folders no existe")
            return

        if not(len(os.listdir(new_path)) == 0):
            folder_path = new_path
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(new_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                for char in special_characters:
                    if(char == '	'):
                        content = content.replace(char, ' ')
                    else:
                        content = content.replace(char, '')

                with open(new_path + filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                #print(f"Se han quitado los caracteres especiales de:{Color.BLUE} '{filename}'.{Color.RESET}")

        print("Se han quitado los caracteres especiales")
    except Exception as e:
        print(f"{Color.MAGENTA}ERROR: {str(e)}{Color.RESET}")

def fix_spacing(new_path):
    for filename in os.listdir(new_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(new_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                '''
                modified_content = ''

                i = 0
                while i <len(content) - 1:
                    char = content[i]

                    if char == ' ':
                        modified_content += ' '
                        j = i + 1
                        while ((j < len(content)) and (content[j] == ' ')):
                            j += 1
                        i = j
                    if(i >= len(content)):
                        i = len(content) - 1
                    char = content[i]
                    modified_content += char
                    i += 1
                    '''
                modified_content = re.sub(r' +', ' ', content)

            with open(new_path + filename, 'w', encoding='utf-8') as file:
                file.writelines(modified_content)
            print(f"Se han reformateado los espacios en: {Color.BLUE}'{filename}'.{Color.RESET}")

    print("Terminado")



def check_unique_chars(folder_path):
    unique_characters_per_file = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                unique_characters = []
                no_dups = set()
                for line in file:
                    words = re.findall(r'\w+', line)

                    for i, word in enumerate(words):
                        for char in word:
                            if char.lower() not in 'abcdefghijklmnñopqrstuvwxyzáéíóúü1234567890':
                                if(char not in no_dups):
                                    no_dups.add(char)
                                    context_words = words[max(0, i - 3):i] + [word] + words[i + 1:i + 4]
                                    unique_characters.append(char + ' en el contexto: ' + str(context_words))
                    for check_char in line:
                        if((check_char not in '?¿!¡._-:;"&() ,1234567890\n\'') and (check_char not in no_dups) and not(check_char.isalpha())):
                            no_dups.add(check_char)
                            unique_characters.append("El caracter especial: " + check_char + " ha sido encontrado")

                if unique_characters:
                    unique_characters_per_file[filename] = unique_characters

    for filename, characters in unique_characters_per_file.items():
        print(f'{Color.RESET}Caracteres unicos en {Color.BLUE} [{filename}]{Color.RESET}:')
        for char_info in characters:
            print(f'{Color.YELLOW} {char_info}{Color.RESET}')

    return unique_characters_per_file.items()

def fix_seperation_errors(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                original_text = file.read()

            processed_text = re.sub(r'(?<=[a-z])\s*([A-Z])', r' \1', original_text)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(processed_text)

def remove_first_space(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            updated_lines = []

            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if(len(lines) > 1):
                    for line in lines:
                        updated_line = line.lstrip() if line and line[0] == ' ' else line
                        updated_lines.append(updated_line)
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(updated_lines)  
                elif(lines[0] == ' '):
                    updated_lines = lines[1:]
                    with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(updated_lines)

    print('Se han quitado los espacios del inicio')

def delete_special_text(folder_path, phrases_to_delete):
    for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                for phrase in phrases_to_delete:
                    content = content.replace(phrase, '')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

    print(f'Se han eliminado las frases especiales')

def delete_empty_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.getsize(file_path) == 0:
                    print(f"{Color.RED}El archivo: [{filename}] esta vacio por lo que se ha borrado{Color.RESET}")
                    reports.write_report('general_reports','general_reports','Archivos Vacios',[filename])
                    os.remove(file_path)
            except os.error as e:
                print(f"Error: {filename}, {e}")

def check_language(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                language = detect(text)
                if(language != 'es'):
                    report = [filename, language]
                    reports.write_report('general_reports','general_reports','Idiomas Diferentes',report)
                    print(f"{Color.RED}El archivo {Color.RESET}{filename}{Color.RED} no esta en español, por lo que ha sido borrado{Color.RESET}")
                    file.close()
                    os.remove(file_path)
        except Exception as e:
            print(f"Error abriendo el archivo: {filename} o detectando idioma: {e}")
            return None
    print('Analisis de Idioma terminado')

delete_phrases = ['EDITORIAL SUDAMERICANAQueda hecho el depósitoque previene la ley 11.723.1994, Editorial Sudamericana S.A.,Humberto 1531, Buenos AiresDerechos exclusivos para ARGENTINA, CHILE,URUGUAY y PARAGUAY: EDITORIAL SUDAMERICANA S.A.,Humberto 1531, Buenos Aires, Argentina.',
                  'textos disponibles en http://www.textos.infoCon',
                  'ebookelo.com - Página 89',
                  '¿Te gustó este libro? Para más e Books GRATUITOS visita  freeditorial.comes',
                  'LA SOMBRA SOBRE INNSMOUTH   H. P. LOVECRAFT ',
                  '..............................................................................',
                  'EDITORIAL SUDAMERICANA Queda hecho el depósito que previene la ley 11.723.',
                  '1994, Editorial Sudamericana S.A., Humberto 1531, Buenos Aires Derechos exclusivos para ARGENTINA, CHILE, URUGUAY y PARAGUAY: EDITORIAL SUDAMERICANA S.A., Humberto 1531,',
                  'Buenos Aires, Argentina.',
                  'Parte primera ......................................................................... 5 Parte segunda .......................................................................12 Parte tercera .........................................................................23 ESCENA I........................................................................24 ESCENA II.......................................................................25 ESCENA III .....................................................................30 ESCENA IV .....................................................................35 Parte cuarta...........................................................................36']

#copy_files(folder_path, new_path)
#delete_empty_files(new_path)
#check_language(new_path)#
#remove_first_space(new_path)#
#fix_spacing(new_path)
#check_unique_chars(new_path)
#clean_special_characters(folder_path,new_path)
#check_text_similarity(new_path)
#all_unique_characters(new_path)
#fix_seperation_errors(new_path)
delete_special_text(new_path,delete_phrases)

