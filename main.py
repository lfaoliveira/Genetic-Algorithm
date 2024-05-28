import random


class Algoritmo:
  def __init__(self) -> None:
    pass



#dicionario com informações para o problema
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

#funcao de adaptacao que deve julgar a necessidade de cada item
def funcao_adapta():
  pass



#funcao de cross over 
def reproducao(pai, mae, tam_sol):
  #em quantas partes o gene deve ser dividido para o cross-over 
  div_gene = 2
  tam_div = tam_sol // div_gene
  
  #copia dados do pai pra ser mais pratico
  filho = pai.copy()
  #TODO:tornar bit_pai variavel de classe para que crossover fique mais igualitario entre os progenitores
  bit_pai = 1
  index = 0
  #loop alterna entre partes do pai e da mae que ira para cada
  while index < len(filho):
    parente = None
    if(bit_pai == 1):
      # filho recebe parte do pai
      #comeca em index e vai ate index + tam_div - 1 
      parente = parte_pai
      bit_pai = 0
    else:
      # filho recebe parte da mae
      bit_pai = 1
      parente = parte_mae
    for i in range(index, index + tam_div):
      if(i >= len(filho)):
        break
      filho[i] = parente[i]
    index += tam_div



  return filho


def gerar_pop_inicial(tam_pop, tam_sol):
  solucao = [0 for i in range(tam_sol)]
  pop_inicial = []
  indices_validos = [i for i in range(tam_sol)]
  for i in range(tam_pop):
    pop_inicial.append(solucao)
    
  #loop insere um item DIFERENTE aleatoriamente em cada solucao
  #ou seja, esolhe aleatoriamente um item pra botar em cada solucao
  for index in range(tam_pop):
    
    nova_sol = pop_inicial[index]
    index_mut = random.choice(indices_validos)
    indices_validos.remove(index_mut)
    nova_sol[index_mut] = 1
  return pop_inicial



def inicializar(dicio_produtos):
  #parametros
  limite_preco = 75
  tam_pop = 10
  tam_sol = len(dicio_produtos)
  tx_sobrevive = 50/100
  tx_mutacao = 3/100
  
  #cada individuo deve ser uma lista
  pop_inicial = gerar_pop_inicial(tam_pop, tam_sol)


