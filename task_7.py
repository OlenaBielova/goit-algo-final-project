import random
import math
import matplotlib.pyplot as plt

def analytic_probabilities():
    counts = {s: c for s, c in zip(range(2, 13), [1,2,3,4,5,6,5,4,3,2,1])}
    return {s: counts[s] / 36 * 100 for s in range(2, 13)}

def monte_carlo_dice_simulation(num_rolls=1_000_000, seed=42):
    rng = random.Random(seed)
    sums_count = {s: 0 for s in range(2, 13)}
    for _ in range(num_rolls):
        total = rng.randint(1, 6) + rng.randint(1, 6)
        sums_count[total] += 1
    probabilities = {s: sums_count[s] / num_rolls * 100 for s in sums_count}
    return sums_count, probabilities, num_rolls

def print_probability_table(mc_probs, n_rolls):
    an_probs = analytic_probabilities()
    print("| Сума | Монте-Карло, % | Аналітична, % | |Δ|, п.п. | 95% CI (МК)         |")
    print("|----:|---------------:|--------------:|---------:|:--------------------:|")
    mae = 0.0
    for s in range(2, 13):
        mc = mc_probs[s]
        an = an_probs[s]
        p = mc / 100.0
        se = math.sqrt(p * (1 - p) * (1 / n_rolls)) * 100
        ci_lo, ci_hi = mc - 1.96 * se, mc + 1.96 * se
        diff = abs(mc - an)
        mae += diff
        print(f"| {s:4d} | {mc:14.2f} | {an:12.2f} | {diff:9.2f} | [{ci_lo:6.2f}; {ci_hi:6.2f}] |")
    mae /= 11
    print(f"\nСереднє абсолютне відхилення (МК vs аналітика): {mae:.2f} п.п.")

def plot_probabilities(mc_probs):
    an_probs = analytic_probabilities()
    sums = list(range(2, 13))
    mc = [mc_probs[s] for s in sums]
    an = [an_probs[s] for s in sums]

    plt.figure(figsize=(10, 6))
    plt.bar([s - 0.2 for s in sums], mc, width=0.4, label='Монте-Карло')
    plt.bar([s + 0.2 for s in sums], an, width=0.4, label='Аналітичні')
    plt.xlabel('Сума')
    plt.ylabel('Ймовірність (%)')
    plt.title('Ймовірності сум при киданні двох кубиків')
    plt.xticks(sums)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    sums_count, probabilities, n = monte_carlo_dice_simulation(num_rolls=1_000_000, seed=42)
    print("Результати симуляції методом Монте-Карло (1,000,000 кидків):")
    print_probability_table(probabilities, n)
    plot_probabilities(probabilities)
