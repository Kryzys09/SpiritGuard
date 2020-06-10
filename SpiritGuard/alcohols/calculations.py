import datetime
from collections import OrderedDict

"""
@author Krzysztof Klęczek
"""

WATER_IN_BLOOD = 0.806
METABOLISM = [0.015, 0.017]
BODY_WATER = [0.58, 0.49]
MIL_TO_GRAM = 0.789


class Alcohol:
    def __init__(self, name, volume, percentage, date):
        self.name = name
        self.volume = volume
        self.percentage = percentage
        self.date = date

    def __str__(self):
        return self.name


"""
Metoda do obliczania stanu upojenia alkoholowego

@var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
@var alcohols - tablica zawierająca wypite alkohole (
    alc.percentage - zawartość samego alkoholu (5% = 0.05)
    alc.volume - ilość spożytego napoju (ml)
@var weight - waga osoby (kg)
@var hours - czas który upłynął od rozpoczęcia spożycia (h)

@return (float) - promile alkoholu we krwi
"""


def blood_alcohol_content(gender, alcohols, weight, hours):
    overall = 0.0
    for alc in alcohols:
        overall += alc.percentage * alc.volume * MIL_TO_GRAM

    bac = ((WATER_IN_BLOOD * overall * 0.12) / (BODY_WATER[gender] * weight) - (METABOLISM[gender] * hours)) * 10

    if bac < 0:
        return 0.0
    return bac


"""
Metoda do obliczania procesu trzeźwienia

@var interval - co jaki czas mają być kolejne kroki (min)
@var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
@var bac - ilość alkoholu we krwi (promile)
@var date_time @optional - dokładna data dla której znamy @bac (obiekt datetime)

@return (dictionary) - rozkład opadu ilości promili w stosunku do czasu (klucze to obiekty datetime, wartości to ilość promili)
"""


def sobering_time_projection(interval, gender, bac, date_time=datetime.datetime.now()):
    sobering = OrderedDict()
    time = date_time
    while bac > 0.0:
        sobering[str(time.strftime("%Y-%m-%d %H:%M:%S"))] = "{:.3f}".format(bac)
        time += datetime.timedelta(minutes=interval)
        bac -= METABOLISM[gender] * interval / 6
    sobering[str(time.strftime("%Y-%m-%d %H:%M:%S"))] = 0.0
    return sobering


"""
Metoda do obliczania jakie może być maksymalne stężenie alkoholi we krwi
aby wytrzeźwieć (albo raczej osiągnąć podany poziom)

@var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
@var date_finish - data do której chcemy wytrzeźwieć (obiekt datetime)
@var date_now @optional - data od której zaczynamy trzeźwieć (obiekt datetime, domyślnie teraz)
@var start_bac @optional - początkowe stężenie alkoholu we krwi (promile, domyślnie 0)
@var end_bac @optional - dopuszczalne końcowe stężenie alkoholu we krwi (promile, domyślnie 0)

@return (float) - maksymalne stążenie początkowe, żeby organizm zdążył zejść do stężenia końcowego (promile)
"""


def max_alcohol_intake(gender, date_finish, date_now=datetime.datetime.now(), start_bac=0.0, end_bac=0.0):
    time = date_finish - date_now
    return end_bac - start_bac + METABOLISM[gender] * time.total_seconds() / 360


"""
Metoda do obliczania ile jakiego alkoholu powinniśmy spożyć, żeby otrzymać
dane stężenie alkoholu we krwi

@var gender - płeć osoby (0 - mężczyzna, 1 - kobieta)
@var weight - waga osoby (kg)
@var bac - stężenie alkoholu we krwi (promile)
@var alcohols - słownik/lista/tablica z róznymi alkoholami dla których chemy wykonać obliczenia

@return (dictionary) - słownik postaci: nazwa_alkoholu -> ilość do wypicia (ml)
"""


def translate_bac(gender, weight, bac, alcohols):
    amounts = {}
    grams = (bac * BODY_WATER[gender] * weight) / (1.2 * WATER_IN_BLOOD)
    for alc in alcohols:
        am = int(grams / (alc.percentage * MIL_TO_GRAM))
        if am > 0:
            amounts[str(alc)] = am
        else:
            amounts[str(alc)] = 0

    return amounts


"""
Metoda do obliczania Body Mass Index

@var weight - waga osoby (kg)
@var height - wzrost osoby (cm)
"""


def get_bmi(weight, height):
    return weight / (pow(height / 100, 2))


"""
Czy opis jest tu w ogóle potrzebny?
;-)
"""


def interprete_bmi(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    else:
        return "overweight"


def get_sober_date(gender, bac, date=datetime.datetime.now()):
    hours = bac / (METABOLISM[gender] * 10)
    print(date + datetime.timedelta(hours=hours))
    return date + datetime.timedelta(hours=hours)


def get_relevant_drinks(gender, weight, drinks):
    if len(drinks) == 0:
        return []
    start_date = datetime.datetime.strptime(drinks[0].date, "%d-%m-%Y %H:%M")
    relevant_drinks = [drinks[0]]
    for i in range(1, len(drinks)):
        bac = blood_alcohol_content(gender, relevant_drinks, weight, 0)
        sd = get_sober_date(gender, bac, start_date)
        newd = datetime.datetime.strptime(drinks[1].date, "%d-%m-%Y %H:%M")
        print("SD: ", sd)
        print("NEWD: ", newd)
        if sd <= newd:
            print("DISCARDED: ", relevant_drinks)
            relevant_drinks = []
            start_date = newd
        relevant_drinks.append(drinks[i])

    bac = blood_alcohol_content(gender, relevant_drinks, weight, 0)
    sd = get_sober_date(gender, bac, start_date)
    if sd < datetime.datetime.now():
        return []
    return relevant_drinks


classic_alcohols = [
    Alcohol("beer", 500, 0.05, "1-1-2020 00:00"),
    Alcohol("wine", 500, 0.116, "1-1-2020 00:00"),
    Alcohol("vodka", 50, 0.4, "1-1-2020 00:00")
]
