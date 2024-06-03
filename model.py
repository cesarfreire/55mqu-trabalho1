import os
import numpy as np
import pyomo.environ as pyo


# Função auxiliar que le as instâncias
def ler_instancia(caminho_arquivo):
    # abre o arquivo como variavel arquivo
    with open(caminho_arquivo, 'r') as arquivo:
        # joga todas as linahs para a variavel
        linhas = arquivo.readlines()

    # Primeira linha contém
    # n = qtdade de vértices
    # a = qtdade de arestas
    # p = qtdade de vertices a serem selecionados
    # optimal = valor da solução ótima da instancia - nao utilizado
    primeira_linha = linhas[0].strip().split()
    n = int(primeira_linha[0])
    a = int(primeira_linha[1])
    p = int(primeira_linha[2])

    # Criar matriz de distâncias com valores grandes para vértices não conectados
    distancias = np.full((n, n), 10000)

    # Preenche a diagonal com 0
    np.fill_diagonal(distancias, 0)

    # Demais linhas contém as arestas e distâncias
    for linha in linhas[2:]:
        # separa as colunas
        colunas = linha.strip().split()

        # vertice 1
        i = int(colunas[0]) - 1
        # vertice 2
        j = int(colunas[1]) - 1
        # distancia entre vertice 1 e 2
        dist = float(colunas[2])
        # define valor no array de distancias
        distancias[i, j] = dist
        distancias[j, i] = dist  # Não sei se é o ideal, mas aqui eu fiz a definicao para ser um grafo não direcionado

    # retorna os valores
    return n, a, p, distancias


# Caminho para a pasta de instâncias
pasta_instancias = 'instances'
nome_instancia = 'pmed10n.txt'  # Mudar para o nome do arquivo de instância que deseja usar
caminho_arquivo = os.path.join(pasta_instancias, nome_instancia)

# Ler a instância
n, a, p, distancias = ler_instancia(caminho_arquivo)


def init_m():
    m = 0
    for i in range(n):
        for j in range(n):
            if i != j and m < distancias[i, j] < 10000:
                m = distancias[i, j]
    return m


# Defino valor alto para M, conforme citado no modelo
M = init_m()
print("Vertices:", n)
print("Arestas:", a)
print("p:", p)
print("Distâncias:\n", distancias)

# Cria o modelo
model = pyo.ConcreteModel()

# Variáveis de decisao
# x = 1 se o vertice i for selecionado, 0 caso contrário
model.x = pyo.Var([i for i in range(n)], domain=pyo.Binary)


# definição do d
def init_d(model):
    r = np.inf
    for i in range(n):
        for j in range(n):
            if i != j and distancias[i, j] < r:
                r = distancias[i, j]

    print("Valor inicial de d:", r)
    return r


# d = distancia mínima máxima
model.d = pyo.Var(domain=pyo.NonNegativeReals, initialize=init_d)

# funcao objetivo é maximizar o valor de d
model.obj = pyo.Objective(
    expr=model.d,
    sense=pyo.maximize,
)

# Cria a lista de restrições
model.cons = pyo.ConstraintList()

# Adiciona restricao 1
# A soma dos vertices selecionados deve ser igual a p
model.cons.add(sum(model.x[i] for i in range(n)) == p)

# para cada par de vertices i e j
for i in range(n):
    for j in range(n):
        # se i for menor que j
        if i < j and i != j:
            # adiciona a restrição conforme modelo
            #model.cons.add(model.d <= distancias[i, j] * (1 + M * (1 - model.x[i]) + M * (1 - model.x[j])))
            model.cons.add(model.d <= distancias[i, j] + M * (2 - model.x[i] - model.x[j]))
opt = pyo.SolverFactory("glpk")
results = opt.solve(model)

tc = results.solver.termination_condition

if tc == "optimal":
    print(results)

    locais_selecionados = [i for i in model.x if pyo.value(model.x[i]) > 0.5]
    distancia_minima_maxima = pyo.value(model.d)

    print("Locais selecionados:", locais_selecionados)
    print("Distância mínima máxima:", distancia_minima_maxima)
else:
    print("deu ruimmmmm")
