from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class bienvenida(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.round_number == 1


class instrucciones_practica(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        return {
            "meritocracia" : self.session.config["meritocracia"]
        }

class instrucciones_torneo(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self): 
        return {
            "observabilidad" : self.session.config["observabilidad"]
        }
            
class tarea_practica(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        self.player.set_palabras_azar()
        return {
            "palabras" : self.player.palabras
        }

class tarea_torneo(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.round_number > 1
    def vars_for_template(self):
        self.player.set_palabras_azar()
        return {
            "palabras" : self.player.palabras,
            "pago_A": Constants.pago_A ,
            "pago_B": Constants.pago_B,
            "contrato_A": self.player.contrato_A
        }

class calculos(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_ranking()
        self.subsession.set_ranking_grupos()
        self.subsession.set_posiciones_jugadores()

class resultados_practica(Page):
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        return {
            "palabras" : self.player.palabras,
        }

class resultados_torneo(Page):
    def is_displayed(self):
        return self.round_number > 1
    def vars_for_template(self):
        return {
            "ronda": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
            "palabras" : self.player.palabras,
            "pago_ronda": self.player.pago_ronda,
            "posicion_grupo": self.player.posicion_grupo,
            "contrato_A": self.player.contrato_A,
            "posicion_contrato": self.player.posicion_contrato,
            "probabilidad_contrato_A": "{0:.2f}".format(self.player.probabilidad_contrato_A)
        }

class asignacion(Page):
    def is_displayed(self):
        return self.round_number < Constants.num_rounds
    def vars_for_template(self): 
        return {
            "ronda": self.round_number,
            "contrato_A_torneo" : self.player.contrato_A_torneo,
            #"palabras" : 
            #"contrato_A" : 
        }

class espera_grupos(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'creating_groups'
    def is_displayed(self):
        return self.round_number < Constants.num_rounds

class espera_pago_total(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_pago_jugadores()
    def is_displayed(self):
        return self.round_number == Constants.num_rounds 
		
class pago_total(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self): 
        return {
            "ronda_pagar" :  Constants.ronda_pagar - 1,
            "pago_total" : self.player.pago.to_real_world_currency(self.session)
        }
    
class gracias(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class ruleta(Page):
    timeout_seconds = 12000
    def is_displayed(self):
        return self.round_number == 1

page_sequence = [
	bienvenida, 
	instrucciones_practica,
    instrucciones_torneo,
	tarea_practica,
    tarea_torneo,
    calculos,
    resultados_practica,
    resultados_torneo,
    asignacion,
    espera_grupos,
    espera_pago_total,
	pago_total,
    gracias,
]
