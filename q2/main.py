import asyncio
import random

from aluno_ufcg import ThreadAlunoUFCG
from aluno_uepb import ThreadAlunoUEPB
from estado import Estado

'''
Cria aleatoriamente um aluno da UFCG ou da UEPB.
'''
def cria_aluno(estado, id_aluno):
  return [
    (ThreadAlunoUFCG(estado, id_aluno), 'ufcg'),
    (ThreadAlunoUEPB(estado, id_aluno), 'uepb')
  ][random.randint(0, 1)]

'''
Gera alunos aleatoriamente de acordo com total solicitado, respeitando restrição
de números de alunos de cada universidade para que seja possível acontecer
todas as viagens.
'''
def gera_alunos(n):
  ufcg_total = 0
  uepb_total = 0
  estado = Estado()
  alunos = []
  
  for i in range(n - 1):
    aluno, universidade = cria_aluno(estado, i + 1)
    
    if universidade == 'ufcg':
      ufcg_total += 1
    else:
      uepb_total += 1
    alunos.append(aluno)
  
  if ufcg_total % 2 == 1: # Garantia de que número de cada universidade é par
    ufcg_total += 1
    alunos.append(ThreadAlunoUFCG(estado, n))
  else:
    uepb_total += 1
    alunos.append(ThreadAlunoUEPB(estado, n))

  print('\nForam gerados ' + str(n) + ' alunos: ' + str(ufcg_total) + ' da UFCG e ' + str(uepb_total) + ' da UEPB.\n')
  
  return alunos

'''
Código que cria e invoca threads.
'''
async def main():
  n = input('Quantos alunos estarão passeando de barco hoje? (Será arredondado a um número divisível por 4; default: n = 8) ')
  
  try:
    n = int(n)
    if n == 0:
      n = 4
    elif n % 4 != 0:
      n = int(n) + (4 - int(n) % 4)
  except ValueError:
    n = 8

  alunos = gera_alunos(n)
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
