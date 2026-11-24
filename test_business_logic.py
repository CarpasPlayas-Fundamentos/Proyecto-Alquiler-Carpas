"""Pruebas automaticas de la logica. Ejecutar: python -m unittest -v"""
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from business_logic import Cooperativa, Playa


class PruebasCarpas(unittest.TestCase):
    def setUp(self):
        self.coop = Cooperativa()
        self.playa = self.coop.crear_playa("Playa Blanca", 120, date(2026, 11, 1))

    def test_total_promedio_porcentaje(self):
        self.playa.alquileres = [100, 80]
        self.assertEqual(self.playa.total_alquileres(), 180)
        self.assertEqual(self.playa.promedio(), 90)
        self.assertEqual(self.playa.porcentaje_alquiler(), 75)

    def test_desviacion_poblacional(self):
        self.playa.alquileres = [100, 80]
        self.assertEqual(round(self.playa.desviacion_estandar(), 2), 10.0)

    def test_niveles_en_limites(self):
        # 120 carpas: 47 bajo, 48 medio, 83 medio, 84 alto, 113 alto, 114 agotado.
        self.assertEqual(self.playa.nivel_de_alquiler(47), "Bajo")
        self.assertEqual(self.playa.nivel_de_alquiler(48), "Medio")
        self.assertEqual(self.playa.nivel_de_alquiler(83), "Medio")
        self.assertEqual(self.playa.nivel_de_alquiler(84), "Alto")
        self.assertEqual(self.playa.nivel_de_alquiler(113), "Alto")
        self.assertEqual(self.playa.nivel_de_alquiler(114), "Agotado")

    def test_fechas_extremas_primera_aparicion(self):
        self.playa.alquileres = [90, 120, 30, 120, 30]
        mayor, menor = self.playa.fechas_extremas()
        self.assertEqual(mayor, date(2026, 11, 2))
        self.assertEqual(menor, date(2026, 11, 3))

    def test_racha_agotada_primera_en_empate(self):
        # Con 120 carpas, 114 es agotado. Dos rachas de longitud dos.
        self.playa.alquileres = [114, 120, 10, 115, 120]
        longitud, inicio = self.playa.racha_mas_larga_agotada()
        self.assertEqual(longitud, 2)
        self.assertEqual(inicio, date(2026, 11, 1))

    def test_sin_dias(self):
        self.assertEqual(self.playa.promedio(), 0)
        self.assertEqual(self.playa.desviacion_estandar(), 0)
        self.assertEqual(self.playa.fechas_extremas(), (None, None))
        self.assertEqual(self.playa.racha_mas_larga_agotada(), (0, None))

    def test_nombre_distingue_mayusculas_y_tildes(self):
        self.assertIsNone(self.coop.buscar_playa("playa blanca"))
        self.assertIsNone(self.coop.buscar_playa("Playa Blánca"))
        self.assertIs(self.coop.buscar_playa("  Playa Blanca  "), self.playa)

    def test_registro_rechaza_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.playa.registrar_alquiler(121)
        with self.assertRaises(ValueError):
            self.playa.registrar_alquiler(-1)

    def test_simulacion_no_agrega_si_limites_invertidos(self):
        with self.assertRaises(ValueError):
            self.playa.simular_dias(3, 80, 20)
        self.assertEqual(self.playa.alquileres, [])

    def test_comparacion_porcentaje_sin_redondear(self):
        otra = self.coop.crear_playa("Playa Grande", 100, date(2026, 11, 1))
        self.playa.alquileres = [60]       # 50 %
        otra.alquileres = [50, 51]        # 50.5 %
        mayor, menor = self.coop.playa_con_porcentaje_mayor_y_menor()
        self.assertIs(mayor, otra)
        self.assertIs(menor, self.playa)

    def test_csv_playas_y_alquileres_con_lineas_invalidas(self):
        with TemporaryDirectory() as carpeta:
            ruta_playas = Path(carpeta) / "playas.csv"
            ruta_alquileres = Path(carpeta) / "alquileres.csv"
            ruta_playas.write_text(
                "playa;carpas;anio;mes;dia\n"
                "Playa Uno;10;2026;11;1\n"
                "Playa Mala;0;2026;11;1\n"
                "Playa Dos;20;2026;2;30\n",
                encoding="utf-8"
            )
            nueva = Cooperativa()
            r1 = nueva.cargar_playas_csv(ruta_playas)
            self.assertEqual(r1["cargadas"], 1)
            self.assertEqual(len(r1["errores"]), 2)

            ruta_alquileres.write_text(
                "playa;carpas_alquiladas\n"
                "Playa Uno;5\n"
                "Playa Uno;11\n"
                "No Existe;2\n"
                "Playa Uno;cinco\n",
                encoding="utf-8"
            )
            r2 = nueva.cargar_alquileres_csv(ruta_alquileres)
            self.assertEqual(r2["cargados"], 1)
            self.assertEqual(nueva.buscar_playa("Playa Uno").alquileres, [5])
            self.assertEqual(len(r2["errores"]), 3)


if __name__ == "__main__":
    unittest.main()
