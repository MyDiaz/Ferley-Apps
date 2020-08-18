from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import numpy as np
import random
import json

author = 'Ferley Rincón & Cesar Mantilla'

doc = """
Informalidad Laboral: Movilidad y Observabilidad Laboral
"""

class Constants(BaseConstants):
    name_in_url = 'Torneo'
    players_per_group = 4
    num_rounds = 6
    pago_A = c(2000)
    pago_B = c(1000)
    ronda_pagar = random.randint(2, num_rounds)

class Subsession(BaseSubsession):
    meritocracia = models.BooleanField()
    observabilidad = models.BooleanField()
    torneo = models.BooleanField()
    ronda_pagar = models.IntegerField()

    def creating_session(self):
        """Esta función define los valores iniciales para cada ronda
        incluye la subsession y demás clases.
        Este método se ejecuta al comiezo de la sesion tantas veces como
        rondas haya"""
        self.observabilidad = self.session.config["observabilidad"]
        self.meritocracia = self.session.config["meritocracia"]
        self.ronda_pagar = Constants.ronda_pagar
        # Subsession Ronda Practica (ronda<1), Torneo (ronda>1)
        self.torneo = self.round_number > 1

    def creating_groups(self):
        # Creando el grupo aleatoriamente (debe ser estratificado!!!)
        players = self.get_players() #devuelve un array de objeto jugador
        num_groups = len(self.get_groups())
        a1, a2, b1, b2 = [], [], [], []
        for i in players:
            if i.contrato_A_torneo:
                if i.posicion_contrato_torneo == 1:
                    a1.append(i.in_round(self.round_number+1))  
                else:
                    a2.append(i.in_round(self.round_number+1))
            else:
                if i.posicion_contrato_torneo == 1:
                    b1.append(i.in_round(self.round_number+1))  
                else:
                    b2.append(i.in_round(self.round_number+1))
            i.in_round(self.round_number+1).contrato_A = i.contrato_A_torneo

        matrix = np.c_[a1, a2, b1, b2]
        for i in range(Constants.players_per_group):
            x = np.random.choice(num_groups, num_groups, replace=False)
            matrix[:, i] = matrix[x, i]
        self.in_round(self.round_number+1).set_group_matrix(matrix)

    def sort(self, rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    """Este método retorna la posición del jugador en el ranking grupal"""
    def set_ranking(self):
        jugadores = self.get_players()
        rank = {}
        for k, j in enumerate(jugadores):
            rank['j' + str(k)] = j.palabras
        if (self.meritocracia and self.round_number==1) or (self.observabilidad and 
            self.round_number!=1):
            rank = self.sort(rank)
        else:
            l = list(rank.items())
            random.shuffle(l)
            rank = dict(l)
        for j, i in enumerate(rank.keys()):
            jugador = jugadores[int(i.split('j')[1])]
            # Primera mitad de los jugadores es contrato A
            if j < len(jugadores)//2:
                jugador.contrato_A_torneo = True
                # Primeta mitad de la mitad (primer cuarto) son posicion 1 contrato A
                if j < len(jugadores)//4:
                    jugador.posicion_contrato_torneo = 1
                # La otra mitad seria posicion 2 contrato A
                else:
                    jugador.posicion_contrato_torneo = 2
            # La otra mitad son contato B
            else:
                jugador.contrato_A_torneo = False
                # La primera mitad de la mitad de B (osea 3/4) son posicion 1
                if j < 3*len(jugadores)//4:
                    jugador.posicion_contrato_torneo = 1
                else:
                    jugador.posicion_contrato_torneo = 2
            if(self.round_number==1):
                jugador.contrato_A = jugador.contrato_A_torneo
    
    def set_ranking_grupos(self):
        for g in self.get_groups():
            g.set_ranking()
            g.set_ranking_contrato()
    
    def set_posiciones_jugadores(self):
        for j in self.get_players():
            j.set_pago_ronda()
            j.set_posicion_grupo()
            j.set_posicion_contrato()
            j.set_probabilidad_contrato_A()

    def set_pago_jugadores(self):
        for j in self.get_players():
            j.set_pago()

class Group(BaseGroup):
    #solo deben declararse variables por medio de models.
    rank = models.StringField()
    rankA = models.StringField()
    rankB = models.StringField()

    ganador_contrato_A = models.IntegerField(initial=0)

    def get_palabras_torneo(self):
        rankA = json.loads(self.rankA)
        rankB = json.loads(self.rankB) 
        p2 = list(rankA.values())[1]  # palabras del jugador en la posicion 2 del ranking A
        p3 = list(rankB.values())[0]  # palabras del jugador en la posicion 1 del ranking B
        palabras_torneo = p2 + p3
        return palabras_torneo

    def set_asignar_contrato_A(self):
        rankA = json.loads(self.rankA)
        rankB = json.loads(self.rankB)
        p2 = self.get_player_by_id(int(rankA.keys()[1].split('j')[1]))
        p3 = self.get_player_by_id(int(rankB.keys()[0].split('j')[1]))
        self.ganador_contrato_A = random.choices([rankA.keys()[1].split('j')[1], rankB.keys()[0].split('j')[1]],
                                                 weights=(p2.probabilidad_contrato_A, p3.probabilidad_contrato_A))

    def sort(self, rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    def set_ranking(self):
        jugadores = self.get_players() # [<P1>,<P2>,]
        rank = {}
        for k,j in enumerate(jugadores):
            rank['j' + str(k+1)] = j.palabras
        self.rank = json.dumps(self.sort(rank))
        # '{'j1':7, 'j2':5 }'

    def set_ranking_contrato(self):
        rankA = {}
        rankB = {}
        for k,j in enumerate(self.get_players()):
            if j.contrato_A:
                rankA['j' + str(k+1)] = j.palabras
            else:
                rankB['j' + str(k+1)] = j.palabras
        self.rankA = json.dumps(self.sort(rankA))
        self.rankB = json.dumps(self.sort(rankB))

class Player(BasePlayer):
    contrato_A = models.BooleanField()
    palabras = models.IntegerField() 
    probabilidad_contrato_A = models.FloatField()
    contrato_A_torneo = models.BooleanField()
    posicion_grupo = models.IntegerField() #De 1-4
    posicion_contrato = models.IntegerField() #De 1-2
    posicion_contrato_torneo = models.IntegerField() #De 1-2
    pago_ronda = models.CurrencyField()
    pago = models.CurrencyField()

    #Esta función define el pago final
    def set_pago(self):
        if (self.round_number==Constants.num_rounds):
#           jugadores = self.get_players()
            ronda = self.subsession.ronda_pagar
            pagos_rondas = []
            for j in self.in_all_rounds():
                pagos_rondas.append(j.pago_ronda)
            self.pago= pagos_rondas[ronda - 1]
        else:
            self.pago= 0
 #           j.pago = j.pago_ronda.in_all_rounds()[ronda - 1]
        
    def set_probabilidad_contrato_A(self):
        if self.subsession.observabilidad == True:
            if (self.contrato_A == True and self.posicion_contrato == 1):
                self.probabilidad_contrato_A = 1
            elif (self.contrato_A == False and self.posicion_contrato == 2):
                self.probabilidad_contrato_A = 0
            else:
                self.probabilidad_contrato_A = self.palabras / self.group.get_palabras_torneo()
        else:
            self.probabilidad_contrato_A = 0.5

    def set_posicion_grupo(self):
        rank = json.loads(self.group.rank)
        self.posicion_grupo = list(rank.keys()).index('j' + str(self.id_in_group)) + 1

    def set_posicion_contrato(self):
        rankA = json.loads(self.group.rankA)
        rankB = json.loads(self.group.rankB)
        if self.contrato_A:
            self.posicion_contrato = list(rankA).index('j' + str(self.id_in_group)) + 1
        else:
            self.posicion_contrato = list(rankB).index('j' + str(self.id_in_group)) + 1

    def set_contrato_A_torneo(self):
        ganador = self.group.set_ganador_contrato_A()
        if (self.contrato_A == True and self.posicion_contrato == 1) or (self.contrato_A == False and self.posicion_contrato == 2):
            self.contrato_A_torneo = self.contrato_A
            if self.posicion_contrato == 1:
                self.posicion_contrato_torneo = 1
            else:
                self.posicion_contrato_torneo = 2
        else:
            if self.id_in_group == int(ganador):
                self.contrato_A_torneo = True
                self.posicion_contrato_torneo = 2
            else:
                self.contrato_A_torneo = False
                self.posicion_contrato_torneo = 1

    def set_palabras_azar(self):
        self.palabras = np.random.randint(1, 10)  ##Tarea de odificación palabras

    def set_pago_ronda(self):
        if (self.contrato_A):
            self.pago_ronda = Constants.pago_A * self.palabras
        else:
            self.pago_ronda = Constants.pago_B * self.palabras
        # cantidad de dinero que recibiría el jugador si la ronda actual es elegida para ser pagada
 