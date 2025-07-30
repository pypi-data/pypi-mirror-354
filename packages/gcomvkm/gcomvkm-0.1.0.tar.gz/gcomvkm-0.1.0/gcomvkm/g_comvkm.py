import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import time

class GCoMVKM:
    """
    Globally Collaborative Multi-View K-Means (G-CoMVKM) algorithm
    
    G-CoMVKM integrates a collaborative transfer learning framework with 
    entropy-regularized feature-view reduction, enabling dynamic elimination 
    of uninformative components. This method achieves clustering by balancing 
    local view importance and global consensus.
    """
    
    def __init__(self, n_clusters, gamma=0.5, theta=0.1, max_iter=100, tol=1e-4, verbose=True, random_state=None):
        """
        Initialize G-CoMVKM algorithm
        
        Parameters:
        -----------
        n_clusters : int
            Number of clusters to form
        gamma : float, default=0.5
            Exponent parameter to control the weights of V (typically in range [0,1])
        theta : float, default=0.1
            Coefficient parameter to control the weights of W (typically > 0)
        max_iter : int, default=100
            Maximum number of iterations
        tol : float, default=1e-4
            Convergence tolerance
        verbose : bool, default=True
            Whether to print progress information
        random_state : int, default=None
            Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.gamma = gamma
        self.theta = theta
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.random_state = random_state
        
        # Set random seed if provided
        if random_state is not None:
            np.random.seed(random_state)
            
        # Results to be stored during/after fitting
        self.view_weights_ = None
        self.feature_weights_ = None
        self.cluster_centers_ = None
        self.labels_ = None
        self.data_reduced_ = None
        self.memberships_ = None
        self.delta_ = None
        self.dimensions_ = None
        self.objective_values_ = None
        
    def fit(self, X):
        """
        Fit G-CoMVKM model to multi-view data
        
        Parameters:
        -----------
        X : list of numpy.ndarray
            List of data views, where each element is a data view of shape (n_samples, n_features)
            
        Returns:
        --------
        self : object
            Fitted estimator
        """
        # Validate input
        if not isinstance(X, list):
            raise ValueError("X must be a list of arrays, one per view")
        
        # Number of views
        s = len(X)
        
        # Number of data points (should be the same across all views)
        data_n = X[0].shape[0]
        
        # Check if all views have the same number of samples
        for h in range(s):
            if X[h].shape[0] != data_n:
                raise ValueError(f"All views must have the same number of samples, but view {h} has {X[h].shape[0]} samples")
        
        # Store original dimensions of each view
        dh = [X[h].shape[1] for h in range(s)]
        
        # Initialize cluster centers A
        A = []
        for h in range(s):
            # Use k-means for initialization
            kmeans = KMeans(n_clusters=self.n_clusters, n_init=10, random_state=self.random_state)
            kmeans.fit(X[h])
            A.append(kmeans.cluster_centers_)
        
        # Initialize view weights V (equal weights)
        V = np.ones(s) / s
        
        # Initialize feature weights W (equal weights for each view)
        W = []
        for h in range(s):
            W.append(np.ones(dh[h]) / dh[h])
        
        # Initialize delta (regularization parameter)
        delta = []
        for h in range(s):
            # Compute delta as in MATLAB implementation
            delta_left = X[h] / np.sum(X[h])
            delta_right = np.max(X[h], axis=0) - np.min(X[h], axis=0)
            delta.append(np.mean(delta_left / delta_right))
        
        # Store for use in the algorithm
        time_step = 1
        obj_values = np.zeros(self.max_iter)
        
        # Create figure for visualization of convergence if verbose
        if self.verbose:
            plt.figure(figsize=(10, 6))
            plt.grid(True)
            plt.xlabel('Iteration')
            plt.ylabel('Objective Function Value')
            plt.title('G-CoMVKM Convergence')
            
            print(f'G-CoMVKM: Starting the algorithm with {s} views, {self.n_clusters} clusters')
            print(f'G-CoMVKM: Data size: {data_n} samples')
            print(f'G-CoMVKM: Parameters - Gamma: {self.gamma:.4f}, Theta: {self.theta:.4f}\n')
        
        # Start iteration
        while time_step <= self.max_iter:
            if self.verbose:
                print(f'\n============= G-CoMVKM Iteration {time_step}/{self.max_iter} =============')
            
            # Step 1: Compute the memberships U
            D = []
            for h in range(s):
                # Compute weighted distances
                WVdel = W[h] * delta[h] * V[h]
                D_h = np.zeros((data_n, self.n_clusters))
                
                for k in range(self.n_clusters):
                    # Compute squared distances
                    diff = X[h] - A[h][k]
                    D_h[:, k] = np.sum(diff**2 * WVdel, axis=1)
                
                D.append(D_h)
            
            # Compute average distance
            D_average = np.zeros((data_n, self.n_clusters))
            for h in range(s):
                D_average += D[h]
            
            D_average = (1 - self.gamma * data_n) * D_average
            
            # Update cluster assignments based on distances
            U = []
            Cluster_elem = []
            
            for h in range(s):
                U_h = np.zeros((data_n, self.n_clusters))
                A_dist = (self.gamma * data_n) * D[h] - D_average
                Update_cluster_elem = np.argmin(A_dist, axis=1)
                Cluster_elem.append(Update_cluster_elem)
                
                # Create binary membership matrix
                for i in range(data_n):
                    U_h[i, Cluster_elem[h][i]] = 1
                
                U.append(U_h)
            
            # Step 2: Update the cluster centers A
            U_mix = np.zeros((data_n, self.n_clusters))
            for h in range(s):
                U_mix += U[h]
            
            U_mean = []
            for h in range(s):
                U_mean.append((1 - self.gamma) * U[h] + self.gamma * U_mix)
            
            for h in range(s):
                for k in range(self.n_clusters):
                    # Update cluster centers
                    if np.sum(U_mean[h][:, k]) > 0:
                        A[h][k] = X[h].T @ U_mean[h][:, k] / np.sum(U_mean[h][:, k])
            
            # Step 3: Update the h-th view of weighted feature W
            B = []
            for h in range(s):
                B_h = np.zeros(dh[h])
                
                for i in range(data_n):
                    for k in range(self.n_clusters):
                        if U_mean[h][i, k] != 0:
                            diff_sq = (X[h][i] - A[h][k])**2
                            B_h += ((dh[h] + data_n) / data_n) * V[h]**self.theta * U_mean[h][i, k] * diff_sq * delta[h]
                
                # Compute B using entropy regularization
                B_h = (1 / delta[h]) * np.exp((-B_h - self.theta) / self.theta)
                B.append(B_h)
            
            for h in range(s):
                # Normalize feature weights
                W[h] = B[h] / np.sum(B[h])
            
            # Step 4: Discard irrelevant feature-view component
            d_new = np.zeros(s, dtype=int)
            X_new = []
            W_new = []
            delta_new = []
            A_new = []
            
            for h in range(s):
                # Get current view data
                data_h = X[h]
                W_h = W[h]
                delta_h = delta[h]
                A_h = A[h]
                d_h = dh[h]
                
                # Get dimensions of current view
                d = data_h.shape[1]
                
                # Set threshold for feature selection
                th_h = 1 / sum(dh)  # For artificial datasets
                
                # Find unimportant features
                exclude_idx = np.where(W_h < th_h)[0]
                
                # Step 5: Adjusting variables W, delta, A, X, and dh
                # Adjust feature weights W
                W_adj = np.delete(W_h, exclude_idx)
                W_adj = W_adj / np.sum(W_adj)
                
                # Adjust delta
                delta_adj = np.delete(delta_h, exclude_idx)
                
                # Adjust cluster centers A
                A_adj = np.delete(A_h, exclude_idx, axis=1)
                
                # Adjust dimensionality
                d_h_new = d - len(exclude_idx)
                
                # Adjust data-view points X
                data_h_new = np.delete(data_h, exclude_idx, axis=1)
                
                # Store adjusted values
                d_new[h] = d_h_new
                X_new.append(data_h_new)
                W_new.append(W_adj)
                delta_new.append(delta_adj)
                A_new.append(A_adj)
            
            # Update variables for next iteration
            X = X_new
            W = W_new
            delta = delta_new
            A = A_new
            dh = d_new
            
            # Step 6: Update the Weighted view V
            # Update weighted Euclidean distance D
            D_new = []
            for h in range(s):
                WVdel_new = W[h] * delta[h]
                D_h_new = np.zeros((data_n, self.n_clusters))
                
                for k in range(self.n_clusters):
                    diff = X[h] - A[h][k]
                    D_h_new[:, k] = np.sum(diff**2 * WVdel_new, axis=1)
                
                D_new.append(D_h_new)
            
            D = D_new
            
            # Compute weights for each view
            U_mean_right = []
            for h in range(s):
                U_mean_right.append(U_mix - U[h])
            
            DV_average = np.zeros((data_n, self.n_clusters))
            for h in range(s):
                DV_average += D[h]
            
            DV_average = (self.gamma * self.theta) * DV_average
            
            E = np.zeros(s)
            for h in range(s):
                Et_left = np.sum(U_mean[h] * D[h])
                Et_right = np.sum(U_mean_right[h] * DV_average)
                E[h] = (Et_left + Et_right)**(-1 / (self.gamma - 1))
            
            # Normalize view weights
            V = E / np.sum(E)
            
            # Compute objective function value
            term1 = np.zeros(s)
            for h in range(s):
                term1[h] += np.sum(U[h] * D[h])
                term1[h] = term1[h] * V[h]**self.gamma / dh[h]
            
            term1_sum = np.sum(term1)
            
            term2 = np.zeros(s)
            for h in range(s):
                for hh in range(s):
                    term2[h] += np.sum(np.abs(V[h]**2 * (U_mean[h] * D[h] - U_mean[hh] * D[hh])))
            
            term2_sum = np.sum(term2)
            
            term3 = 0
            for h in range(s):
                # Add small epsilon to avoid log(0)
                term3 += np.abs(np.sum(W[h] * np.log(delta[h] * W[h] + 1e-10)))
            
            term3 = self.theta * term3
            
            obj_values[time_step-1] = term1_sum + term2_sum + term3
            
            # Update convergence plot if verbose
            if self.verbose and time_step > 1:
                plt.plot(range(1, time_step+1), obj_values[:time_step], 'b-o')
                plt.pause(0.01)
                
                improvement = np.abs(obj_values[time_step-1] - obj_values[time_step-2])
                print(f'G-CoMVKM: Iteration {time_step}, Objective = {obj_values[time_step-1]:.6f}, Improvement = {improvement:.6f}')
                
                # Check convergence
                if improvement <= self.tol:
                    print('\n==========================================')
                    print(f'G-CoMVKM: Converged after {time_step} iterations!')
                    print(f'Final objective value: {obj_values[time_step-1]:.6f}')
                    print('==========================================\n')
                    break
            elif self.verbose:
                print(f'G-CoMVKM: Iteration {time_step}, Objective = {obj_values[time_step-1]:.6f}')
            
            # Display summary of feature reduction
            if self.verbose:
                print(f'Feature dimensions after iteration {time_step}: {dh}')
                print(f'View weights after iteration {time_step}: {V}')
            
            time_step += 1
        
        # Store final results
        self.view_weights_ = V
        self.feature_weights_ = W
        self.cluster_centers_ = A
        self.data_reduced_ = X
        self.memberships_ = U
        self.delta_ = delta
        self.dimensions_ = dh
        self.objective_values_ = obj_values[:time_step-1]
        
        # Determine final cluster assignments by fusing memberships from different views
        self._determine_final_clusters()
        
        return self
    
    def _determine_final_clusters(self):
        """
        Determine final cluster assignments by fusing memberships from different views
        """
        if self.memberships_ is None or self.view_weights_ is None:
            raise ValueError("Model has not been fitted yet")
        
        # Combine memberships from different views based on view weights
        UU = np.zeros_like(self.memberships_[0])
        for h in range(len(self.memberships_)):
            UU += self.memberships_[h] * self.view_weights_[h]
        
        # Get final cluster assignments
        self.labels_ = np.argmax(UU, axis=1)
        
        return self.labels_
    
    def predict(self, X):
        """
        Predict cluster labels for new data points
        
        Parameters:
        -----------
        X : list of numpy.ndarray
            List of data views for new data points
            
        Returns:
        --------
        labels : numpy.ndarray
            Predicted cluster labels
        """
        if self.cluster_centers_ is None:
            raise ValueError("Model has not been fitted yet")
        
        # Validate input
        if not isinstance(X, list) or len(X) != len(self.cluster_centers_):
            raise ValueError(f"X must be a list of {len(self.cluster_centers_)} arrays, one per view")
        
        # Number of views
        s = len(X)
        
        # Number of data points
        data_n = X[0].shape[0]
        
        # Compute distances to cluster centers for each view
        D = []
        for h in range(s):
            # Compute weighted distances
            WVdel = self.feature_weights_[h] * self.delta_[h] * self.view_weights_[h]
            D_h = np.zeros((data_n, self.n_clusters))
            
            for k in range(self.n_clusters):
                # Compute squared distances
                diff = X[h] - self.cluster_centers_[h][k]
                D_h[:, k] = np.sum(diff**2 * WVdel, axis=1)
            
            D.append(D_h)
        
        # Compute weighted average of distances across views
        D_weighted = np.zeros((data_n, self.n_clusters))
        for h in range(s):
            D_weighted += D[h] * self.view_weights_[h]
        
        # Assign to closest cluster
        labels = np.argmin(D_weighted, axis=1)
        
        return labels
