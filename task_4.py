import uuid
from typing import List, Optional

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """Вузол бінарного дерева для візуалізації."""
    def __init__(self, key, color: str = "skyblue"):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор для networkx


def add_edges(graph: nx.DiGraph, node: Optional[Node], pos: dict, x=0.0, y=0.0, layer=1) -> nx.DiGraph:
    """Рекурсивно додає вершини та ребра в граф, формуючи координати для гарної розкладки."""
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)
    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / 2 ** layer
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / 2 ** layer
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root: Node, figsize=(8, 5), node_size=2500) -> None:
    """Малює дерево з кореня tree_root за допомогою networkx."""
    if tree_root is None:
        print("Порожнє дерево — нічого малювати.")
        return

    G = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(G, tree_root, pos)

    colors = [data["color"] for _, data in G.nodes(data=True)]
    labels = {n: data["label"] for n, data in G.nodes(data=True)}

    plt.figure(figsize=figsize)
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=node_size, node_color=colors)
    plt.axis("off")
    plt.show()


def heap_to_tree(heap: List[Optional[int]]) -> Optional[Node]:
    """
    Перетворює масив-кучу (0-й індекс — корінь, 2i+1 — лівий, 2i+2 — правий) у дерево Node.
    Підтримує опціональні None-значення (для “дірявих” масивів).
    """
    if not heap:
        return None

    def build_node(i: int) -> Optional[Node]:
        if i >= len(heap) or heap[i] is None:
            return None
        node = Node(heap[i])
        node.left = build_node(2 * i + 1)
        node.right = build_node(2 * i + 2)
        return node

    return build_node(0)


# ---------------- Демонстрація ----------------
if __name__ == "__main__":
    # приклад мін-купи або просто будь-якої бінарної купи у вигляді масиву
    min_heap = [0, 4, 1, 5, 10, 3]  # 0 — корінь; діти 4 і 1; далі 5, 10, 3

    root = heap_to_tree(min_heap)
    draw_tree(root)
