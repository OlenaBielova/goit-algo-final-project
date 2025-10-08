import uuid
from collections import deque
from typing import Dict, Tuple, List, Optional

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx


# --- Модель вузла ---
class Node:
    """Вузол бінарного дерева для візуалізації обходу."""
    def __init__(self, key: int, color: str = "#D3D3D3") -> None:
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val: int = key
        self.color: str = color
        self.id: str = str(uuid.uuid4())


# --- Побудова графа та позицій ---
def add_edges(graph: nx.DiGraph, node: Optional[Node], pos: Dict[str, Tuple[float, float]],
    x: float = 0, y: float = 0, layer: int = 1) -> nx.DiGraph:
    """
    Рекурсивно додає вузли/ребра дерева у graph та обчислює позиції для красивого малювання.
    (рекурсія лише для побудови графу, обхід буде без рекурсії)
    """
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)
    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / (2 ** layer)
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / (2 ** layer)
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def build_graph(root: Node) -> Tuple[nx.DiGraph, Dict[str, Tuple[float, float]]]:
    """Створює networkx-ґраф дерева та словник позицій вузлів."""
    graph = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}
    add_edges(graph, root, pos)
    return graph, pos


# --- Малювання ---
def draw_tree(graph: nx.DiGraph, pos: Dict[str, Tuple[float, float]], ax: plt.Axes) -> None:
    """Малює дерево у переданий Axes без блокування."""
    ax.clear()
    colors = [data["color"] for _, data in graph.nodes(data=True)]
    labels = {n: data["label"] for n, data in graph.nodes(data=True)}
    nx.draw(graph, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, font_size=10, ax=ax)
    ax.set_axis_off()


# --- Допоміжне: градієнт кольорів ---
def generate_gradient_colors(n: int, base_color: str = "#1296F0") -> List[str]:
    """
    Повертає n кольорів від темнішого до світлішого на базі base_color.
    Уникає ділення на нуль при n=1.
    """
    if n <= 1:
        return [base_color]

    base_rgb = mcolors.to_rgb(base_color)
    colors: List[str] = []
    for i in range(n):
        alpha = i / (n - 1)
        brightness = 0.35 + 0.65*alpha

        color = tuple(base_rgb[j]*brightness + (1-brightness)*1.0 for j in range(3))
        colors.append(mcolors.to_hex(color))
    return colors


# ---Обходи без рекурсії ----
def bfs_order(root: Optional[Node]) -> List[Node]:
    """Повертає порядок відвідування вузлів у ширину (BFS) без рекурсії."""
    if root is None:
        return []
    order: List[Node] = []
    q: deque[Node] = deque([root])
    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order


def dfs_order(root: Optional[Node]) -> List[Node]:
    """Повертає порядок відвідування вузлів у глибину (DFS, стек) без рекурсії."""
    if root is None:
        return []
    order: List[Node] = []
    stack: List[Node] = [root]
    while stack:
        node = stack.pop()
        order.append(node)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


# --- Візуалізація обходу ---
def visualize_traversal(root: Node, traversal: str = "bfs", base_color: str = "#1296F0",
                        interval: float = 0.6) -> None:
    """
    Анімує обхід дерева:
      traversal ∈ {"bfs", "dfs"}
      base_color — колір старту градієнта
      interval — пауза між кроками (сек)
    """
    graph, pos = build_graph(root)

    if traversal == "bfs":
        order = bfs_order(root)
        title = "BFS — обхід у ширину"
    elif traversal == "dfs":
        order = dfs_order(root)
        title = "DFS — обхід у глибину (стек)"
    else:
        raise ValueError("Unknown traversal type. Use 'bfs' or 'dfs'.")

    colors = generate_gradient_colors(len(order), base_color)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.suptitle(title)

    # Початковий стан
    draw_tree(graph, pos, ax)
    plt.pause(0.5)

    for node, color in zip(order, colors):
        node.color = color
        # оновлюємо атрибут вузла в графі
        graph.nodes[node.id]["color"] = node.color
        draw_tree(graph, pos, ax)
        plt.pause(interval)

    plt.show()


if __name__ == "__main__":
    # Будуємо дерево
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    print("BFS:")
    visualize_traversal(root, traversal="bfs", base_color="#1296F0", interval=0.5)

    # Створюємо нове дерево (щоб кольори не перетікали)
    root2 = Node(0)
    root2.left = Node(4)
    root2.left.left = Node(5)
    root2.left.right = Node(10)
    root2.right = Node(1)
    root2.right.left = Node(3)

    print("DFS:")
    visualize_traversal(root2, traversal="dfs", base_color="#D24A2C", interval=0.5)
