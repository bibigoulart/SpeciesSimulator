import random
import yaml

#test data
# yaml = {'years':100,
# 		'iterations':4,
# 		'species': [{'name':'kangaroo', 
# 					'attributes': {
# 									'monthly_food_consumption':3,
# 									'monthly_water_consumption':4,
# 									'life_span':30,
# 									'minimum_breeding_age':5,
# 									'maximum_breeding_age':20,
# 									'gestation_period':9,
# 									'minimum_temperature':30,
# 									'maximum_temperature':110
# 									}
# 									}],
# 		'habitats': [{
# 					'name':'plains',
# 					'monthly_food':100,
# 					'monthly_water':150,
# 					'average_temperature': {
# 											'summer':85,
# 											'spring':60,
# 											'fall':50,
# 											'winter':30
# 					}
# 					}]
# 					}


def yaml_parser(yaml):
	f = open('config.txt')
	data = f.read()
	output = yaml.load(data)
	return output

def dice_roller(percentage):
	'''
		given the probability of an event occuring, returns True if 
		event is successful
	'''
	chance = random.random()
	percentage = percentage / 100.0
	if chance <= percentage:
		return True
	else:
		return False

class Animal:
	def __init__(self, species, monthly_food_consumption, monthly_water_consumption, 
				life_span, minimum_breeding_age, maximum_breeding_age, gestation_period,
				minimum_temperature, maximum_temperature, gender=None):
		self.species = species
		self.monthly_food_consumption = monthly_food_consumption
		self.monthly_water_consumption = monthly_water_consumption
		self.life_span_years = life_span
		self.minimum_breeding_age_years = minimum_breeding_age
		self.maximum_breeding_age_years = maximum_breeding_age
		self.life_span = self.life_span_years * 12 #all time units converted to months
		self.minimum_breeding_age = self.minimum_breeding_age_years * 12
		self.maximum_breeding_age = self.maximum_breeding_age_years * 12
		self.gestation_period = gestation_period
		self.minimum_temperature = minimum_temperature
		self.maximum_temperature = maximum_temperature
		self.age = 0
		self.living = True
		if gender: #1 is female, 2 is male
			self.gender = gender
		else:
			self.gender = random.randint(1,2)
		self.pregnant = {'pregnant': False, 'months':0}
		self.cause_of_death = None
		self.months_without_water = 0
		self.months_without_food = 0
		self.months_of_extreme_temperature = 0
		self.fertility_rate = 80 #TODO: this value is made up for now



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
		self.population_record = []

	def set_temperature(self,season):
		'''
		sets temperature which fluctuates by up to 5 degrees, with a 
		1/200 chance of fluctuating by up to 15 degrees
		''' 
		multiplier = 1
		if dice_roller(.5):
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
		self.food_supply += self.monthly_food
		self.water_supply += self.monthly_water

	def consume_food_and_water(self):
		'''
			for each living animal in population: if food and water supply is
			adequate, decreases supply by animal's consumption.  Otherwise,
			increases months without food/water by one
		'''
		for animal in self.population:
			if animal.living:
				if self.food_supply >= animal.monthly_food_consumption:
					self.food_supply -= animal.monthly_food_consumption
					animal.months_without_food = 0
				else:
					animal.months_without_food += 1
				if self.water_supply >= animal.monthly_water_consumption:
					self.water_supply -= animal.monthly_water_consumption
					animal.months_without_water = 0
				else:
					animal.months_without_water += 1

	def age_animals(self):
		'''
			increments age of each living animal by one month, along with 
			months pregnant if applicable
		'''
		for animal in self.population:
			if animal.living:
				animal.age += 1
				if animal.pregnant['pregnant']:
					animal.pregnant['months'] += 1

	def breed_animals(self):
		babies = []
		male_available = False
		for animal in self.population:
			if animal.gender == 2 and animal.age >= animal.minimum_breeding_age:
				#check for at least one male of age
				male_available = True
				break
		for animal in self.population:
			if animal.gender == 1 and animal.living:
				if animal.pregnant['pregnant'] and (animal.pregnant['months'] >= animal.gestation_period):
					animal.pregnant = {'pregnant': False, 'months':0}
					new_animal = Animal(
									animal.species,
									animal.monthly_food_consumption,
									animal.monthly_water_consumption,
									animal.life_span_years,
									animal.minimum_breeding_age_years,
									animal.maximum_breeding_age_years,
									animal.gestation_period,
									animal.minimum_temperature,
									animal.maximum_temperature
									)
					babies.append(new_animal)
				elif (not animal.pregnant['pregnant'] and 
						  animal.minimum_breeding_age <= animal.age < animal.maximum_breeding_age):
					fertility = animal.fertility_rate
					if (self.food_supply < animal.monthly_food_consumption or
						self.water_supply < animal.monthly_water_consumption):
						fertility *= .005 #reduces fertility rate if insuff. resources
					if dice_roller(fertility):
						animal.pregnant['pregnant'] = True
		self.population += babies

	def kill_the_weak(self):
		'''
		sets living to False if any fatal conditions are met and stores
		cause of death.  Also tracks remaining living population.
		'''
		living_count = 0
		for animal in self.population:
			if animal.living:
				living_count += 1
				if animal.age > animal.life_span:
					animal.living = False
					animal.cause_of_death = 'age'
				elif animal.months_without_water > 1:
					animal.living = False
					animal.cause_of_death = 'thirst'
				elif animal.months_without_food > 3:
					animal.living = False
					animal.cause_of_death = 'starvation'
				elif self.temperature > animal.maximum_temperature:
					animal.months_of_extreme_temperature += 1
					if animal.months_of_extreme_temperature > 1:
						animal.living = False
						animal.cause_of_death = 'hot_weather'
				elif self.temperature < animal.minimum_temperature:
					animal.months_of_extreme_temperature += 1
					if animal.months_of_extreme_temperature > 1:
						animal.living = False
						animal.cause_of_death = 'cold_weather'
				else:
					animal.months_of_extreme_temperature = 0

		self.population_record.append(living_count)




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


def monthly_tasks(month, environment):
	season = current_season(month)
	environment.refresh_food_and_water()
	environment.set_temperature(season)
	environment.kill_the_weak()
	environment.consume_food_and_water()
	environment.breed_animals()
	environment.age_animals()

def percentage_converter(part, whole):
	'''
	converts to a percentage to two decimal places
	'''
	percentage = round(part/float(whole) * 100.0, 2)
	return percentage

def results_generator(species,habitat,iteration_results,months,iterations):
	'''
		iteration_results should consist of a list of completed habitats, returns dictionary of results
	'''
	animal_type = species['name']
	habitat_type = habitat.name
	total_population = 0
	max_population = max([max(environment.population_record) for environment in iteration_results])
	for environment in iteration_results:
		total_population += sum(environment.population_record)
	average_population = total_population / (months * iterations)

	number_of_dead = 0
	death_by_age = 0
	death_by_starvation = 0
	death_by_thirst = 0
	death_by_cold = 0
	death_by_heat = 0
	total_animals = 0
	for environment in iteration_results:
		total_animals += len(environment.population)
		for animal in environment.population:
			if not animal.living:
				number_of_dead += 1
				if animal.cause_of_death == 'age':
					death_by_age += 1
				elif animal.cause_of_death == 'starvation':
					death_by_starvation += 1
				elif animal.cause_of_death == 'thirst':
					death_by_thirst += 1
				elif animal.cause_of_death == 'cold_weather':
					death_by_cold += 1
				elif animal.cause_of_death == 'hot_weather':
					death_by_heat += 1
		for cause_of_death in ([death_by_heat, death_by_cold, death_by_thirst, 
								death_by_starvation, death_by_age]):
			cause_of_death = percentage_converter(cause_of_death, number_of_dead)

	mortality_rate = str(round(number_of_dead / float(total_animals) * 100, 2)) + '%'
	causes_of_death = {'age' : death_by_age,
						'starvation' : death_by_starvation,
						'thirst' : death_by_thirst,
						'hot_weather' : death_by_heat,
						'cold_weather' : death_by_cold
						}
	for cause, count in causes_of_death.iteritems():
		causes_of_death[cause] = str(percentage_converter(count, number_of_dead)) + '%'
	results = {habitat_type : {
								'Average Population' : average_population,
								'Max Population' : max_population,
								'Mortality Rate' : mortality_rate,
								'Cause of Death' : causes_of_death
								}
				}
	return results



def simulation_runner():
	'''
	Main function of the simulator, calls functions to parse and run data
	'''
	data = yaml_parser(yaml)
	months = data['years'] * 12
	iterations = data['iterations']
	results = {}
	results['Conditions'] = "Simulation ran for {0} iterations at {1} years per iteration".format(iterations, data['years'])
	for species in data['species']:
		name = species['name']
		animal_results = []
		habitat_population_tracker = [] #will keep track of populations over iterations
		for habitat in data['habitats']:
			iteration_results = []
			for i, iteration in enumerate(range(iterations)):
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
				iteration_results.append(environment)
			animal_results.append(results_generator(species, environment, iteration_results, months, iterations))
		results[name] = animal_results
	return yaml.dump(results, default_flow_style=False)




print simulation_runner()







