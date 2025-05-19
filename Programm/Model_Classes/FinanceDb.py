import sqlite3


class FinanceDb:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        # Проверяем наличие таблицы "users"
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        result = self.cursor.fetchone()
        if not result:
            # Если таблицы нет, то создаем ее
            self.cursor.execute('''CREATE TABLE users
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT,
                                    password TEXT)''')

        # Проверяем наличие таблицы "incomes"
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incomes';")
        result = self.cursor.fetchone()
        if not result:
            # Если таблицы нет, то создаем ее
            self.cursor.execute('''CREATE TABLE incomes
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    category TEXT,
                                    amount REAL,
                                    date TEXT)''')

        # Проверяем наличие таблицы "expenses"
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses';")
        result = self.cursor.fetchone()
        if not result:
            # Если таблицы нет, то создаем ее
            self.cursor.execute('''CREATE TABLE expenses
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    category TEXT,
                                    amount REAL,
                                    date TEXT)''')

        self.conn.commit()

    def check_user(self, login, password):
        query = "SELECT * FROM users WHERE name = ? AND password = ?"
        self.cursor.execute(query, (login, password))
        result = self.cursor.fetchone()
        if result:
            user_id = result[0]
            return user_id
        else:
            return None

    def register_user(self, newLogin, newPassword):
        query = "SELECT COUNT(*) FROM users WHERE name = ?"
        self.cursor.execute(query, (newLogin,))
        result = self.cursor.fetchone()[0]
        if result > 0:
            return False
        else:
            self.cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (newLogin, newPassword))
            self.conn.commit()
            return True

    def recovery_password(self, login, recoveredPassword):
        query = "SELECT COUNT(*) FROM users WHERE name = ?"
        self.cursor.execute(query, (login,))
        result = self.cursor.fetchone()[0]
        if result < 0:
            return False
        else:
            self.cursor.execute("UPDATE users SET password = ? WHERE name = ?", (recoveredPassword, login))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                return True
            else:
                return False

    def get_user_incomes(self, user_id):
        query = "SELECT category, amount, date FROM incomes WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def get_user_expenses(self, user_id):
        query = "SELECT category, amount, date FROM expenses WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def add_income(self, category, amount, date, user_id):
        query = "INSERT INTO incomes (user_id, category, amount, date) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (user_id, category, amount, date))
        self.conn.commit()

    def add_expense(self, category, amount, date, user_id):
        query = "INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (user_id, category, amount, date))
        self.conn.commit()

    def delete_transaction(self, category, amount, date, user_id, flag):
        table_name = 'incomes' if flag else 'expenses'
        query = f"DELETE FROM {table_name} WHERE user_id = ? AND category = ? AND amount = ? AND date = ?"
        self.cursor.execute(query, (user_id, category, amount, date))
        self.conn.commit()

    def give_user_name(self, user_id):
        query = "SELECT name FROM users WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()

    def date_sort(self, user_id, flag, start_date, end_date):
        table_name = 'incomes' if flag else 'expenses'
        query = f"SELECT category, amount, date FROM {table_name} WHERE user_id = ? AND strftime('%s', " \
                f"substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) BETWEEN " \
                f"strftime('%s', ?) AND strftime('%s', ?) ORDER BY strftime('%s', substr(date, 7, 4) || '-' || " \
                f"substr(date, 4, 2) || '-' || substr(date, 1, 2))"
        self.cursor.execute(query, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def categories_sort(self, user_id, flag, start_date, end_date, sort_by):
        table_name = 'incomes' if flag else 'expenses'
        query = f"SELECT category, amount, date FROM {table_name} WHERE user_id = ? AND category = ? " \
                f"AND strftime('%s', " f"substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) BETWEEN " \
                f"strftime('%s', ?) AND strftime('%s', ?)"
        self.cursor.execute(query, (user_id, sort_by, start_date, end_date))
        return self.cursor.fetchall()

    def update_transaction(self, user_id, flag, before_category, before_amount, before_date, after_category,
                           after_amount, after_date):
        table_name = 'incomes' if flag else 'expenses'
        query = f"UPDATE {table_name} SET category = ?, amount = ?, date = ? WHERE " \
                f"user_id = ? AND category = ? AND amount = ? AND date = ?"
        self.cursor.execute(query, (after_category, after_amount, after_date, user_id, before_category,
                                    before_amount, before_date))
        self.conn.commit()

    def chart_categories(self, user_id, start_date, end_date, flag):
        table_name = 'incomes' if flag else 'expenses'
        query = f"SELECT category, SUM(amount) FROM {table_name} WHERE user_id = ? AND strftime('%s', " \
                f"substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)) BETWEEN " \
                f"strftime('%s', ?) AND strftime('%s', ?) GROUP BY category"
        self.cursor.execute(query, (user_id, start_date, end_date))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

    def check_tables(self):

        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()

        # Вывод содержимого таблицы в консоль
        for row in rows:
            print(row)

        self.cursor.execute('SELECT * FROM incomes')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

        self.cursor.execute('SELECT * FROM expenses')
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)
