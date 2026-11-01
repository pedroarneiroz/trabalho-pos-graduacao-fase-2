import pandas as pd
import random
from src.fitness import calcular_fitness

import random
import numpy as np

# 1. Configuração Logística (Mock baseado nas capturas de tela)
HOSPITAL_BASE = (0, 0)
DESTINOS = {
    1: {'coord': (10, 20), 'demanda': 40, 'prioridade': 'critico', 'nome': 'Hospital A'},
    2: {'coord': (15, 5), 'demanda': 40, 'prioridade': 'normal', 'nome': 'Hospital B'},
    3: {'coord': (-10, 15), 'demanda': 30, 'prioridade': 'critico', 'nome': 'Hospital C'},
    4: {'coord': (-5, -10), 'demanda': 30, 'prioridade': 'normal', 'nome': 'Hospital D'}
}
VEICULOS = [{'id': 1, 'capacidade': 100}, {'id': 2, 'capacidade': 100}]
AUTONOMIA_MAXIMA = 100 

# 2. Representação e Decodificação do Cromossomo
def criar_populacao_inicial(tamanho_populacao, pontos_entrega):
    return [random.sample(pontos_entrega, len(pontos_entrega)) for _ in range(tamanho_populacao)]

def decodificar_cromossomo(cromossomo):
    """Divide a permutação única (TSP) em múltiplas rotas (VRP) baseando-se na capacidade de carga."""
    rotas = [[] for _ in VEICULOS]
    veiculo_atual = 0
    carga_atual = 0
    
    for ponto in cromossomo:
        demanda = DESTINOS[ponto]['demanda']
        # Troca de veículo se a capacidade exceder (e se ainda houver veículos disponíveis)
        if carga_atual + demanda > VEICULOS[veiculo_atual]['capacidade'] and veiculo_atual < len(VEICULOS) - 1:
            veiculo_atual += 1
            carga_atual = 0
            
        rotas[veiculo_atual].append(ponto)
        carga_atual += demanda
    return rotas

def calcular_distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# 3. Avaliação de Restrições (Fitness)
def fitness(cromossomo):
    rotas = decodificar_cromossomo(cromossomo)
    distancia_total = 0
    penalidade = 0
    
    for i, rota in enumerate(rotas):
        if not rota: continue
        
        carga_atual = 0
        distancia_veiculo = 0
        ponto_anterior = HOSPITAL_BASE
        
        for j, ponto_id in enumerate(rota):
            dados_ponto = DESTINOS[ponto_id]
            distancia_veiculo += calcular_distancia(ponto_anterior, dados_ponto['coord'])
            carga_atual += dados_ponto['demanda']
            
            # Penalidade: Medicamento crítico não entregue no início da rota (índice 0)
            if dados_ponto['prioridade'] == 'critico' and j > 0:
                penalidade += 5000 
                
            ponto_anterior = dados_ponto['coord']
            
        # Adiciona a distância de volta à base
        distancia_veiculo += calcular_distancia(ponto_anterior, HOSPITAL_BASE)
        distancia_total += distancia_veiculo
        
        # Penalidade matemática por quebra de restrições de negócio
        if carga_atual > VEICULOS[i]['capacidade']:
            penalidade += 10000 * (carga_atual - VEICULOS[i]['capacidade'])
        if distancia_veiculo > AUTONOMIA_MAXIMA:
            penalidade += 10000 * (distancia_veiculo - AUTONOMIA_MAXIMA)
            
    return distancia_total + penalidade

# 4. Operadores Genéticos Especializados
def crossover(pai1, pai2):
    """Crossover de Ordem (OX1): Garante que nenhum destino seja duplicado ou esquecido."""
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    filho[inicio:fim] = pai1[inicio:fim] # Herda segmento do pai1
    
    ponteiro_pai2 = 0
    for i in range(tamanho):
        if filho[i] is None:
            while pai2[ponteiro_pai2] in filho:
                ponteiro_pai2 += 1
            filho[i] = pai2[ponteiro_pai2] # Preenche o resto com genes do pai2 na ordem original
    return filho

def mutacao(cromossomo, taxa_mutacao=0.1):
    """Mutação Swap: Troca a ordem de duas entregas aleatórias para evitar mínimos locais."""
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromossomo)), 2)
        cromossomo[idx1], cromossomo[idx2] = cromossomo[idx2], cromossomo[idx1]
    return cromossomo

# 5. Loop Principal de Evolução
def executar_algoritmo_genetico(geracoes=100, tamanho_populacao=50):
    pontos_entrega = list(DESTINOS.keys())
    populacao = criar_populacao_inicial(tamanho_populacao, pontos_entrega)
    
    for _ in range(geracoes):
        populacao = sorted(populacao, key=fitness)
        nova_populacao = populacao[:2] # Elitismo: preserva as 2 melhores rotas intactas
        
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.choices(populacao[:10], k=2) # Seleção baseada no ranking dos melhores
            filho = crossover(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao=0.15)
            nova_populacao.append(filho)
            
        populacao = nova_populacao
        
    melhor_cromossomo = min(populacao, key=fitness)
    return decodificar_cromossomo(melhor_cromossomo)

if __name__ == "__main__":
    melhor_rota = executar_algoritmo_genetico()
    print("Melhor distribuição por veículo (IDs dos Hospitais):", melhor_rota)