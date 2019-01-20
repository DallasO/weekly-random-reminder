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
daysOfWeek          = maxDayOfWeek - minDayOfWeek + 1 # range of max - min
# ++++++++++++++++++++++++++++++++++++++++++++
# --------------------------------------------
# Set these variables to alter behavior
# --------------------------------------------
# Filename to save upcoming reminders
reminderFile = 'reminderFile'
# Filename to save history
reminderHistory = 'reminderHistory'
# Log filename
reminderLog = 'reminder.log'
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
def writeToFile(filename = reminderFile, list = None, permissions = 'w+'):
    if list != None:
        try:
            with open(filename, permissions) as f:
                try:
                    for date in list:
                        f.write(date + "\n")
                except ValueError as e:
                    pass
        except FileNotFoundError as e:
            raise
# END :: function to overwrite file



reminders = []



# BEGIN :: Read file and save stored dates
try:
    with open(reminderFile, 'r') as f:
        for line in f:
            reminders.append(datetime.strptime(line.strip(), preferredDateFormat))
except FileNotFoundError as e:
    pass    # First time running or dates were reset
# END :: Read file and save stored dates



# BEGIN :: Check if the reminder should go off
if len(reminders):
    # Get first reminder
    currentReminder = reminders[0]
    oldReminders = []

    if today > currentReminder:
        # Trigger Notification
        # log any notification errors
        hass.bus.fire('input_boolean.turn_on', {"entity_id": "input_boolean.send_notification"})
        # remove this from reminders
        currentReminder = str(reminders.pop(0))
        oldReminders.append(currentReminder)
        writeToFile(reminderHistory, oldReminders, "a+")

# END :: Check if the reminder should go off



# BEGIN :: Create new dates to save to file
while len(reminders) < upperLimit:
    randomDate = random.randint(minDaysBetween, 6)
    possibleDate = True

    if len(reminders) >= 0 and len(reminders) <= upperLimit:
        dates = [int(date.strftime("%w")) for date in reminders]
        for date in dates:
            if (
                randomDate == date or
                randomDate == date + 1 or
                randomDate + 1 == date or
                randomDate == date + 2 or
                randomDate + 2 == date
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

writeToFile(reminderFile, reminders)
# END :: Create new dates to save to file
