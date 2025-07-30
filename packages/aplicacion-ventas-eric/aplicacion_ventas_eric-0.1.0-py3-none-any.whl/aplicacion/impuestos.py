from .exceptions import ImpuestosInvalidoError

class Impuesto:
    def __init__(self,impuesto):
        if not (0 <= impuesto <= 1):
            raise ImpuestosInvalidoError("La tasa de impuesto debe estar entre 0 y 1")
        self.impuesto = impuesto

    def aplicar_impuesto(self,precio):
        return precio*self.impuesto