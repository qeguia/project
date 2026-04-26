import sys
import argparse
import numpy as np


def compute_final_scores(P, A, alpha=0.7):
    P = np.array(P)
    A = np.array(A)

    # Normalize A
    A_normalized = A / np.max(A)

    # Final score
    final_scores = alpha * P + (1 - alpha) * A_normalized

    return final_scores


def main():
    parser = argparse.ArgumentParser(
        description="Compute probability and final score for a country."
    )

    parser.add_argument(
        "country",
        type=str,
        help="Country name (Spain, France, Germany, Hungary)"
    )

    parser.add_argument(
        "--alpha",
        type=float,
        default=0.7,
        help="Weight for probability component (default: 0.7)"
    )

    args = parser.parse_args()

    # Data from report
    countries = ["Spain", "France", "Germany", "Hungary"]
    P = np.array([0.183, 0.167, 0.170, 0.480])
    A = np.array([-0.37, -0.14, -0.09, 0.43])

    country = args.country.capitalize()

    if country not in countries:
        print(f"Invalid country. Choose from: {countries}")
        sys.exit(1)

    idx = countries.index(country)

    # Compute scores
    final_scores = compute_final_scores(P, A, alpha=args.alpha)

    # Output
    print(f"\nCountry: {country}")
    print(f"Probability of outperforming others: {P[idx]:.3f}")
    print(f"Final score (alpha={args.alpha}): {final_scores[idx]:.3f}")

    # Optional: show ranking
    ranking = sorted(zip(countries, final_scores), key=lambda x: x[1], reverse=True)

    print("\nRanking:")
    for i, (c, score) in enumerate(ranking, 1):
        print(f"{i}. {c}: {score:.3f}")