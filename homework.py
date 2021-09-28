import datetime as dt


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            moment = dt.datetime.strptime(date, self.DATE_FORMAT)
            self.date = moment.date()


class Calculator(Record):

    DELTA_WEEK = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - self.DELTA_WEEK
        return sum(rec.amount for rec in self.records
                   if week_ago < rec.date <= today)


class CashCalculator(Calculator):

    USD_RATE = 60.0
    EURO_RATE = 70.0

    CURRENCIES = {
        'usd': ['USD', USD_RATE],
        'eur': ['Euro', EURO_RATE],
        'rub': ['руб', 1]
    }

    REMAINDER = 'На сегодня осталось {remainder} {currency}'
    DUTY = 'Денег нет, держись: твой долг - {duty} {currency}'
    LIMIT = 'Денег нет, держись'
    VALUE_ERROR = 'Некорректное значение валюты: {unknown_currency}'

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError(
                self.VALUE_ERROR.format(unknown_currency=currency)
            )
        today_stats = self.get_today_stats()
        if today_stats == self.limit:
            return self.LIMIT
        name, rate = self.CURRENCIES[currency]
        remainder = round((self.limit - today_stats) / rate, 2)
        if today_stats < self.limit:
            return self.REMAINDER.format(remainder=remainder,
                                         currency=name)
        return self.DUTY.format(duty=-remainder, currency=name)


class CaloriesCalculator(Calculator):

    REMAINDER = ('Сегодня можно съесть что-нибудь ещё,'
                 ' но с общей калорийностью не более {remainder} кКал')
    LIMIT = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            return self.REMAINDER.format(
                remainder=self.limit - today_stats
            )
        return self.LIMIT
