import os


def list_files(path, extension):

    """Lista todos los archivos con extensión .dat en un directorio dado.

    Parameters
    ----------

    path : str
        la ruta al directorio para buscar

    extension : str
        la extensión del archivo a buscar

    Returns
    -------
    list
        lista con los nombres de los archivos .dat
    """

    files = [f for f in os.listdir(path)]

    return [path+f for f in files if f.endswith('.' + extension)]


def dat_files_clean(files_names):

    """Limpieza de los archivos '.dat'.
    Se eliminan las filas que no son de interés para la
    obtención de información.

    Parameters
    ----------

    files : list
        nombres de los archivos .dat

    Returns
    -------

    filtered_file : list
        lista con el contenido relevante para ser procesado.

    """

    for f in files_names:
        #print("\n")
        with open(f, 'r', encoding='iso-8859-1') as input_file:
            # print("Nombre del archivo: " + f + "\n")
            lines = input_file.readlines()
            filtered_file = []
            #print(lines)
            num_lineas = 0
            for linea in lines:
                print(linea)
                num_lineas += 1
                #linea = linea.split(';')

                if linea.startswith('Tipo Transacc'):
                    # print(linea)
                    # print(num_lineas)
                    break
            # print(num_lineas)
            filtered_file = lines[num_lineas-1:]
            # print(filtered_file)
        #save_files(f, filtered_file)
    return filtered_file


def bsale_clean_file(file):

    """Limpieza de los archivos '.xlsx'.
    Se eliminan las filas que no son de interés para la
    obtención de información.

    Parameters
    ----------

    file : str
        nombre del archivo .xlsx

    Returns
    -------

    filtered_file : list
        lista con el contenido relevante para ser procesado.
    """

    with open(file, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()
        newlines = []
        #print(lines)
        i = 0
        for linea in lines:
            # print(linea)
            i += 1
            linea = linea.split(';')
            if linea[1] == 'Tipo Documento' and linea[2] == 'Nº Documento':
                #print(linea)
                #print(i)
                break
        #print(i)
        newlines = lines[i-1:]
    return newlines


def save_files(output_file_name, content):

    """Se guardan los archivos .dat filtrados en archivos .csv

    Parameters
    ----------

    output_file_name : list
        nombres de los archivos .dat

    content : list
        contenido que se guardará en el archivo
    """

    # Obtengo solo el nombre de los archivos, sin extensión
    file_names = [os.path.splitext(f)[0] for f in output_file_name]
    print(file_names)
    # print(content)

    for f in file_names:
        new_files_csv = '{}.{}'.format(f, 'csv')
        with open(new_files_csv, 'w') as output_file:
            for linea in content:
                output_file.write(linea)


def get_file_encoding(src_file_path):
    """Obtiene el tipo de codificación de un archivo

    Parameters
    ----------
    src_file_path : str
        Ruta del archivo

    Returns
    -------

    src_file : str
        Tipo de codificación del archivo
    """

    with open(src_file_path) as src_file:
        return src_file.encoding
