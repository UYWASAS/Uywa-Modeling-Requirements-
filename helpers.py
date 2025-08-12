import numpy as np

def kcal_to_kj(val):
    """Convierte kcal a kJ"""
    return val * 4.184

def kj_to_kcal(val):
    """Convierte kJ a kcal"""
    return val / 4.184

def kcal_to_mj(val):
    """Convierte kcal a MJ"""
    return val * 0.004184

def mj_to_kcal(val):
    """Convierte MJ a kcal"""
    return val / 0.004184

def energy_unit_convert(val, from_unit, to_unit):
    if from_unit == to_unit:
        return val
    if from_unit == "kcal":
        if to_unit == "kJ":
            return kcal_to_kj(val)
        elif to_unit == "MJ":
            return kcal_to_mj(val)
    elif from_unit == "kJ":
        if to_unit == "kcal":
            return kj_to_kcal(val)
        elif to_unit == "MJ":
            return val / 1000
    elif from_unit == "MJ":
        if to_unit == "kcal":
            return mj_to_kcal(val)
        elif to_unit == "kJ":
            return val * 1000
    raise ValueError("Unidades de energía no soportadas")
