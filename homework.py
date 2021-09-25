import datetime as dt


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            moment = dt.datetime.strptime(date, Record.DATE_FORMAT)
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
        return sum(rec.amount for rec in self.records if rec.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - self.TIME_DELTA
        return sum(rec for rec in self.records if today >= rec.date > week_ago)


class CashCalculator(Calculator):

    USD_RATE = 72.71
    EURO_RATE = 85.25

    cur = {
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro'],
        'rub': [1, 'руб']
    }

    REM = 'На сегодня осталось {rem} {curr}'
    DUT = 'Денег нет, держись: твой долг - {duty} {curr}'
    LIM = 'Денег нет, держись'

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        difference = (self.limit - today_stats) / self.cur[currency][0]
        remainder = round(difference, 2)
        if today_stats < self.limit:
            return self.REM.format(rem=remainder, curr=self.cur[currency][1])
        elif today_stats > self.limit:
            return self.DUT.format(duty=-remainder, curr=self.cur[currency][1])
        return self.LIM


class CaloriesCalculator(Calculator):

    REM = ('Сегодня можно съесть что-нибудь ещё,'
           ' но с общей калорийностью не более {rem} кКал')
    LIM = 'Хватит есть!'

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            remainder = self.limit - today_stats
            return self.REM.format(rem=remainder)
        return self.LIM


r1 = Record(17, 'dgfb')
r2 = Record(3, "fbd")

r = CaloriesCalculator(20)
r.add_record(r1)
r.add_record(r2)
print(r.get_calories_remained())
