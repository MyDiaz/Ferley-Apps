from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class presentacion(Page):
    timeout_seconds = 30
    def is_displayed(self):
        return self.round_number == 1

class instrucciones_practica(Page):
    timeout_seconds = 60
    def is_displayed(self):
        return self.round_number == 2
    
    def vars_for_template(self):
        return {
            meritocracia: self.session.config["meritocracia"] 
            #observabilidad: self.session.config["observabilidad"]
        }

class tarea_practica(Page):
    timeout_seconds = 60
    self.player.set_palabras_azar()
    def vars_for_template(self): 
        return {
            palabras: self.player.get_palabras_azar()
        }

class instrucciones_practica(Page):
    self.player.set_palabras_azar()
    def vars_for_template(self): 
        return {
            observabilidad: self.session.config["observabilidad"]
        }
    

class ResultsWaitPage(WaitPage):
    pass


class resultados_practica(Page):
    def vars_for_template(self): 
        return { 
            palabras: self.player.get_palabras_azar(),
        }

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
	presentacion, 
	Tarea, 
	precalculos, 
	Results,
	calculos,
	Asignacion,
	espera_grupos,
	Ganancia, 
	gracias
]
