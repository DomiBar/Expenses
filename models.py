import json


class Expenses:
    def __init__(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    def all(self):
        return self.expenses

    def get(self, id):
        return self.expenses[id]

    def create(self, data):
        data.pop('csrf_token')
        self.expenses.append(data)

    def save_all(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def update(self, id, data):
        data.pop("csrf_token")
        self.expenses[id] = data
        self.save_all()

    def delete(self, id):
        del self.expenses[id]
        self.save_all()

    def get_sum(self):
        expenses_sum=0
        for expense in self.expenses:
            expenses_sum+=expense['value']
        return round(expenses_sum,2)

    def get_category(self, category):
        category_list=[]
        for expense in self.expenses:
            if expense['category']==category:
                category_list.append(expense)
        return category_list


expenses = Expenses()
