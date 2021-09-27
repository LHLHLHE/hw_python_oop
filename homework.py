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

    TIME_DELTA = dt.timedelta(days=7)

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
        week_ago = today - self.TIME_DELTA
        return sum(rec.amount for rec in self.records
                   if today >= rec.date > week_ago)


class CashCalculator(Calculator):

    USD_RATE = 60.0
    EURO_RATE = 70.0

    CURRENCIES = {
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro'],
        'rub': [1, 'руб']
    }

    REMAINDER = 'На сегодня осталось {insert_remainder} {insert_currency}'
    DUTY = 'Денег нет, держись: твой долг - {insert_duty} {insert_currency}'
    LIMIT = 'Денег нет, держись'

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        if today_stats == self.limit:
            return self.LIMIT
        rate = self.CURRENCIES[currency][0]
        name = self.CURRENCIES[currency][1]
        difference = (self.limit - today_stats) / rate
        remainder = round(difference, 2)
        if today_stats < self.limit:
            return self.REMAINDER.format(insert_remainder=remainder,
                                         insert_currency=name)
        return self.DUTY.format(insert_duty=-remainder, insert_currency=name)


class CaloriesCalculator(Calculator):

    REMAINDER = ('Сегодня можно съесть что-нибудь ещё,'
                 ' но с общей калорийностью не более {insert_remainder} кКал')
    LIMIT = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            return (self.REMAINDER.format(
                    insert_remainder=self.limit - today_stats))
        return self.LIMIT
