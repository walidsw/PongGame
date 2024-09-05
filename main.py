from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty, ObjectProperty
from kivy.vector import Vector 
from kivy.clock import Clock 
from random import randint


class PongBall(Widget):
	
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class Paddel(Widget):
	ct = NumericProperty(0)
	
	def bounce_ball(self,ball):
		if self.collide_widget(ball):
			
			#top and bottom hit
			if (ball.x>=self.x and ball.right<=self.right):
				ball.velocity_y*=-1

			#side hit
			elif (ball.top<=self.top and ball.y>=self.y):
				ball.velocity_x*=-1

			#corner hit
			else:
				ball.velocity_y*=-1
				ball.velocity_x*=-1



class PongGame(Widget):
	ball_1 = ObjectProperty(None)
	ball_2= ObjectProperty(None)
	val = NumericProperty(0)
	player = ObjectProperty(None)
	speed = NumericProperty(5)
	m = NumericProperty(1)

	def serve_ball(self):
		self.ball_1.center_x = self.center_x - 100
		self.ball_1.center_y = self.center_y - 100

		self.ball_2.center_x = self.center_x + 100
		self.ball_2.center_y = self.center_y + 100

		self.ball_1.velocity = Vector(self.speed, 0).rotate(randint(0,360))
		self.ball_2.velocity = Vector(self.speed, 0).rotate(randint(0,360))

	def exchange_velocity(self):
		temp_x = self.ball_1.velocity_x
		temp_y = self.ball_1.velocity_y

		self.ball_1.velocity_x = self.ball_2.velocity_x
		self.ball_1.velocity_y = self.ball_2.velocity_y

		self.ball_2.velocity_x = temp_x
		self.ball_2.velocity_y = temp_y


	
	def update(self, dt):
		# print(f"Ball_1: {self.ball_1.pos}")

		self.player.bounce_ball(self.ball_1)
		self.player.bounce_ball(self.ball_2)

		self.ball_1.move()
		self.ball_2.move()

		

	

		#collision with ball
		if self.ball_1.collide_widget(self.ball_2):
			self.val += self.m
			sc = str(self.val)
			self.ids._score.text = sc
			self.exchange_velocity()
			

		#bounce off top
		if(self.ball_1.top>self.height):
			self.ball_1.velocity_y *= -1

		if(self.ball_2.top>self.height):
			self.ball_2.velocity_y *= -1

		#game Over for bounce down
		if (self.ball_1.y<0) or (self.ball_2.y<0):
			#Game over 
			self.ids._word.text="Game Over"
			self.m = 0
			


		#bounce off left and right
		if (self.ball_1.x<0) or (self.ball_1.right>self.width):
			self.ball_1.velocity_x *= -1

		if (self.ball_2.x<0) or (self.ball_2.right>self.width):
			self.ball_2.velocity_x *= -1

	

	
	def on_touch_move(self, touch):
		if touch.y<self.height/2:
			self.player.center_x = touch.x 
	





	
class PongApp(App):
	def build(self):
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0/70.0)
		return game
		
if __name__=='__main__':
	PongApp().run()










