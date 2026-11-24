"""
Logica del negocio para la Cooperativa de Carperos de Santa Marta.
Este archivo no contiene instrucciones input() ni print() de la interfaz.
"""

from datetime import date, timedelta
import csv
import random


class Playa:
    """Guarda los datos y calcula indicadores de una playa."""

    def __init__(self, nombre, carpas_instaladas, fecha_inicio):
        self.nombre = nombre.strip()
        self.carpas_instaladas = carpas_instaladas
        self.fecha_inicio = fecha_inicio
        self.alquileres = []

    def fecha_de_dia(self, posicion):
        """Devuelve la fecha del alquiler en una posicion que comienza en cero."""
        return self.fecha_inicio + timedelta(days=posicion)

    def registrar_alquiler(self, cantidad):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise ValueError("Las carpas alquiladas deben ser un numero entero.")
        if cantidad < 0 or cantidad > self.carpas_instaladas:
            raise ValueError(
                f"Las carpas alquiladas deben estar entre 0 y {self.carpas_instaladas}."
            )
        self.alquileres.append(cantidad)

    def simular_dias(self, cantidad_dias, minimo, maximo, generador=None):
        """Agrega dias aleatorios. Los limites minimo y maximo estan incluidos."""
        if cantidad_dias < 1:
            raise ValueError("Se debe simular al menos un dia.")
        if minimo < 0 or minimo > self.carpas_instaladas:
            raise ValueError(
                f"Las carpas alquiladas deben estar entre 0 y {self.carpas_instaladas}."
            )
        if maximo < 0 or maximo > self.carpas_instaladas:
            raise ValueError(
                f"Las carpas alquiladas deben estar entre 0 y {self.carpas_instaladas}."
            )
        if minimo > maximo:
            raise ValueError("El minimo no puede ser mayor que el maximo.")

        if generador is None:
            generador = random
        nuevos = []
        for _ in range(cantidad_dias):
            nuevos.append(generador.randint(minimo, maximo))
        self.alquileres.extend(nuevos)
        return nuevos

    def total_alquileres(self):
        return sum(self.alquileres)

    def promedio(self):
        if len(self.alquileres) == 0:
            return 0
        return self.total_alquileres() / len(self.alquileres)

    def porcentaje_alquiler(self):
        if len(self.alquileres) == 0:
            return 0
        return self.promedio() / self.carpas_instaladas * 100

    def desviacion_estandar(self):
        """Desviacion estandar poblacional: divide entre N, no entre N-1."""
        if len(self.alquileres) == 0:
            return 0
        media = self.promedio()
        suma = 0
        for valor in self.alquileres:
            suma += (valor - media) ** 2
        varianza = suma / len(self.alquileres)
        return varianza ** 0.5

    def fechas_extremas(self):
        """Retorna (fecha_maximo, fecha_minimo); conserva la primera fecha empatada."""
        if not self.alquileres:
            return None, None
        maximo = max(self.alquileres)
        minimo = min(self.alquileres)
        indice_maximo = self.alquileres.index(maximo)
        indice_minimo = self.alquileres.index(minimo)
        return self.fecha_de_dia(indice_maximo), self.fecha_de_dia(indice_minimo)

    def nivel_de_alquiler(self, cantidad):
        porcentaje = cantidad / self.carpas_instaladas * 100
        if porcentaje < 40:
            return "Bajo"
        if porcentaje < 70:
            return "Medio"
        if porcentaje < 95:
            return "Alto"
        return "Agotado"

    def conteo_niveles(self):
        conteos = {"Bajo": 0, "Medio": 0, "Alto": 0, "Agotado": 0}
        for cantidad in self.alquileres:
            nivel = self.nivel_de_alquiler(cantidad)
            conteos[nivel] += 1
        return conteos

    def racha_mas_larga_agotada(self):
        """Retorna (longitud, fecha_inicio); en empate conserva la primera racha."""
        mejor_longitud = 0
        mejor_inicio = None
        longitud_actual = 0
        inicio_actual = None

        for indice, cantidad in enumerate(self.alquileres):
            if self.nivel_de_alquiler(cantidad) == "Agotado":
                if longitud_actual == 0:
                    inicio_actual = self.fecha_de_dia(indice)
                longitud_actual += 1
                if longitud_actual > mejor_longitud:
                    mejor_longitud = longitud_actual
                    mejor_inicio = inicio_actual
            else:
                longitud_actual = 0
                inicio_actual = None

        return mejor_longitud, mejor_inicio

    def dias_pendientes(self, hoy=None):
        """Cuenta desde el dia siguiente al ultimo registro hasta ayer."""
        if hoy is None:
            hoy = date.today()
        if not self.alquileres:
            return None, 0
        ultimo_dia = self.fecha_de_dia(len(self.alquileres) - 1)
        ayer = hoy - timedelta(days=1)
        pendientes = (ayer - ultimo_dia).days
        if pendientes < 0:
            pendientes = 0
        return ultimo_dia, pendientes

    def informe(self, hoy=None):
        ultimo_dia, pendientes = self.dias_pendientes(hoy)
        return {
            "nombre": self.nombre,
            "carpas_instaladas": self.carpas_instaladas,
            "dias_registrados": len(self.alquileres),
            "alquileres_totales": self.total_alquileres(),
            "promedio": self.promedio(),
            "porcentaje": self.porcentaje_alquiler(),
            "desviacion_estandar": self.desviacion_estandar(),
            "fechas_extremas": self.fechas_extremas(),
            "conteo_niveles": self.conteo_niveles(),
            "racha_agotada": self.racha_mas_larga_agotada(),
            "ultimo_dia": ultimo_dia,
            "dias_pendientes": pendientes,
        }


class Cooperativa:
    """Administra la lista de playas."""

    def __init__(self):
        self.playas = []

    def buscar_playa(self, nombre):
        nombre = nombre.strip()
        for playa in self.playas:
            # La comparacion distingue mayusculas y tildes, pero ignora espacios externos.
            if playa.nombre == nombre:
                return playa
        return None

    def crear_playa(self, nombre, carpas_instaladas, fecha_inicio):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la playa no puede estar vacio.")
        if self.buscar_playa(nombre) is not None:
            raise ValueError("Ya existe una playa con ese nombre.")
        if not isinstance(carpas_instaladas, int) or isinstance(carpas_instaladas, bool):
            raise ValueError("El numero de carpas instaladas debe ser un numero entero.")
        if carpas_instaladas < 1:
            raise ValueError("La playa debe tener al menos una carpa instalada.")
        if not isinstance(fecha_inicio, date):
            raise ValueError("La fecha de inicio no es valida.")
        playa = Playa(nombre, carpas_instaladas, fecha_inicio)
        self.playas.append(playa)
        return playa

    def playa_con_porcentaje_mayor_y_menor(self):
        """Compara porcentajes sin redondear; max/min conservan el primer empate."""
        candidatas = [p for p in self.playas if len(p.alquileres) > 0]
        if not candidatas:
            return None, None
        mayor = candidatas[0]
        menor = candidatas[0]
        for playa in candidatas[1:]:
            if playa.porcentaje_alquiler() > mayor.porcentaje_alquiler():
                mayor = playa
            if playa.porcentaje_alquiler() < menor.porcentaje_alquiler():
                menor = playa
        return mayor, menor

    def cargar_playas_csv(self, ruta):
        """Carga playas desde CSV separado por punto y coma."""
        if self.playas:
            return {"cargadas": 0, "errores": ["La carga solo se permite cuando no hay playas."]}
        cargadas = 0
        errores = []
        try:
            archivo = open(ruta, "r", encoding="utf-8-sig", newline="")
        except FileNotFoundError:
            return {"cargadas": 0, "errores": ["El archivo de playas no existe."], "archivo_no_existe": True}

        with archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado is None:
                return {"cargadas": 0, "errores": ["El archivo de playas esta vacio."]}
            for numero_linea, fila in enumerate(lector, start=2):
                if not fila or all(campo.strip() == "" for campo in fila):
                    continue
                if len(fila) != 5:
                    errores.append(f"Linea {numero_linea}: debe tener cinco campos.")
                    continue
                nombre = fila[0].strip()
                if not nombre:
                    errores.append(f"Linea {numero_linea}: el nombre de la playa no puede estar vacio.")
                    continue
                if self.buscar_playa(nombre) is not None:
                    errores.append(f"Linea {numero_linea}: ya existe una playa con ese nombre.")
                    continue
                try:
                    carpas = int(fila[1].strip())
                except ValueError:
                    errores.append(f"Linea {numero_linea}: las carpas instaladas deben ser un numero entero.")
                    continue
                if carpas < 1:
                    errores.append(f"Linea {numero_linea}: la playa debe tener al menos una carpa instalada.")
                    continue
                try:
                    anio = int(fila[2].strip())
                    mes = int(fila[3].strip())
                    dia = int(fila[4].strip())
                    fecha_inicio = date(anio, mes, dia)
                except ValueError:
                    errores.append(f"Linea {numero_linea}: la fecha de inicio no es valida.")
                    continue
                self.crear_playa(nombre, carpas, fecha_inicio)
                cargadas += 1
        return {"cargadas": cargadas, "errores": errores}

    def cargar_alquileres_csv(self, ruta):
        """Cada fila valida se agrega como el siguiente dia de la playa indicada."""
        cargados = 0
        errores = []
        try:
            archivo = open(ruta, "r", encoding="utf-8-sig", newline="")
        except FileNotFoundError:
            return {"cargados": 0, "errores": ["El archivo de alquileres no existe."], "archivo_no_existe": True}

        with archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado is None:
                return {"cargados": 0, "errores": ["El archivo de alquileres esta vacio."]}
            for numero_linea, fila in enumerate(lector, start=2):
                if not fila or all(campo.strip() == "" for campo in fila):
                    continue
                if len(fila) != 2:
                    errores.append(f"Linea {numero_linea}: debe tener dos campos.")
                    continue
                nombre = fila[0].strip()
                playa = self.buscar_playa(nombre)
                if playa is None:
                    errores.append(f"Linea {numero_linea}: no hay una playa con ese nombre.")
                    continue
                try:
                    cantidad = int(fila[1].strip())
                except ValueError:
                    errores.append(f"Linea {numero_linea}: las carpas alquiladas deben ser un numero entero.")
                    continue
                if cantidad < 0 or cantidad > playa.carpas_instaladas:
                    errores.append(
                        f"Linea {numero_linea}: las carpas alquiladas deben estar entre 0 y {playa.carpas_instaladas}."
                    )
                    continue
                playa.registrar_alquiler(cantidad)
                cargados += 1
        return {"cargados": cargados, "errores": errores}
