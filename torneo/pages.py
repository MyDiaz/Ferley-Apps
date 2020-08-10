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
            #observabilidad: self.session.config["observabilidad"]
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

class instrucciones_torneo(Page):
    def vars_for_template(self): 
        return {
            "observabilidad" : self.session.config["observabilidad"]
        }
    

class ResultsWaitPage(WaitPage):
    pass

class Asignacion(Page):
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
    ruleta, 
	instrucciones_practica,
	tarea_practica,
    resultados_practica,
    instrucciones_torneo,

	# calculos,
	# Asignacion,
	# espera_grupos,

	# gracias
]
