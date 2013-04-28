
class Fund(object):
	fund_goods = {
		"AGR": ["beans", "broccoli", "carrot", "celery", "corn", "cucumber",
				"dill", "lettuce", "pea", "pepper", "sunflower", "tomato",
				"apple", "aspparagus", "cherry", "grape", "hops", "lemon",
				"orange", "peach", "pear", "plum", "starfruit", "strawberry"],
		"CTR": ["lemon", "orange", "starfruit"],
		"FRT": ["tomato", "apple", "cherry", "grape", "lemon", "orange",
				"peach", "pear", "plum", "starfruit", "strawberry"],
		"PIE": ["apple", "cherry", "peach", "plum"],
		"JUC": ["orange", "apple", "grape", "carrot"],
		"SLD": ["lettuce", "tomato", "carrot", "onion", "cucumber"],
		"VEG": ["beans", "broccoli", "carrot", "celery", "corn", "cucumber",
				"dill", "lettuce", "pea", "pepper", "tomato"],
		"CTR": ["lemon", "orange", "starfruit"],
		"SUP": ["celery", "onion", "carrot"],
		"DRI": ["grape", "cherry", "plum", "pea", "corn"],
		"BUZ": ["grape", "hops"],
		"VYN": ["pea", "beans", "hops", "grape", "strawberry"]}
	
	def __init__(self, name, garden):
		self.name = name
		self.color = colors.
		self.goods = self.fund_goods[self.name]
		self.price = 0
			for good in self.goods:
				self.price += garden.base_prices[good]
			self.price = self.price / len(self.goods)

def make_funds(garden):
	for key in Fund.fund_goods:
		fund = Fund(key, garden)
		garden.funds.append(fund)
