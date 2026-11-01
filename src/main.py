from src.fitness import gerar_instrucoes_rota, gerar_relatorio_gerencial
from src.mapa import desenhar_mapa_rotas
from src.operadores import selecao_torneio, crossover_ordem, mutacao_swap

matriz = {
    "veiculos": [
        {
            "veiculo": "Veículo 1",
            "destinos": ["Hospital A", "Hospital B"],
            "distancia_percorrida_km": 42,
            "capacidade_utilizada": 80,
            "capacidade_total": 100,
        },
        {
            "veiculo": "Veículo 2",
            "destinos": ["Hospital C", "Hospital D"],
            "distancia_percorrida_km": 35,
            "capacidade_utilizada": 60,
            "capacidade_total": 100,
        },
    ],
}

coordenadas_hospital = [-23.5505, -46.6333]
rotas_otimizadas = [
    [
        {"id": "Hospital A", "coordenada": [-23.56, -46.64]},
        {"id": "Hospital B", "coordenada": [-23.57, -46.65]},
    ],
    [
        {"id": "Hospital C", "coordenada": [-23.54, -46.62]},
        {"id": "Hospital D", "coordenada": [-23.53, -46.61]},
    ],
]

arquivo_mapa = desenhar_mapa_rotas(coordenadas_hospital, rotas_otimizadas)
print(f"Mapa salvo em: {arquivo_mapa}")

print("Instruções para os motoristas:")
print(gerar_instrucoes_rota(matriz))

print("\nRelatório gerencial:")
print(gerar_relatorio_gerencial(matriz))