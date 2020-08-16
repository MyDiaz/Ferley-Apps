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
from random import randint
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
    ronda_pagar = randint(2, num_rounds+1)

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
        if self.round_number > 1:
            players = self.get_players() #devuelve un array de objeto jugador
            a1 = [], a2 = [], b1 = [], b2 = []
            for i in players:
                if i.contrato_A_torneo:
                    a1.append(i) if i.posicion_contrato_torneo == 1 else a2.append(i)
                else:
                    b1.append(i) if i.posicion_contrato_torneo == 1 else b2.append(i)

            matrix = np.c_[a1, a2, b1, b2]
            for i in range(4):
                x = np.random.choice(4, 4, replace=False)
                matrix[:, i] = matrix[x, i]

            self.set_group_matrix(matrix)
        else:
            self.group_randomly()

    """Este método retorna la posición del jugador en el ranking grupal"""
    def set_ranking(self):
        jugadores = self.get_players()
        rank = {}
        for j, k in jugadores:
            rank['j' + str(k)] = j.palabras
        if self.meritocracia:
            rank = self.group.sort(rank)
        else:
            l = list(rank.items())
            random.shuffle(l)
            rank = dict(l)
        for i, j in rank.keys():
            jugador = self.get_player_by_id(int(i.split('j')[1]))
            if j < 8:
                jugador.contrato_A_torneo = True
            else:
                jugador.contrato_A_torneo = False
            if j < 4:
                jugador.posicion_contrato_torneo = 1
            else:
                jugador.posicion_contrato_torneo = 2
            if j >= 8 & j < 12:
                jugador.posicion_contrato_torneo = 1
            else:
                jugador.posicion_contrato_torneo = 2


class Group(BaseGroup):
    #solo deben declararse variables por medio de models.
    rank = models.StringField()
    rankA = models.StringField()
    rankB = models.StringField()

    ganador_contrato_A = models.IntegerField(initial=0)

    def get_palabras_torneo(self):
        rankA, rankB = self.get_ranking_group()
        p2 = rankA[1]  # palabras del jugador en la posicion 2 del ranking A
        p3 = rankB[0]  # palabras del jugador en la posicion 1 del ranking B
        palabras_torneo = p2 + p3
        return palabras_torneo

    def set_asignar_contrato_A(self):
        rankA, rankB = self.get_ranking_group()
        p2 = self.get_player_by_id(int(rankA.keys()[1].split('j')[1]))
        p3 = self.get_player_by_id(int(rankB.keys()[0].split('j')[1]))
        self.ganador_contrato_A = random.choices([rankA.keys()[1].split('j')[1], rankB.keys()[0].split('j')[1]],
                                                 weights=(p2.probabilidad_contrato_A, p3.probabilidad_contrato_A))

    def sort(rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    def set_ranking(self):
        jugadores = self.get.players()
        rank = {}
        for j, k in jugadores:
            rank['j' + str(k)] = j.palabras
        self.rank = json.dump(self.sort(rank))

    def set_ranking_contrato(self):
        rankA = {}
        rankB = {}
        for j, k in self.get_players():
            if j.Contrato_A:
                rankA['j' + str(k)] = j.palabras
            else:
                rankB['j' + str(k)] = j.palabras
        self.rankA = json.dump(self.sort(rankA))
        self.rankB = json.dump(self.sort(rankB))


class Player(BasePlayer):
    contrato_A = models.BooleanField()
    palabras = models.IntegerField() 
    probabilidad_contrato_A = models.FloatField()
    contrato_A_torneo = models.BooleanField()
    posicion_grupo = models.IntegerField() #De 1-4
    posicion_contrato = models.IntegerField() #De 1-2
    posicion_contrato_torneo = models.IntegerField() #De 1-2
    pago = models.CurrencyField()
    pago_ronda = models.CurrencyField()

    def set_pagar_jugador(self):
        jugadores = self.get.players()
        ronda = self.subsession.get_ronda_pagar()
        for j in jugadores:
            j.pago = j.pago_ronda.in_all_rounds()[ronda - 1]

    def set_probabilidad_contrato_A(self):
        if self.subsession.observabilidad == True:
            self.probabilidad_contrato_A = self.palabras / Group.get_palabras_torneo()
        else:
            self.probabilidad_contrato_A = 0.5

    def set_posicion_grupo(self):
        rank = self.group.get_ranking()
        self.posicion_grupo = list(rank).index('j' + str(self.id_in_group)) + 1

    def set_posicion_contrato(self):
        rankA, rankB = self.group.get_ranking_contrato()
        if self.contrato_A:
            self.posicion_contrato = list(rankA).index('j' + str(self.id_in_group)) + 1
        else:
            self.posicion_contrato = list(rankB).index('j' + str(self.id_in_group)) + 1

    def set_contrato_A_torneo(self):
        ganador = self.group.get_ganador_contrato_A()
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

    # Payoff=pago_ronda

