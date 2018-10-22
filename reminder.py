import datetime
import random

today = datetime.datetime.now()
dayOfWeek = int(today.strftime("%w"))
timeOfDay = int(today.strftime("%H"))
upperLimit = 2

print("Today is:", today)
print("Day is:", dayOfWeek)
print("Time is:", timeOfDay)

reminderFile = 'reminderHistory'
reminderHistory = []

if dayOfWeek == 0 and timeOfDay == 21:
    randoDates = []
    for i in range(upperLimit):
        randomDate = random.randint(0,6)
        while not randoDates.index(randomDate):
            randoDates.append()
            randomDate = random.randint(0,6)

    print(randoDates)

with open(reminderFile, 'w+') as f:
    try:
        reminderHistory.append(datetime.datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S"))
    except ValueError as e:
        pass
if not reminderHistory:
    reminderHistory.append(datetime.datetime(2010, 1, 1))

lastReminder = today - reminderHistory[0]
print("Last reminder:", lastReminder)

# Is weekday after 5
itsTime = False
if dayOfWeek > 0 or dayOfWeek < 6:
    if timeOfDay >= 17 and lastReminder > datetime.timedelta(hours=-12):
        itsTime = True

if itsTime:
    print("It's time")
