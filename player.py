from py4godot import signal
from py4godot.classes import gdclass
from py4godot.classes.Area2D import Area2D
from py4godot.classes.Input import Input
from py4godot.classes.core import Vector2


@gdclass
class player(Area2D):
	hit = signal([]) #essa variável funciona como um trigger
	speed = 400
	screen_size = None
	
	def _ready(self) -> None:  #Função que roda somente no início da execução do programa
		self.screen_size = self.get_viewport_rect().size #define o tamanho da tela de acordo com a configuração do projeto
		#self.hide()
		self._input_singleton = Input.instance() #permite a leitura dos inputs definidos pelo projeto
		
	def _process(self, delta: float) -> None: #Função que vai rodar constantemente durante a execução do programa
		zero = Vector2.new3(0,0)
		velocity = zero
		_input = self._input_singleton
		if _input.is_action_pressed("move_right"):
			velocity.x += 1
		if _input.is_action_pressed("move_left"):
			velocity.x -= 1
		if _input.is_action_pressed("move_down"):
			velocity.y += 1
		if _input.is_action_pressed("move_up"):
			velocity.y -= 1
		if velocity.length() > 0: #normaliza a velocidade diagonal do personagem
			velocity = velocity.normalized() * self.speed
			sprite = self.get_node("AnimatedSprite2D")
			sprite.play()
			pass
		else:
			self.get_node("AnimatedSprite2D").stop()
			pass
		
		self.position += velocity * delta
		self.position = self.position.clamp(zero, self.screen_size) #impede o personagem de atravessar o limite da tela
		
		animated_sprite = self.get_node("AnimatedSprite2D") #facilita o acesso do AnimatedSprite2D
		
		#troca de animações do personagem:
		if velocity.x != 0:
			animated_sprite.animation = "walk"
			animated_sprite.flip_h = velocity.x < 0
		elif velocity.y != 0:
			animated_sprite.animation = "up"
			animated_sprite.flip_h = velocity.y > 0
			
