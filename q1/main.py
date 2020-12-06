import asyncio
from carro import ThreadCarro
from passageiro import ThreadPassageiro
from estado import Estado

def leitura_entradas():
  capacidade = input('Quantas threads cabem no carro? (Default: C = 3) ')
  n = input('Quantos passageiros viajando hoje? (Default: n = 12) ')

  try:
    capacidade = int(capacidade)
  except ValueError:
    capacidade = 3 
  
  try:
    n = int(n)
  except ValueError:
    n = 12
  
  return capacidade, n

'''
Código que cria e invoca threads.
'''
async def main():
  capacidade, n = leitura_entradas()
  estado = Estado(capacidade, n)
  carro = ThreadCarro(capacidade, n, estado)
  passageiras = [ThreadPassageiro(i + 1, estado) for i in range(n)]
  await asyncio.gather(carro.rodar(), *(passageira.rodar() for passageira in passageiras))

asyncio.run(main())
