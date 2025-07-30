import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import time
import os
import sys

from .g_comvkm import GCoMVKM
from .utils.data_loader import load_synthetic_data
from .evaluation.metrics import nmi, rand_index, adjusted_rand_index, error_rate

def run_demo():
    """
    Demo script for G-CoMVKM algorithm on 2V2D2C dataset
    """
    print("=" * 70)
    print("Demo: G-CoMVKM algorithm on 2V2D2C dataset (2 Views, 2 Dimensions, 2 Clusters)")
    print("=" * 70)
    
    # Load the synthetic data
    data_name = 'Numerical Data 2V2D2C'
    print(f'Loading {data_name}...')
    X, label = load_synthetic_data()
    
    if X is None or label is None:
        print("Error: Could not load the dataset")
        return
    
    # Parameters setup
    c = int(np.max(label))  # Number of clusters
    points_view = len(X)    # Number of views
    points_n = X[0].shape[0]  # Number of data points
    
    # Get dimensions of each view
    dh = [X[h].shape[1] for h in range(points_view)]
    
    # Algorithm parameters
    gamma = 5.0  # Parameter 1 (Gamma)
    theta = 4.0  # Parameter 2 (Theta)
    
    # Experimental setup
    num_seeds = 50  # Number of different random seeds to try
    seeds = np.random.randint(2**13-1, size=num_seeds)  # Random seeds generator
    result = np.zeros((num_seeds, 3))  # Array to store AR, RI, NMI results
    
    print(f"\nParameters:")
    print(f"  - Number of clusters: {c}")
    print(f"  - Number of views: {points_view}")
    print(f"  - Data dimensions: {dh}")
    print(f"  - Gamma parameter: {gamma}")
    print(f"  - Theta parameter: {theta}")
    print(f"  - Number of random seeds: {num_seeds}")
    
    # Arrays to store best results
    best_AR = 0
    best_RI = 0
    best_NMI = 0
    best_model = None
    best_index = None
    best_time = 0
    
    print("\nRunning multiple experiments with different initializations...")
    
    for time_idx in range(num_seeds):
        print(f"\n----- Experiment {time_idx+1}/{num_seeds} -----")
        
        # Set random seed for reproducibility
        np.random.seed(seeds[time_idx])
        
        # Run G-CoMVKM algorithm
        print(f'Running G-CoMVKM for seed {seeds[time_idx]}...')
        start_time = time.time()
        
        # Create and fit the model
        model = GCoMVKM(
            n_clusters=c,
            gamma=gamma,
            theta=theta,
            max_iter=100,
            tol=1e-4,
            verbose=False,
            random_state=seeds[time_idx]
        )
        
        model.fit(X)
        
        elapsed_time = time.time() - start_time
        
        # Get the cluster assignments
        index = model.labels_
        
        # Calculate the clustering performance evaluation
        NMI = nmi(label, index)
        RI = rand_index(label, index)
        AR = 1 - error_rate(label, index, c) / points_n
        
        # Display metrics for current run
        print(f'Run {time_idx+1} - AR: {AR:.4f}, RI: {RI:.4f}, NMI: {NMI:.4f} (Time: {elapsed_time:.2f} sec)')
        
        # Save results
        result[time_idx, 0] = AR
        result[time_idx, 1] = RI
        result[time_idx, 2] = NMI
        
        # Update best results if current run is better
        if AR > best_AR:
            best_AR = AR
            best_RI = RI
            best_NMI = NMI
            best_model = model
            best_index = index
            best_time = time_idx + 1
    
    # Compute statistical results
    min_result = np.min(result, axis=0)   # Minimum values of clustering metrics
    mean_result = np.mean(result, axis=0)  # Mean values of clustering metrics
    max_result = np.max(result, axis=0)   # Maximum values of clustering metrics
    std_result = np.std(result, axis=0)   # Standard deviation of metrics
    
    # Display final results
    print('\n' + '=' * 70)
    print(f'G-CoMVKM on {data_name} - Results Summary')
    print('=' * 70)
    print(f'Statistical results over {num_seeds} runs:\n')
    
    print('             AR        RI        NMI')
    print(f'Min:      {min_result[0]:.4f}    {min_result[1]:.4f}    {min_result[2]:.4f}')
    print(f'Mean:     {mean_result[0]:.4f}    {mean_result[1]:.4f}    {mean_result[2]:.4f}')
    print(f'Max:      {max_result[0]:.4f}    {max_result[1]:.4f}    {max_result[2]:.4f}')
    print(f'Std Dev:  {std_result[0]:.4f}    {std_result[1]:.4f}    {std_result[2]:.4f}')
    
    print(f'\nBest result was achieved on run {best_time}:')
    print(f'AR: {best_AR:.4f}, RI: {best_RI:.4f}, NMI: {best_NMI:.4f}')
    
    if best_model is not None:
        print('\nFinal dimensionality reduction:')
        print(f'Original dimensions: {dh}')
        print(f'Reduced dimensions: {best_model.dimensions_}')
        print(f'Reduction: {(1 - best_model.dimensions_[0]/dh[0])*100:.1f}%, {(1 - best_model.dimensions_[1]/dh[1])*100:.1f}%')
        
        # Visualize results
        visualize_results(X, best_model, best_index, label, c, result)
    
    return best_model, result

def visualize_results(X, model, predicted_labels, true_labels, n_clusters, result):
    """
    Visualize the clustering results
    """
    print("\nGenerating visualizations...")
    
    # 1. Performance distribution across runs
    plt.figure(figsize=(10, 6))
    plt.boxplot(result, labels=['AR', 'RI', 'NMI'])
    plt.title('Distribution of Clustering Metrics Across Runs')
    plt.ylabel('Metric Value')
    plt.grid(True)
    plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/boxplot_metrics.png'))
    
    # 2. Final view weights
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(model.view_weights_) + 1), model.view_weights_)
    plt.title('Final View Weights')
    plt.xlabel('View Index')
    plt.ylabel('Weight')
    plt.ylim([0, 1])
    plt.grid(True)
    plt.xticks(range(1, len(model.view_weights_) + 1), 
               [f'View {i}' for i in range(1, len(model.view_weights_) + 1)])
    plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/view_weights.png'))
    
    # 3. Dimensionality reduction visualization
    plt.figure(figsize=(8, 6))
    original_dims = [X[h].shape[1] for h in range(len(X))]
    width = 0.35
    x = np.arange(len(original_dims))
    
    plt.bar(x - width/2, original_dims, width, label='Original')
    plt.bar(x + width/2, model.dimensions_, width, label='Reduced')
    
    plt.title('Dimension Reduction')
    plt.xlabel('View')
    plt.ylabel('Number of Dimensions')
    plt.legend()
    plt.grid(True)
    plt.xticks(x, [f'View {i+1}' for i in range(len(original_dims))])
    plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/dimension_reduction.png'))
    
    # 4. Clustering visualization (if 2D data)
    if all(d <= 2 for d in model.dimensions_) or all(X[h].shape[1] <= 2 for h in range(len(X))):
        plt.figure(figsize=(15, 6))
        
        # Create colormap for clusters
        colors = plt.cm.get_cmap('tab10', n_clusters)
        
        # Plot the clustering results for each view
        for h in range(len(X)):
            plt.subplot(1, len(X), h + 1)
            
            # If data is 2D, plot directly
            if model.data_reduced_[h].shape[1] == 2:
                for k in range(n_clusters):
                    cluster_points = (predicted_labels == k)
                    plt.scatter(model.data_reduced_[h][cluster_points, 0], 
                                model.data_reduced_[h][cluster_points, 1], 
                                s=50, color=colors(k), 
                                alpha=0.7, edgecolors='k')
                
                # Also plot cluster centers
                plt.scatter(model.cluster_centers_[h][:, 0], 
                            model.cluster_centers_[h][:, 1], 
                            s=150, marker='d', 
                            c=range(n_clusters), cmap=colors, 
                            edgecolors='k', linewidths=2)
            
            elif model.data_reduced_[h].shape[1] == 1:
                # For 1D data, create a scatter plot with a dummy y-axis
                for k in range(n_clusters):
                    cluster_points = (predicted_labels == k)
                    plt.scatter(model.data_reduced_[h][cluster_points, 0], 
                                np.zeros(np.sum(cluster_points)) + 0.1*np.random.randn(np.sum(cluster_points)), 
                                s=50, color=colors(k), 
                                alpha=0.7, edgecolors='k')
                
                # Also plot cluster centers
                plt.scatter(model.cluster_centers_[h][:, 0], 
                            np.zeros(n_clusters), 
                            s=150, marker='d', 
                            c=range(n_clusters), cmap=colors, 
                            edgecolors='k', linewidths=2)
                plt.ylim([-0.5, 0.5])
                plt.ylabel('Jittered Position')
            
            else:
                # For higher dimensions, use PCA to reduce to 2D for visualization
                pca = PCA(n_components=2)
                data_pca = pca.fit_transform(model.data_reduced_[h])
                
                for k in range(n_clusters):
                    cluster_points = (predicted_labels == k)
                    plt.scatter(data_pca[cluster_points, 0], 
                                data_pca[cluster_points, 1], 
                                s=50, color=colors(k), 
                                alpha=0.7, edgecolors='k')
                
                # Project and plot cluster centers
                centers_pca = pca.transform(model.cluster_centers_[h])
                plt.scatter(centers_pca[:, 0], 
                            centers_pca[:, 1], 
                            s=150, marker='d', 
                            c=range(n_clusters), cmap=colors, 
                            edgecolors='k', linewidths=2)
            
            plt.title(f'View {h+1} Clustering')
            plt.xlabel('Dimension 1')
            if model.data_reduced_[h].shape[1] > 1:
                plt.ylabel('Dimension 2')
            plt.grid(True)
        
        plt.suptitle('G-CoMVKM Clustering Results')
        plt.tight_layout()
        plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/clustering_results.png'))
    
    # 5. Confusion Matrix Visualization
    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(true_labels, predicted_labels)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix: True vs. Predicted Clusters')
    plt.xlabel('Predicted Cluster')
    plt.ylabel('True Cluster')
    plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/confusion_matrix.png'))
    
    # 6. Performance Metrics Across Runs
    plt.figure(figsize=(12, 6))
    plt.plot(range(1, result.shape[0] + 1), result[:, 0], 'r-o', label='AR', linewidth=1.5, markersize=5)
    plt.plot(range(1, result.shape[0] + 1), result[:, 1], 'g-s', label='RI', linewidth=1.5, markersize=5)
    plt.plot(range(1, result.shape[0] + 1), result[:, 2], 'b-d', label='NMI', linewidth=1.5, markersize=5)
    plt.xlabel('Experiment Number')
    plt.ylabel('Metric Value')
    plt.title('Clustering Performance Across Different Initializations')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/performance_metrics.png'))
    
    # 7. Convergence Plot
    if hasattr(model, 'objective_values_') and model.objective_values_ is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(model.objective_values_) + 1), model.objective_values_, 'b-o')
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function Value')
        plt.title('G-CoMVKM Convergence')
        plt.grid(True)
        plt.savefig(os.path.expanduser('~/Desktop/G-CoMVKM-Python/convergence_plot.png'))
    
    print("Visualizations saved to ~/Desktop/G-CoMVKM-Python/")

if __name__ == "__main__":
    run_demo()
