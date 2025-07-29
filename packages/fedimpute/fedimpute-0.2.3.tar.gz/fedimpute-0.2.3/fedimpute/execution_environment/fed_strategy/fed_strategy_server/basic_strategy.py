from typing import List, Tuple, Union, OrderedDict
from copy import deepcopy
import numpy as np

# TODO: base class for all strategies for consistent APIs
from abc import ABC, abstractmethod

class RawBaseStrategyServer(ABC):

    def __init__(self, initial_impute: str, name: str, fine_tune_epochs: int = 0):
        self.initial_impute = initial_impute
        self.name = name
        self.fine_tune_epochs = fine_tune_epochs
        self.global_model_params_dict = None

    @abstractmethod
    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        pass

    @abstractmethod
    def fit_instruction(self, params_list: List[dict]) -> List[dict]:
        pass
    
    @abstractmethod
    def update_instruction(self, params: dict) -> dict:
        pass

    @abstractmethod
    def get_global_model_params(self) -> Union[OrderedDict, None]:
        pass

class CentralStrategyServer(RawBaseStrategyServer):

    def __init__(self):
        super().__init__('central', 'central', 0)

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """
        central_model_params = local_model_parameters[-1]

        agg_model_parameters = [deepcopy(central_model_params) for _ in range(len(local_model_parameters))]
        agg_res = {}
        
        # update global model parameters
        self.global_model_params_dict = central_model_params

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:
        fit_instructions = []
        for _ in range(len(params_list) - 1):
            fit_instructions.append({'fit_model': False})

        fit_instructions.append({'fit_model': True})

        return fit_instructions

    def update_instruction(self, params: dict) -> dict:

        return {}
    
    def get_global_model_params(self) -> Union[OrderedDict, None]:
        return self.global_model_params_dict
    
    def __str__(self):
        return f"Central Strategy Server"

    def __repr__(self):
        return f"Central Strategy Server"


class LocalStrategyServer(RawBaseStrategyServer):

    def __init__(self):
        super().__init__('local', 'local', 0)

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[Union[OrderedDict, None]], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """
        return [None for _ in range(len(local_model_parameters))], {}


    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:
        return {}
    
    def get_global_model_params(self) -> Union[OrderedDict, None]:
        return None
    
    def __str__(self):
        return f"Local Strategy Server"
    
    def __repr__(self):
        return f"Local Strategy Server"


class SimpleAvgStrategyServer(RawBaseStrategyServer):

    def __init__(self, initial_impute: str, name: str, fine_tune_epochs: int = 0):
        super().__init__(initial_impute, name, fine_tune_epochs)

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """

        # federated averaging implementation
        averaged_model_state_dict = OrderedDict([])  # global parameters
        sample_sizes = [item['sample_size'] for item in fit_res]
        normalized_coefficient = [size / sum(sample_sizes) for size in sample_sizes]

        for it, local_model_state_dict in enumerate(local_model_parameters):
            for key in local_model_state_dict.keys():
                if it == 0:
                    averaged_model_state_dict[key] = normalized_coefficient[it] * local_model_state_dict[key]
                else:
                    averaged_model_state_dict[key] += normalized_coefficient[it] * local_model_state_dict[key]

        # copy parameters for each client
        agg_model_parameters = [deepcopy(averaged_model_state_dict) for _ in range(len(local_model_parameters))]
        agg_res = {}
        
        # update global model parameters
        self.global_model_params_dict = averaged_model_state_dict

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:

        return {}
    
    def get_global_model_params(self) -> Union[OrderedDict, None]:
        return self.global_model_params_dict
    
    def __str__(self):
        return f"Simple Average Strategy Server"
    
    def __repr__(self):
        return f"Simple Average Strategy Server"

class FedMICEStrategyServer(SimpleAvgStrategyServer):

    def __init__(self):
        super().__init__('fedavg', 'fedmice', 0)
        
    def __str__(self):
        return f"FedMICE Strategy Server"
    
    def __repr__(self):
        return f"FedMICE Strategy Server"
        
class FedEMStrategyServer(SimpleAvgStrategyServer):

    def __init__(self):
        super().__init__('fedavg', 'fedem', 0)
        
    def __str__(self):
        return f"FedEM Strategy Server"
    
    def __repr__(self):
        return f"FedEM Strategy Server"
        
class FedMeanStrategyServer(SimpleAvgStrategyServer):

    def __init__(self):
        super().__init__('fedavg', 'fedmean', 0)

    def __str__(self):
        return f"FedMean Strategy Server"
    
    def __repr__(self):
        return f"FedMean Strategy Server"

class FedTreeStrategyServer(RawBaseStrategyServer):

    def __init__(self):
        super().__init__('fedavg', 'fedtree', 0)

    def aggregate_parameters(
            self, local_model_parameters: List[OrderedDict], fit_res: List[dict], params: dict, *args, **kwargs
    ) -> Tuple[List[OrderedDict], dict]:
        """
        Aggregate local models
        :param local_model_parameters: List of local model parameters
        :param fit_res: List of fit results of local training
            - sample_size: int - number of samples used for training
        :param params: dictionary for information
        :param args: other params list
        :param kwargs: other params dict
        :return: List of aggregated model parameters, dict of aggregated results
        """

        # federated tree sampling strategy
        sample_sizes = [item['sample_size'] for item in fit_res]
        sample_fracs = [size / sum(sample_sizes) for size in sample_sizes]

        np.random.seed(1203401)
        # all local trees
        global_trees = []
        for local_model_state_dict, sample_frac in zip(local_model_parameters, sample_fracs):
            local_trees = local_model_state_dict['estimators']
            sampled_trees = np.random.choice(local_trees, int(len(local_trees) * sample_frac), replace=False)
            global_trees.extend(sampled_trees)

        global_params = OrderedDict({"estimators": global_trees})
        # copy parameters for each client
        agg_model_parameters = [deepcopy(global_params) for _ in range(len(local_model_parameters))]
        agg_res = {}
        
        # update global model parameters
        self.global_model_params_dict = global_params

        return agg_model_parameters, agg_res

    def fit_instruction(self, params_list: List[dict]) -> List[dict]:

        return [{'fit_model': True} for _ in range(len(params_list))]

    def update_instruction(self, params: dict) -> dict:

        return {}
    
    def get_global_model_params(self) -> Union[OrderedDict, None]:
        return self.global_model_params_dict
    
    def __str__(self):
        return f"FedTree Strategy Server"
    
    def __repr__(self):
        return f"FedTree Strategy Server"

