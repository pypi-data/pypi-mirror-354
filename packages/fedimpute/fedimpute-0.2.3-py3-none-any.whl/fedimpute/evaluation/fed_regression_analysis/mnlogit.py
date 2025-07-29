import numpy as np
from scipy.special import expit
from typing import List
from statsmodels.base.model import LikelihoodModelResults
from statsmodels.discrete.discrete_model import LogitResults, BinaryResultsWrapper, Logit
import statsmodels.api as sm

def distributed_logistic_regression(
        X_parts, y_parts, max_iter=100, tol=1e-6
):
    """
    Distributed logistic regression using Newton-Raphson
    
    Parameters:
    -----------
    X_parts : list of arrays
        Partitioned feature matrices
    y_parts : list of arrays
        Partitioned target vectors
    
    Returns:
    --------
    beta : array
        Coefficients
    """
    # Get dimensions from first partition
    n_features = X_parts[0].shape[1]
    
    # Initialize parameters
    beta = np.zeros(n_features)
    
    for iteration in range(max_iter):
        # Initialize aggregated gradient and hessian
        total_gradient = np.zeros(n_features)
        total_hessian = np.zeros((n_features, n_features))
        
        # Process each partition
        for X_part, y_part in zip(X_parts, y_parts):
            # Calculate predicted probabilities
            z = X_part.dot(beta)
            p = expit(z)
            
            # Calculate gradient for this partition
            gradient = X_part.T.dot(y_part - p)
            
            # Calculate Hessian for this partition
            W = np.diag(p * (1 - p))
            hessian = -X_part.T.dot(W).dot(X_part)
            
            # Aggregate
            total_gradient += gradient
            total_hessian += hessian
        
        # Update parameters using Newton-Raphson step
        try:
            beta_update = np.linalg.solve(total_hessian, total_gradient)
        except np.linalg.LinAlgError:
            beta_update = np.linalg.pinv(total_hessian).dot(total_gradient)
        
        beta -= beta_update
        
        # Check convergence
        if np.linalg.norm(beta_update) < tol:
            break
    
    return beta, hessian


def eval_fed_reg_logit(
    X_train_imps: List[np.ndarray], 
    y_trains: List[np.ndarray]
):
    N = X_train_imps[0].shape[0]
    # Add constant term (intercept) to each client's data
    X_train_imps = [
        np.concatenate([np.ones((X_train_imp.shape[0], 1)), X_train_imp.copy()], axis=1).copy() 
        for X_train_imp in X_train_imps
    ]
    beta, hessian = distributed_logistic_regression(X_train_imps, y_trains)
    normalized_cov_params = np.linalg.inv(-hessian)/N

    X = np.concatenate(X_train_imps, axis=0)
    y = np.concatenate(y_trains, axis=0)
    X_with_const = sm.add_constant(X)
    logit_model = Logit(y, X_with_const)

    mlefit = LikelihoodModelResults(logit_model, beta, normalized_cov_params, scale=1.)
    mlefit.mle_retvals = {'converged': True}
    mlefit.mle_settings = {'optimizer': 'newton'}
    discretefit = LogitResults(logit_model, mlefit)
    discretefit_wrapper = BinaryResultsWrapper(discretefit)
    return discretefit_wrapper


