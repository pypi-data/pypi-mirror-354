import pandas as pd
from sports_prediction_framework.utils.MLFlowTracker import MLFlowTracker
import inspect
import numpy as np
from sports_prediction_framework.datawrapper.DataWrapper import *


class Model:
    """
    Base class for a machine learning model.

    Attributes
    ----------
    in_cols : list
        List of input column names used by the model.
    model : object
        The underlying model object (e.g., sklearn, PyTorch, etc.).
    """

    in_cols = []
    model = None

    def __init__(self, **kwargs):
        """
        Initialize the model and capture initialization parameters.

        Parameters
        ----------
        **kwargs : dict
            Arbitrary keyword arguments passed during model initialization.
        """
        self._init_params = self._get_init_params()

    def fit(self, features: pd.DataFrame, labels: pd.DataFrame):
        """
        Train the model using provided features and labels.

        Parameters
        ----------
        features : pd.DataFrame
            Input features for training.
        labels : pd.DataFrame
            Target labels for training.

        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions from the model for given input data.

        Parameters
        ----------
        data : pd.DataFrame
            Input features for prediction.

        Returns
        -------
        np.ndarray
            Model predictions.

        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    def set_parameters_from_wrapper(self, wrapper: DataWrapper):
        """
        Set model parameters based on the provided DataWrapper.

        Parameters
        ----------
        wrapper : DataWrapper
            A wrapper containing relevant configuration or metadata.
        """
        pass

    def reset_state(self):
        """
        Reset the internal state of the model, if applicable.

        Raises
        ------
        NotImplementedError
            This method must be implemented by subclasses.
        """
        raise NotImplementedError

    def set_params(self, params: dict):
        """
        Set parameters on the underlying model object.

        Parameters
        ----------
        params : dict
            Dictionary of parameter names and values to set.
        """
        for key, value in params.items():
            setattr(self.model, key, value)

    def _get_init_params(self) -> dict:
        """
        Retrieve the constructor parameters of the model instance.

        Uses introspection to get arguments passed to __init__, except 'self'.

        Returns
        -------
        dict
            Dictionary of parameter names and values.
        """
        frame = inspect.currentframe()
        init_args = inspect.getargvalues(frame.f_back)
        params = {k: v for k, v in init_args.locals.items() if k != 'self'}
        return params

    def log_params(self) -> None:
        """
        Log the model's constructor parameters to MLflow using MLFlowTracker.

        Raises
        ------
        RuntimeError
            If MLFlowTracker has no active run.
        """
        MLFlowTracker.log_params(self._init_params)
