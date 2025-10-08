class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        if iterable:
            for x in iterable:
                self.append(x)

    def append(self, data):
        """Додає елемент у кінець за O(1) завдяки tail."""
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.data)
            cur = cur.next
        return out

    def print_list(self):
        print(" -> ".join(map(str, self.to_list())) or "(порожньо)")

    def reverse(self):
        """Ітеративний реверс"""
        prev = None
        cur = self.head
        old_head = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev
        self.tail = old_head

    # --- Сортування злиттям ---
    def sort(self):
        """Публічний метод: відсортувати список злиттям. Міняє head лише один раз."""
        self.head = self._merge_sort(self.head)
        self._recompute_tail()

    def _merge_sort(self, head):
        if head is None or head.next is None:
            return head
        mid = self._get_middle(head)
        right = mid.next
        mid.next = None  # розрізаємо список на [head..mid] і [right..]
        left_sorted = self._merge_sort(head)
        right_sorted = self._merge_sort(right)
        return self._sorted_merge_iter(left_sorted, right_sorted)

    @staticmethod
    def _get_middle(head):
        """Повертає середній вузол (нижня середина)."""
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    @staticmethod
    def _sorted_merge_iter(a, b):
        """Ітеративне злиття двох відсортованих списків"""
        dummy = Node(0)
        tail = dummy
        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a else b
        return dummy.next

    def _recompute_tail(self):
        """Оновити tail відповідно до поточного head."""
        cur = self.head
        if cur is None:
            self.tail = None
            return
        while cur.next:
            cur = cur.next
        self.tail = cur

    # --- Злиття двох відсортованих списків ---
    @staticmethod
    def merge_two_sorted_lists(list1, list2):
        """
        Зливає два ВІДСОРТОВАНІ LinkedList в один новий відсортований.
        Використовує наявні вузли (вхідні списки де-факто «споживаються»).
        """
        head = LinkedList._sorted_merge_iter(list1.head, list2.head)
        merged = LinkedList()
        merged.head = head
        merged._recompute_tail()
        return merged


if __name__ == "__main__":
    ll = LinkedList([3, 1, 4, 2])
    print("Оригінальний список:")
    ll.print_list()

    print("\nРеверсований список:")
    ll.reverse()
    ll.print_list()

    print("\nВідсортований список:")
    ll.sort()
    ll.print_list()

    ll2 = LinkedList([0, 5, 6])
    ll2.sort()
    print("\nДругий відсортований список:")
    ll2.print_list()

    print("\nЗлитий відсортований список:")
    merged = LinkedList.merge_two_sorted_lists(ll, ll2)
    merged.print_list()
