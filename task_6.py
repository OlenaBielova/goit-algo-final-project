from typing import Dict, Tuple, List


items: Dict[str, Dict[str, int]] = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def compute_totals(selected: List[str], items: Dict[str, Dict[str, int]]) -> Tuple[int, int]:
    """Підрахунок сумарних калорій і вартості вибраних страв."""
    total_cost = sum(items[name]["cost"] for name in selected)
    total_cal = sum(items[name]["calories"] for name in selected)
    return total_cal, total_cost


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний підхід: обираємо за найбільшим ratio = calories/cost.
    Повертає (список страв, сумарні калорії, сумарна вартість).
    """
    sorted_items = sorted(
        items.items(),
        key=lambda x: (x[1]["calories"] / x[1]["cost"], x[1]["calories"]),
        reverse=True,
    )

    selected: List[str] = []
    total_cost = 0

    for name, info in sorted_items:
        if total_cost + info["cost"] <= budget:
            selected.append(name)
            total_cost += info["cost"]

    total_cal, total_cost = compute_totals(selected, items)
    return selected, total_cal, total_cost


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    максимізуємо калорійність при обмеженні бюджету.
    Повертає (список страв у оптимальному наборі, калорії, вартість).
    """
    item_list = list(items.items())
    n = len(item_list)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, data = item_list[i - 1]
        cost = data["cost"]
        calories = data["calories"]
        for j in range(budget + 1):
            if cost > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - cost] + calories)

    res: List[str] = []
    j = budget
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            name = item_list[i - 1][0]
            res.append(name)
            j -= item_list[i - 1][1]["cost"]

    res.reverse()
    total_cal, total_cost = compute_totals(res, items)
    return res, total_cal, total_cost


if __name__ == "__main__":
    budget = 100

    g_items, g_cal, g_cost = greedy_algorithm(items, budget)
    d_items, d_cal, d_cost = dynamic_programming(items, budget)

    print(f"Бюджет: {budget}\n")

    print("Жадібний алгоритм:")
    print("  набір:", g_items)
    print(f"  калорії = {g_cal}, вартість = {g_cost}\n")

    print("Динамічне програмування:")
    print("  набір:", d_items)
    print(f"  калорії = {d_cal}, вартість = {d_cost}")
