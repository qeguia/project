import numpy as np

def compute_final_scores(P, A, alpha=0.7):
    """
    Compute final scores for countries.

    Parameters:
    P (array-like): Probabilities of outperforming others (P_i)
    A (array-like): Risk-adjusted returns (A_i)
    alpha (float): Weight for probability component (default 0.7)

    Returns:
    np.ndarray: Final scores
    """
    P = np.array(P)
    A = np.array(A)

    # Normalize A by its maximum
    A_normalized = A / np.max(A)

    # Compute final score
    final_scores = alpha * P + (1 - alpha) * A_normalized

    return final_scores