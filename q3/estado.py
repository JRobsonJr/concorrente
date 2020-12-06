from asyncio import Lock, Semaphore

'''
Guarda referências às estruturas úteis para o controle de concorrência.
'''
class Estado:
  def __init__(self):
    self.alunos_bebendo = 0 # Número de alunos bebendo atualmente
    self.alunos_remediados = 0 # Número de alunos já remediados
    self.mutex = Lock() # Protege acesso às variáveis alunos_bebendo e alunos_remediados
    self.fila_saida = Semaphore(0) # Controla o aviso de que aluno pode ir embora sem ser antissocial
