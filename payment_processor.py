import readline


class PaymentProcessor:
    categories: list[str] = []
    labels: list[str] = []

    def __init__(self, data, process_one):
        self.data = data
        self.data_iter = iter(data)
        self.process_one = process_one

    def __iter__(self):
        self.labels.append(self.process_one(next(self.data_iter)))



    
