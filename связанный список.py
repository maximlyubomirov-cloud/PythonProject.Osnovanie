class Box:
    def __init__(self, name=None):
        self.name = name
        self.next = None

    def __str__(self):
        return f'{self.name}'

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0  # <--- Add this!

    def append(self, name):
        new_box = Box(name)
        if self.head is None:
            self.head = new_box
            self.tail = new_box
        else:
            self.tail.next = new_box
            self.tail = new_box

    def pop(self):
        if self.head is None:
            return None

        if self.head == self.tail:
            popped_name = self.head.name
            self.head = None
            self.tail = None
            return popped_name

        current = self.head
        while current.next != self.tail:
            if cnt == ind:
                prev.nexx
            current = current.next

        popped_name = self.tail.name
        self.tail = current
        self.tail.next = None
        return popped_name

    def __str__(self):
        result = []
        current = self.head
        # FIXED: Changed current/next to current.next
        while current:
            result.append(str(current.name))
            current = current.next
        return " -> ".join(result)

    def insert(self, name: str, ind: int) -> None:
        # 1. Check bounds
        if ind < 0 or ind > self.size:
            raise IndexError('Индекс вне диапазона')

        new_box = Box(name)

        # 2. Case: Inserting into an empty list (or at the very beginning)
        if ind == 0:
            new_box.next = self.head
            self.head = new_box
            if self.tail is None:  # If the list was empty, tail is also the new box
                self.tail = new_box

        # 3. Case: Inserting at the very end (acts like append, but safer for tail)
        elif ind == self.size:
            self.tail.next = new_box
            self.tail = new_box

        # 4. Case: Inserting somewhere in the middle
        else:
            current = self.head
            # We need to stop at the box *just before* the target index
            for _ in range(ind - 1):
                current = current.next

            new_box.next = current.next
            current.next = new_box

        # 5. Increase the size since we added a box
        self.size += 1


# --- Test your code ---
llist = LinkedList()
llist.append('Барсик')
llist.append('Атос')
llist.append('Маркиза')
llist.append('Мурчик')

print(llist)          # Output: Барсик -> Атос -> Маркиза -> Мурчик
print(llist.pop())    # Output: Мурчик
print(llist)          # Output: Барсик -> Атос -> Маркиза





