class Level(object):
	starting_cash = 500
	interest_rate = .05
	def level_setup(self):
		pass
	def failcheck(self):
		return self.days < 1

class Level1(Level):
	def __init__(self):
		self.num = 1
		self.days = 10  #length of level
		self.goals = ["- Harvest 5 dill"]
		self.interest_rate = .02	
	def wincheck(self, player, garden):
		return player.crops_harvested["dill"] >= 5
			
class Level2(Level):
	def __init__(self):
		self.num = 2
		self.days = 20  #length of level
		self.goals = ["- Harvest 5 lettuce", "- Harvest 5 tomato"]
		self.interest_rate = .02
	def wincheck(self, player, garden):
		return player.crops_harvested["lettuce"] >= 5 and player.crops_harvested["tomato"] >= 5
			
			
class Level3(Level):
	def __init__(self):
		self.num = 3
		self.days = 30    #length of level
		self.goals = ["- Earn $500 in farm profits"]
		self.interest_rate = .03
	def wincheck(self, player, garden):
		return player.tot_crop_sales + player.tot_contract_sales + -player.tot_water_usage +\
				-player.tot_manure_usage + -player.tot_fertilizer_usage + -player.tot_seed_usage +\
				-player.tot_equip_usage >= 500
			
class Level4(Level):
	def __init__(self):
		self.num = 4
		self.days = 40    #length of level
		self.goals = ["- Build a windmill", "-Earn $500 in farming profits"]
		self.interest_rate = .03
	def wincheck(self, player, garden):
		return player.tot_crop_sales + player.tot_contract_sales + -player.tot_water_usage +\
				-player.tot_manure_usage + -player.tot_fertilizer_usage + -player.tot_seed_usage +\
				-player.tot_equip_usage >= 500 and garden.has_windmill

class Level5(Level):
	def __init__(self):
		self.num = 5
		self.days = 50    #length of level
		self.goals = ["- Earn $2000 in farm profits"]
		
	def wincheck(self, player, garden):
		return player.tot_crop_sales + player.tot_contract_sales + -player.tot_water_usage +\
				-player.tot_manure_usage + -player.tot_fertilizer_usage + -player.tot_seed_usage +\
				-player.tot_equip_usage >= 2000

class Level6(Level):
	def __init__(self):
		self.num = 6
		self.days = 50    #length of level
		self.starting_cash = 5000
		self.goals = ["- Earn $500 in index fund profits"]
		
	def wincheck(self, player, garden):
		return player.fund_sales - player.fund_purchases >= 500

class Level7(Level):
	def __init__(self):
		self.num = 7
		self.days = 100    #length of level
		self.starting_cash = 500
		self.goals = ["- Harvest 10 tomato", "- Harvest 10 onion", "- Harvest 10 pepper"]
		
	def wincheck(self, player, garden):
		return player.crops_harvested["tomato"] >= 10 and player.crops_harvested["onion"] >= 10 and player.crops_harvested["pepper"] >= 10
		
class Level8(Level):
	def __init__(self):
		self.num = 8
		self.days = 150    #length of level
		self.starting_cash = 5000
		self.goals = ["- Earn $5000 in operating profits", "- Harvest 50 beans", "- Harvest 50 peas", "- Harvest 10 hops"]
		
	def wincheck(self, player, garden):
		if player.tot_crop_sales + player.tot_contract_sales + -player.tot_water_usage +\
				-player.tot_manure_usage + -player.tot_fertilizer_usage + -player.tot_seed_usage +\
				-player.tot_equip_usage >= 5000:
			return player.crops_harvested["beans"] >= 50 and player.crops_harvestd["peas"] >= 50 and playuer.crops_harvestd["hops"] >= 10

class Level9(Level):
	def __init__(self):
		self.num = 9
		self.days = 120
		self.starting_cash = 500
		self.goals = ["- Have $3000 in contract sales", "- Build a Greenhouse"]
	
	def wincheck(self, player, garden):
		return player.tot_contract_sales >= 3000 and garden.has_greenhouse
		
class Level10(Level):
	def __init__(self):
		self.num = 10
		self.days = 180
		self.starting_cash = 2000
		self.goals = ["- Have $10,000 cash", "- Build a Pig Pen", "- Earn $500 in Index Fund profits"]
	
	def wincheck(self, player, garden):
		return player.cash >= 10000 and garden.has_pigpen and (player.fund_sales - player.fund_purchases) >= 500
			
level_map = {
	1: Level1, 2: Level2, 3: Level3, 4: Level4, 5: Level5, 6: Level6, 7: Level7, 8: Level8}