#Python imports
import datetime, random, math



# Application imports
import secrets



# ++++++++++++++++++++++++++++++++++++++++++++
preferredDateFormat = "%Y-%m-%d %H:%M:%S"
today               = datetime.datetime.replace(datetime.datetime.now(), microsecond=0)
year                = int(today.strftime("%Y"))
month               = int(today.strftime("%m"))
dayOfMonth          = int(today.strftime("%d"))
minDayOfWeek        = 1 # Monday
maxDayOfWeek        = 5 # Friday
anyDay              = maxDayOfWeek + minDayOfWeek == 0
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
minDaysBetween = 2
# Limit times to send reminder (24hr)
earliestHour = 17
latestHour = 22
# ++++++++++++++++++++++++++++++++++++++++++++



# BEGIN :: function to overwrite file
def writeToFile(filename = reminderFile, list = None, permissions = 'w+'):
    if list != None:
        try:
            with open(filename, permissions) as f:
                try:
                    for item in list:
                        f.write(str(item) + "\n")
                except ValueError as e:
                    errors.append(str(today) + ":\tError ##0:\tlist is not of type list.")
        except FileNotFoundError as e:
            errors.append(str(today) + ":\tError ##1:\tFileNotFoundError. Does " + filename + " exist?")
    else:
        errors.append(str(today) + ":\tError ##1:\tValueError. Tried to write nothing to file")
# END :: function to overwrite file



reminders = []
errors = []



# BEGIN :: Read file and save stored dates
try:
    with open(reminderFile, 'r') as f:
        for line in [l.strip() for l in f]:
            try:
                reminders.append(datetime.datetime.strptime(line, preferredDateFormat))
            except ValueError as e:
                # Catch invalid dates
                dateFileError = str(today) + ":\tError ##2:\tValueError. "
                if len(line) > 0:
                    errors.append("%sInvalid date in %s - %s" % (dateFileError, reminderFile, line))
                else:
                    errors.append("%sInvalid date in %s." % (dateFileError, reminderFile))
except FileNotFoundError as e:
    errors.append(str(today) + ":\tError ##3:\tFileNotFoundError. Assuming first run.")
# END :: Read file and save stored dates



# BEGIN :: Check if the reminder should go off
if len(reminders):

    if today > min(reminders):
        # Trigger notification
        from mqtt import send_notification
        send_notification()
        # Remember removed date(s)
        oldReminders = [rem for rem in reminders if rem <= today]
        reminders    = [rem for rem in reminders if rem > today]
        writeToFile(reminderHistory, oldReminders, "a+")
# END :: Check if the reminder should go off



# BEGIN :: Create new dates to save to file
if len(reminders) < upperLimit:
    infinityGauntlet = 0
    while len(reminders) < upperLimit:
        infinityGauntlet += 1
        randomDate = random.randint(minDaysBetween, max(minDaysBetween, math.ceil(7 / upperLimit)))
        possibleDate = True

        dates = [datetime.datetime.replace(reminder, hour=0, minute=0, second=0) for reminder in reminders] or []
        dates.append(datetime.datetime(year, month, dayOfMonth))

        testDay = max(dates) + datetime.timedelta(days=randomDate) # New Date at midnight
        testDayOfWeek = int(testDay.strftime("%w"))

        if not anyDay and (testDayOfWeek < minDayOfWeek or testDayOfWeek > maxDayOfWeek):
            possibleDate = False

        if infinityGauntlet > 3:
            possibleDate = True
            errors.append(str(today) + ":\tError ##4:\tGauntletError. Blocked a run to infinity.")

        if possibleDate == True:
            randomHour   = random.randint(earliestHour, latestHour)
            randomMinute = random.randint(0, 59)
            saveDay      = testDay + datetime.timedelta(hours=randomHour, minutes=randomMinute)
            reminders.append(saveDay)

    reminders.sort()
    writeToFile(reminderFile, reminders)

if len(errors):
    writeToFile(reminderLog, errors)
# END :: Create new dates to save to file
