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
    special_characters = ['«', '»', '<', '°', '*', '„', '“', '…', '~', '§', '=', '•', ']', '[', '>', '—', '/', '`', '^','-','{','}','‘','’','”','›','¬','ª','´','%','$', '‐', '–', '―', '−','	','_','©','£', 'Æ', '¼', '½', '®', 'µ', '×', 'Ø', '˛', '†', '‹', '⁄', '∫', 'Λ', 'Μ', 'Σ', 'ά', 'έ', 'ή', 'ί', 'α', 'γ', 'ε', 'ι', 'κ', 'λ', 'ν', 'ο', 'π', 'ρ', 'ς', 'σ', 'υ', 'φ', 'χ', 'ω','¢','¨','­·','\xad','\xa0','\u200b','+','|','\\','′''¸', '·', '#','¸']
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
                modified_content = modified_content.replace('  ',' ')

            with open(new_path + filename, 'w', encoding='utf-8') as file:
                file.writelines(modified_content)
            #print(f"Se han reformateado los espacios en: {Color.BLUE}'{filename}'.{Color.RESET}")

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
                        if(not(line == '\n')):
                            updated_line = line.lstrip() if line and line[0] == ' ' else line
                            updated_lines.append(updated_line)
                            with open(file_path, 'w', encoding='utf-8') as file:
                                file.writelines(updated_lines)  
                elif(len(lines) == 1 and (lines[0][0] == ' ' or lines[0][0] == ':')):
                    keep_formatting = True
                    updated_lines = lines[0][1:]
                    while(keep_formatting):
                        updated_lines = updated_lines[1:]
                        if(not(updated_lines[0] == ' ') or not(updated_lines[0] == ':')):
                            keep_formatting = False
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
                  'textos disponibles en http://www.textos.infoCon','cap1','cap2','cap3','cap4','cap5','cap6','cap7','cap8','cap9','cap10','cap11','cap12','cap13','cap14','cap15','cap15','cap16','cap17','cap18','cap19'
                  'ebookelo.com - Página 89',
                  '¿Te gustó este libro? Para más e Books GRATUITOS visita  freeditorial.comes',
                  'LA SOMBRA SOBRE INNSMOUTH   H. P. LOVECRAFT ',
                  '..............................................................................',
                  'EDITORIAL SUDAMERICANA Queda hecho el depósito que previene la ley 11.723.',
                  '1994, Editorial Sudamericana S.A., Humberto 1531, Buenos Aires Derechos exclusivos para ARGENTINA, CHILE, URUGUAY y PARAGUAY: EDITORIAL SUDAMERICANA S.A., Humberto 1531,',
                  'Buenos Aires, Argentina.','www.biblioteca.org.ar',
                  'Parte primera ......................................................................... 5 Parte segunda .......................................................................12 Parte tercera .........................................................................23 ESCENA I........................................................................24 ESCENA II.......................................................................25 ESCENA III .....................................................................30 ESCENA IV .....................................................................35 Parte cuarta...........................................................................36',
                  ': Garci Rodríguez de Montalvo : Novela, Novela de Caballerías Más textos disponibles en http:www.textos.info ',
                  'Este es un libro de dominio público en tanto que los derechos de autor, según la legislación española han caducado.',
                  'Luarna lo presenta aquí como un obsequio a sus clientes, dejando claro que: 1) La edición no está supervisada por nuestro departamento editorial, de forma que no nos responsabilizamos de la fidelidad del conte nido del mismo.',
                    '2) Luarna sólo ha adaptado la obra para que pueda ser fácilmente visible en los habitua les readers de seis pulgadas.'
                    '3) A todos los efectos no debe considerarse como un libro editado por Luarna.',
                    'www.luarna.com ','TUCIA DEL ABURRIMIENTO ',' MADRIGUERA DEL CONEJO UNA CARRERA LOCA Y UNA LARGA HISTORIA LA HISTORIA DE LA FALSA TORTUGA ¿QUIEN ROBO LAS TARTAS? LA DECLARACION DE ALICIA ',
                     ' : ','IIIEl señor Myriel se convierte en monseñor Bienvenido IIILas obras en armonía con las palabras ILa noche de un día de marcha IILa prudencia aconseja a la sabiduría IIIHeroísmo de la obediencia pasiva IVVEl interior de la desesperación VIVIIVIIIIXXIIIAlegre fin de la alegría IUna madre encuentra a otra madre IIPrimer bosquejo de dos personas turbias IIII. Progreso en el negocio de los abalorios negros II. III. Depósitos en la casa Laffitte IV. El señor Magdalena de luto V. Vagos relámpagos en el horizonte VI. VII. VIII. Christus nos liberavit IX. Solución de algunos asuntos de policía municipal IIICómo Jean se convierte en Champ IUna tempestad interior IIEl viajero toma precauciones para regresar IIIEntrada de preferencia IVUn lugar donde empiezan a formarse algunas convicciones VChampmathieu cada vez más asombrado IIIIIILa autoridad recobra sus derechos IVIIIEl campo de batalla por la noche IEl número 24.601 se convierte en el 9.430 IIEl diablo en Montfermeil IIILa cadena de la argolla se rompe de un solo martillazo IIIDos retratos completos IIIVino para los hombres y agua a los caballos IVEntrada de una muñeca en escena VVICosette con el desconocido en la oscuridad VIIInconvenientes de recibir a un pobre que tal vez era rico VIIIIXEl que busca lo mejor puede hallar lo peor XVuelve a aparecer el número 9.430 INido para un búho y una calandria IIDos desgracias unidas producen felicidad IIILo que observa la portera IVUna moneda de 5 francos que cae al suelo hace mucho ruido ILos rodeos de la estrategia IIIIIIVVVISe explica cómo Javert hizo una batida en vano IEl Convento Pequeño Picpus IISe busca una manera de entrar al convento IIIFauchelevent en presencia de la dificultad IVParece que Jean Valjean conocía a Agustín Castillejo VVIInterrogatorio con buenos resultados VIIIIIINoventa años y treinta y dos dientes IIIIIIIICuán útil es ir a misa para hacerse revolucionario IVVIUn grupo que estuvo a punto de ser histórico IIOración fúnebre por Blondeau IIIIVEnsanchando el horizonte IIIIIIIVLa pobreza es buena vecina de la miseria IEl apodo. Manera de formar nombres de familia IIIIIIVVIIIBabet, Gueulemer, Claquesous y Montparnasse IIIUna rosa en la miseriaIIILa ventanilla de la providencia IVLa fiera en su madriguera VEl rayo de sol en la cueva VIVIIOfertas de servicio de la miseria al dolor VIIIUso de la moneda del señor Blanco IXUn policía da dos puñetazos a un abogado XUtilización del Napoleón de Marius XILas dos sillas de Marius frente a frente XIIXIIISe debería comenzar siempre por apresar a las víctimas XIVEl niño que lloraba en la segunda parte IBien cortado y mal cosido IIEnjolras y sus tenientes IIIFormación embrionaria de crímenes en las prisiones IIIAparición al señor Mabeuf IVVVIJean Valjean, guardia nacional VIILa rosa descubre que es una máquina de guerra VIIIIXA tristeza, tristeza y media XSocorro de abajo puede ser socorro de arriba IIIUn corazón bajo una piedra IIILos viejos desaparecen en el momento oportuno IIIGavroche saca partido de Napoleón el Grande IIIPeripecias de la evasión IVVVIMarius desciende a la realidad VIIEl corazón viejo frente al corazón joven IIIIIIILa superficie y el fondo del asunto IIIIIIVVEl hombre reclutado en la calle Billettes VIMarius entra en la sombre ILa bandera, primer acto IILa bandera, segundo acto IIIGavroche habría hecho mejor en tomar la carabina de Enjolras IVLa agonía de la muerte después de la agonía de la vida VGavroche, preciso calculador de distancias VIVIIEl pilluelo es enemigo de las luces VIIIMientras Cosette dormía ICinco de menos y uno de más IIIIILos talentos que influyeron en la condena de 1796 IVGavroche fuera de la barricada VUn hermano puede convertirse en padre VIVIILa venganza de Jean Valjean VIIIIXMarius otra vez prisionero IIILa cloaca y sus sorpresas IIIIVVVILa vuelta del hijo pródigo VIIIJavert comete una infracción IVolvemos a ver el árbol con el parche de zinc IIMarius saliendo de la guerra civil, se prepara para la guerra familiar IIIIVEl señor Fauchelevent con un bulto debajo del brazo VMás vale depositar el dinero en el bosque que en el banco VIDos ancianos procuran labrar, cada uno a su manera, la felicidad de Cosette VIIVIIIDos hombres difíciles de encontrar IIIJean Valjean continúa enfermo IIIIEl séptimo círculo y el octavo cielo IILa oscuridad que puede contener una revelación IIIIIIRecuerdos en el jardín de la calle Plumet IVLa atracción y la extinción ICompasión para los desdichados e indulgencia para los dichosos IIÚltimos destellos de la lámpara sin aceite IIIEl que levantó la carreta de Fauchelevent no puede levantar una pluma IVEquívoco que sirvió para limpiar las manchas VNoche que deja entrever el día VI',
                      'Más textos disponibles en http:www.textos.info ','ANTIGUA FAMILIA PYNCHEON ','I N O P S I S D E L A S E Ñ O R A D A L L O W A Y ','CILIA VOLANGES A SOFIA CARNAY EN EL CONVENTO DE ','I N O P S I S D E L A S A V E N T U R A S D E ',''
                       ': Amar Después de la Muerte : Pedro Calderón de la Barca Más textos disponibles en http:www.textos.info Don Álvaro Tuzaní.','I N O P S I S D E C I E N A Ñ O S D E S O L E D A D ',
                        'una peripecia gÓtica de ann radcliffe direcciÓn literaria: rafael díaz santander juan luis gonzález caballero ensayo: agustín izquierdo diseÑo de la colecciÓn: cristina belmonte paccini & valdemar ilustraciÓn de cubierta: lan kolonics:  de esta ediciÓn, valdemar enokia s.l.  de la traducciÓn: jacobo rodrÍguez  del prologo: jesÚs palacios telÉfono y fax: 91 542 88 97  91 559 08 84 isbn: 8477022380 deposito legal: m24.7711998 alexdumas(27092002)',
                         'Cuento Texto completo. W.W. Jacobs ','I N O P S I S D E R O J O Y N E G R O','I.','PRIMERA PARTE  ','PEDRO, EL PRESUMIDO ','03  Reservados todos los derechos ','',
                          '2003  ','.\n','II.\n','I.\n','El señor Myriel se convierte en monseñor Bienvenido III.\n','Las obras en armonía con las palabras I.\n','La noche de un día de marcha II.\n','La prudencia aconseja a la sabiduría III.\n','Heroísmo de la obediencia pasiva IV.\n','V.\n','El interior de la desesperación VI.\n'
                           'EL LATÍN DEL DUQUE DE GUISA ', 'EL ÚLTIMO MONSTRUO SOBRE  EL ESCARABAJO  DE RICHARD  MARSH ','UN VIEJO GENTILHOMBRE Y UN VIEJO MAESTRESALA ','S I N O P S I S D E R O J O Y N E G R O ','LA VIDA DE LAZARILLO DE TORMES Y DE SUS FORTUNAS Y Autor desconocido.',
                            'Edición de Burgos, 1554.','EL BERGANTÍN GOLETA PILGRIM ','Titulo original: A FAREWELL TO ARMS ','Capítulo I.','DE CÓMO LA OVEJA DESCARRIADA ABANDONÓ EL REDIL ','HISTORIA DE UNA FAMILIA I. ',
                             'CAPÍTULO I  ','S I N O P S I S D E C I E N A Ñ O S D E S O L E D A D ','DEL DIARIO DE JONATHAN HARKER ' ,'SINOPSIS DE EL RETRATO DE DORIAN GRAY ','S I N O P S I S D E L A S A V E N T U R A S D E ',
                             'S I N O P S I S D E L A S E Ñ O R A D A L L O W A Y',' 2006  Reservados todos los derechos , para promover el crecimiento y la difusión de la www.biblioteca.org.ar Si se advierte algún tipo de error, o desea realizar alguna sugerencia le solicitamos visite . www.biblioteca.org.arcomentario ']

#copy_files(folder_path, new_path)
#delete_empty_files(new_path)
#check_language(new_path)#
#remove_first_space(new_path)#
#fix_spacing(new_path)
#check_unique_chars(folder_path)
#clean_special_characters(folder_path,new_path)
#check_text_similarity(new_path)
#print(f'{Color.BLUE}Antes:{Color.RESET}')
#all_unique_characters(folder_path)
#print(f'{Color.BLUE}Despues:{Color.RESET}')
#all_unique_characters(new_path)
####fix_seperation_errors(new_path)
delete_special_text(new_path,delete_phrases)

