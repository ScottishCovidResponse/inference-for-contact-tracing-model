'''
Created on 2020/06/12

@author: rikiya
'''
import numpy as np
from sklearn.utils import check_random_state
from collections import OrderedDict


class PopulationSettings(object):
    '''
    Generate diseaseSettings.json
    '''
    
    def __init__(
            self,
            population_concentration=10.0,
            random_state=None):
        self.random_state = check_random_state(random_state)
        self.population_concentration = population_concentration
    
    def next(self):
        """
        Simulate a vector of parameters.
        Results are obtained as a dictionary.
        """
        random_state = self.random_state
        result = OrderedDict()

        alpha = np.array([0.1759, 0.1171, 0.4029, 0.1222, 0.1819]) * self.population_concentration
        popdist = random_state.dirichlet(alpha)
        # Occasionally, popdist above does not satisfy the constraint s.t. sum=1.
        popdist /= popdist.sum()
        
        for i in range(5):
            result['population_distribution_{}'.format(i)] = popdist[i]
        
        result['gender_balance'] = random_state.beta(0.99 * 50.0, 0.01 * 50.0)
        
        return result
        
    @classmethod
    def export(cls, param_dict):

        result = {
            "populationDistribution": {
                "0": param_dict['population_distribution_0'],
                "1": param_dict['population_distribution_1'],
                "2": param_dict['population_distribution_2'],
                "3": param_dict['population_distribution_3'],
                "4": param_dict['population_distribution_4']
            },
            "populationAges": {
                "0": {
                  "min": 0,
                  "max": 14
                },
                "1": {
                  "min": 15,
                  "max": 24
                },
                "2": {
                  "min": 25,
                  "max": 54
                },
                "3": {
                  "min": 55,
                  "max": 64
                },
                "4": {
                  "min": 65,
                  "max": 90
                }
            },
            "genderBalance": param_dict['gender_balance']
        }
        return result
            
