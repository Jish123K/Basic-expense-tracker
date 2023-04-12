from PyQt5.QtWidgets import *

from PyQt5.QtCore import Qt

from PyQt5.uic import loadUi

import sqlite3 as db

from datetime import datetime

class ExpenseTracker(QMainWindow):

    def __init__(self):

        super(ExpenseTracker, self).__init__()

        loadUi('expense_tracker.ui', self) # load UI design from Qt Designer

        self.init_ui()

        self.show()

        

    def init_ui(self):

        self.setWindowTitle("Expense Tracker Application")

        self.submit_button.clicked.connect(self.submit_expense)

        self.view_button.clicked.connect(self.view_expenses)

        self.expense_table.setColumnWidth(0, 100)

        self.expense_table.setColumnWidth(1, 150)

        self.expense_table.setColumnWidth(2, 150)

        self.expense_table.setColumnWidth(3, 100)

        self.total_expenses.setText('Total Expenses: $0')

        

        self.create_database_table()

        

    def create_database_table(self):

        connectionObjn = db.connect("expenseTracker.db")

        curr = connectionObjn.cursor()

        query = '''

        create table if not exists expenses (

            date string,

            name string,

            title string,

            expense number

            )

        '''

        curr.execute(query)

        connectionObjn.commit()

        

    def submit_expense(self):

        values = [self.date_entry.text(), self.name_entry.text(), self.title_entry.text(), self.expense_entry.value()]

        self.expense_table.insertRow(self.expense_table.rowCount())

        for i, value in enumerate(values):

            cell = QTableWidgetItem(str(value))

            cell.setTextAlignment(Qt.AlignCenter)

            self.expense_table.setItem(self.expense_table.rowCount()-1, i, cell)

        connectionObjn = db.connect("expenseTracker.db")

        curr = connectionObjn.cursor()

        query = '''

        INSERT INTO expenses VALUES 

        (?, ?, ?, ?)

        '''

        curr.execute(query,(self.date_entry.text(), self.name_entry.text(), self.title_entry.text(), self.expense_entry.value()))

        connectionObjn.commit()

        

    def view_expenses(self):

        connectionObjn = db.connect("expenseTracker.db")

        curr = connectionObjn.cursor()

        query = '''

        select * from expenses

        '''

        total='''

        select sum(expense) from expenses

        '''

        curr.execute(query)

        rows=curr.fetchall()

        curr.execute(total)

        amount=curr.fetchall()[0][0]

        

        self.expense_table.setRowCount(0)

        for row in rows:

            self.expense_table.insertRow(self.expense_table.rowCount())

            for i, value in enumerate(row):

                cell = QTableWidgetItem(str(value))

                cell.setTextAlignment(Qt.AlignCenter)

                self.expense_table.setItem(self.expense_table.rowCount()-1, i, cell)

        self.total_expenses.setText(f'Total Expenses: ${amount}')

        

if __name__ == '__main__':

    app = QApplication([])

    window = ExpenseTracker()

    app.exec_()

