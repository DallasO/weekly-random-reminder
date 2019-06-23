# This file contains general functions that don't belong in the main file

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


# BEGIN :: log an error

# END :: log an error
