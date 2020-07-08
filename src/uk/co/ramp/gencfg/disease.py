'''
Created on 2020/06/12

@author: rikiya
'''
from sklearn.utils import check_random_state
from collections import OrderedDict


class DiseaseSettings(object):
    '''
    Generate diseaseSettings.json
    '''
    
    def __init__(
            self,
            test_acc_mean=0.95,
            test_acc_concentration=5.0,
            random_infection_rate_mean=0.05,
            random_infection_rate_concentration=20.0,
            exposure_probability4unit_contact_mean=0.01,
            exposure_probability4unit_contact_concentration=20.0,
            random_state=None):
        self.random_state = check_random_state(random_state)
        self.test_acc_mean = test_acc_mean
        self.test_acc_concentration = test_acc_concentration
        self.random_infection_rate_mean = random_infection_rate_mean
        self.random_infection_rate_concentration = random_infection_rate_concentration
        self.exposure_probability4unit_contact_mean = exposure_probability4unit_contact_mean
        self.exposure_probability4unit_contact_concentration = exposure_probability4unit_contact_concentration
    
    def next(self):
        """
        Simulate a vector of parameters.
        Results are obtained as a dictionary.
        """
        random_state = self.random_state
        result = OrderedDict()
        result['time_latent_mean'] = random_state.randint(low=3, high=10)
        result['time_latent_max'] = result['time_latent_mean'] + random_state.randint(low=5, high=10)
        result['time_recovery_asymp_mean'] = random_state.randint(low=3, high=10)
        result['time_recovery_asymp_max'] = result['time_recovery_asymp_mean'] + random_state.randint(low=5, high=10)
        result['time_recovery_symp_mean'] = random_state.randint(low=3, high=10)
        result['time_recovery_symp_max'] = result['time_recovery_symp_mean'] + random_state.randint(low=5, high=10)
        result['time_recovery_syv_mean'] = random_state.randint(low=3, high=10)
        result['time_recovery_syv_max'] = result['time_recovery_syv_mean'] + random_state.randint(low=5, high=10)
        result['time_symptoms_onset_mean'] = random_state.randint(low=3, high=10)
        result['time_symptoms_onset_max'] = result['time_symptoms_onset_mean'] + random_state.randint(low=5, high=10)
        result['time_decline_mean'] = random_state.randint(low=3, high=10)
        result['time_decline_max'] = result['time_decline_mean'] + random_state.randint(low=5, high=10)
        result['time_death_mean'] = random_state.randint(low=3, high=10)
        result['time_death_max'] = result['time_death_mean'] + random_state.randint(low=5, high=10)
        result['time_test_administered_mean'] = random_state.randint(low=1, high=3)
        result['time_test_administered_max'] = result['time_test_administered_mean'] + random_state.randint(low=1, high=5)
        result['time_test_result_mean'] = random_state.randint(low=1, high=3)
        result['time_test_result_max'] = result['time_test_result_mean'] + random_state.randint(low=1, high=5)

        result['test_accuracy'] = random_state.beta(
            self.test_acc_concentration * self.test_acc_mean,
            self.test_acc_concentration * (1.0 - self.test_acc_mean)
            )
        
        result['exposure_threshold'] = 50.0 * random_state.lognormal(0.0, 1.0)
        result['exposure_probability4unit_contact'] = random_state.beta(
            self.exposure_probability4unit_contact_concentration * self.exposure_probability4unit_contact_mean,
            self.exposure_probability4unit_contact_concentration * (1.0 - self.exposure_probability4unit_contact_mean)
            )
        result['exposure_exponent'] = random_state.lognormal(0.0, 1.0)
        
        result['random_infection_rate'] = random_state.beta(
            self.random_infection_rate_concentration * self.random_infection_rate_mean,
            self.random_infection_rate_concentration * (1.0 - self.random_infection_rate_mean)
            )        
        
        return result
        
    @classmethod
    def export(cls, param_dict):
        
        result = {
            "timeLatent": {
                "mean": param_dict['time_latent_mean'],
                "max": param_dict['time_latent_max']
            },
            "timeRecoveryAsymp": {
                "mean": param_dict['time_recovery_asymp_mean'],
                "max": param_dict['time_recovery_asymp_max']
            },
            "timeRecoverySymp": {
                "mean": param_dict['time_recovery_symp_mean'],
                "max": param_dict['time_recovery_symp_max']
            },
            "timeRecoverySev": {
                "mean": param_dict['time_recovery_syv_mean'],
                "max": param_dict['time_recovery_syv_max']
            },
            "timeSymptomsOnset": {
                "mean": param_dict['time_symptoms_onset_mean'],
                "max": param_dict['time_symptoms_onset_max']
            },
            "timeDecline": {
                "mean": param_dict['time_decline_mean'],
                "max": param_dict['time_decline_max']
            },
            "timeDeath": {
                "mean": param_dict['time_death_mean'],
                "max": param_dict['time_death_max']
            },
            "timeTestAdministered": {
                "mean": param_dict['time_test_administered_mean'],
                "max": param_dict['time_test_administered_max']
            },
            "timeTestResult": {
                "mean": param_dict['time_test_result_mean'],
                "max": param_dict['time_test_result_max']
            },
            "testAccuracy": param_dict['test_accuracy'],
            "exposureThreshold": param_dict['exposure_threshold'],
            "exposureProbability4UnitContact": param_dict['exposure_probability4unit_contact'],
            "exposureExponent": param_dict['exposure_exponent'],
            "randomInfectionRate": param_dict['random_infection_rate'],
            "progressionDistribution": "EXPONENTIAL"
            }
        return result
            
