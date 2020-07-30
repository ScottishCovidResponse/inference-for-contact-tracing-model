'''
Created on 2020/06/12

@author: rikiya
'''
from copy import deepcopy
from sklearn.utils import check_random_state
from collections import OrderedDict


class IsolationPolicies(object):
    '''
    Generate isolationPolicies.json
    '''

    _virus_statuses = [
        'symptomatic',
        'severely_symptomatic']
    _alert_statuses = [
        'alerted',
        'requested_test',
        'awaiting_result',
        'tested_positive',
        'tested_negative']
    
    def __init__(
            self,
            simplified=True,
            random_state=None):
        '''
        simplified : whether to search in a lower-dimensional simplified policy space
        '''
        self.simplified = simplified
        self.random_state = check_random_state(random_state)
    
    def next(self):
        """
        Simulate a vector of parameters.
        Results are obtained as a dictionary.
        """
        random_state = self.random_state
        result = OrderedDict()
        
        result['alert_policy_prioritised'] = random_state.choice([0, 1])
        result['no_isolation_tested_negative'] = random_state.choice([0, 1])
        if self.simplified:
            is_absolute = random_state.choice([0, 1]) 
            time_mean = random_state.randint(low=1, high=14)
            for sta in IsolationPolicies._virus_statuses + IsolationPolicies._alert_statuses:
                result['{}_isolation_time_mean'.format(sta)] = time_mean
                result['{}_start_of_isolation_is_absolute'.format(sta)] = is_absolute
        else:
            for sta in IsolationPolicies._virus_statuses + IsolationPolicies._alert_statuses:
                result['{}_isolation_time_mean'.format(sta)] = random_state.randint(low=1, high=14)
                result['{}_start_of_isolation_is_absolute'.format(sta)] = random_state.choice([0, 1])
        
        return result
        
    @classmethod
    def export(cls, param_dict):
        result = {}
        result['globalIsolationPolicies'] = []
        result['defaultPolicy'] = {
            "id": "Default Policy",
            "isolationProbabilityDistribution": {
                "type": "FLAT",
                "mean": 0,
                "max": 0
            },
            "priority": 0
        }
        result['isolationProbabilityDistributionThreshold'] = {
            "type": "LINEAR",
            "mean": 50,
            "max": 100
        }

        virus_lst = []
        alert_lst = []
        for key, val in param_dict.items():
            if 'isolation_time_mean' in key:
                sta = key.replace('_isolation_time_mean', '')
                entry = {
                        'isolationProperty': {
                            'id': '{} Policy'.format(sta.title().replace('_', ' ')),
                            'isolationProbabilityDistribution': {
                              'type': 'FLAT',
                              'mean': 100,
                              'max': 100
                            },
                            'isolationTimeDistribution': {
                              'type': 'FLAT',
                              'mean': val,
                              'max': val
                            },
                            'startOfIsolationTime': "ABSOLUTE" if param_dict['{}_start_of_isolation_is_absolute'.format(sta)] == 1 else 'CONTACT_TIME',
                            }
                        }
                
                if sta in IsolationPolicies._virus_statuses:
                    entry['virusStatus'] = sta.upper()
                    entry['isolationProperty']['priority'] = 2
                    virus_lst.append(entry)
                elif sta in IsolationPolicies._alert_statuses:
                    if sta == 'tested_negative' and param_dict['no_isolation_tested_negative'] > 0:
                        continue
                    entry['alertStatus'] = sta.upper()
                    entry['isolationProperty']['priority'] = 3 if param_dict['alert_policy_prioritised'] else 1
                    alert_lst.append(entry)
                    
        result['virusStatusPolicies'] = virus_lst
        result['alertStatusPolicies'] = alert_lst

        return result
            
