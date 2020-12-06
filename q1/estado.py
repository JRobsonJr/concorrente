from asyncio import Lock, Semaphore

'''
Guarda referências às estruturas úteis para o controle de concorrência.
'''
class Estado:
  def __init__(self, capacidade, n):
    self.capacidade = capacidade # Capacidade da thread carro
    self.n = n # Número de threads passageiras
    self.mutex_entrada = Lock() # Controle de concorrência da variável threads_dentro
    self.mutex_saida = Lock() # Controle de concorrência da variável threads_fora
    self.threads_dentro = 0 # Número de threads dentro do carro
    self.threads_fora = 0 # Número de threads fora do carro
    self.embarque_liberado = Semaphore(0) # Controla o aviso de que pode entrar no carro
    self.desembarque_liberado = Semaphore(0) # Controla o aviso de que pode sair do carro
    self.todas_dentro = Semaphore(0) # Avisa ao carro que todas as threads estão dentro para que ele possa dar a partida
    self.todas_fora = Semaphore(0) # Avisa ao carro que todas as threads estão dentro para que ele possa reiniciar sua rotina
