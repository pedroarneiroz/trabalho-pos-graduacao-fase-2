import numpy as np

AUTONOMIA_MAXIMA = 100

def calcular_distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calcular_fitness(rota_veiculos, coordenadas, capacidades, demandas, prioridades):
    distancia_total = 0
    penalidade = 0
    
    for i, rota in enumerate(rota_veiculos):
        carga_atual = 0
        distancia_veiculo = 0
        
        # 1 - Calcula a distância da rota
        for j in range(len(rota) - 1):
            distancia_veiculo += calcular_distancia(coordenadas[rota[j]], coordenadas[rota[j+1]])
            carga_atual += demandas[rota[j+1]]
            
            # 2 - Penalidade por quebra de prioridade [ex: medicamento crítico atrasado]
            if prioridades[rota[j+1]] == 'critico' and j > 2:
                penalidade += 5000 
                
        distancia_total += distancia_veiculo
        
        # 3 - Penalidade por quebra de restrições de capacidade e autonomia
        if carga_atual > capacidades[i]:
            penalidade += 10000 * (carga_atual - capacidades[i])
        
        if distancia_veiculo > AUTONOMIA_MAXIMA:
            penalidade += 10000 * (distancia_veiculo - AUTONOMIA_MAXIMA)

    return distancia_total + penalidade