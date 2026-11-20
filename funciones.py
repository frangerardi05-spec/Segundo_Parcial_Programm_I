#---------------------------- Segundo Parcial de Francisco Gerardi ----------------------------#
# Módulo que contiene las funciones para el programa
import random



# 1 | FUNCIONES DE ARCHIVOS (CSV)
def leer_archivo(ruta: str) -> str | None:
    """
    Abre un archivo de texto en modo lectura ("r") y devuelve todo su contenido.

    Parámetros:
        ruta (str): ruta relativa del archivo a leer (por ejemplo "juegos.csv").

    Retorna:
        str: el contenido completo del archivo.
        None: si el archivo no existe o no se pudo abrir.
    """
    try:
        with open(ruta, "r") as archivo:
            datos = archivo.read()
    except:
        datos = None
    return datos


def escribir_archivo(ruta: str, texto: str) -> bool:
    """
    Abre un archivo en modo escritura ("w") y lo sobrescribe con el texto recibido.
    Si el archivo no existe, lo crea.

    Parámetros:
        ruta (str): ruta relativa del archivo.
        texto (str): contenido completo que se va a guardar.

    Retorna:
        bool: True si se pudo guardar, False si ocurrió un error.
    """
    retorno = True
    try:
        with open(ruta, "w") as archivo:
            archivo.write(texto)
    except:
        retorno = False
    return retorno


def parsear_csv(datos: str) -> list[dict]:
    """
    Convierte el texto leído de un CSV en una lista de diccionarios.
    La primera línea (encabezado) se usa como claves de cada diccionario.
    Las líneas vacías o con datos inválidos se descartan.

    Parámetros:
        datos (str): texto completo del archivo CSV.

    Retorna:
        list[dict]: lista de videojuegos con los tipos ya convertidos (int / float).
    """
    lista = []
    datos_limpios = datos.strip()                 # saco el último \n
    lista_lineas = datos_limpios.split("\n")      # una línea por juego
    encabezado = lista_lineas.pop(0)              # saco el encabezado
    claves = encabezado.split(",")

    for i in range(len(lista_lineas)):
        linea = lista_lineas[i].strip()
        if linea != "":
            valores = linea.split(",")
            if len(valores) == len(claves) and validar_valores_linea(valores) == True:
                juego = {}
                for j in range(len(claves)):
                    juego.update({claves[j]: valores[j]})
                convertir_tipos_juego(juego)
                lista.append(juego)
    return lista


def validar_valores_linea(valores: list) -> bool:
    """
    Verifica que los valores numéricos de una línea del CSV sean correctos, para que
    no falle la conversión con int() / float().
    Orden esperado: codigo, nombre, genero, precio, stock, unidades_vendidas.

    Parámetros:
        valores (list): lista de strings obtenida con split(",").

    Retorna:
        bool: True si la línea se puede convertir, False si no.
    """
    retorno = False
    if (es_entero(valores[0]) == True and es_flotante(valores[3]) == True and
            es_entero(valores[4]) == True and es_entero(valores[5]) == True):
        retorno = True
    return retorno


def convertir_tipos_juego(juego: dict) -> None:
    """
    Convierte los valores de un juego leídos del CSV (que siempre son str) a su tipo real.
    No retorna nada porque el diccionario es MUTABLE: se modifica el original.

    Parámetros:
        juego (dict): diccionario de un videojuego con todos sus valores en str.
    """
    juego["codigo_identificador"] = int(juego["codigo_identificador"])
    juego["precio"] = float(juego["precio"])
    juego["stock"] = int(juego["stock"])
    juego["unidades_vendidas"] = int(juego["unidades_vendidas"])


def cargar_juegos(ruta: str) -> list[dict] | None:
    """
    Lee el archivo CSV y arma la lista de videojuegos (se usa al iniciar el programa).

    Parámetros:
        ruta (str): ruta del archivo CSV.

    Retorna:
        list[dict]: la lista de juegos cargada.
        None: si el archivo no existe.
    """
    retorno = None
    datos = leer_archivo(ruta)
    if datos != None and datos.strip() != "":
        retorno = parsear_csv(datos)
    return retorno


def juego_a_linea_csv(juego: dict, claves: list) -> str:
    """
    Transforma un diccionario de un juego en una línea de texto con formato CSV.

    Parámetros:
        juego (dict): videojuego a convertir.
        claves (list): lista de claves en el orden en el que se escriben las columnas.

    Retorna:
        str: línea del CSV terminada en salto de línea. Ej: "4831207,Elden Ring,RPG,59999.0,12,35\\n"
    """
    valores = []
    for i in range(len(claves)):
        valores.append(str(juego[claves[i]]))   # join solo une strings
    return ",".join(valores) + "\n"


def guardar_juegos(lista_juegos: list[dict], ruta: str, claves: list) -> bool:
    """
    Guarda TODA la lista de juegos en el CSV (encabezado + una línea por juego),
    sobrescribiendo el archivo. Se usa después de un alta y después de una venta.

    Parámetros:
        lista_juegos (list[dict]): lista con todos los videojuegos.
        ruta (str): ruta del archivo CSV.
        claves (list): claves en el orden del encabezado.

    Retorna:
        bool: True si se guardó correctamente, False si no.
    """
    texto = ",".join(claves) + "\n"
    for i in range(len(lista_juegos)):
        texto += juego_a_linea_csv(lista_juegos[i], claves)
    return escribir_archivo(ruta, texto)



# 2 | FUNCIONES DE VALIDACIÓN Y NORMALIZACIÓN
def es_entero(cadena: str) -> bool:
    """
    Valida que un string esté formado solo por dígitos (0-9). Sirve para entero positivo o 0.

    Parámetros:
        cadena (str): texto a validar.

    Retorna:
        bool: True si son todos dígitos, False si está vacío o tiene otro carácter.
    """
    retorno = True
    if len(cadena) > 0:
        for caracter in cadena:
            if caracter < "0" or caracter > "9":
                retorno = False
                break
    else:
        retorno = False
    return retorno


def es_flotante(cadena: str) -> bool:
    """
    Valida que un string represente un número decimal positivo (ej: "1500", "1500.50").
    Acepta como máximo un punto decimal y al menos un dígito.

    Parámetros:
        cadena (str): texto a validar.

    Retorna:
        bool: True si se puede convertir con float(), False si no.
    """
    retorno = True
    contador_puntos = 0
    contador_digitos = 0
    for caracter in cadena:
        if caracter == ".":
            contador_puntos += 1
        elif caracter >= "0" and caracter <= "9":
            contador_digitos += 1
        else:
            retorno = False
            break
    if contador_puntos > 1 or contador_digitos == 0:
        retorno = False
    return retorno


def normalizar_texto(texto: str) -> str:
    """
    Normaliza un texto ingresado por consola: le quita los espacios de los extremos
    y lo pasa a minúsculas. Así "  AsC " y "aSC" quedan iguales a "asc".

    Parámetros:
        texto (str): texto a normalizar.

    Retorna:
        str: texto normalizado.
    """
    return texto.strip().lower()


def contiene_caracter(cadena: str, caracter_buscado: str) -> bool:
    """
    Indica si un carácter aparece dentro de una cadena.
    (Se usa para evitar comas en el nombre, porque romperían el formato del CSV).

    Parámetros:
        cadena (str): texto donde buscar.
        caracter_buscado (str): carácter a buscar.

    Retorna:
        bool: True si lo encuentra, False si no.
    """
    retorno = False
    for caracter in cadena:
        if caracter == caracter_buscado:
            retorno = True
            break
    return retorno


def buscar_genero_valido(texto: str, generos: list) -> str | None:
    """
    Busca el género ingresado (ya normalizado) dentro de la lista de géneros válidos.

    Parámetros:
        texto (str): género ingresado por el usuario normalizado (ej: "rpg").
        generos (list): lista de géneros válidos (ej: ["RPG", "Deportes", ...]).

    Retorna:
        str: el género escrito tal como está en la lista oficial (ej: "RPG").
        None: si no es un género válido.
    """
    retorno = None
    for i in range(len(generos)):
        if normalizar_texto(generos[i]) == texto:
            retorno = generos[i]
            break
    return retorno



# 3 | FUNCIONES DE INGRESO DE DATOS (opción 1)
def pedir_nombre() -> str:
    """
    Pide el nombre del videojuego hasta que sea válido:
    entre 3 y 50 caracteres y sin comas (la coma es el separador del CSV).

    Retorna:
        str: nombre válido, sin espacios en los extremos.
    """
    nombre = input("Nombre del videojuego (3 a 50 caracteres): ").strip()
    while len(nombre) < 3 or len(nombre) > 50 or contiene_caracter(nombre, ",") == True:
        print("ERROR. El nombre debe tener entre 3 y 50 caracteres y no puede tener comas.")
        nombre = input("Nombre del videojuego (3 a 50 caracteres): ").strip()
    return nombre


def pedir_genero(generos: list) -> str:
    """
    Pide el género hasta que sea uno de los válidos. Normaliza la entrada, por lo que
    "rpg", "Rpg" o "  RPG " se aceptan igual.

    Parámetros:
        generos (list): lista de géneros válidos.

    Retorna:
        str: género válido escrito como en la lista oficial.
    """
    mensaje = "Género (" + ", ".join(generos) + "): "
    genero = buscar_genero_valido(normalizar_texto(input(mensaje)), generos)
    while genero == None:
        print("ERROR. Género inválido.")
        genero = buscar_genero_valido(normalizar_texto(input(mensaje)), generos)
    return genero


def pedir_precio() -> float:
    """
    Pide el precio hasta que sea un número mayor a 0 (acepta decimales con punto).

    Retorna:
        float: precio válido.
    """
    precio = input("Precio (mayor a 0): ").strip()
    while es_flotante(precio) == False or float(precio) <= 0:
        print("ERROR. El precio debe ser un número mayor a 0 (use punto para decimales).")
        precio = input("Precio (mayor a 0): ").strip()
    return float(precio)


def pedir_entero_en_rango(mensaje: str, minimo: int, maximo: int | None = None) -> int:
    """
    Pide un número entero hasta que esté dentro del rango [minimo, maximo].
    Si maximo es None, no hay límite superior.

    Parámetros:
        mensaje (str): texto que se muestra en el input.
        minimo (int): valor mínimo permitido (inclusive).
        maximo (int | None): valor máximo permitido (inclusive). Opcional.

    Retorna:
        int: número válido.
    """
    valido = False
    while valido == False:
        dato = input(mensaje).strip()
        if es_entero(dato) == True:
            numero = int(dato)
            if numero >= minimo and (maximo == None or numero <= maximo):
                valido = True
        if valido == False:
            if maximo == None:
                print(f"ERROR. Ingrese un número entero mayor o igual a {minimo}.")
            else:
                print(f"ERROR. Ingrese un número entero entre {minimo} y {maximo}.")
    return numero


def generar_codigo_unico(lista_juegos: list[dict]) -> int:
    """
    Genera aleatoriamente un código de 7 dígitos (1000000 a 9999999) que no exista
    en la lista. Si ya existe, genera otro (único e irrepetible).

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos actuales.

    Retorna:
        int: código identificador nuevo.
    """
    codigo = random.randint(1000000, 9999999)
    while buscar_indice_por_codigo(lista_juegos, codigo) != None:
        codigo = random.randint(1000000, 9999999)
    return codigo


def dar_alta_juego(lista_juegos: list[dict], generos: list) -> dict:
    """
    Pide por consola todos los datos de UN videojuego (validados), le genera el código
    único, pone las unidades vendidas en 0 y lo agrega a la lista.

    Parámetros:
        lista_juegos (list[dict]): lista donde se agrega el juego (se modifica por referencia).
        generos (list): géneros válidos.

    Retorna:
        dict: el juego dado de alta.
    """
    nombre = pedir_nombre()
    genero = pedir_genero(generos)
    precio = pedir_precio()
    stock = pedir_entero_en_rango("Stock (0 o más): ", 0)

    juego = {"codigo_identificador": generar_codigo_unico(lista_juegos),
             "nombre": nombre,
             "genero": genero,
             "precio": precio,
             "stock": stock,
             "unidades_vendidas": 0}
    lista_juegos.append(juego)
    return juego



# 4 | FUNCIONES DE BÚSQUEDA Y VENTA 
def buscar_indice_por_codigo(lista_juegos: list[dict], codigo: int) -> int | None:
    """
    Busca un juego por su código identificador.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
        codigo (int): código a buscar.

    Retorna:
        int: índice del juego en la lista.
        None: si no existe.
    """
    retorno = None
    for i in range(len(lista_juegos)):
        if lista_juegos[i]["codigo_identificador"] == codigo:
            retorno = i
            break
    return retorno


def filtrar_juegos_con_stock(lista_juegos: list[dict]) -> list[dict]:
    """
    Arma una lista nueva solo con los juegos que tienen stock mayor a 0.
    Los diccionarios son los mismos (referencias), no copias.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.

    Retorna:
        list[dict]: juegos con stock disponible.
    """
    con_stock = []
    for juego in lista_juegos:
        if juego["stock"] > 0:
            con_stock.append(juego)
    return con_stock


def pedir_codigo() -> int:
    """
    Pide un código identificador hasta que tenga exactamente 7 dígitos numéricos.

    Retorna:
        int: código ingresado.
    """
    codigo = input("Ingrese el código identificador del juego (7 dígitos): ").strip()
    while es_entero(codigo) == False or len(codigo) != 7:
        print("ERROR. El código debe tener exactamente 7 dígitos numéricos.")
        codigo = input("Ingrese el código identificador del juego (7 dígitos): ").strip()
    return int(codigo)


def registrar_venta(lista_juegos: list[dict], ruta: str, claves: list) -> bool:
    """
    Opción 2 completa: muestra los juegos con stock, pide el código y la cantidad,
    descuenta el stock, suma las unidades vendidas y guarda los cambios en el CSV.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
        ruta (str): ruta del CSV.
        claves (list): claves en el orden del encabezado del CSV.

    Retorna:
        bool: True si la venta fue exitosa y se guardó, False si no.
    """
    exito = False
    juegos_con_stock = filtrar_juegos_con_stock(lista_juegos)

    if len(juegos_con_stock) == 0:
        print("No hay juegos con stock disponible para vender.")
    else:
        print("JUEGOS CON STOCK DISPONIBLE:")
        mostrar_juegos(juegos_con_stock)
        codigo = pedir_codigo()
        indice = buscar_indice_por_codigo(juegos_con_stock, codigo)

        if indice == None:
            print("ERROR. No existe un juego con stock con ese código.")
        else:
            juego = juegos_con_stock[indice]
            cantidad = pedir_entero_en_rango(f"Unidades a vender (1 a {juego['stock']}): ",
                                             1, juego["stock"])
            juego["stock"] -= cantidad              # modifica el dict ORIGINAL (referencia)
            juego["unidades_vendidas"] += cantidad
            if guardar_juegos(lista_juegos, ruta, claves) == True:
                exito = True
                print(f"Venta exitosa: {cantidad} unidad/es de {juego['nombre']}. "
                      f"Stock restante: {juego['stock']}.")
            else:
                print("ERROR. No se pudo guardar la venta en el archivo.")
    return exito



# 5 | FUNCIONES DE ESTADÍSTICAS
def obtener_mas_vendidos(lista_juegos: list[dict]) -> list[dict]:
    """
    Busca el/los videojuego/s con más unidades vendidas (si hay empate, devuelve todos).
    Usa una bandera para inicializar el máximo con el primer elemento.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.

    Retorna:
        list[dict]: juego/s más vendido/s (lista vacía si no hay juegos).
    """
    bandera_primero = True
    maximo = 0
    for juego in lista_juegos:
        if bandera_primero == True or juego["unidades_vendidas"] > maximo:
            maximo = juego["unidades_vendidas"]
            bandera_primero = False

    mas_vendidos = []
    for juego in lista_juegos:
        if juego["unidades_vendidas"] == maximo:
            mas_vendidos.append(juego)
    return mas_vendidos


def calcular_unidades_por_genero(lista_juegos: list[dict], generos: list) -> dict:
    """
    Acumula las unidades vendidas de cada género en un diccionario.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
        generos (list): géneros válidos.

    Retorna:
        dict: {genero: unidades_vendidas_totales}. Ej: {"RPG": 62, "Deportes": 141, ...}
    """
    unidades = {}
    for genero in generos:
        unidades.update({genero: 0})          # inicializo los acumuladores en 0
    for juego in lista_juegos:
        if juego["genero"] in unidades:       # por si el CSV trae un género desconocido
            unidades[juego["genero"]] += juego["unidades_vendidas"]
    return unidades


def obtener_generos_mas_vendidos(unidades_por_genero: dict) -> list[str]:
    """
    Obtiene el/los género/s con mayor cantidad de unidades vendidas.

    Parámetros:
        unidades_por_genero (dict): diccionario {genero: unidades}.

    Retorna:
        list[str]: género/s con el máximo (si hay empate, todos).
    """
    bandera_primero = True
    maximo = 0
    for valor in unidades_por_genero.values():
        if bandera_primero == True or valor > maximo:
            maximo = valor
            bandera_primero = False

    generos_max = []
    for genero, valor in unidades_por_genero.items():
        if valor == maximo:
            generos_max.append(genero)
    return generos_max


def calcular_valor_inventario(lista_juegos: list[dict]) -> float:
    """
    Calcula el valor total del inventario: suma de (stock * precio) de cada juego.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.

    Retorna:
        float: valor total del inventario.
    """
    acumulador = 0
    for juego in lista_juegos:
        acumulador += juego["stock"] * juego["precio"]
    return acumulador


def calcular_porcentaje_sin_stock(lista_juegos: list[dict]) -> float:
    """
    Calcula el porcentaje de videojuegos que tienen stock igual a 0.
    Controla la división por cero si la lista está vacía.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.

    Retorna:
        float: porcentaje (0 a 100).
    """
    porcentaje = 0
    contador_sin_stock = 0
    for juego in lista_juegos:
        if juego["stock"] == 0:
            contador_sin_stock += 1
    if len(lista_juegos) > 0:
        porcentaje = contador_sin_stock * 100 / len(lista_juegos)
    return porcentaje


def calcular_promedio_precios_por_genero(lista_juegos: list[dict], generos: list) -> dict:
    """
    Calcula el precio promedio de cada género (acumulador de precios / contador de juegos).
    Si un género no tiene juegos, su promedio queda en None (evita dividir por 0).

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
        generos (list): géneros válidos.

    Retorna:
        dict: {genero: promedio (float) o None}.
    """
    acumuladores = {}
    contadores = {}
    for genero in generos:
        acumuladores.update({genero: 0})
        contadores.update({genero: 0})

    for juego in lista_juegos:
        if juego["genero"] in acumuladores:   # por si el CSV trae un género desconocido
            acumuladores[juego["genero"]] += juego["precio"]
            contadores[juego["genero"]] += 1

    promedios = {}
    for genero in generos:
        if contadores[genero] > 0:
            promedios.update({genero: acumuladores[genero] / contadores[genero]})
        else:
            promedios.update({genero: None})
    return promedios


def mostrar_estadisticas(lista_juegos: list[dict], generos: list) -> None:
    """
    Calcula y muestra por consola todas las estadísticas de la opción 3.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
        generos (list): géneros válidos.
    """
    if len(lista_juegos) == 0:
        print("No hay juegos cargados para calcular estadísticas.")
    else:
        print("================ ESTADÍSTICAS ================")

        print("❖ Videojuego/s más vendido/s:")
        mas_vendidos = obtener_mas_vendidos(lista_juegos)
        for juego in mas_vendidos:
            print(f"    - {juego['nombre']} ({juego['unidades_vendidas']} unidades)")

        unidades_por_genero = calcular_unidades_por_genero(lista_juegos, generos)
        generos_max = obtener_generos_mas_vendidos(unidades_por_genero)
        print("❖ Género/s con mayor cantidad de unidades vendidas:")
        for genero in generos_max:
            print(f"    - {genero} ({unidades_por_genero[genero]} unidades)")

        valor = calcular_valor_inventario(lista_juegos)
        print(f"❖ Valor total del inventario: ${valor:.2f}")

        porcentaje = calcular_porcentaje_sin_stock(lista_juegos)
        print(f"❖ Porcentaje de videojuegos sin stock: {porcentaje:.2f}%")

        print("❖ Promedio de precios por género:")
        promedios = calcular_promedio_precios_por_genero(lista_juegos, generos)
        for genero, promedio in promedios.items():
            if promedio == None:
                print(f"    - {genero:<10}: sin juegos cargados")
            else:
                print(f"    - {genero:<10}: ${promedio:.2f}")
        print("==============================================")



# 6 | FUNCIONES DE ORDENAMIENTO Y MUESTRA 
def pedir_criterio_orden() -> str:
    """
    Pide el criterio de ordenamiento (nombre, genero o precio). Normaliza la entrada,
    y acepta "género" con tilde.

    Retorna:
        str: "nombre", "genero" o "precio".
    """
    criterio = normalizar_texto(input("Ordenar por (nombre / genero / precio): "))
    if criterio == "género":
        criterio = "genero"
    while criterio != "nombre" and criterio != "genero" and criterio != "precio":
        print("ERROR. Opción inválida.")
        criterio = normalizar_texto(input("Ordenar por (nombre / genero / precio): "))
        if criterio == "género":
            criterio = "genero"
    return criterio


def pedir_sentido_orden() -> bool:
    """
    Pide si el orden es ascendente o descendente. Acepta "Asc", "aSC", "DeSc", etc.

    Retorna:
        bool: True si es ascendente, False si es descendente.
    """
    sentido = normalizar_texto(input("Orden (ASC - Ascendente / DESC - Descendente): "))
    while sentido != "asc" and sentido != "desc":
        print("ERROR. Ingrese ASC o DESC.")
        sentido = normalizar_texto(input("Orden (ASC - Ascendente / DESC - Descendente): "))
    return sentido == "asc"


def obtener_valor_comparable(juego: dict, criterio: str) -> str | float:
    """
    Devuelve el valor del juego que se usa para comparar al ordenar.
    Los textos se pasan a minúsculas para que "zelda" y "Zelda" se ordenen igual
    (en ASCII las mayúsculas van antes que las minúsculas).

    Parámetros:
        juego (dict): videojuego.
        criterio (str): "nombre", "genero" o "precio".

    Retorna:
        str | float: valor a comparar.
    """
    valor = juego[criterio]
    if criterio != "precio":
        valor = valor.lower()
    return valor


def intercambiar_elementos(lista: list, i: int, j: int) -> None:
    """
    Intercambia (swap) dos elementos de una lista usando una variable auxiliar.

    Parámetros:
        lista (list): lista donde están los elementos.
        i (int), j (int): índices de los elementos a intercambiar.
    """
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux


def ordenar_juegos(lista_juegos: list[dict], criterio: str, ascendente: bool) -> None:
    """
    Ordena la lista de juegos con el método de burbujeo, según el criterio elegido.
    Doble criterio: si dos juegos empatan (ej. mismo género o mismo precio),
    se desempata por nombre en el mismo sentido.

    Parámetros:
        lista_juegos (list[dict]): lista a ordenar (se modifica por referencia).
        criterio (str): "nombre", "genero" o "precio".
        ascendente (bool): True = ASC, False = DESC.
    """
    for i in range(len(lista_juegos) - 1):
        for j in range(i + 1, len(lista_juegos)):
            valor_i = obtener_valor_comparable(lista_juegos[i], criterio)
            valor_j = obtener_valor_comparable(lista_juegos[j], criterio)
            nombre_i = obtener_valor_comparable(lista_juegos[i], "nombre")
            nombre_j = obtener_valor_comparable(lista_juegos[j], "nombre")

            if (ascendente == True and (valor_i > valor_j or (valor_i == valor_j and nombre_i > nombre_j))) or \
               (ascendente == False and (valor_i < valor_j or (valor_i == valor_j and nombre_i < nombre_j))):
                intercambiar_elementos(lista_juegos, i, j)


def calcular_ancho_nombre(lista_juegos: list[dict]) -> int:
    """
    Calcula el ancho de la columna "nombre" según el nombre más largo (máximo),
    para que la tabla quede alineada.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.

    Retorna:
        int: ancho de la columna (mínimo 6, el largo de la palabra "Nombre").
    """
    ancho = 6
    for juego in lista_juegos:
        if len(juego["nombre"]) > ancho:
            ancho = len(juego["nombre"])
    return ancho


def mostrar_juegos(lista_juegos: list[dict]) -> None:
    """
    Muestra los juegos en forma de tabla: una fila por juego y una columna por dato.
    (No se imprime la lista con print, se recorre y se muestra elemento por elemento).

    Parámetros:
        lista_juegos (list[dict]): juegos a mostrar.
    """
    if len(lista_juegos) == 0:
        print("No hay juegos para mostrar.")
    else:
        ancho = calcular_ancho_nombre(lista_juegos)
        encabezado = f"{'Código':<8} | {'Nombre':<{ancho}} | {'Género':<10} | {'Precio':>12} | {'Stock':>5} | {'Vendidas':>8}"
        print(encabezado)
        print("-" * len(encabezado))
        for juego in lista_juegos:
            print(f"{juego['codigo_identificador']:<8} | {juego['nombre']:<{ancho}} | "
                  f"{juego['genero']:<10} | {juego['precio']:>12.2f} | "
                  f"{juego['stock']:>5} | {juego['unidades_vendidas']:>8}")


def mostrar_catalogo_ordenado(lista_juegos: list[dict]) -> None:
    """
    Opción 4 completa: pide criterio y sentido, ordena una COPIA de la lista
    (para no alterar el orden original del catálogo) y la muestra.

    Parámetros:
        lista_juegos (list[dict]): lista de videojuegos.
    """
    if len(lista_juegos) == 0:
        print("No hay juegos cargados.")
    else:
        criterio = pedir_criterio_orden()
        ascendente = pedir_sentido_orden()
        copia = lista_juegos.copy()
        ordenar_juegos(copia, criterio, ascendente)
        if ascendente == True:
            print(f"\nCATÁLOGO ORDENADO POR {criterio.upper()} - ASCENDENTE")
        else:
            print(f"\nCATÁLOGO ORDENADO POR {criterio.upper()} - DESCENDENTE")
        mostrar_juegos(copia)



# 7 | OTRAS
def pausar() -> None:
    """Detiene el programa hasta que el usuario presione Enter."""
    input("\nPresione Enter para volver al menú...")


def limpiar_teclado_os()->None:
    """
    Objetivo: Función con el {import os} que al convocarlo sirve para limpiar el teclado según el OS del usuario sin necesidad de repetir código.
    """
    import os 

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")