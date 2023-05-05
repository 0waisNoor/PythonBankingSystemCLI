# importing modules
import datetime
import os


# miscellaneous functions
def findLine(db, id):
    # uses Id database to find what line id is on
    # returns -1 if id is not found
    # db is a text file existing in the current directory
    # id is a 5 digit customer or admin id
    # all arguments are string
    with open(db, 'r') as f:
        lines = f.readlines()
    index = 0
    position = -1
    while index < len(lines):
        if id == lines[index][0:5]:
            position = index
            break
        index += 1
    return position


# validations
def validateID(id):
    # id must be a 5 digit decimal string
    # length check
    if len(id) != 5:
        return False
    # type check
    try:
        int(id)
    except ValueError:
        return False
    return True


def duplicateCheck(id, db):
    # duplicate check
    # id is a 5 digit customer or admin id
    # db is a text file existing in the current directory
    # all arguments are string
    with open(db, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line[0:5] == id:
            return False
    return True


def validatePass(passwd):
    # password must have atleast 8 characters, a number and a symbol
    # passwd is a string
    # length check
    if len(passwd) < 8:
        return False
    # format check
    symbols = '!@#$%^&*()`~-_+={}[]|;:"?/>.,<'
    numbers = '1234567890'
    symbolCheck = False
    for symbol in symbols:
        for char in passwd:
            if char == symbol:
                symbolCheck = True
    numCheck = False
    for num in numbers:
        for char in passwd:
            if char == num:
                numCheck = True

    if not (numCheck and symbolCheck):
        return False
    return True


def validateType(type):
    # type can only be string current or savings
    if type != 'savings' and type != 'current':
        return False
    return True


def validateDate(dt):
    # split the date and attempt to convert it to date
    # if there is an error, it indicates invalid values were entered by user
    # dt is a string in the format dd/mm/yyyy
    # format check
    instances = 0
    for char in dt:
        if char == '/':
            instances += 1
    if instances != 2:
        return False

    newDt = dt.split('/')
    # range check on values
    try:
        datetime.datetime(int(newDt[2]), int(newDt[1]), int(newDt[0]))
    except:
        return False
    return True


def calculateAge(dob):
    # no validations as assumption is dob is already validated
    # dob is a string in the format dd/mm/yyyy
    # convert dob to the datetime object
    dob = dob.split('/')
    dob = datetime.datetime(int(dob[2]), int(dob[1]), int(dob[0]))
    now = datetime.datetime.now()
    days = (now - dob).days
    age = days // 365
    return str(age)


def convertToDateObj(dt):
    # dt is a string in the form dd/mm/yyyy
    dt = dt.split('/')
    try:
        obj = datetime.datetime(int(dt[2]), int(dt[1]), int(dt[0]))
        return obj
    except:
        return -1


def validateCol(col, v=0):
    # column can be the string all or an index
    # v=0 is user version and v=1 is admin version
    try:
        int(col)
    except ValueError:
        if col != 'all':
            return False
    # if it is a digit
    if v == 0:
        if not (0 <= int(col) <= 5):
            return False
    elif v == 1:
        if not (0 <= int(col) <= 2):
            return False
    else:
        return False
    return True


def validateValue(value, col):
    # ensures that value meets its respective validation
    # col is an index
    # all arguments are strings
    # id
    if col == '0':
        if not (validateID(value)):
            return False
        # type
    if col == '2':
        if not validateType(value):
            return False
        # dob
    if col == '4':
        if not (validateDate(value)):
            return False
    return True


def validateBranch(branch):
    # branch can only be the string 1,2 or 3
    if not (branch == '1' or branch == '2' or branch == '3'):
        return False
    return True


# base functions for file manipulation and validation
# some functions return negative numbers to indicate errors
# others return strings to indicate status

def createUser(id, name, passwd, type, balance, dob, address):
    # creates an entry in userDB.txt
    # all arguments are strings
    # id is a 5 digit decimal number
    # name is a normal string
    # Password must be at least 8 letters with a number and symbol
    # type can only be string savings or current
    # balance is an integer in the form of a string
    # dob is a date string in the format dd/mm/yyyy
    # address is normal string

    # validations
    if not validateID(id):
        return 'Error: id must be 5 digit decimal number'
    if not duplicateCheck(id, 'userPK.txt'):
        return 'Error:duplicate entry, account was NOT created!'
    if not validateDate(dob):
        return 'Error:date is in wrong format'
    # age must be more than 11
    age = calculateAge(dob)
    if not (11 <= int(age) <= 122):
        return 'User must be at least 11 yo to create an account'

    if not validatePass(passwd):
        return 'Error: Password must be at least 8 letters with a number and symbol'
    if not validateType(type):
        return 'Error:type can be only savings or current'

    # creating user
    arguments = [id, name, type, balance, dob, address]
    with open('userDB.txt', 'a') as f:
        for arg in arguments:
            f.write(arg + ',')
        f.write('\n')
    # creating entry in adminPK database
    with open('userPK.txt', 'a') as f:
        f.write(id + ',')
        f.write(passwd)
        f.write('\n')
    return 'successful'


def createAdmin(id, name, passwd, dep):
    # all arguments are string
    # id is a 5 digit decimal number
    # name is a normal string
    # Password must be at least 8 letters with a number and symbol
    # dep can only be 1,2 or 3

    # validations
    if not validateID(id):
        return 'id must be 5 digit decimal number'
    if not duplicateCheck(id, 'adminPK.txt'):
        return 'Error: duplicate entry'
    if not validatePass(passwd):
        return 'password must be at least 8 letters with a number and symbol'
    if not validateBranch(dep):
        return 'department can only be 1,2,3'
    # creating user
    arguments = [id, name, dep]
    with open('adminDB.txt', 'a') as f:
        for arg in arguments:
            f.write(arg + ',')
        f.write('\n')
    # creating entry in adminPK database
    with open('adminPK.txt', 'a') as f:
        f.write(id + ',')
        f.write(passwd)
        f.write('\n')
    return 'Successful'


def read(id, db, column):
    # retrieves the field value of a certain record from its respective database
    # all arguments are string
    # id is a 5 digit decimal number
    # db can either be the string userDB.txt or adminDB.txt
    # column is an index

    # output is always a string as it will be used by table()
    # validate db
    if not (db == 'userDB.txt' or db == 'adminDB.txt'):
        return -1

    # determine the id file and version of validateCol to use
    if db == 'userDB.txt':
        idfile = 'userPK.txt'
        v = 0
    elif db == 'adminDB.txt':
        idfile = 'adminPK.txt'
        v = 1
    # find position of line for id
    linePos = findLine(idfile, id)
    if linePos == -1:
        return -2
    # extract the line
    with open(db, 'r') as f:
        records = f.readlines()
        reqRec = records[linePos]
    # output the column
    # column is validated differently for each type of account(admin and user)

    if column == 'all':
        # remove the \n at the end
        reqRec = reqRec.split(',')
        # remove line break at the end
        del reqRec[len(reqRec) - 1]
        return reqRec
    if validateCol(column, v):
        # if a specific field is required, split the into a list and output the value
        reqRec = reqRec.split(',')
        return [reqRec[int(column)]]
    else:
        return -3


def edit(id, column, value):
    # changes specified field value of a record (admin or user/customer)
    # all arguments are string
    # id is a 5 digit decimal number
    # value is a normal string and criteria depends on the column string
    # column is an index

    # this function will only be used for the user
    db = 'userDB.txt'
    # this file stores user ids and passwords
    idfile = 'userPK.txt'
    # find position of line for id
    linePos = findLine(idfile, id)
    if linePos == -1:
        return 'Error: account does not exist\n'
    # extract the line
    with open(db, 'r') as f:
        records = f.readlines()
        reqRec = records[linePos]

    # ensure that id,name,type cannot be changed

    # change the column
    if validateCol(column, 0) == True:
        # validateCol allows all but all is not needed
        if column == 'all':
            return 'Error: all is not allowed in this context'
        else:
            # validate the value
            if not validateValue(value, column):
                return 'Error: invalid value'

            # if a specific field is required, split the into a list and change the value
            # convert the list back to string and replace it in lines list
            reqRec = reqRec.split(',')
            reqRec[int(column)] = value
            reqRec = ','.join(reqRec)
            records[linePos] = reqRec

            with open(db, 'w') as file:
                for r in records:
                    file.write(r)
    else:
        return 'Error: invalid column specified'
    return 'Successful'


def delete(id, adm=0):
    # deletes an entry in a database
    # id is a 5 digit decimal number in the form of string
    # adm is an integers which can be either 0 or 1

    if adm == 0:
        db = 'userDB.txt'
        idfile = 'userPK.txt'
    elif adm == 1:
        db = 'adminDB.txt'
        idfile = 'adminPK.txt'
    else:
        return -2
    # vaildations
    if findLine(db, id) == -1:
        return 'account not found'
    # get line number
    line = findLine(idfile, id)
    # if id doesnt exist, do not execute following line and indicate
    if line == -1:
        return -3
    # read the lines
    with open(db, 'r') as f:
        dbContents = f.readlines()
    with open(idfile, 'r') as f:
        idContents = f.readlines()

    # delete the specified line
    del dbContents[line]
    del idContents[line]

    # rewrite the contents in idfile and db
    with open(db, 'w') as f:
        for line in dbContents:
            f.write(line)
    with open(idfile, 'w') as f:
        for line in idContents:
            f.write(line)
    return 'Successful'


def withdraw(id, value, desc):
    # withdraws funds from balance of user and creates entry in transactions database
    # all arguments are strings
    # id is a 5 digit decimal number in the form of string
    # value must be an integer (in the form of string)
    # desc is string with letter limit of 39 letters

    # generate the date
    now = datetime.datetime.now()
    # set the format to dd/mm/yyyy
    now = now.strftime('%d/%m/%Y')
    # validations
    # id check
    if findLine('userDB.txt', id) == -1:
        return 'Error: sender does not exist'
    # type check on value
    try:
        int(value)
    except ValueError:
        return 'Error: invalid value'
    # range check on value(depends on account type)
    # retrieve account type
    accType = read(id, 'userDB.txt', '2')[0]
    if accType == 'savings':
        maximum = 100
    else:
        maximum = 500
    if int(value) > maximum:
        result = 'Error: {0} account can only withdraw a maximum {1} dollars'.format(accType, maximum)
        return result
    # range check2: ensure value/amount is positive
    if int(value) < 0:
        return 'Error: withdrawal amount cannot be negative'
    # length check on description
    if len(desc) > 40:
        return 'Error: description must be less than 40 letters'
    # adjust and rewrite the balance
    bal = int(read(id, 'userDB.txt', '3')[0])
    # prevent balance from reaching negative number
    if bal < int(value):
        return 'Error: Insufficient funds'
    bal = bal - int(value)
    edit(id, '3', str(bal))

    # make the entry in withdrawals database
    with open('transactions.txt', 'a') as f:
        f.write(now + ',')
        f.write(id + ',')
        f.write('w,')
        f.write(value + ',')
        f.write(desc + '\n')
    return 'Successful'


def deposit(id, value, desc):
    # deposit funds to balance of user and creates entry in transactions database
    # all arguments are strings
    # id is a 5 digit decimal number in the form of string
    # value must be an integer (in the form of string)
    # desc is string with letter limit of 39 letters

    # generate the date
    now = datetime.datetime.now()
    # set the format to dd/mm/yyyy
    now = now.strftime('%d/%m/%Y')
    # validations
    # id check
    if findLine('userDB.txt', id) == -1:
        return 'Error: receiver does not exist'
    # type check on value
    try:
        int(value)
    except ValueError:
        return 'Error: invalid value'
    # range check on value(depends on account type)
    # length check on description
    if len(desc) > 40:
        return 'Error: description must be less than 40 letters'
    # range check: ensure value/amount is positive
    if int(value) < 0:
        return 'Error: deposit amount cannot be negative'
    # adjust and rewrite the balance
    bal = int(read(id, 'userDB.txt', '3')[0])
    bal = bal + int(value)
    edit(id, '3', str(bal))

    # make the entry in withdrawals database
    with open('transactions.txt', 'a') as f:
        f.write(now + ',')
        f.write(id + ',')
        f.write('d,')
        f.write(value + ',')
        f.write(desc + '\n')

    return 'Successful'


def transfer(id, sender, receiver, value, desc):
    # is used by admin account to transfer funds between 2 user accounts
    # withdraws funds from balance of user and creates entry in transactions database
    # all arguments are strings
    # id,sender,receiver is a 5 digit decimal number in the form of string
    # value must be an integer (in the form of string)
    # desc is string with letter limit of 39 letters

    # validations
    if findLine('adminPK.txt', id) == -1:
        return 'id not found'

    # validations
    if findLine('userPK.txt', sender) == -1:
        return 'Error: sender does not exist'
    if findLine('userPK.txt', receiver) == -1:
        return 'Error:receiver does not exist'
    if len(desc) > 40:
        return 'description must be less than 40 letters'
    try:
        int(value)
    except ValueError:
        return 'Error: invalid value'
    if int(value) < 0:
        return 'Error: value cannot be negative'

    withdrawStatus = withdraw(sender, value, desc)
    if withdrawStatus != 'Successful':
        return withdrawStatus
    depositStatus = deposit(receiver, value, desc)
    if depositStatus != 'Successful':
        # remove the withdraw transaction from transactions.txt and transfers.txt
        return depositStatus

    # store in the transfers database if both transactions succeeded
    # generate the date
    now = datetime.datetime.now()
    # set the format to dd/mm/yyyy
    now = now.strftime('%d/%m/%Y')
    # write to the file
    with open('transfers.txt', 'a') as f:
        f.write(now + ',')
        f.write(id + ',')
        f.write(value + ',')
        f.write(desc + '\n')
    return 'Successful'


def table(heading, args):
    # displays args in form of a table
    # args value is a list with embedded lists
    # all args must be the same length
    # heading is a normal string

    standardLength = len(args[0])
    for arg in args:
        if not len(arg) == standardLength:
            print("All rows must be the same length")
            return 0

    # find the width of each column(index)
    # width = largest width in a column
    # in this case args[0] is used but all args have the same length
    length = len(args[0])
    colLens = []  # this will store the width for each column
    for col in range(0, length):
        # this loop iterates through the columns
        largest = 0
        for arg in args:
            if len(arg[col]) > largest:
                largest = len(arg[col])
        colLens.append(largest)

        # add extra spaces to words that do not meet the width requirement
        # this is for the sake of even spacing
    for arg in args:
        index = 0
        while index < length:
            spaces = ' ' * (colLens[index] - len(arg[index]))
            arg[index] = arg[index] + spaces
            index += 1

    # draws the header
    print('___________________________________________________________________________________________________________')
    print(heading)
    print('___________________________________________________________________________________________________________')
    # this draws the actual table
    for row in args:
        # a cell consists of 4 lines

        line1 = []
        line2 = []
        line3 = []
        line4 = []
        for val in row:
            # stores values in order to draw table line by line later
            line1.append(' ' * (len(val) + 4) + '|')
            line2.append('  ' + val + '  |')
            line3.append(' ' * (len(val) + 4) + '|')
            line4.append('_' * (len(val) + 4) + '|')
        # print the contents of all the lines

        # converts to string to display contents without commas as strings
        line1 = ''.join(line1)
        line2 = ''.join(line2)
        line3 = ''.join(line3)
        line4 = ''.join(line4)
        print(line1)
        print(line2)
        print(line3)
        print(line4)


def showUsers():
    # shows all Users in a database

    with open('userPK.txt', 'r') as f:
        lines = f.readlines()
    print('\n')
    for line in lines:
        print(line)


def genStat(id, sdate, edate):
    # get the transactions from transactions database
    # all arguments are string
    # edate and sdate are in the format dd/mm/yyyy
    # id is a 5 digit decimal number in the form of string

    # validations
    if findLine('userPK.txt', id) == -1:
        return 'Error: account does not exist'
    if not (validateDate(sdate) and validateDate(edate)):
        return 'Error: invalid dates'
    # sdate must be larger than edate
    sdate = convertToDateObj(sdate)
    edate = convertToDateObj(edate)
    if sdate > edate:
        print('Error: Start date cannot be larger than End date')
        return 0

    # read tranactions database contents
    with open('transactions.txt', 'r') as f:
        transactions = f.readlines()
    # convert the values to list by splitting using a comma
    index = 0
    while index < len(transactions):
        transactions[index] = transactions[index].split(',')
        index += 1

        # only have transactions of specified account
    inRangeData1 = []
    for transaction in transactions:
        if transaction[1] == id:
            inRangeData1.append(transaction)
    # this contains all accounts' data

    # inRange stores transactions between edate and sdate
    inRangeData2 = []

    # add values that are between sdate and edate
    for transaction in inRangeData1:
        # transaction[0] is date field
        if sdate <= convertToDateObj(transaction[0]) <= edate:
            inRangeData2.append(transaction)

    # format inRangeData2 properly to be used in table()
    # current format: [[dt,id,w/d,amount,desc\n],[dt,id,w/d,amount,desc\n]]

    # calculate running balance:
    # First value must be the balance brought down calculated by reversing transactions from current bal
    balcd = int(read(id, 'userDB.txt', '3')[0])
    balbd = balcd
    for record in inRangeData2:
        if record[2] == 'w':
            balbd = balbd + int(record[3])
        elif record[2] == 'd':
            balbd = balbd - int(record[3])

    runningBal = [str(balbd), ]
    previousVal = balbd
    for record in inRangeData2:
        # record[3] is the value/amount
        if record[2] == 'w':
            runningBal.append(str(previousVal - int(record[3])))
            # previous value is the accumulated sum
            previousVal = previousVal - int(record[3])
        if record[2] == 'd':
            runningBal.append(str(int(record[3]) + previousVal))
            # previous value needs to be an integer type
            previousVal = int(record[3]) + previousVal

    # prepend balance b/d row to inRangeData2
    # we inserted dummy value and line break on description as this is the format required for following code
    # note: dummy value will be removed
    inRangeData2.insert(0, [' ', 'Dummy account', 'Balance b/d', str(balbd), ' \n'])

    # insert respective running balance in each record in inRangeData2
    # this is because table() prints row by row
    index = 0
    while index < len(inRangeData2):
        # inRangeData2 and running Bal are the same dimensions
        inRangeData2[index].insert(4, runningBal[index])
        index += 1

    # remove the account field
    for ls in inRangeData2:
        del ls[1]

    # remove \n at the end of description
    index = 0
    while index < len(inRangeData2):
        # inRangeData2[index][3] is the desc
        val = inRangeData2[index][4]
        # exclude line break
        inRangeData2[index][4] = val[:len(val) - 1]
        index += 1

    # append current balance to inRangeData2 so it shows in account statement

    # avoid printing an empty table
    if inRangeData2 == []:
        return 'No transaction found that meet this criteria'
    # add the header
    inRangeData2.insert(0, ['Date', 'Transaction type', 'amount', 'runningBal', 'Desc'])
    table('OWAIS BANK\n' + id + ' statement of accounts', inRangeData2)
    return 'Successful'


# commands functions
# These take in user input, format it in arguments required by their respective function,
# and give output accordingly

def showCommand(v=0):
    # shows user/admin the specified account information
    # user can only view their own account information
    # v can only be the integer 0 or 1

    # v = 1 is the admin version of this command
    colNames = ['id', 'name', 'type', 'balance', 'date of birth', 'country']
    print('You can view your account properties here')
    print('account properties include: ', end='')
    print('id,name,account type,balance, date of birth and country')
    # assign id from cache file
    if v == 1:
        id = input('Enter user account id\n')
    elif v == 0:
        with open('cache.txt', 'r') as f:
            id = f.readlines()[0]
    # user database is used in this account
    db = 'userDB.txt'
    # determine the field to display
    print('enter field to display:\n')
    col = input('0:all\n1:id\n2:name\n3:type\n4:balance\n5:dob\n6:country\n7:exit\n')
    # ensure that col is an integer as this validation does not exist in read()
    try:
        int(col)
    except ValueError:
        print('Error:invalid input')
        return 0

    # if not (int(col) in [0, 1, 2, 3, 4, 5, 6, 7]):
    #     print('Error:invalid column. Try again')
    #     # exit the code
    #     return 0
    if col == '7':
        # exit the code
        return 'exit'
    elif col == '0':
        col = 'all'
    # else do not change the value of col
    # extract required column name for single field value
    else:
        # convert to list as it will be used in table command
        col = str(int(col) - 1)
    # read() outputs in the form of list so no need for conversions
    contents = read(id, db, col)
    # validation checks
    if contents == -1:
        print('Error: database does not exist')
        return 0
    elif contents == -2:
        print('Error: account does not exist')
        return 0
    elif contents == -3:
        print('Error: invalid input')
        return 0

    # colNames will be single value if not all values are printed
    if col != 'all':
        colNames = [colNames[int(col)]]
    table(id + ' User Table', [colNames, contents])
    # all needed values have been taken from user


def createUserCommand():
    # creates a user entry, is used only by admin account

    id = input('Enter account ID\n')
    name = input('Enter customer full name\n')
    passwd = 'defaultpass#0'
    type = input('Enter type of account - 0 for current, 1 for savings:\n')
    balance = '100'
    dob = input('Enter Date of Birth(dd/mm/yyyy):\n')
    address = input("Enter address\n")
    if type == '0':
        type = 'savings'
    elif type == '1':
        type = 'current'

    status = createUser(id, name, passwd, type, balance, dob, address)
    print(status)


def withdrawCommand():
    # withdraws money from user account and creates entry in database

    value = input('Enter value to withdraw\n')
    passwd = input('Enter password to confirm transaction\n')
    with open('cache.txt', 'r') as cache:
        id = cache.readlines()[0]
    # check if password matches
    with open('userPK.txt', 'r') as f:
        lines = f.readlines()
        if not passwd + '\n' == lines[position][6:]:
            print('Error: Password does not match')
            return 0
    desc = input('Enter description\n')
    status = withdraw(id, value, desc)
    print(status)
    if status == 'Successful':

        balance = read(id, 'userDB.txt', '3')[0]
        print(value, 'dollars have been withdrawn, new balance is', balance)



def depositCommand():
    # withdraws money from user account and creates entry in database
    value = input('Enter value to deposit\n')
    passwd = input('Enter password to confirm transaction\n')
    with open('cache.txt', 'r') as cache:
        id = cache.readlines()[0]
    # check if password matches
    with open('userPK.txt', 'r') as f:
        lines = f.readlines()
        if not passwd + '\n' == lines[position][6:]:
            print('Error: Password does not match')
            return 0
    desc = input('Enter description\n')
    status = deposit(id, value, desc)
    print(status)
    if status == 'Successful':
        balance = read(id, 'userDB.txt', '3')[0]
        print(value, 'dollars have been deposited, new balance is', balance)


def genStatCommand(v=0):
    # generates electronic statement of accounts
    # v is the integer 0 or 1
    # v=1 is administrator version
    if v == 0:
        with open('cache.txt', 'r') as cache:
            id = cache.readlines()[0]
    elif v == 1:
        id = input('Enter id\n')
    sdate = input('Enter start date(dd/mm/yyyy)\n')
    edate = input('Enter end date(dd/mm/yyyy)\n')
    status = genStat(id, sdate, edate)
    print(status)


def changePassCommand():
    # changes the password of user account
    with open('cache.txt', 'r') as c:
        id = c.readlines()[0]
    lineNum = findLine('userPK.txt', id)
    if lineNum == -1:
        print('Error: account does not exist')
        return 0
    oldpass = input('Enter existing password\n')
    # check if oldPass matches
    with open('userPK.txt', 'r') as f:
        lines = f.readlines()
        print()
        if not (oldpass + '\n' == lines[lineNum][6:]):
            print('Error: Wrong Password')
            return 0

    newpass = input('Enter new password\n')
    # validate the password
    if not (validatePass(newpass)):
        print('Error: new password must have at least 8 characters, a symbol and a number')
        return 0
    # change the password

    newLine = lines[lineNum]
    newLine = newLine.replace(oldpass, newpass)
    lines[lineNum] = newLine

    with open('userPK.txt', 'w') as f:
        for line in lines:
            f.write(line)
    print('Successful')


def createAdminCommand():
    # create new admin record in Admin database, only used by superuser
    id = input('Enter account ID\n')
    name = input('Enter employee full name\n')
    passwd = input('Enter Password\n')
    branch = input('Enter employee branch\n')
    status = createAdmin(id, name, passwd, branch)
    print(status)


def deleteAdminCommand():
    # deletes admin in Admin database, only used by superuser
    id = input('Enter adminstrator account id to delete\n')
    confirmation = input('are you sure? Y/N\n')
    if confirmation == 'N' or confirmation == 'n':
        print('Acknowledged')
        return 0
    elif confirmation == 'Y' or confirmation == 'y':
        status = delete(id, 1)
        print(status)
    else:
        print('invalid value provided. Please try again')


def clearCommand():
    # clears contents of specified database
    print('Choose which history file to clear')
    files = os.listdir()
    index = 0
    for file in files:
        print(index, ':', end='')
        print(file)
        index += 1

    fileToDel = input('Choose which file to clear\n')

    # validations
    try:
        fileToDel = int(fileToDel)
    except ValueError:
        print('Error: Invalid value')
        return 0
    if not (0 <= fileToDel < len(files)):
        print('Error: Invalid value')
        return 0
    # the python file must not be cleared
    if fileToDel == files.index('MOHAMMAD_OWAIS_NOOR_BUTT_TP066233.py'):
        print('Error: you cannot tamper with the system file')
        return 0
    with open(files[fileToDel], 'w') as f:
        f.write('')
    print('Successful')


def deleteUserCommand():
    # deletes user from user database, only used by admin
    id = input('Enter user account id to delete\n')
    confirmation = input('are you sure? Y/N\n')
    if confirmation == 'N' or confirmation == 'n':
        print('Acknowledged')
        return 0
    elif confirmation == 'Y' or confirmation == 'y':
        status = delete(id, 0)
        print(status)
    else:
        print('invalid value provided. Please try again')


def transferCommand():
    # transfers funds between two users, only used by admin
    with open('cache.txt', 'r') as cache:
        id = cache.readlines()[0]
    sender = input('Enter sender ID\n')
    receiver = input('Enter receiver ID\n')
    value = input('Enter value to transfer\n')
    desc = input('Enter description\n')
    status = transfer(id, sender, receiver, value, desc)
    print(status)


def editCommand():
    # edits user field value, only used by admin
    # only the following values can be edited
    id = input('enter account ID\n')
    print('Enter column index:\n0:date of birth\n1:address')
    col = input()
    if col == '0':
        colIndex = '4'
    elif col == '1':
        colIndex = '5'
    else:
        print('Error: invalid input')
        return 0
    value = input('Enter value\n')
    status = edit(id, colIndex, value)
    print(status)


def adminProcess(command):
    # Takes in command input and passes it to respective command function
    if command == '1':
        showCommand(1)
    if command == '2':
        createUserCommand()
    if command == '3':
        deleteUserCommand()
    if command == '4':
        editCommand()
    if command == '5':
        genStatCommand(1)
    if command == '6':
        transferCommand()
    if command == '7':
        showUsers()


def suProcess(command):
    # Takes in command input and passes it to respective command function
    if command == '1':
        createAdminCommand()
    elif command == '2':
        deleteAdminCommand()
    elif command == '3':
        clearCommand()


def userProcess(command):
    # Takes in command input and passes it to respective command function

    if command == '1':
        showCommand()
    elif command == '2':
        withdrawCommand()
    elif command == '3':
        depositCommand()
    elif command == '4':
        changePassCommand()
    elif command == '5':
        genStatCommand()


# main loop

running = True
while running:
    # used to prevent execution of of following code if wrong accType is entered
    accepted = True
    # asks and determines which account user wishes to log into
    print('\n==========OWAIS BANKING SYSTEM V2==========\n')
    print('\n==========LOG IN PAGE==========\n')

    accType = input('Enter your account type:\n0 - SuperUser\n1 - Administrator\n2 - User\n')

    # validation
    if accType != '0' and accType != '1' and accType != '2':
        print('Error: Enter 0,1,2')
        accepted = False

    while accepted:

        # unlike admin and user, superuser does not have an associated database
        if accType == '0':
            passwd = input('Enter password\n')
            if passwd == 'supass':
                with open('cache.txt', 'w') as cache:
                    cache.write('SU')
                print('Log in successful')
                while True:  # continous loop for super user menu
                    print('1:create account\n2:delete account\n3:clear database\n')
                    command = input()
                    # ensure input is a number
                    if command == 'q' or command == 'Q':
                        break
                    try:
                        int(command)
                    except ValueError:
                        print('Error: Invalid input\n')
                        continue  # skip the rest of the code and restart

                    # range check
                    if 0 < int(command) <= 3:
                        suProcess(command)
                        # go to the next instance
                    else:
                        print('Error:invalid input\n')

                # break out of second loop
                break  # do not execute following code as it is reserved for other 2 accounts
            else:
                print('wrong password')
                break

                # log in
        id = input('Enter account ID(Q to exit)\n')

        # check if account type exists (only for admin and user accounts)
        if accType == '1':
            file = 'adminPK.txt'
        elif accType == '2':
            file = 'userPK.txt'

        # Q is used to exit the loop
        if id == 'Q' or id == 'q':
            break

        with open(file, 'r') as f:
            # check if the id exists in the id database
            lines = f.readlines()
            # assumption is id does not exist and password does not match
            exists = False

            # determine if account exists
            index = 0
            while index < len(lines):
                if lines[index][0:5] == id:  # id file entries are in the format: xxxxx,password
                    exists = True
                    position = index
                index += 1

        # if account exists, check the password else tell the user to re-enter credentials
        if exists:

            passwd = input('Enter password\n')
            # check if the password matches

            if passwd + '\n' == lines[position][6:]:
                # password matches
                # write account to cache database
                with open('cache.txt', 'w') as cache:
                    cache.write(id)
                print('Log in successful')
                if accType == '2':
                    while True:
                        print('\n===========USER MODE===========\n')
                        command = input(
                            'WHAT WOULD YOU LIKE TO DO?\n1:show property\n2:withdraw\n3:deposit\n4:change password\n5:generate statement of accounts\n')
                        # validation
                        if command == 'q' or command == 'Q':
                            break
                        # ensure input is a number
                        try:
                            int(command)
                        except ValueError:
                            print('Error: Invalid input')
                            continue  # skips remaining code and shifts to next line

                        # range check
                        if 1 <= int(command) <= 5:
                            userProcess(command)
                        else:
                            print('Error: Invalid input')
                elif accType == '1':
                    while True:
                        print('\n===========ADMINISTRATOR MODE===========\n')
                        print('WHAT WOULD YOU LIKE TO DO?')
                        print('1:show user property\n2:create user account\n3:delete\n4:edit user property')
                        print('5:generate user statement\n6:transfer\n7:show all users and passwords\n')
                        command = input()
                        # validation
                        # ensure input is a number
                        if command == 'q' or command == 'Q':
                            break
                        try:
                            int(command)
                        except ValueError:
                            print('Error: Invalid input')
                            continue  # skips remaining code and shifts to next line

                        # range check
                        if 0 <= int(command) <= 7:
                            adminProcess(command)
                        else:
                            print('Error: Invalid input')
            else:
                print('Error: Password does not match! try again')

        else:
            print('Error:account non-existent, please try again')
            break
    # clear cache contents
    with open('cache.txt', 'w') as cache:
        cache.write('')
