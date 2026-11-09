from threading import Thread
from models import Card


class Transaction(Thread):
    def __init__(self, card: Card, amount: float):  # Add parameters you need
        super().__init__()  # Required: Initialize the Thread parent class
        self.card = card
        self.amount = amount

    def run(self):
        # This is the code that runs when you call .start()
        # For example:
        print(f"Processing transaction for {self.card}")

class Card:  # 5 usages, 1 Igor (likely a type hint or related class)
    def credit(self):
          # ... code cut off ...
          return True

          else:
          print(f'На карте № {self.number} не достаточно средств')

    def __str__(self):  # new *
          return (f'Владелец: {self...\n'
          f'Карта: {self...\n'
          f'Операций: {self.count}\n')

          class Card:
              def __init__(self, ...):
                  # ... other code ...
                  self.lock = threading.Lock()

              def credit(self):
                  with self.lock:  # This ensures only one thread runs this block at a time
                      # ... your balance checking and deducting logic ...
                      pass
