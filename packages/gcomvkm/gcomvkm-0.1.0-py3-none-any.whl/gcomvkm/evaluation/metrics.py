import numpy as np
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

def nmi(labels_true, labels_pred):
    """
    Normalized Mutual Information between two clusterings.
    
    Parameters:
    -----------
    labels_true : array-like
        Ground truth class labels
    labels_pred : array-like
        Cluster labels to evaluate
        
    Returns:
    --------
    nmi_score : float
        Score between 0.0 and 1.0. 1.0 represents perfect correlation
    """
    return normalized_mutual_info_score(labels_true, labels_pred)

def rand_index(labels_true, labels_pred):
    """
    Rand Index between two clusterings.
    
    Parameters:
    -----------
    labels_true : array-like
        Ground truth class labels
    labels_pred : array-like
        Cluster labels to evaluate
        
    Returns:
    --------
    ri_score : float
        Score between 0.0 and 1.0. 1.0 represents perfect agreement
    """
    from sklearn.metrics.cluster import contingency_matrix
    
    # Calculate contingency matrix
    c = contingency_matrix(labels_true, labels_pred)
    
    # Calculate Rand Index
    n = len(labels_true)
    sum_comb_c = sum(sum(np.array([nij * (nij - 1) for nij in c.flatten()]) / 2))
    sum_comb_a = sum(sum(np.array([ni * (ni - 1) for ni in np.sum(c, axis=1)]) / 2))
    sum_comb_b = sum(sum(np.array([nj * (nj - 1) for nj in np.sum(c, axis=0)]) / 2))
    sum_comb = n * (n - 1) / 2
    
    # Rand Index
    return (sum_comb + 2 * sum_comb_c - sum_comb_a - sum_comb_b) / sum_comb

def adjusted_rand_index(labels_true, labels_pred):
    """
    Adjusted Rand Index between two clusterings.
    
    Parameters:
    -----------
    labels_true : array-like
        Ground truth class labels
    labels_pred : array-like
        Cluster labels to evaluate
        
    Returns:
    --------
    ari_score : float
        Score between -1.0 and 1.0. 1.0 represents perfect agreement
    """
    return adjusted_rand_score(labels_true, labels_pred)

def error_rate(labels_true, labels_pred, n_clusters):
    """
    Calculate error rate (percentage of misclassified samples).
    
    Parameters:
    -----------
    labels_true : array-like
        Ground truth class labels
    labels_pred : array-like
        Cluster labels to evaluate
    n_clusters : int
        Number of clusters
        
    Returns:
    --------
    error_count : int
        Number of misclassified samples
    """
    from scipy.optimize import linear_sum_assignment
    from sklearn.metrics.cluster import contingency_matrix
    
    # Create contingency matrix
    c = contingency_matrix(labels_true, labels_pred)
    
    # Use Hungarian algorithm to find optimal mapping
    row_ind, col_ind = linear_sum_assignment(-c)
    
    # Count correctly assigned samples
    correct_count = c[row_ind, col_ind].sum()
    
    # Return error count
    return len(labels_true) - correct_count
