# Definir a classe Nó para representar um estado do jogo 8 puzzle
class No:
    def __init__(self, estado, pai=None, acao=None, custo=0):
        self.estado = estado # uma lista de 9 números representando as peças do jogo
        self.pai = pai # o nó que gerou este nó
        self.acao = acao # a ação que levou a este estado (mover uma peça em branco para cima, baixo, esquerda ou direita)
        self.custo = custo # o custo do caminho desde o estado inicial até este nó (o número de ações)
        self.heuristica = self.calcular_heuristica() # a heurística do estado, que é o número de peças fora do lugar
        self.funcao = self.custo + self.heuristica # o valor da função f(n) = g(n) + h(n)

    # Definir um método para calcular a heurística do estado
    def calcular_heuristica(self):
        objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0] # o estado objetivo do jogo
        heuristica = 0
        for i in range(9):
            if self.estado[i] != objetivo[i]: # se a peça está fora do lugar
                heuristica += 1
        return heuristica

    # Definir um método para verificar se o estado é o objetivo
    def eh_objetivo(self):
        return self.heuristica == 0

    # Definir um método para gerar os sucessores do nó (os estados possíveis após uma ação válida)
    def gerar_sucessores(self):
        sucessores = []
        indice_branco = self.estado.index(0) # encontrar o índice da peça em branco
        # definir as possíveis ações e os índices correspondentes para mover a peça em branco
        acoes = {"cima": -3, "baixo": 3, "esquerda": -1, "direita": 1}
        for acao, indice in acoes.items():
            # verificar se a ação é válida (não sai dos limites da lista)
            if 0 <= indice_branco + indice < 9:
                # criar um novo estado trocando a peça em branco com a peça adjacente
                novo_estado = self.estado[:]
                novo_estado[indice_branco], novo_estado[indice_branco + indice] = novo_estado[indice_branco + indice], novo_estado[indice_branco]
                # criar um novo nó com o novo estado, o nó atual como pai, a ação realizada e o custo incrementado
                novo_no = No(novo_estado, self, acao, self.custo + 1)
                # adicionar o novo nó à lista de sucessores
                sucessores.append(novo_no)
        return sucessores

# Definir uma função para resolver o problema do jogo 8 puzzle com a função de busca A*
def resolver(estado_inicial):
    # criar um nó inicial com o estado inicial
    no_inicial = No(estado_inicial)
    # criar uma lista aberta para armazenar os nós que estão sendo explorados
    aberta = [no_inicial]
    # criar um conjunto fechado para armazenar os nós que já foram explorados
    fechada = set()
    # enquanto houver nós na lista aberta
    while aberta:
        # ordenar a lista aberta pelo valor da função f(n) = g(n) + h(n), que é o custo mais a heurística
        aberta.sort(key=lambda no: no.funcao)
        # remover o nó com o menor valor de f(n) da lista aberta
        no_atual = aberta.pop(0)
        # adicionar o estado do nó atual ao conjunto fechado
        fechada.add(tuple(no_atual.estado))
        # se o nó atual é o objetivo, retornar o caminho desde o nó inicial até o nó atual
        if no_atual.eh_objetivo():
            return caminho(no_atual)
        # gerar os sucessores do nó atual
        sucessores = no_atual.gerar_sucessores()
        # para cada sucessor
        for sucessor in sucessores:
            # se o estado do sucessor não está no conjunto fechado
            if tuple(sucessor.estado) not in fechada:
                # adicionar o sucessor à lista aberta
                aberta.append(sucessor)

# Definir uma função para retornar o caminho desde o nó inicial até o nó objetivo
def caminho(no_objetivo):
    # criar uma lista vazia para armazenar o caminho
    caminho = []
    # começar pelo nó objetivo e ir seguindo os pais até chegar ao nó inicial
    no_atual = no_objetivo
    while no_atual:
        # adicionar o estado, a ação e o valor da função do nó atual à lista do caminho
        caminho.append((no_atual.estado, no_atual.acao, no_atual.funcao))
        # ir para o pai do nó atual
        no_atual = no_atual.pai
    # inverter a ordem da lista do caminho, pois ela está do objetivo para o inicial
    caminho.reverse()
    # retornar a lista do caminho
    return caminho

# Definir uma função para exibir o estado do jogo em uma matriz 3x3
def exibir(estado):
    # criar uma matriz vazia
    matriz = []
    # percorrer a lista do estado em intervalos de 3 elementos
    for i in range(0, 9, 3):
        # adicionar uma linha com os 3 elementos à matriz
        matriz.append(estado[i:i+3])
    # imprimir a matriz formatada
    for linha in matriz:
        print("|", " ".join(map(str, linha)), "|")

# Testar a função resolver com um estado inicial aleatório
estado_inicial = [7, 2, 4, 5, 6, 0, 8, 3, 1]
print("Estado inicial:")
exibir(estado_inicial)
print('-----------')
solucao = resolver(estado_inicial)
for estado, acao, funcao in solucao:
    exibir(estado)
    print("Ação:", acao)
    print("Função:", funcao)

print("Solução encontrada em", len(solucao) - 1, "passos")

