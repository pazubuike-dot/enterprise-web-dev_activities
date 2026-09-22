class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)



class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("dequeue from empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)



def test_stack_and_queue():
    # Testing Stack
    s = Stack()
    s.push(10)
    s.push(20)
    assert s.pop() == 20  # LIFO check
    assert s.size() == 1
    
    # Testing Queue
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    assert q.dequeue() == 10  # FIFO check
    assert q.size() == 1
    print("All stack and queue tests passed successfully!")

if __name__ == "__main__":
    test_stack_and_queue()