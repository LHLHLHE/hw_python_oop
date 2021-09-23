import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            moment = dt.datetime.strptime(date, date_format)
            self.date = moment.date()


class Calculator(Record):

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        sum_today = 0
        for record in self.records:
            if record.date == dt.date.today():
                sum_today += record.amount
        return sum_today

    def get_week_stats(self):
        sum_week = 0
        date_week_ago = dt.date.today() - dt.timedelta(days=7)
        for record in self.records:
            if dt.date.today() >= record.date > date_week_ago:
                sum_week += record.amount
        return sum_week


class CashCalculator(Calculator):

    USD_RATE = 72.71
    EURO_RATE = 85.25

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        if self.get_today_stats() < self.limit:
            difference = self.limit - self.get_today_stats()
            if currency == 'usd':
                reminder = difference / CashCalculator.USD_RATE
                return f'На сегодня осталось {round(reminder, 2)} USD'
            elif currency == 'eur':
                reminder = difference / CashCalculator.EURO_RATE
                return f'На сегодня осталось {round(reminder, 2)} Euro'
            else:
                return f'На сегодня осталось {round(difference, 2)} руб'
        elif self.get_today_stats() == self.limit:
            return 'Денег нет, держись'
        else:
            difference = self.get_today_stats() - self.limit
            print(difference)
            if currency == 'usd':
                duty = difference / CashCalculator.USD_RATE
                return f'Денег нет, держись: твой долг - {round(duty, 2)} USD'
            elif currency == 'eur':
                duty = difference / CashCalculator.EURO_RATE
                return f'Денег нет, держись: твой долг - {round(duty, 2)} Euro'
            else:
                duty = difference
                return f'Денег нет, держись: твой долг - {round(duty, 2)} руб'


class CaloriesCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        if self.get_today_stats() < self.limit:
            remainder = self.limit - self.get_today_stats()
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {remainder} кКал')
        else:
            return 'Хватит есть!'