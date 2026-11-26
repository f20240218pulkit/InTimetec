import matplotlib.pyplot as plt
import numpy as np

def get_seed():
    while True:
        answer = input("Enter a random seed ").strip()

        if answer == "":
            return None

        try:
            seed = int(answer)
        except ValueError:
            print("only whole positive.")
            continue

        if seed >= 0:
            return seed

        print("The seed cant be negative.")
def rand_freq(seed):
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

    other_count = 0
    for value, count in ranked[5:]:
        other_count += count

    labels.append("Other")
    bar_counts.append(other_count)

    return labels, bar_counts
def run_charts(seed):
    values, counts = rand_freq(seed)

    print("\nNumber | Frequency")
    for value, count in zip(values, counts):
        print(f"{value:6} | {count:9}")

    histogram, histogram_ax = plt.subplots(layout="constrained")
    bin_edges = np.arange(0.5, 101.5, 1)

    histogram_ax.hist(values, bins=bin_edges, weights=counts, edgecolor="white")
    histogram_ax.set(
        xlabel="Integer",
        ylabel="Frequency",
        title="Q9: Frequency of 1,000 random integers",
    )

    top_chart, top_ax = plt.subplots(layout="constrained")
    labels, bar_counts = top_five_and_other(values, counts)

    bars = top_ax.bar(labels, bar_counts)
    top_ax.bar_label(bars, padding=3)
    top_ax.margins(y=0.12)
    top_ax.set(
        xlabel="Number or category",
        ylabel="Frequency",
        title="Q10: Five most frequent values and Other",
    )

    plt.show()
    plt.close(histogram)
    plt.close(top_chart)
def main():
    seed = get_seed()
    run_charts(seed)
if __name__ == "__main__":
    main()