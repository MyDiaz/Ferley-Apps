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

class resultados_practica(Page):
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        return {
            "palabras" : self.player.palabras,
        }

class calculos(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_ranking()

class resultados_torneo(Page):
    def is_displayed(self):
        return self.round_number > 1
    def vars_for_template(self):
        return {
            "ronda": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
            "palabras" : self.player.palabras,
            "pago_ronda": self.player.set_pago_ronda(),
            "posicion_grupo": self.player.set_posicion_grupo(),
            "contrato_A": self.player.contrato_A,
            "posicion_contrato": self.player.posicion_contrato,
            "probabilidad_contrato_A": self.player.set_probabilidad_contrato_A()
        }

class asignacion(Page):
    def vars_for_template(self): 
        return {
            "ronda": self.round_number,
            "contrato_A_torneo" : self.player.contrato_A_torneo,
            #"palabras" : 
            #"contrato_A" : 
        }

class espera_grupos(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number > 1
    
		
class pago_total(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self): 
        return {
            "ronda_pagar" :  Constants.ronda_pagar - 1,
            "pago_total" : 'set_pagar_jugador',
            #"palabras" : 
            #"contrato_A" : 
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
	tarea_practica,
    resultados_practica, 
    espera_grupos,
    instrucciones_torneo,
    tarea_torneo,
    calculos,
    resultados_torneo,
    asignacion,
	pago_total,
    gracias,
]
