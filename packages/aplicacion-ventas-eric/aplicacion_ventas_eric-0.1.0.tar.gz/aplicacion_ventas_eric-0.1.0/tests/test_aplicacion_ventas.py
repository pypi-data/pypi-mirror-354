import unittest
from aplicacion.gestor_ventas import GestorVentas
from aplicacion.exceptions import ImpuestosInvalidoError, DescuentoInvalidoError


class TestGestorVentas(unittest.TestCase):
    def test_calculo_precio_final(self):
        gestor = GestorVentas(100,0.05,0.1)
        self.assertEqual(gestor.calcular_precio_final(),95.0)
    def test_impuesto_invalido(self):
        with self.assertRaises(ImpuestosInvalidoError):
            GestorVentas(100,1.5,0.10)
    def test_descuento_invalido(self):
        with self.assertRaises(DescuentoInvalidoError):
            GestorVentas(100,0.05,1.5)

if __name__ == "__main__":
    unittest.main()

