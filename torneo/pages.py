from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class bienvenida(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class ruleta(Page):
    timeout_seconds = 12000
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
        
class tarea_practica(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        self.player.set_palabras_azar()
        return {
            "palabras" : self.player.palabras
        }

class resultados_practica(Page):
    def vars_for_template(self):
        return {
            "palabras" : self.player.palabras,
        }

class asignacion_practica(Page):
    pass

class instrucciones_torneo(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self): 
        return {
            "observabilidad" : self.session.config["observabilidad"]
        }
    
class tarea_torneo(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.round_number > 1
    def vars_for_template(self):
        self.player.set_palabras_azar()
        return {
            "palabras" : self.player.palabras,
            "pago_A": self.session.pago_A ,
            "pago_B": self.session.pago_B,
            "contrato_A": self.player.contrato_A
        }
class ResultsWaitPage(WaitPage):
    pass

class resultados_torneo(Page):
    def vars_for_template(self):
        return {
            "ronda": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
            "palabras" : self.player.palabras,
            "pago_ronda": self.player.pago_ronda,
            "posicion_grupo": self.player.posicion_grupo,
            "contrato_A": self.player.contrato_A,
            "posicion_contrato": self.player.posicion_contrato,
            "probabilidad_contrato_A": self.player.probabilidad_contrato_A
        }



class asignacion_torneo(Page):
    pass

class espera_grupos(WaitPage):
    wait_for_all_groups = True


class precalculos(WaitPage):
	pass

class calculos(WaitPage):
	pass
		
class GananciaTotal(Page):
	pass

class gracias(Page):
    def is_displayed(self):
        return self.round_number == self.session.config["Rounds"]

page_sequence = [
	bienvenida, 
	instrucciones_practica,
	tarea_practica,
    resultados_practica,
    #ruleta,
    instrucciones_torneo,
    tarea_torneo,
    resultados_torneo,
    #ruleta,

	# gracias
]
