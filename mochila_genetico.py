# -*- coding: utf-8 -*-
# mochila_genetico.py

import random

# ... (demais funções como calcular_peso_e_valor, funcao_fitness, criar_individuo, etc. permanecem as mesmas) ...

# função para calcular o peso e o valor total de uma solução (indivíduo)
def calcular_peso_e_valor(solucao, itens):
    peso_total = 0
    valor_total = 0
    for i, item_incluido in enumerate(solucao):
        if item_incluido == 1:
            peso_total += itens[i]["peso"]
            valor_total += itens[i]["valor"]
    return peso_total, valor_total

# função de fitness (aptidão)
def funcao_fitness(solucao, itens, capacidade_mochila):
    peso_da_solucao, valor_da_solucao = calcular_peso_e_valor(solucao, itens)
    if peso_da_solucao > capacidade_mochila:
        return 0  
    else:
        return valor_da_solucao

# função para criar um indivíduo aleatório
def criar_individuo(numero_de_itens):
    return [random.randint(0, 1) for _ in range(numero_de_itens)]

# função para criar a população inicial
def criar_populacao_inicial(tamanho_populacao, numero_de_itens):
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(criar_individuo(numero_de_itens))
    return populacao

# função de seleção (torneio)
def selecao_torneio(populacao, itens, capacidade_mochila, tamanho_torneio=3):
    participantes_torneio = random.sample(populacao, tamanho_torneio)
    fitness_participantes = [(individuo, funcao_fitness(individuo, itens, capacidade_mochila)) for individuo in participantes_torneio]
    fitness_participantes.sort(key=lambda x: x[1], reverse=True)
    return fitness_participantes[0][0]

# função de crossover (um ponto)
def crossover_um_ponto(pai1, pai2):
    numero_de_itens = len(pai1)
    if numero_de_itens < 2:
        return pai1, pai2
    ponto_de_corte = random.randint(1, numero_de_itens - 1)
    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]
    return filho1, filho2

# função de mutação (bit flip)
def mutacao_bit_flip(individuo, taxa_de_mutacao=0.01):
    individuo_mutado = []
    for gene in individuo:
        if random.random() < taxa_de_mutacao:
            individuo_mutado.append(1 - gene) 
        else:
            individuo_mutado.append(gene)
    return individuo_mutado

# loop principal do algoritmo genético
def algoritmo_genetico_mochila(itens, capacidade_mochila, tamanho_populacao, numero_geracoes, taxa_mutacao, tamanho_torneio=3, callback_geracao=None):
    # Adicionado callback_geracao como parâmetro opcional
    numero_de_itens = len(itens)
    populacao_atual = criar_populacao_inicial(tamanho_populacao, numero_de_itens)
    melhor_individuo_global = None
    melhor_fitness_global = -1
    historico_melhor_fitness_geracao = []

    for geracao in range(numero_geracoes):
        populacao_com_fitness = []
        melhor_fitness_da_geracao_atual = -1

        for individuo in populacao_atual:
            fitness = funcao_fitness(individuo, itens, capacidade_mochila)
            populacao_com_fitness.append((individuo, fitness))
            if fitness > melhor_fitness_global:
                melhor_fitness_global = fitness
                melhor_individuo_global = individuo
            if fitness > melhor_fitness_da_geracao_atual:
                melhor_fitness_da_geracao_atual = fitness
        
        populacao_com_fitness.sort(key=lambda x: x[1], reverse=True)
        historico_melhor_fitness_geracao.append(populacao_com_fitness[0][1])

        # Chama o callback aqui, se fornecido
        if callback_geracao:
            # Passa o número da geração (base 1) e o melhor fitness da geração atual
            callback_geracao(geracao + 1, populacao_com_fitness[0][1])

        proxima_populacao = []
        # Elitismo simples: manter o melhor indivíduo da geração atual se ele for bom
        # Para garantir que o melhor global seja preservado, podemos adicioná-lo se não estiver lá
        # ou se a população for totalmente nova. Uma forma mais simples é adicionar o melhor da geração atual.
        if populacao_com_fitness: # Garante que a população não está vazia
             proxima_populacao.append(populacao_com_fitness[0][0])

        while len(proxima_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao_atual, itens, capacidade_mochila, tamanho_torneio)
            pai2 = selecao_torneio(populacao_atual, itens, capacidade_mochila, tamanho_torneio)
            filho1, filho2 = crossover_um_ponto(pai1, pai2)
            filho1_mutado = mutacao_bit_flip(filho1, taxa_mutacao)
            filho2_mutado = mutacao_bit_flip(filho2, taxa_mutacao)
            proxima_populacao.append(filho1_mutado)
            if len(proxima_populacao) < tamanho_populacao:
                proxima_populacao.append(filho2_mutado)
        
        populacao_atual = proxima_populacao[:tamanho_populacao] # Garante o tamanho da população

    peso_final, valor_final = calcular_peso_e_valor(melhor_individuo_global, itens) if melhor_individuo_global else (0,0)

    return melhor_individuo_global, valor_final, peso_final, historico_melhor_fitness_geracao

if __name__ == "__main__":
    def meu_callback_simples(num_ger, fitness_ger):
        print(f"Callback da Geracao: {num_ger}, Melhor Fitness: {fitness_ger}")

    itens_exemplo = [
        {"nome": "item_1", "peso": 2, "valor": 30},
        {"nome": "item_2", "peso": 3, "valor": 40},
        {"nome": "item_3", "peso": 4, "valor": 55}
    ]
    capacidade_mochila_exemplo = 5
    tamanho_pop = 10
    num_geracoes = 20 # Reduzido para teste rápido do callback
    taxa_mut = 0.1
    tam_torneio = 3

    print(f"Resolvendo o problema da mochila com callback...")
    melhor_solucao, melhor_valor, peso_da_melhor_solucao, historico_fitness = algoritmo_genetico_mochila(
        itens_exemplo, capacidade_mochila_exemplo, tamanho_pop, num_geracoes, taxa_mut, tam_torneio,
        callback_geracao=meu_callback_simples # Passando o callback
    )
    print("--- resultado final ---")
    if melhor_solucao:
        print(f"Melhor solucao: {melhor_solucao}, Valor: {melhor_valor}, Peso: {peso_da_melhor_solucao}")
    else:
        print("Nenhuma solucao viavel encontrada.")

print("Algoritmo genético atualizado para aceitar callback por geração.")

