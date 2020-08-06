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
    
    tratamiento = models.IntegerField() 
    meritocracia = models.BooleanField()
    observabilidad = models.BooleanField()

class Subsession(BaseSubsession):

    torneo = models.BooleanField()
    ronda_pagar = models.IntegerField()

    def set_variables_subsesion(self, ronda, rondas_totales):
        #Subsession Ronda Practica (ronda<1), Torneo (ronda>1)
        self.torneo = ronda > 1
    
    def AssignGroups(grupo):
        for i in range(4):
            x = np.random.choice(4, 4, replace=False)
            grupo[:,i] = grupo[x,i]
        return grupo

    def creating_session(self, ronda):
        # Creando el grupo aleatoriamente (debe ser estratificado!!!)
        self.ronda_pagar = np.random.randint(2,6)
        if ronda > 1:
            players = self.get_players()

        else:
            self.group_randomly()
    
    def get_ronda_pagar(self):
        return self.ronda_pagar

class Group(BaseGroup):
    rank = {}
    rankA = {}
    rankB = {}
    ganador_contrato_A = 0

    def get_palabras_torneo(self):
        rankA, rankB = self.get_ranking_group()
        p2 = rankA[1] #palabras del jugador en la posicion 2 del ranking A
        p3 = rankB[0] #palabras del jugador en la posicion 1 del ranking B
        palabras_torneo = p2 + p3
        return palabras_torneo

    def set_asignar_contrato_A(self):
        rankA, rankB = self.get_ranking_group()
        p2 = self.get_player_by_id(rankA.keys()[1].split('j')[1])
        p3 = self.get_player_by_id(rankB.keys()[0].split('j')[1])
        self.ganador_contrato_A = random.choices([rankA.keys()[1].split('j')[1], rankB.keys()[0].split('j')[1]],weights=(p2.probabilidad_contrato_A, p3.probabilidad_contrato_A))

    def get_ganador_contrato_A(self):
        return self.ganador_contrato_A

    def sort(rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    def set_ranking(self):
        jugadores=self.get.players()
        rank = {}
        for j,k in jugadores:
            rank['j'+str(k)] = j.palabras
        self.rank = self.sort(rank)

    def set_ranking_contrato(self):
        rankA = {}
        rankB = {}
        for j,k in self.get_players():
            if j.Contrato_A:
                rankA['j'+str(k)] = j.palabras
            else:
                rankB['j'+str(k)] = j.palabras
        self.rankA = self.sort(rankA)
        self.rankB = self.sort(rankB)
    
    def get_ranking(self):
        return self.rank

    def get_ranking_contrato(self):
        return self.rankA, self.rankB


class Player(BasePlayer):
    contrato_A = models.BooleanField()
    palabras = models.IntegerField() 
    probabilidad_contrato_A = models.FloatField()
    contrato_A_torneo = models.BooleanField()
    posicion_grupo = models.IntegerField() #De 1-4
    posicion_contrato = models.IntegerField() #De 1-2
    pago = models.CurrencyField()
    pago_ronda = models.CurrencyField()


    def pagar_jugador(self):
        jugadores=self.get.players()
        ronda = self.subsession.get_ronda_pagar()
        for j in jugadores:
            j.pago = j.pago_ronda.in_all_rounds()[ronda-1]

    def set_probabilidad_contrato_A(self):
        if observabilidad == True:
            self.probabilidad_contrato_A=self.palabras / Group.get_palabras_torneo()
        else:
            self.probabilidad_contrato_A = 0.5

    def set_posicion_grupo(self):
        rank = self.group.get_ranking()
        self.posicion_grupo = list(rank).index('j'+str(self.id_in_group)) + 1

    def set_posicion_contrato(self):   
        rankA, rankB = self.group.get_ranking_contrato()
        if self.contrato_A:
            self.posicion_contrato= list(rankA).index('j'+str(self.id_in_group)) + 1
        else:
            self.posicion_contrato= list(rankB).index('j'+str(self.id_in_group)) + 1

    def set_contrato_A_torneo(self):
        ganador = self.group.get_ganador_contrato_A()
        if (self.contrato_A= True and self.posicion_contrato==1) or (self.contrato_A= False and self.posicion_contrato==2):
            self.contrato_A_torneo = self.contrato_A
        else: 
            if self.id_in_group == int(ganador):
                self.contrato_A_torneo = True
            else: 
                self.contrato_A_torneo = False  

    def set_palabras_azar(self):
         self.palabras = np.random.randint(1,10) ##Tarea de odificación palabras

    def get_palabras_azar(self):
        return self.palabras

    def set_pago_ronda(self):
        if(self.contrato_A):
            self.pago_ronda= Constants.pago_A*self.palabras
        else:
            self.pago_ronda= Constants.pago_B*self.palabras
        #cantidad de dinero que recibiría el jugador si la ronda actual es elegida para ser pagada
    
    #Payoff=pago_ronda

