import asyncio

from estado import Estado
from aluno import ThreadAluno

async def main():
  n = int(input())
  estado = Estado()
  alunos = [ThreadAluno(i + 1, estado) for i in range(n)]
  
  await asyncio.gather(*(aluno.rodar() for aluno in alunos))

asyncio.run(main())
