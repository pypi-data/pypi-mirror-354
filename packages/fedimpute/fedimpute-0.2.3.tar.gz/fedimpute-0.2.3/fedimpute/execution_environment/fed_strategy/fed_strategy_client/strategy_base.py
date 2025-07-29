from abc import ABC, abstractmethod

import numpy as np
import torch
from typing import Tuple
from ...imputation.base.base_imputer import BaseNNImputer


class StrategyBaseClient(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def set_parameters(self, updated_model_params: dict, local_model: torch.nn.Module, params: dict):
        """
        Set parameters global model to local model
        :param updated_model_params: received updated model parameters
        :param local_model: local model
        :param params: config params
        :return: None
        """
        pass

    @abstractmethod
    def get_parameters(self, local_model: torch.nn.Module, params: dict) -> dict:
        """
        Get parameters from local model
        :param local_model: local model
        :param params: config params
        :return: parameters dict
        """
        pass

    @abstractmethod
    def pre_training_setup(self, params: dict) -> dict:
        """
        Local training pre setup
        :param params: config params
        :return: setup results dict
        """
        pass

    @abstractmethod
    def post_training_setup(self, params: dict) -> dict:
        """
        Local training post setup
        :param params: config params
        :return: setup results dict
        """
        pass

    @abstractmethod
    def train_local_nn_model(
            self, imputer: BaseNNImputer, training_params: dict, X_train_imp: np.ndarray,
            y_train: np.ndarray, X_train_mask: np.ndarray
    ) -> Tuple[dict, dict]:
        """
        Train local nn model
        :param imputer: imputer
        :param training_params: training params
        :param X_train_imp: Imputed training data
        :param y_train: y training data
        :param X_train_mask: mask data
        :return: local model and training results dict
        """
        pass

    @abstractmethod
    def get_fit_res(self, local_model: torch.nn.Module, params: dict) -> dict:
        pass
