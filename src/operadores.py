import random

def selecao_torneio(populacao, funcao_fitness, tamanho_torneio=3):
    competidores = random.sample(populacao, tamanho_torneio)
    return min(competidores, key=funcao_fitness)

def crossover_ordem(pai1, pai2):
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    
    filho[inicio:fim] = pai1[inicio:fim]
    
    ponteiro_pai2 = 0
    for i in range(tamanho):
        if filho[i] is None:
            while pai2[ponteiro_pai2] in filho:
                ponteiro_pai2 += 1
            filho[i] = pai2[ponteiro_pai2]
            
    return filho

def mutacao_swap(cromossomo, taxa_mutacao=0.1):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromossomo)), 2)
        cromossomo[idx1], cromossomo[idx2] = cromossomo[idx2], cromossomo[idx1]
    return cromossomo