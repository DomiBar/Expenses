import json


class Expenses:
    def __init__(self):
        file_source = "expenses.json"
        try:
            with open(file_source, "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    def all(self):
        return self.expenses

    def get(self, id):
        expense = [expense for expense in self.all() if expense['id'] == id]
        if expense:
            return expense[0]
        return []

    def create(self, data):
        self.expenses.append(data)
        self.save_all()

    def save_all(self):
        file_source = "expenses.json"
        with open(file_source, "w") as f:
            json.dump(self.expenses, f)

    def update(self, id, data):
        expense = self.get(id)
        if expense:
            index = self.expenses.index(expense)
            self.expenses[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        expense = self.get(id)
        if expense:
            self.expenses.remove(expense)
            self.save_all()
            return True
        return False

    def get_sum(self):
        expenses_sum = 0
        for expense in self.expenses:
            expenses_sum += expense['value']
        return round(expenses_sum, 2)

    def get_category(self, category):
        category_list = []
        for expense in self.expenses:
            if expense['category'] == category:
                category_list.append(expense)
        return category_list


expenses = Expenses()
