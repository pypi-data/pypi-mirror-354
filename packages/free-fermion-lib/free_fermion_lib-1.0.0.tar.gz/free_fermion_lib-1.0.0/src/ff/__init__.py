"""
Free Fermion Library - A Python package for quantum free fermion systems

This package provides comprehensive tools for working with free fermion
quantum systems, including combinatorial functions, graph theory algorithms,
and quantum physics utilities.

Modules:
    ff_lib: Core quantum physics and linear algebra functions
    ff_combinatorics: Combinatorial matrix functions (pfaffian, hafnian, etc.)
    ff_graph_theory: Graph algorithms and visualization for planar graphs
    ff_utils: Common utility functions

Copyright 2025 James.D.Whitfield@dartmouth.edu
Licensed under MIT License.
"""

__version__ = "1.0.0"
__author__ = "James D. Whitfield"
__email__ = "James.D.Whitfield@dartmouth.edu"

# Import all main functions for easy access
from .ff_lib import *
from .ff_combinatorics import *
from .ff_graph_theory import *
from .ff_utils import *

# Define what gets imported with "from ff import *"
__all__ = [
    # Core quantum physics functions from ff_lib
    "permutation_to_matrix",
    "pauli_matrices",
    "jordan_wigner_lowering",
    "jordan_wigner_alphas",
    "jordan_wigner_majoranas",
    "rotate_operators",
    "build_V",
    "build_H",
    "build_Omega",
    "build_reordering_xx_to_xp",
    "build_K",
    "is_symp",
    "check_canonical_form",
    "generate_gaussian_state",
    "build_op",
    "compute_cov_matrix",
    "compute_2corr_matrix",
    "compute_algebra_S",
    "is_matchgate",
    "wick_contraction",
    "eigh_sp",
    "eigv_sp",
    "eigm_sp_can",
    "eigm_sp",
    # Combinatorial functions from ff_combinatorics
    "sgn",
    "pf",
    "hf",
    "pt",
    "dt",
    "dt_eigen",
    # Graph theory functions from ff_graph_theory
    "plot_graph_with_edge_weights",
    "generate_random_planar_graph",
    "plot_planar_embedding",
    "dual_graph_H",
    "faces",
    "complete_face",
    "find_perfect_matchings",
    "pfo_algorithm",
    "compute_tree_depth",
    # Utility functions from ff_utils
    "_print",
    "clean",
    "formatted_output",
    "generate_random_bitstring",
    "kron_plus",
]
