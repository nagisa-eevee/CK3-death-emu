import numpy as np

class DEATH:
    def __init__(self):
        pass

    def run(self,
            _NEWBORN_HEALTH_BASE=4.5,
            _NEWBORN_HEALTH_SPAN=0.5,
            _NEWBORN_HEALTH_FEMALE_BONUS = 0.5,              
            _LOWER_HEALTH_BASE_CHANCE = 0.075,    
            _LOWER_HEALTH_YEARLY_INCREASE = 0.022,         
            _LOWER_HEALTH_AMOUNT = -0.125,               
            _DIE_HEALTH_TRESHOLD = 3.0,                  
            _DIE_HEALTH_CHANCE_ZERO = 0.25,              
            _YEAR_DURATION = 360,
            _DEATH_CHECK_INTERVAL = 30,
            _BATCH_SIZE = int(1e5),                        
            _FEMALE_RATIO = 0.0,                           
            _AGE_RANGE = (25, 100)):
        _INIT_HEALTH = self.init_health(_NEWBORN_HEALTH_BASE, _NEWBORN_HEALTH_SPAN, _NEWBORN_HEALTH_FEMALE_BONUS, _FEMALE_RATIO, _BATCH_SIZE) # size = (BATCH_SIZE, )
        _LOWER_HEALTH_CHANCE = self.lower_health_chance(_LOWER_HEALTH_BASE_CHANCE, _LOWER_HEALTH_YEARLY_INCREASE, _AGE_RANGE) # size = (AGE_RANGE[1] - AGE_RANGE[0] + 1, )
        _HEALTH = self.health(_INIT_HEALTH, _LOWER_HEALTH_CHANCE, _LOWER_HEALTH_AMOUNT)
        _DEATH = self.death(_HEALTH, _AGE_RANGE, _DIE_HEALTH_TRESHOLD, _DIE_HEALTH_CHANCE_ZERO, _YEAR_DURATION, _DEATH_CHECK_INTERVAL)
        return _DEATH

    @staticmethod
    def init_health(HEALTH_BASE=4.5, HEALTH_SPAN=0.5, FEMALE_BONUS=0.5, female_ratio=0.5,number=10):
        return HEALTH_BASE + (2 * np.random.rand(number) - 1) * HEALTH_SPAN + \
        np.ceil(female_ratio-np.random.randint(0,2, size=number)) * FEMALE_BONUS

    @staticmethod
    def lower_health_chance(LOWER_HEALTH_BASE_CHANCE=0.075, LOWER_HEALTH_YEARLY_INCREASE=0.022, AGE_RANGE=(25, 100)):
        table = np.array([LOWER_HEALTH_BASE_CHANCE] + [LOWER_HEALTH_YEARLY_INCREASE] * (AGE_RANGE[1] - AGE_RANGE[0]))
        return np.clip(np.cumsum(table), 0, 1)

    @staticmethod
    def health(INIT_HEALTH, LOWER_HEALTH_CHANCE, LOWER_HEALTH_AMOUNT):
        fortune = np.random.random(size=(INIT_HEALTH.size, LOWER_HEALTH_CHANCE.size))
        lower_health = np.zeros(fortune.shape)
        lower_health[fortune < LOWER_HEALTH_CHANCE] = LOWER_HEALTH_AMOUNT
        health = np.reshape(INIT_HEALTH, (INIT_HEALTH.size, 1)) + np.cumsum(lower_health, axis=1)
        return health

    @staticmethod
    def death(HEALTH, AGE_RANGE, DIE_HEALTH_TRESHOLD=3, DIE_HEALTH_CHANCE_ZERO=0.25, YEAR_DURATION=360, DEATH_CHECK_INTERVAL=30):
        death_probility = 1 - (1 - np.clip((1 - HEALTH/DIE_HEALTH_TRESHOLD), 0, 1) ** 2 * DIE_HEALTH_CHANCE_ZERO) ** (YEAR_DURATION/DEATH_CHECK_INTERVAL)
        death_probility = np.hstack((death_probility, np.ones((death_probility.shape[0], 1)))) # if alive, mark the character dies at AGE_RANGE[1] + 1
        fortune = np.random.random(size=death_probility.shape)
        death = np.zeros(fortune.shape)
        death[fortune<death_probility] = 1
        return np.argmax(death, axis=1) + AGE_RANGE[0]

    @staticmethod
    def stats(_DEATH, percent = [5, 25, 50, 75, 95]):
        max_age = np.max(_DEATH)
        min_age = np.min(_DEATH)
        avg_age = np.mean(_DEATH)
        percent = [5, 25, 50, 75, 95]
        percentile = np.percentile(_DEATH, percent)
        stats = f"min: {min_age}, max: {max_age}, average {avg_age}. \n"
        for p, age in zip(percent, list(percentile)):
            stats += f"{p: >2}% characters died at age {age}.\n"
        print(stats)
        plt.hist(_DEATH, bins=max_age-min_age+1)
        return {"max_age": max_age, "min_age": min_age, "avg_age": avg_age, "percentile": list(zip(percent, percentile))}



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    """
    formula:
    DEATH_PROBABILITY_IN_EACH_YEAR = 1 - (1 - (1 - CURRENT_HEALTH/DIE_HEALTH_TRESHOLD)^2) ** (YEAR_DURATION/DEATH_CHECK_INTERVAL) * DIE_HEALTH_CHANCE_ZERO

    parameters:
    _NEWBORN_HEALTH_BASE=4.5
    _NEWBORN_HEALTH_SPAN=0.5
    _NEWBORN_HEALTH_FEMALE_BONUS = 0.5
    
    _LOWER_HEALTH_START_AGE = 25                   # At this age characters start getting the chance to lose health each year
    _LOWER_HEALTH_BASE_CHANCE = 0.075              # This is the base chance of losing health at the START_AGE
    _LOWER_HEALTH_YEARLY_INCREASE = 0.022          # This is the yearly increase of the chance to lose health
    _LOWER_HEALTH_AMOUNT = -0.125                  # This is the health change on each failed yearly health roll
           
    _DIE_HEALTH_TRESHOLD = 3.0                     # Characters have a chance to die each DEATH_CHECK_INTERVAL days they have less health than this
    _DIE_HEALTH_CHANCE_ZERO = 0.25                 # This is the DEATH_CHECK_INTERVAL chance that a character dies at zero health (or lower)
    _YEAR_DURATION = 360
    _DEATH_CHECK_INTERVAL = 30                     # Check if the character should die from health this often (in days)

    _BATCH_SIZE = int(1e5)                         # How many characters are generated at the same time 
    _FEMALE_RATIO = 0.0                            # The ratio of female, between 0 and 1
    _AGE_RANGE = (_LOWER_HEALTH_START_AGE, 100)     # Only gives statistics of deaths between [Lower, High] 
    """   
    
    death = DEATH()
    _DEATH = death.run()
    _STATS = death.stats(_DEATH)
    print(_STATS)
    plt.show()