# -*- coding: utf-8 -*-
# mochila_genetico.py

# --- modelagem do problema da mochila ---

# cada item é representado por um dicionário contendo seu nome (opcional, para identificação),
# peso e valor.
# exemplo de um item:
# item_exemplo = {"nome": "item_1", "peso": 2, "valor": 3}

# a lista de itens disponíveis será uma lista desses dicionários.
# exemplo de lista de itens:
# itens_disponiveis = [
#     {"nome": "item_1", "peso": 2, "valor": 3},
#     {"nome": "item_2", "peso": 3, "valor": 4},
#     {"nome": "item_3", "peso": 4, "valor": 5},
#     {"nome": "item_4", "peso": 5, "valor": 6}
# ]

# a capacidade da mochila é um valor numérico que representa o peso máximo
# que a mochila pode carregar.
# exemplo de capacidade da mochila:
# capacidade_maxima_mochila = 5

# --- representação da solução (indivíduo no algoritmo genético) ---

# uma solução (ou indivíduo) será representada por um vetor binário (lista de 0s e 1s).
# o tamanho do vetor será igual ao número de itens disponíveis.
# cada posição no vetor corresponde a um item na lista de itens_disponiveis.
# se o valor na posição 'i' do vetor for 1, significa que o item 'i' está na mochila.
# se o valor na posição 'i' do vetor for 0, significa que o item 'i' não está na mochila.
# exemplo de uma solução para 4 itens:
# solucao_exemplo = [1, 0, 1, 0]  # significa que o item 0 e o item 2 estão na mochila

print("modelagem básica do problema da mochila definida em mochila_genetico.py")




# --- implementação do algoritmo genético ---
import random

# função para calcular o peso e o valor total de uma solução (indivíduo)
def calcular_peso_e_valor(solucao, itens):
    # solucao: um vetor binário representando quais itens estão na mochila
    # itens: a lista de dicionários de itens (com 'peso' e 'valor')
    peso_total = 0
    valor_total = 0
    for i, item_incluido in enumerate(solucao):
        if item_incluido == 1:
            peso_total += itens[i]['peso']
            valor_total += itens[i]['valor']
    return peso_total, valor_total

# função de fitness (aptidão)
# avalia uma solução. o objetivo é maximizar o valor total, sem exceder a capacidade da mochila.
def funcao_fitness(solucao, itens, capacidade_mochila):
    # solucao: um vetor binário
    # itens: a lista de itens
    # capacidade_mochila: a capacidade máxima da mochila

    peso_da_solucao, valor_da_solucao = calcular_peso_e_valor(solucao, itens)

    # penalizar soluções que excedem a capacidade da mochila
    # uma forma simples de penalizar é retornar um fitness muito baixo (ou zero)
    if peso_da_solucao > capacidade_mochila:
        return 0  # penalidade: fitness zero se o peso excede a capacidade
    else:
        return valor_da_solucao # caso contrário, o fitness é o próprio valor da solução

# função para criar um indivíduo aleatório (uma solução inicial)
def criar_individuo(numero_de_itens):
    # numero_de_itens: o total de itens disponíveis
    # retorna um vetor binário aleatório
    return [random.randint(0, 1) for _ in range(numero_de_itens)]

# função para criar a população inicial
def criar_populacao_inicial(tamanho_populacao, numero_de_itens):
    # tamanho_populacao: o número de indivíduos na população
    # numero_de_itens: o total de itens disponíveis
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(criar_individuo(numero_de_itens))
    return populacao

print("funções iniciais do algoritmo genético (fitness, criação de indivíduo/população) adicionadas a mochila_genetico.py")



# função de seleção (torneio)
# seleciona um indivíduo da população para reprodução usando o método do torneio.
def selecao_torneio(populacao, itens, capacidade_mochila, tamanho_torneio=3):
    # populacao: a lista de indivíduos
    # itens: a lista de itens
    # capacidade_mochila: a capacidade máxima da mochila
    # tamanho_torneio: o número de indivíduos que participam de cada torneio

    # seleciona 'tamanho_torneio' indivíduos aleatoriamente da população
    participantes_torneio = random.sample(populacao, tamanho_torneio)

    # calcula o fitness de cada participante
    fitness_participantes = [(individuo, funcao_fitness(individuo, itens, capacidade_mochila)) for individuo in participantes_torneio]

    # ordena os participantes pelo fitness (do maior para o menor)
    fitness_participantes.sort(key=lambda x: x[1], reverse=True)

    # retorna o melhor indivíduo do torneio
    return fitness_participantes[0][0]

# função de crossover (um ponto)
# cria dois novos indivíduos (filhos) a partir de dois pais.
def crossover_um_ponto(pai1, pai2):
    # pai1, pai2: dois indivíduos (vetores binários)
    # retorna dois novos indivíduos (filhos)
    numero_de_itens = len(pai1)
    if numero_de_itens < 2:
        return pai1, pai2 # não faz crossover se houver menos de 2 itens

    ponto_de_corte = random.randint(1, numero_de_itens - 1)

    filho1 = pai1[:ponto_de_corte] + pai2[ponto_de_corte:]
    filho2 = pai2[:ponto_de_corte] + pai1[ponto_de_corte:]

    return filho1, filho2

# função de mutação (bit flip)
# altera aleatoriamente um ou mais bits (genes) de um indivíduo.
def mutacao_bit_flip(individuo, taxa_de_mutacao=0.01):
    # individuo: o indivíduo a ser mutado (vetor binário)
    # taxa_de_mutacao: a probabilidade de cada bit ser mutado
    individuo_mutado = []
    for gene in individuo:
        if random.random() < taxa_de_mutacao:
            individuo_mutado.append(1 - gene) # inverte o bit (0 vira 1, 1 vira 0)
        else:
            individuo_mutado.append(gene)
    return individuo_mutado

print("funções de seleção, crossover e mutação adicionadas a mochila_genetico.py")



# loop principal do algoritmo genético
def algoritmo_genetico_mochila(itens, capacidade_mochila, tamanho_populacao, numero_geracoes, taxa_mutacao, tamanho_torneio=3):
    # itens: lista de itens (dicionários com 'peso' e 'valor')
    # capacidade_mochila: capacidade máxima da mochila
    # tamanho_populacao: número de indivíduos na população
    # numero_geracoes: número de iterações (gerações) que o algoritmo executará
    # taxa_mutacao: probabilidade de mutação de um gene
    # tamanho_torneio: número de indivíduos no torneio de seleção

    numero_de_itens = len(itens)

    # 1. criar a população inicial
    populacao_atual = criar_populacao_inicial(tamanho_populacao, numero_de_itens)

    # variáveis para rastrear o melhor indivíduo encontrado até agora
    melhor_individuo_global = None
    melhor_fitness_global = -1 # inicializa com um valor baixo

    # histórico de melhores fitness por geração (para visualização, se necessário)
    historico_melhor_fitness_geracao = []

    # 2. loop através das gerações
    for geracao in range(numero_geracoes):
        # calcular o fitness de cada indivíduo na população atual
        populacao_com_fitness = []
        for individuo in populacao_atual:
            fitness = funcao_fitness(individuo, itens, capacidade_mochila)
            populacao_com_fitness.append((individuo, fitness))

            # atualizar o melhor indivíduo global se um melhor for encontrado
            if fitness > melhor_fitness_global:
                melhor_fitness_global = fitness
                melhor_individuo_global = individuo

        # registrar o melhor fitness desta geração
        # (pode ser o fitness do melhor indivíduo da população atual ou o global, dependendo da estratégia)
        # aqui, vamos pegar o melhor da população atual para ver a evolução da geração
        populacao_com_fitness.sort(key=lambda x: x[1], reverse=True)
        historico_melhor_fitness_geracao.append(populacao_com_fitness[0][1])

        # criar a próxima geração
        proxima_populacao = []

        # elitismo: opcionalmente, manter o(s) melhor(es) indivíduo(s) da geração atual
        # por simplicidade, vamos recriar toda a população, mas o elitismo é uma boa prática
        # if melhor_individuo_global and (melhor_individuo_global not in [ind[0] for ind in proxima_populacao]):
        # proxima_populacao.append(melhor_individuo_global)

        # preencher a nova população usando seleção, crossover e mutação
        while len(proxima_populacao) < tamanho_populacao:
            # 3. seleção de pais
            pai1 = selecao_torneio(populacao_atual, itens, capacidade_mochila, tamanho_torneio)
            pai2 = selecao_torneio(populacao_atual, itens, capacidade_mochila, tamanho_torneio)

            # 4. crossover
            filho1, filho2 = crossover_um_ponto(pai1, pai2)

            # 5. mutação
            filho1_mutado = mutacao_bit_flip(filho1, taxa_mutacao)
            filho2_mutado = mutacao_bit_flip(filho2, taxa_mutacao)

            proxima_populacao.append(filho1_mutado)
            if len(proxima_populacao) < tamanho_populacao:
                proxima_populacao.append(filho2_mutado)

        populacao_atual = proxima_populacao

        # opcional: imprimir progresso
        # print(f"geração {geracao + 1}/{numero_geracoes} - melhor fitness: {populacao_com_fitness[0][1]} - melhor global: {melhor_fitness_global}")

    # ao final das gerações, o melhor_individuo_global contém a melhor solução encontrada
    # e melhor_fitness_global o seu valor (fitness)
    peso_final, valor_final = calcular_peso_e_valor(melhor_individuo_global, itens)

    return melhor_individuo_global, valor_final, peso_final, historico_melhor_fitness_geracao

# --- exemplo de uso (para teste) ---
if __name__ == "__main__":
    # definição dos itens (peso, valor)
    itens_exemplo = [
        {"nome": "item_1", "peso": 2, "valor": 30},
        {"nome": "item_2", "peso": 3, "valor": 40},
        {"nome": "item_3", "peso": 4, "valor": 55},
        {"nome": "item_4", "peso": 5, "valor": 60},
        {"nome": "item_5", "peso": 1, "valor": 20},
        {"nome": "item_6", "peso": 6, "valor": 70},
        {"nome": "item_7", "peso": 3, "valor": 45}
    ]
    capacidade_mochila_exemplo = 10

    # parâmetros do algoritmo genético
    tamanho_pop = 50
    num_geracoes = 100
    taxa_mut = 0.02 # 2% de chance de mutação por gene
    tam_torneio = 5

    print(f"resolvendo o problema da mochila com {len(itens_exemplo)} itens e capacidade {capacidade_mochila_exemplo}")
    print(f"parâmetros do ag: população={tamanho_pop}, gerações={num_geracoes}, taxa de mutação={taxa_mut}\n")

    melhor_solucao, melhor_valor, peso_da_melhor_solucao, historico_fitness = algoritmo_genetico_mochila(
        itens_exemplo,
        capacidade_mochila_exemplo,
        tamanho_pop,
        num_geracoes,
        taxa_mut,
        tam_torneio
    )

    print("--- resultado ---")
    print(f"melhor solução (itens selecionados - 1 significa selecionado):")
    itens_selecionados_nomes = []
    for i, selecionado in enumerate(melhor_solucao):
        print(f"  {itens_exemplo[i]['nome']}: {'sim' if selecionado else 'não'}")
        if selecionado:
            itens_selecionados_nomes.append(itens_exemplo[i]['nome'])
    
    print(f"\nitens na mochila: {', '.join(itens_selecionados_nomes)}")
    print(f"valor total da melhor solução: {melhor_valor}")
    print(f"peso total da melhor solução: {peso_da_melhor_solucao} (capacidade máxima: {capacidade_mochila_exemplo})")

    # # opcional: imprimir histórico de fitness (para análise)
    # print("\nhistórico do melhor fitness por geração:")
    # for i, fit in enumerate(historico_fitness):
    #     print(f"geração {i+1}: {fit}")

print("loop principal do algoritmo genético e exemplo de uso adicionados a mochila_genetico.py")

