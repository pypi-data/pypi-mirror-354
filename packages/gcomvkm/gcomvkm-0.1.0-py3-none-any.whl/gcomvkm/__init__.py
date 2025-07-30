"""
G-CoMVKM: Globally Collaborative Multi-View k-Means Clustering
==============================================================

G-CoMVKM integrates a collaborative transfer learning framework with 
entropy-regularized feature-view reduction, enabling dynamic elimination 
of uninformative components. This method achieves clustering by balancing 
local view importance and global consensus.

Author: Kristina P. Sinaga (Original MATLAB implementation)
"""

from .g_comvkm import GCoMVKM

__version__ = '0.1.0'
__all__ = ['GCoMVKM']
