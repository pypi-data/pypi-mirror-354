import numpy as np
import scipy.io as sio
import os
import importlib.resources as pkg_resources

def load_synthetic_data(file_path=None):
    """
    Load the synthetic 2V2D2C dataset (2 Views, 2 Dimensions, 2 Clusters)
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the data_synthetic.mat file. If None, will use the dataset included with the package.
    
    Returns:
    --------
    X : list of numpy.ndarray
        A list of data views
    label : numpy.ndarray
        The ground truth labels
    """
    if file_path is None:
        try:
            # First, try to use the dataset included with the package
            from .. import data
            with pkg_resources.path(data, 'data_synthetic.mat') as data_path:
                file_path = str(data_path)
        except (ImportError, ModuleNotFoundError):
            # Fallback to default location for development
            file_path = os.path.expanduser('~/Desktop/G-CoMVKM/dataset/data_synthetic.mat')
        
        print(f"Looking for dataset at: {file_path}")
        if not os.path.exists(file_path):
            print(f"Warning: Dataset not found at {file_path}")
            print("Please verify the dataset path.")
    
    # Load the MATLAB .mat file
    try:
        mat_data = sio.loadmat(file_path)
        
        # Extract data and labels
        data = mat_data.get('data')
        label = mat_data.get('label').flatten()
        
        # Convert to list of numpy arrays if it's a cell array in MATLAB
        X = []
        for i in range(data.shape[1]):
            X.append(data[0, i])
        
        print(f"Successfully loaded {len(X)} views from {file_path}")
        print(f"View 1 shape: {X[0].shape}, View 2 shape: {X[1].shape}")
        print(f"Labels shape: {label.shape}, Unique labels: {np.unique(label)}")
        
        return X, label
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None
