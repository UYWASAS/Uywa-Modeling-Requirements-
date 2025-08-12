import numpy as np
import pandas as pd

from helpers import energy_unit_convert

class PigGrowEnergy:
    """
    Modelo factorial para porcinos en crecimiento/cebo.
    Todos los valores en kcal/día a menos que se indique.
    Parámetros: véase params/pig_grow.csv
    """
    def __init__(self, params: dict, unidad: str = "kcal"):
        self.params = params
        self.unidad = unidad

    def me_mto(self, PV, a_cat, b):
        """Mantenimiento: ME_mto = a_cat * PV^b"""
        return a_cat * (PV ** b)

    def me_term(self, s_cat, TCI, T_amb):
        """Térmica: ME_term = s_cat * max(0, TCI − T_amb)"""
        return s_cat * max(0, TCI - T_amb)

    def me_growth(self, ADG, f_P, f_G, e_P, e_G, k_P, k_G):
        """
        Crecimiento: ME_crec = (RE_P / k_P) + (RE_G / k_G)
        RE_P = gP * e_P; RE_G = gG * e_G
        gP, gG en g/día
        """
        gP = ADG * f_P
        gG = ADG * f_G
        RE_P = gP * e_P
        RE_G = gG * e_G
        return (RE_P / k_P) + (RE_G / k_G)

    def me_total(self, PV, ADG, f_P, f_G, T_amb, TCI=None):
        a_cat = self.params["a_cat"]
        b = self.params["b"]
        s_cat = self.params["s_cat"]
        TCI = TCI if TCI is not None else self.params["TCI_base"]
        e_P = self.params["e_P"]
        e_G = self.params["e_G"]
        k_P = self.params["k_P"]
        k_G = self.params["k_G"]

        me_mto = self.me_mto(PV, a_cat, b)
        me_term = self.me_term(s_cat, TCI, T_amb)
        me_crec = self.me_growth(ADG, f_P, f_G, e_P, e_G, k_P, k_G)
        # ME_act: opcional, aquí 0 por defecto.
        me_act = 0
        total = me_mto + me_term + me_act + me_crec
        return total

# Implementar otras clases: SowGestationEnergy, SowLactationEnergy, BroilerEnergy, LayerEnergy, con firmas similares.
