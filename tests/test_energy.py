import pytest
from models.energy import PigGrowEnergy

def test_me_mto():
    params = {"a_cat": 100, "b": 0.75, "s_cat": 20, "TCI_base": 20, "e_P": 5.7, "e_G": 9.5, "k_P": 0.5, "k_G": 0.6}
    model = PigGrowEnergy(params)
    assert abs(model.me_mto(50, 100, 0.75) - 100 * (50 ** 0.75)) < 1

def test_me_term():
    params = {"a_cat": 100, "b": 0.75, "s_cat": 20, "TCI_base": 20, "e_P": 5.7, "e_G": 9.5, "k_P": 0.5, "k_G": 0.6}
    model = PigGrowEnergy(params)
    assert model.me_term(20, 20, 15) == 100
    assert model.me_term(20, 20, 25) == 0

def test_me_growth():
    params = {"a_cat": 100, "b": 0.75, "s_cat": 20, "TCI_base": 20, "e_P": 5.7, "e_G": 9.5, "k_P": 0.5, "k_G": 0.6}
    model = PigGrowEnergy(params)
    # 1000g/día, f_P=0.2, f_G=0.1
    res = model.me_growth(1000, 0.2, 0.1, 5.7, 9.5, 0.5, 0.6)
    assert res > 0
