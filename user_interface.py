"""Interfaz de consola. Ejecutar este archivo para iniciar el programa."""

from datetime import date
from business_logic import Cooperativa


def leer_entero(mensaje):
    texto = input(mensaje).strip()
    try:
        return int(texto)
    except ValueError:
        return None


def leer_fecha():
    try:
        anio = int(input("Anio de inicio (AAAA): ").strip())
        mes = int(input("Mes de inicio (1-12): ").strip())
        dia = int(input("Dia de inicio: ").strip())
        return date(anio, mes, dia)
    except ValueError:
        print("La fecha de inicio no es valida.")
        return None


def mostrar_menu():
    print("\n========== COOPERATIVA DE CARPEROS ==========")
    print("1. Crear una playa")
    print("2. Registrar las carpas alquiladas del dia siguiente")
    print("3. Simular dias")
    print("4. Mostrar el informe de una playa")
    print("5. Mostrar el porcentaje de alquiler mas alto y mas bajo")
    print("6. Cargar playas y alquileres desde archivos")
    print("7. Salir")


def crear_playa(cooperativa):
    nombre = input("Nombre de la playa: ").strip()
    if not nombre:
        print("El nombre de la playa no puede estar vacio.")
        return
    if cooperativa.buscar_playa(nombre):
        print("Ya existe una playa con ese nombre.")
        return

    carpas = leer_entero("Numero de carpas instaladas: ")
    if carpas is None:
        print("El numero de carpas instaladas debe ser un numero entero.")
        return
    if carpas < 1:
        print("La playa debe tener al menos una carpa instalada.")
        return

    fecha_inicio = leer_fecha()
    if fecha_inicio is None:
        return
    cooperativa.crear_playa(nombre, carpas, fecha_inicio)
    print("Playa creada correctamente.")


def pedir_playa(cooperativa):
    nombre = input("Nombre de la playa: ").strip()
    playa = cooperativa.buscar_playa(nombre)
    if playa is None:
        print("No hay una playa con ese nombre.")
    return playa


def registrar_dia(cooperativa):
    playa = pedir_playa(cooperativa)
    if playa is None:
        return
    cantidad = leer_entero("Carpas alquiladas en el dia siguiente: ")
    if cantidad is None:
        print("Las carpas alquiladas deben ser un numero entero.")
        return
    if cantidad < 0 or cantidad > playa.carpas_instaladas:
        print(f"Las carpas alquiladas deben estar entre 0 y {playa.carpas_instaladas}.")
        return
    playa.registrar_alquiler(cantidad)
    fecha = playa.fecha_de_dia(len(playa.alquileres) - 1)
    print(f"Registro agregado para {fecha}.")


def simular(cooperativa):
    playa = pedir_playa(cooperativa)
    if playa is None:
        return

    dias = leer_entero("Numero de dias que desea simular: ")
    if dias is None:
        print("El numero de dias debe ser un numero entero.")
        return
    if dias < 1:
        print("Se debe simular al menos un dia.")
        return

    minimo = leer_entero("Minimo de carpas alquiladas: ")
    if minimo is None:
        print("Las carpas alquiladas deben ser un numero entero.")
        return
    if minimo < 0 or minimo > playa.carpas_instaladas:
        print(f"Las carpas alquiladas deben estar entre 0 y {playa.carpas_instaladas}.")
        return

    maximo = leer_entero("Maximo de carpas alquiladas: ")
    if maximo is None:
        print("Las carpas alquiladas deben ser un numero entero.")
        return
    if maximo < 0 or maximo > playa.carpas_instaladas:
        print(f"Las carpas alquiladas deben estar entre 0 y {playa.carpas_instaladas}.")
        return
    if minimo > maximo:
        print("El minimo no puede ser mayor que el maximo.")
        return

    nuevos = playa.simular_dias(dias, minimo, maximo)
    print(f"Se agregaron {len(nuevos)} dias simulados: {nuevos}")


def mostrar_informe(cooperativa):
    playa = pedir_playa(cooperativa)
    if playa is None:
        return
    datos = playa.informe()
    print("\n--------------- INFORME DE PLAYA ---------------")
    print(f"Playa: {datos['nombre']}")
    print(f"Carpas instaladas: {datos['carpas_instaladas']}")
    print(f"Dias registrados: {datos['dias_registrados']}")
    print(f"Alquileres totales: {datos['alquileres_totales']}")
    if datos["dias_registrados"] == 0:
        print("No hay dias registrados; promedio, porcentaje y desviacion estandar: 0.")
    else:
        print(f"Promedio diario: {round(datos['promedio'], 2)}")
        print(f"Porcentaje de alquiler: {round(datos['porcentaje'], 2)}")
        print(f"Desviacion estandar poblacional: {round(datos['desviacion_estandar'], 2)}")
        fecha_max, fecha_min = datos["fechas_extremas"]
        print(f"Fecha con mas carpas alquiladas: {fecha_max}")
        print(f"Fecha con menos carpas alquiladas: {fecha_min}")
        print("Dias por nivel:")
        for nivel, cantidad in datos["conteo_niveles"].items():
            print(f"  {nivel}: {cantidad}")
        longitud, inicio = datos["racha_agotada"]
        if longitud == 0:
            print("No hubo dias agotados consecutivos.")
        else:
            print(f"Mayor racha agotada: {longitud} dias, desde {inicio}")
        print(f"Ultimo dia registrado: {datos['ultimo_dia']}")
        if datos["dias_pendientes"] == 0:
            print("El registro esta al dia.")
        else:
            print(f"Faltan {datos['dias_pendientes']} dias por registrar.")
    print("-------------------------------------------------")


def mostrar_extremos(cooperativa):
    mayor, menor = cooperativa.playa_con_porcentaje_mayor_y_menor()
    if mayor is None:
        print("No hay playas con dias registrados para comparar.")
        return
    print(f"Mayor porcentaje: {mayor.nombre} ({round(mayor.porcentaje_alquiler(), 2)} %)")
    print(f"Menor porcentaje: {menor.nombre} ({round(menor.porcentaje_alquiler(), 2)} %)")


def cargar_archivos(cooperativa):
    if cooperativa.playas:
        print("La carga de archivos solo se permite cuando no hay playas.")
        return
    ruta_playas = input("Ruta del archivo de playas CSV: ").strip()
    resultado_playas = cooperativa.cargar_playas_csv(ruta_playas)
    for error in resultado_playas["errores"]:
        print(error)
    if resultado_playas.get("archivo_no_existe"):
        # Regla: si no existe el archivo de playas, no se pide ni se lee el de alquileres.
        return
    print(f"Playas cargadas: {resultado_playas['cargadas']}")

    ruta_alquileres = input("Ruta del archivo de alquileres CSV: ").strip()
    resultado_alquileres = cooperativa.cargar_alquileres_csv(ruta_alquileres)
    for error in resultado_alquileres["errores"]:
        print(error)
    print(f"Alquileres cargados: {resultado_alquileres['cargados']} dias")


def main():
    cooperativa = Cooperativa()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-7): ").strip()
        if opcion == "1":
            crear_playa(cooperativa)
        elif opcion == "2":
            registrar_dia(cooperativa)
        elif opcion == "3":
            simular(cooperativa)
        elif opcion == "4":
            mostrar_informe(cooperativa)
        elif opcion == "5":
            mostrar_extremos(cooperativa)
        elif opcion == "6":
            cargar_archivos(cooperativa)
        elif opcion == "7":
            print("Programa finalizado.")
            break
        else:
            print("Opcion no valida. Seleccione una opcion del 1 al 7.")


if __name__ == "__main__":
    main()
