from src.fitness import calcular_fitness


COORDENADAS = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (3, 0),
    5: (4, 0),
}
DEMANDAS_SEM_EXCESSO = {ponto: 10 for ponto in COORDENADAS}
PRIORIDADES = {
    1: "normal",
    2: "normal",
    3: "normal",
    4: "normal",
    5: "critico",
}


def test_fitness_sem_penalidades():
    rotas = [[1, 2]]

    pontuacao = calcular_fitness(
        rotas,
        COORDENADAS,
        [100],
        DEMANDAS_SEM_EXCESSO,
        PRIORIDADES,
    )

    assert pontuacao == 1


def test_penalidade_medicamento_critico_atrasado():
    rotas = [[1, 2, 3, 4, 5]]

    pontuacao = calcular_fitness(
        rotas,
        COORDENADAS,
        [100],
        DEMANDAS_SEM_EXCESSO,
        PRIORIDADES,
    )

    assert pontuacao == 5004


def test_penalidade_excesso_de_carga():
    demandas = {1: 40, 2: 40, 3: 40, 4: 40, 5: 10}
    rotas = [[1, 2, 3, 4], []]

    pontuacao = calcular_fitness(
        rotas,
        COORDENADAS,
        [100, 100],
        demandas,
        PRIORIDADES,
    )

    assert pontuacao == 200003
