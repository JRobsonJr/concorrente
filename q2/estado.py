from asyncio import Lock, Semaphore
from barreira import Barreira

'''
Guarda referências às estruturas úteis para o controle de concorrência.
'''
class Estado:
  def __init__(self):
    self.barreira = Barreira(4) # Garante que 4 estarão no barco
    self.mutex = Lock() # Protege acesso às variáveis ufcg e uepb
    self.ufcg = 0 # Número de alunos da UFCG aguardando
    self.uepb = 0 # Número de alunos da UEPB aguardando
    self.embarque_ufcg = Semaphore(0) # Controla o aviso de que aluno da UFCG pode entrar no barco
    self.embarque_uepb = Semaphore(0) # Controla o aviso de que aluno da UEPB pode entrar no barco
