


def appendToFile(filePath, line):
    # open a file for appending
    fileHandle = open(filePath, 'a')

    # write the file and add a new line
    fileHandle.write((line + '\n'))

    # IMPORTANT! close the file
    fileHandle.close()



#  program execution starts here
myTextFile = "pythonOutput.csv"

# write some lines to the file
appendToFile(myTextFile, "first line")
appendToFile(myTextFile, "second line")
appendToFile(myTextFile, raw_input("enter a line"))

# now open pythonOutput.csv 