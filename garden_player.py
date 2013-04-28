import pygame
from pygame import Color

class Player(object):
	def __init__(self):
		self.music_on = True
		self.previous_level = 0
		self.level = 1
		self.cash = 2000.0
		self.water_bill = 0
		self.manure_bill = 0
		self.fert_bill = 0
		self.tot_water_usage = 0
		self.tot_manure_usage = 0
		self.tot_fertilizer_usage = 0
		self.tot_seed_usage = 0
		self.tot_equip_usage = 0
		self.tot_crop_sales = 0
		self.tot_contract_sales = 0
		self.tot_contract_penalties = 0
		self.contracts = []
		self.crops = {
			"beans": 0,
			"broccoli": 0,
			"carrot": 0,
			"celery": 0,
			"corn": 0,
			"cucumber": 0,
			"dill": 0,
			"lettuce": 0,
			"onion": 0,
			"pea": 0,
			"pepper": 0,
			"sunflower": 0,
			"tomato": 0,
			"apple": 0,
			"asparagus": 0,
			"cherry": 0,
			"grape": 0,
			"hops": 0,
			"lemon": 0,
			"orange": 0,
			"peach": 0,
			"pear": 0,
			"plum": 0,
			"starfruit": 0,
			"strawberry": 0}
		self.seeds = {
			"beans": 0,
			"broccoli": 0,
			"carrot": 0,
			"celery": 0,
			"corn": 0,
			"cucumber": 0,
			"dill": 0,
			"lettuce": 0,
			"onion": 0,
			"pea": 0,
			"pepper": 0,
			"sunflower": 0,
			"tomato": 0,
			"apple": 0,
			"asparagus": 0,
			"cherry": 0,
			"grape": 0,
			"hops": 0,
			"lemon": 0,
			"orange": 0,
			"peach": 0,
			"pear": 0,
			"plum": 0,
			"starfruit": 0,
			"strawberry": 0}
		self.crops_harvested = {
			"beans": 0,
			"broccoli": 0,
			"carrot": 0,
			"celery": 0,
			"corn": 0,
			"cucumber": 0,
			"dill": 0,
			"lettuce": 0,
			"onion": 0,
			"pea": 0,
			"pepper": 0,
			"sunflower": 0,
			"tomato": 0,
			"apple": 0,
			"asparagus": 0,
			"cherry": 0,
			"grape": 0,
			"hops": 0,
			"lemon": 0,
			"orange": 0,
			"peach": 0,
			"pear": 0,
			"plum": 0,
			"starfruit": 0,
			"strawberry": 0}
		self.water_usage = 0
		self.manure_usage = 0
		self.fertilizer_usage = 0
		self.fund_shares = {
			"AGR": 0,
			"CTR": 0,
			"FRT": 0,
			"PIE": 0,
			"JUC": 0,
			"SLD": 0,
			"VEG": 0,
			"SUP": 0,
			"DRI": 0,
			"BUZ": 0,
			"VYN": 0}
		self.fund_purchases = 0
		self.fund_sales = 0
	def pay_bill(self, surface, titlefont, itemfont, totalfont, game_clock, framerate):
		pygame.mouse.set_visible(True)
		window = pygame.Rect(200, 100, 580, 480)
		title = titlefont.render("Invoice", True, Color("black"), Color("antiquewhite"))
		title_rect = title.get_rect(midtop = (window.centerx, window.top + 10))
		exit_text = titlefont.render("EXIT", True, Color("blue"), Color("lightgray"))
		exit_rect = exit_text.get_rect(midbottom = (window.centerx, window.bottom - 20))
		water = itemfont.render("Water", True, Color("black"), Color("antiquewhite"))
		water_rect = water.get_rect(topleft = (window.right - 280, title_rect.bottom + 50))
		manure = itemfont.render("Manure", True, Color("black"), Color("antiquewhite"))
		manure_rect = manure.get_rect(topleft = (water_rect.left, water_rect.bottom + 20))
		fert = itemfont.render("Fertilizer", True, Color("black"), Color("antiquewhite"))
		fert_rect = fert.get_rect(topleft = (water_rect.left, manure_rect.bottom + 20))
		total = totalfont.render("Amount Due", True, Color("black"), Color("antiquewhite"))
		total_rect = total.get_rect(bottomleft = (water_rect.left, fert_rect.bottom + 50))
		paying = True
		while paying:
			waternum = itemfont.render("{0:.2f}".format(self.water_bill), True, Color("black"), Color("antiquewhite"))
			waternum_rect = waternum.get_rect(topright = (window.right - 20, water_rect.top))
			manurenum = itemfont.render("{0:.2f}".format(self.manure_bill), True, Color("black"), Color("antiquewhite"))
			manurenum_rect = manurenum.get_rect(topright = (waternum_rect.right, manure_rect.top))
			fertnum = itemfont.render("{0:.2f}".format(self.fert_bill), True, Color("black"), Color("antiquewhite"))
			fertnum_rect = fertnum.get_rect(topright = (waternum_rect.right, fert_rect.top))
			totalnum = totalfont.render(
				"{0:.2f}".format(self.water_bill + self.manure_bill + self.fert_bill),
				True, Color("black"), Color("antiquewhite"))
			totalnum_rect = totalnum.get_rect(topright = (waternum_rect.right, total_rect.top))
			
			for event in pygame.event.get():	
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					if exit_rect.collidepoint(x, y):
						self.cash -= self.water_bill + self.manure_bill + self.fert_bill
						self.tot_water_usage += self.water_bill
						self.tot_manure_usage += self.manure_bill
						self.tot_fertilizer_usage += self.fert_bill
						self.water_bill, self.manure_bill, self.fert_bill = 0, 0, 0
						paying = False
			pygame.draw.rect(surface, Color("antiquewhite"), window) 
			pygame.draw.rect(surface, Color("gray"), window, 5)
			blit_list = [(title, title_rect), (exit_text, exit_rect), (water, water_rect),
			(manure, manure_rect), (fert, fert_rect), (total, total_rect), (waternum, waternum_rect),
			(manurenum, manurenum_rect), (fertnum, fertnum_rect), (totalnum, totalnum_rect)]
			for text, rectangle in blit_list:
				surface.blit(text, rectangle)
			pygame.display.update()
			game_clock.tick(framerate)
			
		
		