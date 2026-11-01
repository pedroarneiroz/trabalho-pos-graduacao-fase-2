import pytest
from src.algoritmo_genetico import decodificar_cromossomo, fitness, DESTINOS, VEICULOS

def test_decodificacao_respeita_capacidade():
    # Um cromossomo com todos os destinos
    cromossomo = [1, 2, 3, 4]
    rotas = decodificar_cromossomo(cromossomo)
    
    # Verifica se os veículos não ultrapassaram a capacidade de 100
    for i, rota in enumerate(rotas):
        carga = sum(DESTINOS[ponto]['demanda'] for ponto in rota)
        assert carga <= VEICULOS[i]['capacidade']

def test_penalidade_prioridade_critica():
    # Rota onde o hospital crítico (1) é o último a ser visitado, devendo gerar penalidade
    cromossomo_ruim = [2, 4, 1, 3]
    cromossomo_bom = [1, 2, 3, 4]
    
    fitness_ruim = fitness(cromossomo_ruim)
    fitness_bom = fitness(cromossomo_bom)
    
    # O fitness ruim deve ser muito maior (pior) devido à penalidade de 5000 aplicada
    assert fitness_ruim > fitness_bom + 4000