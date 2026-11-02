# Relatório Técnico Final: Otimização de Rotas Médicas (VRP)

## 1. Evolução do Código Base e Implementação do Algoritmo
O código base fornecido para o Problema do Caixeiro Viajante (TSP) foi reestruturado para solucionar o Problema de Roteamento de Veículos (VRP). A representação cromossômica foi mantida como uma permutação única de destinos para preservar a integridade dos dados, mas acoplada a uma função de decodificação dinâmica. Esta função segmenta a matriz de destinos entre os múltiplos veículos da frota no momento da avaliação matemática, garantindo que o algoritmo genético opere de forma eficiente e sem duplicar pontos de entrega. O operador de *Crossover* de Ordem (OX1) foi implementado para evitar a corrupção genética (hospitais esquecidos ou visitados duas vezes), enquanto a Mutação *Swap* foi aplicada para garantir a diversidade das rotas.

## 2. Estratégias Matemáticas para Restrições Logísticas
Para lidar com a complexidade do roteamento hospitalar realista, a função de *fitness* foi programada com um sistema rigoroso de penalidades:
* **Prioridade Clínica:** Medicamentos sinalizados como "críticos" forçam o algoritmo a alocá-los nos primeiros índices da rota. Entregas críticas após o segundo atendimento recebem uma penalidade severa de +5000 pontos na função de avaliação.
* **Capacidade de Carga e Autonomia:** O sistema monitoriza continuamente o volume alocado em cada veículo. Qualquer quebra da capacidade máxima ou da autonomia de quilometragem gera uma penalidade exponencial (+10000 pontos por unidade excedente), forçando a evolução genética a descartar rotas logisticamente impossíveis.

## 3. Comparativo de Desempenho e Eficiência
Com base nos dados extraídos da execução no terminal, o modelo não otimizado (aleatório inicial) apresentava custos de deslocamento ineficientes e quebras frequentes de capacidade. Após as gerações de otimização genética:
* **Distância Total Otimizada:** Reduzida para 77 km cravados.
* **Distribuição de Frota:** O Veículo 1 assumiu 42 km (80% de capacidade), enquanto o Veículo 2 assumiu 35 km (60% de capacidade).
* A aplicação das penalidades garantiu 100% de conformidade com as restrições logísticas, com todas as entregas críticas ocorrendo no primeiro ponto de parada de cada veículo.

## 4. Análises das Visualizações Espaciais
A integração com a biblioteca Folium gerou a renderização de um mapa em formato HTML interativo (`mapa_rotas_hospital.html`). A visualização confirmou o sucesso do sequenciamento, plotando vetores de cores distintas para cada veículo. A análise visual demonstra a ausência de sobreposição desnecessária de rotas, comprovando que o algoritmo conseguiu agrupar geograficamente os hospitais (ex: Veículo 1 focado no vetor Leste, Veículo 2 no vetor Oeste), o que facilita a interpretação e a tomada de decisão logística.

## 5. Estratégias de Integração com LLMs (Engenharia de Prompts)
O sistema utilizou o modelo pré-treinado `gpt-4o-mini` da OpenAI de forma desacoplada da matemática. Foram desenhados *system prompts* rigorosos para ingerir matrizes JSON e devolver linguagem natural estruturada:
* **Instruções de Navegação:** A IA traduziu com sucesso os IDs dos nós genéticos para orientações humanas ("Veículo 1 - Hospital A (Prioridade) -> Hospital B"), garantindo clareza para os motoristas.
* **Relatórios Gerenciais:** Os relatórios comprovaram que a IA é capaz de calcular médias (70% de capacidade média utilizada) e sugerir melhorias lógicas, como o planejamento da demanda e otimização do espaço ocioso do Veículo 2, sem alucinar métricas externas ao contexto JSON enviado.