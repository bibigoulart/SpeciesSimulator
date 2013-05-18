import random

yaml = {'years':100,
		'iterations':4,
		'species': {'name':'kangaroo', 
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
									}
		'habitats': {
					'name':'plains',
					'monthly_food':100,
					'monthly_water':150,
					'average_temperature': {
											'summer':85,
											'spring':60,
											'fall':50,
											'winter':30
					}
					}
					}

class Animal:
	def __init__(self, monthly_food_consumption, monthly_water_consumption, life_span,
				minimum_breeding_age, maximum_breeding_age, gestation_period,
				minimum_temperature, maximum_temperature):
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




class Habitat(object):
	pass

def yaml_parser(yaml):
	return yaml




def simulation_runner():
	'''
	Main function of the simulator, calls functions to parse and run data
	'''
	data = yaml_parser(yaml)
	years = data['years']
	iterations = data['iterations']
	for animal in data['species']:
