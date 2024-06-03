import random
import copy
import time

class Algoritmo:
  def __init__(self) -> None:
    pass


# dicionario com informações para o problema
dicio_produtos = {
  1: {'Produto': 'Arroz (5kg)', 'Preço': 22, 'Necessidade': 10},
  2: {'Produto': 'Açúcar (2kg)', 'Preço': 3, 'Necessidade': 5},
  3: {'Produto': 'Óleo (1l)', 'Preço': 8, 'Necessidade': 6},
  4: {'Produto': 'Feijão (1kg)', 'Preço': 5, 'Necessidade': 10},
  5: {'Produto': 'Macarrão (500g)', 'Preço': 5, 'Necessidade': 8},
  6: {'Produto': 'Sardinha (1lata)', 'Preço': 5, 'Necessidade': 7},
  7: {'Produto': 'Carne (1kg)', 'Preço': 32, 'Necessidade': 9},
  8: {'Produto': 'Frango (1kg)', 'Preço': 13, 'Necessidade': 9},
  9: {'Produto': 'Queijo (200g)', 'Preço': 8, 'Necessidade': 5},
  10: {'Produto': 'Presunto (200g)', 'Preço': 4, 'Necessidade': 5},
  11: {'Produto': 'Pão (8un.)', 'Preço': 6, 'Necessidade': 6},
  12: {'Produto': 'Banana (1kg)', 'Preço': 4, 'Necessidade': 7},
  13: {'Produto': 'Laranja (1kg)', 'Preço': 2, 'Necessidade': 7},
  14: {'Produto': 'Abacate (1kg)', 'Preço': 7, 'Necessidade': 2},
  15: {'Produto': 'Sabão (1un.)', 'Preço': 2, 'Necessidade': 9},
  16: {'Produto': 'Limpador multiuso (1un.)', 'Preço': 4, 'Necessidade': 6},
  17: {'Produto': 'Água Tônica (500ml)', 'Preço': 7, 'Necessidade': 1},
  18: {'Produto': 'Polpa de Fruta (500ml)', 'Preço': 6, 'Necessidade': 4},
  19: {'Produto': 'Refrigerante (2l)', 'Preço': 8, 'Necessidade': 3},
  20: {'Produto': 'Cerveja (600ml)', 'Preço': 6, 'Necessidade': 2}
}

limite_custo = 75


class Solucao:
  def __init__(self, tam_sol):
    self.cromo = [0 for i in range(tam_sol)]
    self.fitness = 0
    self.somat_nec = 0
    self.somat_custo = 0

  def calc_fitness(self):
    fitness = 0
    for elem in self.cromo:
      if elem == 1:
        index = self.cromo.index(elem)
        preco_item = dicio_produtos[index + 1]['Preço']
        necessidade = dicio_produtos[index + 1]['Necessidade']
        
        self.somat_nec += necessidade
        self.somat_custo += preco_item

    fitness = self.somat_nec**2  - self.somat_custo
    if (self.somat_custo >= limite_custo):
      fitness = fitness / 10
    
    self.fitness = fitness
    return fitness


def mutacao(filho):
  index = random.randint(0, len(filho.cromo) - 1)
  if (filho.cromo[index] == 1):
    filho.cromo[index] = 0
  else:
    filho.cromo[index] = 1
  return


# funcao de cross over
def reproducao(pai, mae, tam_sol):
  # em quantas partes o gene deve ser dividido para o cross-over
  div_gene = 2
  tam_div = tam_sol // div_gene

  # copia dados do pai pra ser mais pratico
  filho = Solucao(tam_sol)
  # TODO:tornar bit_pai variavel de classe para que crossover fique mais igualitario entre os progenitores
  bit_pai = 1
  index = 0
  # loop alterna entre partes do pai e da mae que ira para filho
  while index < len(filho.cromo):
    parente = None
    if (bit_pai == 1):
      # filho recebe parte do pai
      parente = pai
      bit_pai = 0
    else:
      # filho recebe parte da mae
      bit_pai = 1
      parente = mae
    # comeca em index e vai ate index + tam_div - 1
    for i in range(index, index + tam_div):
      if (i >= len(filho.cromo)):
        break
      filho.cromo[i] = parente.cromo[i]
    index += tam_div
  filho.calc_fitness()
  return filho


def gerar_pop_inicial(tam_pop, tam_sol):
  pop_inicial = []
  indices_validos = [i for i in range(tam_sol)]
  for i in range(tam_pop):
    pop_inicial.append(Solucao(tam_sol))
  # loop insere 10 itens DIFERENTES em cada solucao
  quant_itens = 10
  for index in range(tam_pop):
    nova_sol = pop_inicial[index]
    for i in range(quant_itens):
      flag = True
      #while checa se um item ja foi inserido na solucao  
      while(flag):
        index_mut = random.choice(indices_validos)
        if(nova_sol.cromo[index_mut] == 1):
          flag = True
        else:
          nova_sol.cromo[index_mut] = 1
          flag = False
    nova_sol.calc_fitness()
    pop_inicial[index] = nova_sol  
  return pop_inicial


# Algoritmo de roleta que pega fitness da populacao toda e
def cria_roleta(pop):
  total = 0

  for indiv in pop:
    total += indiv.fitness
  inicio = 0
  fatias = []
  for indiv in pop:
    valor = int(indiv.fitness / total * 100)
    intervalo = [inicio, inicio + valor]
    fatias.append(intervalo)
    inicio =  inicio + valor + 1
  

  return fatias


def sorteia_indiv(pop, fatias):
  #garantido estar entre 0 e 100
  valor = int(random.random() * 100)

  for intervalo in fatias:
    if intervalo[0] <= valor <= intervalo[1]:
      index = fatias.index(intervalo)
      return pop[index]



def algoritmo(dicio_produtos):
  # parametros
  limite_preco = 75
  tam_pop = 10
  tam_sol = len(dicio_produtos)
  tx_mutacao = 3 / 100

  # cada individuo deve ser uma lista
  # pop eh lista de Solucao
  random.seed(2)
  pop = gerar_pop_inicial(tam_pop, tam_sol)

  # contador de iteracoes
  cont = 0
  time_stop = time.time() + 10
  while (time.time() < time_stop):
    nova_pop = list()
    fatias = cria_roleta(pop)
    for i in range(len(pop)):
      pai = sorteia_indiv(pop, fatias)
      mae = sorteia_indiv(pop, fatias)
      filho = reproducao(pai, mae, tam_sol)
      if (random.random() <= tx_mutacao):
        mutacao(filho)
      nova_pop.append(filho)

    # pop.sort(key = lambda elem: elem.fitness, reverse = True)

    '''for elem in nova_pop:
      print(elem.cromo)
'''
    pop = nova_pop
    print(cont)
    cont += 1
  for elem in pop:
    if(elem.somat_custo > limite_custo):
      pop.remove(elem)
  pop = sorted(pop, key=lambda elem: elem.somat_nec, reverse=True)

  return pop[0]


def mostrar_solucao(solucao):
  for i, elem in enumerate(solucao.cromo):
    #pegar dados do dicionario
    if(elem == 1):
      nome = dicio_produtos[i + 1]['Produto']
      necessidade = dicio_produtos[i + 1]['Necessidade']
      custo = dicio_produtos[i + 1]['Preço']

      print(f"|       {nome}, Custo:{custo}, Necessidade:{necessidade}      |")
    else:
      print(f"|       {None}, Custo:{None}, Necessidade:{None}            |")



# ------------------ MAIN ----------------------#

sol_final = algoritmo(dicio_produtos)

print("fitness: " + str(sol_final.somat_nec) + "custo: " + str(sol_final.somat_custo))

mostrar_solucao(sol_final)