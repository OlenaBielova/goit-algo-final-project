import heapq
from typing import Dict, List, Tuple, Optional

class Graph:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, w: float, undirected: bool = True) -> None:
        if w < 0:
            raise ValueError("Алгоритм Дейкстри не працює з від’ємними вагами.")

        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])
        if undirected:
            self.adj[v].append((u, w))

    def dijkstra(self, start: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        if start not in self.adj:
            raise KeyError(f"Стартова вершина {start!r} відсутня у графі")

        dist: Dict[str, float] = {node: float('inf') for node in self.adj}
        parent: Dict[str, Optional[str]] = {node: None for node in self.adj}
        dist[start] = 0.0

        heap: List[Tuple[float, str]] = [(0.0, start)]

        while heap:
            d_u, u = heapq.heappop(heap)
            if d_u > dist[u]:
                continue

            for v, w in self.adj[u]:
                cand = d_u + w
                if cand < dist[v]:
                    dist[v] = cand
                    parent[v] = u
                    heapq.heappush(heap, (cand, v))

        return dist, parent

    @staticmethod
    def reconstruct_path(parent: Dict[str, Optional[str]], target: str) -> List[str]:
        """Повертає список вершин від старту до target (якщо шлях існує)."""
        path: List[str] = []
        cur: Optional[str] = target
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path


if __name__ == "__main__":
    g = Graph()
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 5)
    g.add_edge("B", "D", 10)
    g.add_edge("C", "E", 3)
    g.add_edge("E", "D", 4)
    g.add_edge("D", "F", 11)

    start = "A"
    dist, parent = g.dijkstra(start)

    print(f"Найкоротші відстані від {start}:")
    for node in sorted(dist):
        print(f"  {node}: {dist[node]}")

    print("\nМаршрути:")
    for node in sorted(dist):
        path = Graph.reconstruct_path(parent, node)
        if dist[node] == float('inf'):
            print(f"  {start} -> {node}: недосяжно")
        else:
            print(f"  {start} -> {node}: {' -> '.join(path)} (вартість {dist[node]})")
