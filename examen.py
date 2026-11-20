#---------------------------- Segundo Parcial de Francisco Gerardi ----------------------------#
# Módulo que ejecuta las funciones del módulo "funciones.py"

#Importo las funciones del módulo "funciones.py"
from funciones import cargar_juegos
from funciones import guardar_juegos
from funciones import dar_alta_juego
from funciones import registrar_venta
from funciones import mostrar_estadisticas
from funciones import mostrar_catalogo_ordenado
from funciones import mostrar_juegos
from funciones import pausar
from funciones import limpiar_teclado_os

#-----------------------------------------------------------#
# Variables necesarias para el programa
RUTA_CSV = "juegos.csv"
CLAVES = ["codigo_identificador", "nombre", "genero", "precio", "stock", "unidades_vendidas"]
GENEROS = ["RPG", "Deportes", "Carreras", "Aventura", "Estrategia"]

#-----------------------------------------------------------#
# Defino el diseño del menú como una variable para poder repetirla en el bucle ()
MENU = """
#--------------------------------------#
        GESTIÓN DE VIDEOJUEGOS
#--------------------------------------#
    1)  Alta de videojuego
    2)  Registrar una venta
    3)  Consultar estadísticas
    4)  Mostrar catálogo ordenado
    5)  Salir
#--------------------------------------#
Elegir opción: """

#-----------------------------------------------------------#
# Carga automática del CSV al iniciar el programa
lista_juegos = cargar_juegos(RUTA_CSV)
if lista_juegos == None:
    print(f"No se encontró el archivo '{RUTA_CSV}' (o está vacío). Se inicia con el catálogo vacío.")
    lista_juegos = []
else:
    print(f"Se cargaron {len(lista_juegos)} videojuegos desde '{RUTA_CSV}'.")

#-----------------------------------------------------------#
# Menú principal
seguir = True
while seguir == True:
    opcion = input(MENU).strip()   # se lee como str: si escriben letras, no se rompe

    match opcion:
        case "1":
            print("\n--- ALTA DE VIDEOJUEGO ---")
            juego_nuevo = dar_alta_juego(lista_juegos, GENEROS)
            if guardar_juegos(lista_juegos, RUTA_CSV, CLAVES) == True:
                print("\nJuego dado de alta y guardado en el archivo:")
                mostrar_juegos([juego_nuevo])
            else:
                print("ERROR. El juego se agregó, pero no se pudo guardar en el archivo.")
            pausar()

        case "2":
            print("\n--- REGISTRAR VENTA ---")
            registrar_venta(lista_juegos, RUTA_CSV, CLAVES)
            pausar()

        case "3":
            print()
            mostrar_estadisticas(lista_juegos, GENEROS)
            pausar()

        case "4":
            print("\n--- CATÁLOGO ORDENADO ---")
            mostrar_catalogo_ordenado(lista_juegos)
            pausar()

        case "5":
            print("Cerrando el programa...")
            seguir = False

        case _:
            print("ERROR. Opción inválida, elija un número del 1 al 5.")
    
    limpiar_teclado_os()