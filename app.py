from flask import Flask, request, render_template, redirect, url_for
from forms import ExpensesForm
from models import expenses
from datetime import date
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whisper'


@app.route('/expenses/', methods=['GET', 'POST'])
def expenses_list():
    form = ExpensesForm()
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            expenses.create(form.data)
            expenses.save_all()
            return redirect(url_for('expenses_list'))
        else:
            error = "Niepoprawnie wprowadzono dane"

    return render_template('expenses.html', form=form, error=error, expenses=expenses.all(),
                           sum=expenses.get_sum())


@app.route('/expenses/<int:expense_id>/', methods=['POST', 'GET'])
def expense_details(expense_id):
    expense = expenses.get(expense_id-1)
    form = ExpensesForm(data=expense)

    if request.method == 'POST':
        if form.validate_on_submit():
            if 'submit' in request.form:
                expenses.update(expense_id - 1, form.data)
            elif 'delete' in request.form:
                expenses.delete(expense_id-1)
        return redirect(url_for('expenses_list'))

    return render_template("expense.html", form=form, expense_id=expense_id)


@app.route('/expenses/<category>/', methods=['GET'])
def expense_category(category):
    category_list = expenses.get_category(category)
    form = ExpensesForm()
    total = 0

    for element in category_list:
        total += element['value']

    total = round(total, 2)

    return render_template("category.html", form=form, expenses=category_list,
                           category=category, sum=total)


if __name__ == "__main__":
    app.run(debug=True)
