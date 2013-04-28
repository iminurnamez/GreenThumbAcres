import os
import random
import pygame
from pygame import Color


class Plant(object):
	def pick_image(self):
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.surface = pygame.Surface((self.Rect.width, self.Rect.height))
		self.surface.set_colorkey((157, 187, 97))
		
	def update(self, surface, garden):
		self.water -= garden.daily_evap
		self.solar_energy += garden.daily_sun
		self.water += garden.daily_water
		water_q = float(self.water)/self.max_water
		solar_q = float(self.solar_energy)/self.max_solar
		if water_q > 0.3 and solar_q > 0.3:
			current_growth = self.growth_rate * ((water_q + solar_q)/2)
			self.solar_energy -= current_growth * 2 / 3
		else:
			current_growth = 0.5
			self.solar_energy -= 1
		if self.manured:
			current_growth += current_growth * .2
		self.growth += current_growth
		
		if self.growth > self.stage6_step:
			self.stage = 6
		elif self.growth > self.stage5_step:
			self.stage = 5
		elif self.growth > self.stage4_step:
			self.stage = 4
		elif self.growth > self.stage3_step:
			self.stage = 3
		elif self.growth > self.stage2_step:
			self.stage = 2
		else:
			self.stage = 1
		if self.solar_energy > self.max_solar:
			self.solar_energy = self.max_solar
		if self.solar_energy < 1:
			self.solar_energy = 1
		if self.water > self.max_water:
			self.water = self.max_water
		if self.water < 1:
			self.water = 1
		self.pick_image()
		self.surface.blit(self.image, (0, 0))
		surface.blit(self.surface, self.Rect)
		water_stat_length = (float(self.water)/self.max_water) * self.Rect.width
		solar_stat_length = (float(self.solar_energy)/self.max_solar) * self.Rect.width
		pygame.draw.line(surface, Color("blue"), (self.Rect.left, self.Rect.bottom + 5),
			(self.Rect.left + int(water_stat_length), self.Rect.bottom + 5), 3)
		pygame.draw.line(surface, Color("yellow"), (self.Rect.left, self.Rect.bottom + 15),
			(self.Rect.left + int(solar_stat_length), self.Rect.bottom + 15), 3)


#### Annuals		
class Beans(Plant):
	name = "beans"
	def __init__(self):
		self.name = "beans"
		self.caps_name = "Beans"
		self.color = Color("seagreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 805
		self.stage3_step = 1610
		self.stage4_step = 3220
		self.stage5_step = 4830
		self.stage6_step = 6440
		self.manured = False

class Broccoli(Plant):
	name = "broccoli"
	def __init__(self):
		self.name = "broccoli"
		self.caps_name = "Broccoli"
		self.color = Color("darkseagreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1221
		self.stage3_step = 2443
		self.stage4_step = 4887
		self.stage5_step = 7332
		self.stage6_step = 9775
		self.manured = False
		
class Carrot(Plant):
	name = "carrot"
	def __init__(self):
		self.name = "carrot"
		self.caps_name = "Carrot"
		self.color = Color("orange")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 934
		self.stage3_step = 1868
		self.stage4_step = 3737
		self.stage5_step = 5606
		self.stage6_step = 7475
		self.manured = False
		
class Celery(Plant):
	name = "celery"
	def __init__(self):
		self.name = "celery"
		self.caps_name = "Celery"
		self.color = Color("yellowgreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1725
		self.stage3_step = 3450
		self.stage4_step = 6900
		self.stage5_step = 10350
		self.stage6_step = 13800
		self.manured = False
		
class Corn(Plant):
	name = "corn"
	def __init__(self):
		self.name = "corn"
		self.caps_name = "Corn"
		self.color = Color("goldenrod")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1150
		self.stage3_step = 2300
		self.stage4_step = 4600
		self.stage5_step = 6900
		self.stage6_step = 9200
		self.manured = False

class Cucumber(Plant):
	name = "cucumber"
	def __init__(self):
		self.name = "cucumber"
		self.caps_name = "Cucumber"
		self.color = Color("darkolivegreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 862
		self.stage3_step = 1725
		self.stage4_step = 3450
		self.stage5_step = 5175
		self.stage6_step = 6900
		self.manured = False
		
class Dill(Plant):
	name = "dill"
	def __init__(self):
		self.name = "dill"
		self.caps_name = "Dill"
		self.color = Color("springgreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 575
		self.stage3_step = 1150
		self.stage4_step = 2300
		self.stage5_step = 3450
		self.stage6_step = 4600
		self.manured = False

class Lettuce(Plant):
	name = "lettuce"
	def __init__(self):
		self.name = "lettuce"
		self.caps_name = "Lettuce"
		self.color = Color("lawngreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 575
		self.stage3_step = 1150
		self.stage4_step = 2300
		self.stage5_step = 3450
		self.stage6_step = 4600
		self.manured = False
		
class Onion(Plant):
	name = "onion"
	def __init__(self):
		self.name = "onion"
		self.caps_name = "Onion"
		self.color = Color("seashell")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1437
		self.stage3_step = 2875
		self.stage4_step = 5750
		self.stage5_step = 8625
		self.stage6_step = 11500
		self.manured = False
		
class Pea(Plant):
	name = "pea"
	def __init__(self):
		self.name = "pea"
		self.caps_name = "Pea"
		self.color = Color("palegreen")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 834
		self.stage3_step = 1667
		self.stage4_step = 3335
		self.stage5_step = 5003
		self.stage6_step = 6670		
		self.manured = False
		
class Pepper(Plant):
	name = "pepper"
	def __init__(self):
		self.name = "pepper"
		self.caps_name = "Pepper"
		self.color = Color("violetred")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1078
		self.stage3_step = 2156
		self.stage4_step = 4312
		self.stage5_step = 6468
		self.stage6_step = 8625		
		self.manured = False
		
class Sunflower(Plant):	
	name = "sunflower"
	def __init__(self):
		self.name = "sunflower"
		self.caps_name = "Sunflower"
		self.color = Color("gold")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1006
		self.stage3_step = 2012
		self.stage4_step = 4025
		self.stage5_step = 6037
		self.stage6_step = 8050
		self.manured = False
		
class Tomato(Plant):
	name = "tomato"
	def __init__(self):
		self.name = "tomato"
		self.caps_name = "Tomato"
		self.color = Color("tomato")
		self.perennial = False
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1006
		self.stage3_step = 2012
		self.stage4_step = 4025
		self.stage5_step = 6037
		self.stage6_step = 8050
		self.manured = False
		
#### Perennials
class Apple(Plant):
	name = "apple"
	def __init__(self):
		self.name = "apple"
		self.caps_name = "Apple"
		self.color = Color("red")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 2587
		self.stage3_step = 5175
		self.stage4_step = 10350
		self.stage5_step = 20700
		self.stage6_step = 27600
		self.manured = False

class Asparagus(Plant):
	name = "asparagus"
	def __init__(self):
		self.name = "asparagus"
		self.caps_name = "Asparagus"
		self.color = Color("olivedrab")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 2010
		self.stage3_step = 4025
		self.stage4_step = 8050
		self.stage5_step = 16100
		self.stage6_step = 24150
		self.manured = False
		
class Cherry(Plant):
	name = "cherry"
	def __init__(self):
		self.name = "cherry"
		self.caps_name = "Cherry"
		self.color = Color("lightpink")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 3234
		self.stage3_step = 6467
		self.stage4_step = 12937
		self.stage5_step = 25875
		self.stage6_step = 34500
		self.manured = False
		
class Grape(Plant):
	name = "grape"
	def __init__(self):
		self.name = "grape"
		self.caps_name = "Grape"
		self.color = Color("darkorchid")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 3303
		self.stage3_step = 6606
		self.stage4_step = 11212
		self.stage5_step = 22425
		self.stage6_step = 29900
		self.manured = False
		
class Hops(Plant):
	name = "hops"
	def __init__(self):
		self.name = "hops"
		self.caps_name = "Hops"
		self.color = Color("forestgreen")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1725
		self.stage3_step = 3450
		self.stage4_step = 6900
		self.stage5_step = 13800
		self.stage6_step = 20700
		self.manured = False
		
class Lemon(Plant):
	name = "lemon"
	def __init__(self):
		self.name = "lemon"
		self.caps_name = "Lemon"
		self.color = Color("yellow")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 2300
		self.stage3_step = 4600
		self.stage4_step = 9200
		self.stage5_step = 18400
		self.stage6_step = 27600
		self.manured = False

class Orange(Plant):
	name = "orange"
	def __init__(self):
		self.name = "orange"
		self.caps_name = "Orange"
		self.color = Color("darkorange")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 2156
		self.stage3_step = 4312
		self.stage4_step = 8625
		self.stage5_step = 17250
		self.stage6_step = 25875
		self.manured = False

class Peach(Plant):
	name = "peach"
	def __init__(self):
		self.name = "peach"
		self.caps_name = "Peach"
		self.color = Color("lightcoral")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 3450
		self.stage3_step = 6900
		self.stage4_step = 13800
		self.stage5_step = 27600
		self.stage6_step = 36800
		self.manured = False

class Pear(Plant):
	name = "pear"
	def __init__(self):
		self.name = "pear"
		self.caps_name = "Pear"
		self.color = Color("chartreuse")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 4025
		self.stage3_step = 8050
		self.stage4_step = 16100
		self.stage5_step = 32200
		self.stage6_step = 40250
		self.manured = False
		
class Plum(Plant):
	name = "plum"
	def __init__(self):
		self.name = "plum"
		self.caps_name = "Plum"
		self.color = Color("plum")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 3712
		self.stage3_step = 7425
		self.stage4_step = 14950
		self.stage5_step = 29900
		self.stage6_step = 37375
		self.manured = False
		
class Starfruit(Plant):
	name = "starfruit"
	def __init__(self):
		self.name = "starfruit"
		self.caps_name = "Starfruit"
		self.color = Color("lightgoldenrodyellow")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 3450
		self.stage3_step = 6900
		self.stage4_step = 13800
		self.stage5_step = 27600
		self.stage6_step = 36800
		self.manured = False
		
class Strawberry(Plant):
	name = "strawberry"
	def __init__(self):
		self.name = "strawberry"
		self.caps_name = "Strawberry"
		self.color = Color("mediumorchid")
		self.perennial = True
		self.stage = 1
		self.image = pygame.image.load(os.path.join("Art", self.name + str(self.stage) + ".png")).convert()
		self.Rect = self.image.get_rect()
		self.max_solar = 1000
		self.solar_energy = 1000
		self.max_water = 1000
		self.water = 1000
		self.growth = 0
		self.growth_rate = 5
		self.stage2_step = 1667
		self.stage3_step = 3737
		self.stage4_step = 7475
		self.stage5_step = 14950
		self.stage6_step = 22425
		self.manured = False

crop_types = [Beans, Broccoli, Carrot, Celery, Corn, Cucumber, Dill, Lettuce, Onion, Pea, Pepper,
			Sunflower, Tomato, Apple, Asparagus, Cherry, Grape, Hops, Lemon, Orange,
			Peach, Pear, Plum, Starfruit, Strawberry]		
		
##### Garden classes
class Plot:
	def __init__(self, image_file, leftx, topy):
		self.image = pygame.image.load(os.path.join("Art", image_file)).convert()
		self.Rect = self.image.get_rect(topleft = (leftx, topy))
		self.empty = True
	
	def update(self, surface):
		if self.empty:
			surface.blit(self.image, self.Rect)
class Contract(object):
	def __init__(self, crop, price, amount, length, day_due):
		self.crop = crop
		self.price = price
		self.amount = amount
		self.length = length
		self.day_due = day_due
	def accept_contract(self, player):
		player.contracts.append(self)

	def call_due(self, garden, player, surface, clock, FPS, big_font, med_font, small_font):
		pygame.mouse.set_visible(True)
		window = pygame.Rect(300, 120, 400, 400)
		text = big_font.render("Contract Call", True, Color("black"))
		text_rect = text.get_rect(midtop = (window.centerx, window.top + 20))
		text2 = med_font.render("{0} {1} @ {2:.2f}".format(self.amount, self.crop, self.price), True, Color("black"))
		text2_rect = text2.get_rect(midtop = (window.centerx, text_rect.bottom + 20))
		exit = med_font.render("Continue", True, Color("blue"), Color("light_gray"))
		exit_rect = exit.get_rect(midbottom = (window.centerx, window.bottom - 20))
		failed = False
		if player.crops[self.crop] >= self.amount:
			player.crops[self.crop] -= self.amount
			player.cash += self.amount * self.price
			player.tot_contract_sales += self.amount * self.price
			player.contracts.remove(self)
		else:
			player.cash -= self.amount * self.price * .1
			player.tot_contract_penalties += self.amount * self.price * .1
			text3 = small_font.render("You cannot fulfill the contract and must pay", True, Color("black"))
			text3_rect = text3.get_rect(midbottom = (window.centerx, exit_rect.top - 50))
			text4 = small_font.render(" a 10% penalty of ${0:.2f}.".format(self.amount * self.price * .1), True, Color("black"))
			text4_rect = text4.get_rect(midtop = (window.centerx, text3_rect.bottom + 10))
			failed = True
			player.contracts.remove(self)
		pygame.draw.rect(surface, Color("white"), window)
		pygame.draw.rect(surface, Color("gray"), window, 5)
		surface.blit(text, text_rect)
		surface.blit(text2, text2_rect)
		if failed:	
			surface.blit(text3, text3_rect)
			surface.blit(text4, text4_rect)
		surface.blit(exit, exit_rect)
		pygame.display.update()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					if exit_rect.collidepoint(x, y):
						return False
			clock.tick(FPS)		
		
class Fund(object):
	fund_goods = {
		"AGR": (Color("darkgreen"), ["beans", "broccoli", "carrot", "celery", "corn", "cucumber",
				"dill", "lettuce", "pea", "pepper", "sunflower", "tomato",
				"apple", "asparagus", "cherry", "grape", "hops", "lemon",
				"orange", "peach", "pear", "plum", "starfruit", "strawberry"]),
		"CTR": (Color("yellow"), ["lemon", "orange", "starfruit"]),
		"FRT": (Color("red"), ["tomato", "apple", "cherry", "grape", "lemon", "orange",
				"peach", "pear", "plum", "starfruit", "strawberry"]),
		"PIE": (Color("coral"), ["apple", "cherry", "peach", "plum"]),
		"JUC": (Color("plum"), ["orange", "apple", "grape", "carrot"]),
		"SLD": (Color("springgreen"), ["lettuce", "tomato", "carrot", "onion", "cucumber"]),
		"VEG": (Color("forestgreen"), ["beans", "broccoli", "carrot", "celery", "corn", "cucumber",
				"dill", "lettuce", "pea", "pepper", "tomato"]),
		"SUP": (Color("wheat"), ["celery", "onion", "carrot"]),
		"DRI": (Color("maroon"), ["grape", "cherry", "plum", "pea", "corn"]),
		"BUZ": (Color("gold"), ["grape", "hops"]),
		"VYN": (Color("greenyellow"), ["pea", "beans", "hops", "grape", "strawberry"])}
	
	def __init__(self, name, garden):
		self.name = name
		self.color = self.fund_goods[self.name][0]
		self.goods = self.fund_goods[self.name][1]
		self.price = 0
		for good in self.goods:
			self.price += garden.prices[good]
		self.price = self.price / len(self.goods)

class Garden(object):
	def __init__(self, weather, plots, crop_types, interest_rate):
		self.weather = weather
		self.interest_rate = interest_rate
		self.plots = plots
		self.news_queue = []
		self.crops = []
		self.crop_types = crop_types # a list of plant classes
		for crop_type in self.crop_types:
			crop = crop_type()
			self.crops.append(crop)
		self.round_count = 1
		self.day_count = 1	
		self.daily_sun = 0
		self.daily_water = 0
		self.daily_evap = 0
		self.graph_data = []
		self.fund_graph_data = []
		self.plants = []
		self.base_prices = {
			"manure": 50.00,
			"fertilizer": .015,
			"water": .003,
			"beans": 24.08,
			"broccoli": 36.55,
			"carrot": 27.95,
			"celery": 52.20,
			"corn": 34.40,
			"cucumber": 25.80,
			"dill": 17.00,
			"lettuce": 17.00,
			"onion": 43.00,
			"pea": 24.94,
			"pepper": 32.25,
			"sunflower": 30.10,
			"tomato": 30.10,
			"apple": 41.92,
			"asparagus": 45.15,
			"cherry": 51.60,
			"grape": 45.15,
			"hops": 38.70,
			"lemon": 51.60,
			"orange": 48.38,
			"peach": 54.83,
			"pear": 51.60,
			"plum": 48.38,
			"starfruit": 54.83,
			"strawberry": 41.92}
		self.prices = {}
		for key in self.base_prices:
			self.prices[key] = self.base_prices[key]
		self.seed_prices = {
			"beans": 48.16,
			"broccoli": 73.10,
			"carrot": 55.80,
			"celery": 104.40,
			"corn": 68.80,
			"cucumber": 51.60,
			"dill": 34.00,
			"lettuce": 34.00,
			"onion": 86.00,
			"pea": 49.82,
			"pepper": 64.50,
			"sunflower": 60.20,
			"tomato": 60.20,
			"apple": 146.72,
			"asparagus": 135.45,
			"cherry": 180.60,
			"grape": 158.03,
			"hops": 116.10,
			"lemon": 154.80,
			"orange": 145.14,
			"peach": 219.32,
			"pear": 206.40,
			"plum": 193.502,
			"starfruit": 219.32,
			"strawberry": 125.76}
		self.volatilities = {
			"beans": (15, .15),
			"broccoli": (15, .15),
			"carrot": (15, .15),
			"celery": (15, .15),
			"corn": (15, .15),
			"cucumber": (15, .15),
			"dill": (15, .15),
			"lettuce": (15, .15),
			"onion": (15, .15),
			"pea": (15, .15),
			"pepper": (15, .15),
			"sunflower": (15, .15),
			"tomato": (15, .15),
			"apple": (15, .15),
			"asparagus": (15, .15),
			"cherry": (15, .15),
			"grape": (15, .15),
			"hops": (15, .15),
			"lemon": (15, .15),
			"orange": (15, .15),
			"peach": (15, .15),
			"pear": (15, .15),
			"plum": (15, .15),
			"starfruit": (15, .15),
			"strawberry": (15, .15)}
		self.business_climate = "Normal"
		self.business_climates = {
			"Phenomenal": (1.04, "Strong", "Strong", Color("darkgreen")),
			"Strong":     (1.025, "Phenomenal", "Upbeat", Color("greenyellow")),
			"Upbeat":     (1.012, "Strong", "Normal", Color("yellowgreen")),
			"Normal":     (1, "Upbeat", "Tepid", Color("white")),
			"Tepid":      (.99, "Normal", "Weak", Color("orange")),
			"Weak":       (.98, "Tepid", "Horrendous", Color("orangered")),
			"Horrendous": (.97, "Weak", "Weak", Color("red"))
			}
		self.funds = []
		self.has_windmill = False
		self.has_pigpen = False
		self.has_greenhouse = False
			
		for crop in self.crops:
			self.graph_data.append((0, self.prices[crop.name], crop.color))
		self.daily_contracts = []
	
	def price_update(self):
		for crop in self.crops:
			x = random.randint(1, 6)
			if self.prices[crop.name] > self.base_prices[crop.name]:
				x -= 1
			elif self.prices[crop.name] < self.base_prices[crop.name]:
				x += 1
			price_change = 0
			if x < 3:
				price_change = -(self.prices[crop.name] * random.uniform(0, self.volatilities[crop.name][1]))
			elif x > 4:
				price_change = self.prices[crop.name] * random.uniform(0, self.volatilities[crop.name][1])
			self.prices[crop.name] +=	price_change
			if price_change > 0:
				self.news_queue.append("{0} prices + ${1:.2f}".format(crop.caps_name, price_change))
			elif price_change < 0:
				self.news_queue.append("{0} prices - ${1:.2f}".format(crop.caps_name, abs(price_change)))
		for fund in self.funds:
			fund.price = 0
			for good in fund.goods:
				fund.price += self.prices[good]
			fund.price = fund.price / len(fund.goods)
			
	def economy_check(self):
		x = random.randint(1, 5)
		if x < 4:
			self.business_climate = self.business_climates[self.business_climate][1]
		else:
			self.business_climate = self.business_climates[self.business_climate][2]
		for key in self.prices:
			self.prices[key] = self.prices[key] * self.business_climates[self.business_climate][0]
		for key in self.seed_prices:
			self.seed_prices[key] = self.seed_prices[key] * self.business_climates[self.business_climate][0]
		for key in self.base_prices:
			self.base_prices[key] = self.base_prices[key] * self.business_climates[self.business_climate][0]
	
	def charge_player_tab(self, player):
		player.water_bill += self.prices["water"] * player.water_usage
		if not self.has_pigpen:
			player.manure_bill += self.prices["manure"] * player.manure_usage
		player.fert_bill += self.prices["fertilizer"] * player.fertilizer_usage
		player.water_usage = 0
		player.manure_usage = 0
		player.fertilizer_usage = 0	
	
	def charge_interest(self, player):
		if player.cash >= 0:
			pass
		else:
			player.cash += player.cash * self.interest_rate
		
	def add_fund_data(self):
		for fund in self.funds:
			self.fund_graph_data.append((self.day_count, fund.price, fund.color))
	
	def make_daily_contracts(self):
		self.daily_contracts = []
		for i in range(10):
			crop = random.choice(self.crops)
			amount = random.randint(5, 100)
			length = random.randint(5, 45)
			day_due = self.day_count + length
			contract = Contract(crop.name, self.prices[crop.name], amount, length, day_due)
			if contract.length < 8:
				contract.price += contract.price * .25
			elif contract.length < 12:
				contract.price += contract.price * .15
			elif contract.length < 16:
				contract.price += contract.price * .10
			if contract.amount > 80:
				contract.price += contract.price * .20
			elif contract.amount > 60:
				contract.price += contract.price * .15
			elif contract.amount > 40:
				contract.price += contract.price * .10
			elif contract.amount > 20:
				contract.price += contract.price * .05
			self.daily_contracts.append(contract)

			
def make_garden_plots(empty_plot_image, num_of_plots, row_length, left_margin, top_margin, horiz_space, vert_space) :
	plots = []
	vert = top_margin
	horiz = left_margin
	for i in range(1, num_of_plots + 1):
		plot = Plot(empty_plot_image, horiz, vert)
		plot.Rect.topleft = (horiz, vert)
		if i % (row_length) == 0:
			horiz = left_margin
			vert += plot.Rect.height + vert_space
		else:
			horiz += plot.Rect.width + horiz_space
		plots.append(plot)
	return plots
			

 