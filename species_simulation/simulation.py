import random

#test data
yaml = {'years':100,
		'iterations':4,
		'species': [{'name':'kangaroo', 
					'attributes': {
									'monthly_food_consumption':3,
									'monthly_water_consumption':4,
									'life_span':30,
									'minimum_breeding_age':5,
									'maximum_breeding_age':20,
									'gestation_period':9,
									'minimum_temperature':30,
									'maximum_temperature':110
									}
									}],
		'habitats': [{
					'name':'plains',
					'monthly_food':100,
					'monthly_water':150,
					'average_temperature': {
											'summer':85,
											'spring':60,
											'fall':50,
											'winter':30
					}
					}]
					}



class Animal:
	def __init__(self, species, monthly_food_consumption, monthly_water_consumption, 
				life_span, minimum_breeding_age, maximum_breeding_age, gestation_period,
				minimum_temperature, maximum_temperature, gender=None):
		self.species = species
		self.monthly_food_consumption = monthly_food_consumption
		self.monthly_water_consumption = monthly_water_consumption
		self.life_span = life_span * 12 #all time units converted to months
		self.minimum_breeding_age = minimum_breeding_age * 12
		self.maximum_breeding_age = maximum_breeding_age * 12
		self.gestation_period = gestation_period
		self.minimum_temperature = minimum_temperature
		self.maximum_temperature = maximum_temperature
		self.age = 0
		self.living = True
		if gender: #1 is female, 2 is male
			self.gender = gender
		else:
			self.gender = random.randint(1,2)
		self.pregnant = False
		self.cause_of_death = None
		self.months_without_water = 0
		self.months_without_food = 0




class Habitat:
	def __init__(self, name, monthly_food, monthly_water, summer_temp, spring_temp, 
				fall_temp, winter_temp):
		self.name = name
		self.monthly_food = monthly_food
		self.monthly_water = monthly_water
		self.summer_temp = summer_temp
		self.spring_temp = spring_temp
		self.fall_temp = fall_temp
		self.winter_temp = winter_temp
		self.food_supply = 0
		self.water_supply = 0
		self.population = []

	def set_temperature(self,season):
		'''
		sets temperature which fluctuates by up to 5 degrees, with a 
		1/200 chance of fluctuating by up to 15 degrees
		''' 
		multiplier = 1
		if random.randint(1,200) == 1:
			multiplier = 3
		fluctuation = random.randint(-5,5) * multiplier
		if season == 'summer':
			self.temperature = self.summer_temp + fluctuation
		elif season == 'fall':
			self.temperature = self.fall_temp + fluctuation
		elif season == 'winter':
			self.temperature = self.winter_temp + fluctuation
		elif season == 'spring':
			self.temperature = self.spring_temp + fluctuation

	def refresh_food_and_water(self):
		environment.food_supply += environment.monthly_food
		environment.water_supply += environment.monthly_water

def yaml_parser(yaml):
	return yaml

def current_season(month):
	'''
		given month number, returns season
	'''
	month_of_year = month % 12
	if month_of_year == 0:
		month_of_year = 12
	seasons = {
			1: 'winter',
			2: 'winter',
			3: 'spring',
			4: 'spring', 
			5: 'spring',
			6: 'summer',
			7: 'summer',
			8: 'summer',
			9: 'fall',
			10: 'fall',
			11: 'fall',
			12: 'winter'
			}

	season = seasons[month_of_year]
	return season



def age_animals():
	pass

def consume_food_and_water():
	pass


def monthly_tasks(month, environment):
	season = current_season(month)
	environment.refresh_food_and_water()
	environment.set_temperature(season)
	age_animals()
	consume_food_and_water()

def results_generator():
	pass

def simulation_runner():
	'''
	Main function of the simulator, calls functions to parse and run data
	'''
	data = yaml_parser(yaml)
	months = data['years'] * 12
	iterations = data['iterations']
	for species in data['species']:
		for habitat in data['habitats']:
			environment = Habitat(habitat['name'], 
								  habitat['monthly_food'],
								  habitat['monthly_water'], 
								  habitat['average_temperature']['summer'],
								  habitat['average_temperature']['spring'],
								  habitat['average_temperature']['fall'],
								  habitat['average_temperature']['winter'],
								  )
			for gender_code in [1,2]: #create initial male and female
				new_animal = Animal(species['name'],
									species['attributes']['monthly_food_consumption'],
									species['attributes']['monthly_water_consumption'],
									species['attributes']['life_span'],
									species['attributes']['minimum_breeding_age'],
									species['attributes']['maximum_breeding_age'],
									species['attributes']['gestation_period'],
									species['attributes']['minimum_temperature'],
									species['attributes']['maximum_temperature'],
									gender=gender_code
									)
				environment.population.append(new_animal)
			for month in range(months):
				monthly_tasks(month, environment)



simulation_runner()







