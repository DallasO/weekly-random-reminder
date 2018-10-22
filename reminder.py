from datetime import datetime
import random

# ++++++++++++++++++++++++++++++++++++++++++++
preferredDateFormat = "%Y-%m-%d %H:%M:%S"
today               = datetime.now()
dayOfWeek           = int(today.strftime("%w"))
dayOfMonth          = today.strftime("%d")
month               = today.strftime("%m")
year                = today.strftime("%Y")
timeOfDay           = int(today.strftime("%H"))
minDayOfWeek        = 1 # Monday
maxDayOfWeek        = 5 # Friday
daysOfWeek          = maxDayOfWeek - minDayOfWeek # range of max - min
# ++++++++++++++++++++++++++++++++++++++++++++
# --------------------------------------------
# Set these variables to alter behavior
# --------------------------------------------
# Filename to save history
reminderFile = 'reminderFile'
# Maximum times to be reminded in a week
upperLimit = 2
# Minimum days between reminders
# minDaysBetween = int(daysOfWeek / upperLimit)
minDaysBetween = 1
# Earliest time to send reminder (24hr)
earliestHour = 17
# latest time to send reminder (24hr)
latestHour = 21
# ++++++++++++++++++++++++++++++++++++++++++++



# BEGIN :: function to overwrite file
def writeToFile(filename = reminderFile, reminders = None):
    if reminders != None:
        with open(reminderFile, 'w+') as f:
            try:
                for date in reminders:
                    f.write(date + "\n")
            except ValueError as e:
                pass
# END :: function to overwrite file



reminders = []



# BEGIN :: Read file and save stored dates
with open(reminderFile, 'r') as f:
    # try:
        reminders.append(datetime.strptime(f.read(), preferredDateFormat))
    # except ValueError as e:
    #     print("Error code #0")
print("# in file:", len(reminders))
# END :: Read file and save stored dates



# BEGIN :: Check if the reminder should go off
if len(reminders):
    # FIXME: Get previous reminder, not first in list - or just save previous first
    lastReminder = today - reminders[0]
    print("Last reminder:", lastReminder)

    # Is weekday after 5
    itsTime = False
    if dayOfWeek > 0 or dayOfWeek < 6:
        if timeOfDay >= 17 and lastReminder > datetime.timedelta(hours=-12):
            itsTime = True

    if itsTime:
        # remove this from reminders
        print("It's time")
# END :: Check if the reminder should go off



# BEGIN :: Create new dates to save to file
# Commented IF logic causing loop
while len(reminders) < upperLimit:
    randomDate = random.randint(minDayOfWeek, maxDayOfWeek)
    possibleDate = True

    if len(reminders) >= 0 and len(reminders) <= upperLimit:
        dates = [int(date.strftime("%w")) for date in reminders]
        for date in dates:
            if (
                randomDate == date or
                randomDate == date + 1 or
                randomDate + 1 == date
                ):
                possibleDate = False

    if possibleDate == True:
        randomHour      = str(random.randint(earliestHour, latestHour))
        randomMinute    = str(random.randint(0, 59))
        saveDay         = str(int(dayOfMonth) + randomDate)
        saveTime        = datetime.strptime(
                year + "-" + month + "-" + saveDay + " " + randomHour + ":" + randomMinute + ":00",
                preferredDateFormat
            )
        reminders.append(saveTime)
reminders = [str(reminder) for reminder in reminders]
reminders.sort()

print("Collected Dates:", reminders)
writeToFile(reminderFile, reminders)
# END :: Create new dates to save to file
