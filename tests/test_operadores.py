import pytest
from src.operadores import crossover_ordem, mutacao_swap

def test_crossover_ordem_mantem_integridade():
    pai1 = [1, 2, 3, 4, 5]
    pai2 = [5, 4, 3, 2, 1]
    
    filho = crossover_ordem(pai1, pai2)
    
    # O tamanho precisa ser exatamente igual
    assert len(filho) == 5
    # Não pode haver hospitais duplicados nem esquecidos
    assert set(filho) == set(pai1)

def test_mutacao_swap_mantem_integridade():
    cromossomo_original = [1, 2, 3, 4]
    
    # Forçamos a taxa de mutação para 1.0 (100%) para garantir que a troca ocorra no teste
    cromossomo_mutado = mutacao_swap(cromossomo_original.copy(), taxa_mutacao=1.0)
    
    assert len(cromossomo_mutado) == 4
    assert set(cromossomo_mutado) == set(cromossomo_original)
    # Garante que os elementos apenas mudaram de lugar
    assert cromossomo_mutado != cromossomo_original or len(cromossomo_original) < 2