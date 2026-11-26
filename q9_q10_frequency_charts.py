"""Questions 9 and 10. Generate random counts and plot two charts."""

import argparse
from pathlib import Path


def random_frequencies(seed=None):
    import numpy as np

    rng = np.random.default_rng(seed)
    numbers = rng.integers(1, 101, size=1000)
    values, counts = np.unique(numbers, return_counts=True)
    return values, counts


def top_five_and_other(values, counts):
    frequencies = list(zip(values.tolist(), counts.tolist()))
    ranked = sorted(frequencies, key=lambda pair: (-pair[1], pair[0]))
    top_five = ranked[:5]

    labels = [str(value) for value, count in top_five]
    bar_counts = [count for value, count in top_five]
    labels.append("Other")
    bar_counts.append(sum(count for value, count in ranked[5:]))
    return labels, bar_counts


def run_charts(seed, save_dir):
    import matplotlib.pyplot as plt
    import numpy as np

    values, counts = random_frequencies(seed)
    for value, count in zip(values, counts):
        print(f"{value:3} | {count:3}")

    histogram, ax = plt.subplots(layout="constrained")
    # Each distinct value contributes its count to the corresponding integer bin.
    ax.hist(values, bins=np.arange(0.5, 101.5, 1), weights=counts, edgecolor="white")
    ax.set(xlabel="Integer", ylabel="Frequency", title="Frequency of 1,000 random integers")

    top_chart, ax = plt.subplots(layout="constrained")
    labels, bar_counts = top_five_and_other(values, counts)
    bars = ax.bar(labels, bar_counts)
    ax.bar_label(bars, padding=3)
    ax.margins(y=0.12)
    ax.set(xlabel="Value or category", ylabel="Frequency", title="Five most frequent values and Other")

    if save_dir is None:
        plt.show()
    else:
        save_dir.mkdir(parents=True, exist_ok=True)
        histogram.savefig(save_dir / "histogram.png")
        top_chart.savefig(save_dir / "top_five.png")
    plt.close(histogram)
    plt.close(top_chart)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, help="Make the random draws repeatable.")
    parser.add_argument("--save-dir", type=Path, help="Save both charts as PNGs.")
    args = parser.parse_args()
    try:
        run_charts(args.seed, args.save_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
