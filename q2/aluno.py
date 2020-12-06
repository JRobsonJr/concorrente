from util import esperar

class ThreadAluno:
  '''
  - id_aluno = Diferencia alunos para compreensão da execução
  - estado = Objeto que guarda referências às estruturas úteis para o controle
    de concorrência
  - eh_remador = Indica se o aluno é o remador do barco
  - universidade = UEPB ou UFCG, dependendo do aluno
  '''
  def __init__(self, estado, id_aluno, universidade):
    self.estado = estado
    self.id_aluno = id_aluno
    self.eh_remador = False
    self.universidade = universidade

  def __str__(self):
    return 'Aluno ' + str(self.universidade).upper() + ' ' + str(self.id_aluno)

  '''
  Aguarda um pouco até solicitar viagem.
  '''
  async def boas_vindas(self):
    await esperar()

  def embarca(self):
    print(str(self) + ' (Embarcando): Vamos?')

  '''
  Operação de remar. Leva um tempinho de um lado ao outro do açude.
  '''
  async def rema(self):
    print(str(self) + ' (Remando): Simbora, pessoal!')
    await esperar()
    print(str(self) + ': Acabou nossa viagem...\nO barco retorna magicamente.\n\n')

  '''
  Rotina de aluno: chegar, solicitar embarque, embarcar e remar (se for o remador).
  '''
  async def rodar(self):
    await self.boas_vindas()
    
    await self.solicita_embarque() # Implementado nos filhos

    self.embarca()
    
    await self.estado.barreira.acquire_1()
    if self.eh_remador:
      await self.rema()
      self.estado.mutex.release()
    await self.estado.barreira.acquire_2()
