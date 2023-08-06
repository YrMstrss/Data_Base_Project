from src.func import get_employer_id
import pytest


def test_get_employer_id():
    assert get_employer_id('Яндекс') == '3918788'
