import asyncio

from estado import Estado
from aluno import ThreadAluno

'''
Código que cria e invoca threads.
'''
async def main():
  n = input('Quantos alunos virão ao bar hoje? (Default: n = 8) ')
  
  try:
    n = int(n)
  except:
    n = 8
  
  estado = Estado()
  alunos = [ThreadAluno(i + 1, estado) for i in range(n)]
  
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
