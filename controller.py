import os
import pygame
import time
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 1234))

class Car:
	def __init__(self, x, y, angle = 0.0, length=4, max_steering=30, max_acceleration = 90.0,max_brake_deceleration=90.0):
		self.position = Vector2(x,y)
		self.velocity = Vector2(0.0, 0.0)
		self.angle = angle
		self.length = length
		self.max_acceleration = max_acceleration
		self.max_brake_deceleration = max_brake_deceleration
		self.max_steering = max_steering
		self.max_velocity = 20
		self.brakes=0
		self.brake_deceleration = 0
		self.free_deceleration = 2
		self.acceleration = 0.0
		self.steering = 0.0
	def update(self, dt):
		self.velocity += (self.acceleration * dt, 0)
		self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))
		if self.steering:
			turning_radius = self.length/sin(radians(self.steering))
			angular_velocity = self.velocity.x/turning_radius
		else:
			angular_velocity = 0

		self.position += self.velocity.rotate(-self.angle)*dt
		self.angle += degrees(angular_velocity)*dt

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Golf")
		width=480
		height = 270
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.ticks = 60
		self.exit = False
	def run(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		image_path = os.path.join(current_dir, "car.png")
		car_image = pygame.image.load(image_path)
		car = Car(0,0)
		ppu = 32
		cruisecontrol = True
		while not self.exit:
			dt = self.clock.get_time()/1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit = True

			pressed = pygame.key.get_pressed()
			

			if cruisecontrol == True:
				if pressed[pygame.K_c]:#stop
					client_socket.send(("toggled on").encode())
					
					#client_socket.send(("S").encode()) 
					cruisecontrol = False
					time.sleep(0.5)

				if pressed[pygame.K_w]:
					car.brake_deceleration =0;
					car.brakes=0
					car.acceleration +=5*dt
					client_socket.send(("F:" + str(int(car.acceleration))).encode())
					
				if pressed[pygame.K_s]:
					car.acceleration = 0
					car.brakes=0
					car.brake_deceleration += 5 *dt
					client_socket.send(("R:" + str(int(car.brake_deceleration))).encode())
					
				car.brake_deceleration=max(-car.max_brake_deceleration, min(car.brake_deceleration, car.max_brake_deceleration))
				car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

				if pressed[pygame.K_d]:
					car.steering -= 30 *dt
					client_socket.send(("st: " + str(int(car.steering))).encode())

				elif pressed[pygame.K_a]:
					car.steering +=30 * dt
					client_socket.send(("st: " + str(int(car.steering))).encode())
				else:
					car.steering = 0

				car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

				if pressed[pygame.K_SPACE]: #brakes
					car.acceleration=0
					car.brake_deceleration=0
					car.brakes +=5*dt
					client_socket.send(("b:" + str(int(car.brakes))).encode()) 

				if pressed[pygame.K_LEFT]:#left turn signal
					client_socket.send(("LL").encode()) 
					time.sleep(0.5)
					
				if pressed[pygame.K_RIGHT]:#right turn signal
					client_socket.send(("RL").encode()) 
					time.sleep(0.5)

				if pressed[pygame.K_UP]:#four way flashers
					client_socket.send(("FL").encode()) 
					time.sleep(0.5)

				if pressed[pygame.K_DOWN]:#stop all turn signals/flashers
					client_socket.send(("SL").encode())
					time.sleep(0.5)

				if pressed[pygame.K_h]:#toggle the headlight
					client_socket.send(("HL").encode()) 
					time.sleep(0.5)
					
			elif cruisecontrol == False:
				if pressed[pygame.K_c]:#stop
					client_socket.send(("toggled off").encode())
					client_socket.send(("S").encode())
					
					cruisecontrol = True
					time.sleep(0.5)


			car.update(dt)
			self.screen.fill((0,0,0))
			rotated = pygame.transform.rotate(car_image, car.angle)
			rect = rotated.get_rect()
			self.screen.blit(rotated, car.position *ppu - (rect.width/2, rect.height/2))
			pygame.display.flip()
			self.clock.tick(self.ticks)
		pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

