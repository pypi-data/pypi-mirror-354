class Precios:
    @staticmethod # Es un decorador para definir un clase que no necesita el uso de self(la instancias propias de la clase)
                  # y cls(clase) no depende del estado del objeto ni la clase y simplemente es ahi por organizacion logica
    def calcular_precio_final(precio_base,impuesto,descuento):
        return precio_base+impuesto-descuento