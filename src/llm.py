import json
from openai import OpenAI

def gerar_instrucoes_rota(matriz_rotas: dict | list) -> str:
    # Gera instruções legíveis para os motoristas a partir das rotas em JSON
    prompt_sistema = (
        "Você é um assistente de logística hospitalar. Receba a matriz JSON de "
        "rotas e gere instruções detalhadas e fáceis de ler para os motoristas. "
        "Destaque medicamentos críticos primeiro. Formato exigido: Veículo 1 - "
        "Destino A (Prioridade) -> Destino B."
    )
    dados_rota = json.dumps(matriz_rotas, ensure_ascii=False)
    cliente = OpenAI()
    resposta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {
                "role": "user",
                "content": f"Matriz JSON de rotas:\n{dados_rota}",
            },
        ],
    )

    instrucoes = resposta.choices[0].message.content
    if not instrucoes:
        raise RuntimeError("A API não retornou instruções para a rota.")

    return instrucoes

def gerar_relatorio_gerencial(dados_logisticos: dict | list) -> str:
    # Gera um relatório de eficiência logística com base nos dados fornecidos
    prompt_sistema = (
        "Baseado nas distâncias percorridas e na capacidade utilizada enviada "
        "no JSON, crie um relatório gerencial resumindo a eficiência logística "
        "do dia, a economia de recursos e sugira melhorias no processo com "
        "base nos padrões. Use somente os dados fornecidos e não invente "
        "métricas ausentes."
    )
    dados_json = json.dumps(dados_logisticos, ensure_ascii=False)
    cliente = OpenAI()
    resposta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {
                "role": "user",
                "content": f"Dados logísticos do dia em JSON:\n{dados_json}",
            },
        ],
    )

    relatorio = resposta.choices[0].message.content
    if not relatorio:
        raise RuntimeError("A API não retornou o relatório gerencial.")

    return relatorio