'''
Created on 2020/06/12

@author: rikiya
'''
from copy import deepcopy
from sklearn.utils import check_random_state
from collections import OrderedDict


class TracingPolicies(object):
    '''
    Generate tracingPolicies.json
    '''

    _virus_statuses = [
        'symptomatic',
        'severely_symptomatic']
    
    def __init__(
            self,
            random_state=None):
        self.random_state = check_random_state(random_state)
    
    def next(self):
        """
        Simulate a vector of parameters.
        Results are obtained as a dictionary.
        """
        random_state = self.random_state
        result = OrderedDict()
        
        result['alert_by_tested_positive'] = random_state.choice([0, 1])
        for sta in TracingPolicies._virus_statuses:
            result['{}_recent_contacts_lookbacktime'.format(sta)] = random_state.randint(low=1, high=14)
        
        return result
        
    @classmethod
    def export(cls, param_dict):
        result = {}
        result['description'] = 'Tracing based on Symptomatic individuals reporting with single level tracing'
        lst = []
        for key, val in param_dict.items():
            if 'recent_contacts_lookbacktime' in key:
                sta = key.replace('_recent_contacts_lookbacktime', '')
                entry = {
                    "reporterAlertStatus": "TESTED_NEGATIVE" if param_dict['alert_by_tested_positive'] > 0 else "NONE",
                    "reporterVirusStatus": sta.upper(),
                    "recentContactsLookBackTime": param_dict['{}_recent_contacts_lookbacktime'.format(sta)],
                    "timeDelayPerTraceLink": {
                        "mean": 1,
                        "max": 1,
                        "type": "FLAT"
                        },
                    "probabilitySkippingTraceLink": {
                        "mean": 10,
                        "max": 10,
                        "type": "FLAT"
                        }
                    }
                lst.append(entry)
        result['policies'] = lst
        result['noOfTracingLevels'] = 1
        result['probabilitySkippingTraceLinkThreshold'] = {
            "mean": 50,
            "max": 100,
            "type": "LINEAR"
        }
        
        return result
            
