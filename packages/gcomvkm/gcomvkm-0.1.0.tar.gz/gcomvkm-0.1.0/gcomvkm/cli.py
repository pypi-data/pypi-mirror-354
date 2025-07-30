#!/usr/bin/env python
"""
Command-line interface for G-CoMVKM package
"""
import argparse
import os
import sys
from gcomvkm import GCoMVKM
from gcomvkm.utils import load_synthetic_data
from gcomvkm.evaluation import nmi, rand_index, adjusted_rand_index


def main():
    """
    Main function to run the G-CoMVKM algorithm from command line
    """
    parser = argparse.ArgumentParser(
        description='Globally Collaborative Multi-View k-Means Clustering (G-CoMVKM)'
    )
    
    parser.add_argument(
        '--dataset', 
        type=str, 
        default='2V2D2C',
        choices=['2V2D2C', 'custom'],
        help='Dataset to use (default: 2V2D2C)'
    )
    
    parser.add_argument(
        '--gamma', 
        type=float, 
        default=5.0,
        help='Gamma parameter (default: 5.0)'
    )
    
    parser.add_argument(
        '--theta', 
        type=float, 
        default=4.0,
        help='Theta parameter (default: 4.0)'
    )
    
    parser.add_argument(
        '--clusters', 
        type=int, 
        default=2,
        help='Number of clusters (default: 2)'
    )
    
    parser.add_argument(
        '--seed', 
        type=int, 
        default=42,
        help='Random seed (default: 42)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--max-iter', 
        type=int, 
        default=100,
        help='Maximum number of iterations (default: 100)'
    )
    
    parser.add_argument(
        '--tol', 
        type=float, 
        default=1e-4,
        help='Convergence tolerance (default: 1e-4)'
    )
    
    args = parser.parse_args()
    
    # Load dataset
    if args.dataset == '2V2D2C':
        print(f"Loading {args.dataset} dataset...")
        X, label = load_synthetic_data()
        if X is None:
            print("Error: Could not load the synthetic dataset")
            return 1
    else:
        print("Custom datasets not supported in this demo")
        return 1
    
    # Create and fit the model
    print(f"Running G-CoMVKM with gamma={args.gamma}, theta={args.theta}, clusters={args.clusters}")
    model = GCoMVKM(
        n_clusters=args.clusters,
        gamma=args.gamma,
        theta=args.theta,
        max_iter=args.max_iter,
        tol=args.tol,
        verbose=args.verbose,
        random_state=args.seed
    )
    
    model.fit(X)
    
    # Get the cluster assignments
    predicted_labels = model.labels_
    
    # Calculate metrics
    nmi_score = nmi(label, predicted_labels)
    ri_score = rand_index(label, predicted_labels)
    ari_score = adjusted_rand_index(label, predicted_labels)
    
    # Print results
    print("\nClustering Results:")
    print(f"NMI: {nmi_score:.4f}")
    print(f"RI: {ri_score:.4f}")
    print(f"ARI: {ari_score:.4f}")
    
    print("\nFinal dimensionality reduction:")
    print(f"Original dimensions: {[X[h].shape[1] for h in range(len(X))]}")
    print(f"Reduced dimensions: {model.dimensions_}")
    
    reduction_percentages = [(1 - model.dimensions_[h]/X[h].shape[1])*100 for h in range(len(X))]
    print(f"Reduction: {', '.join([f'{p:.1f}%' for p in reduction_percentages])}")
    
    print("\nFinal view weights:")
    for h, weight in enumerate(model.view_weights_):
        print(f"View {h+1}: {weight:.4f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
