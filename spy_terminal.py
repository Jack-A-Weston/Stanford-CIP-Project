'''This is an encryption file which will ask the user for 'a secret'.
It will then encrypt their message. After asking for a prespecified code word,
it will unscramble the message.'''
import random
import string
import time
import os
from datetime import date
import smtplib
import ssl
import colorama

'''Constants'''
SYSTEM = 'cls'

'''---------------------MAIN CODE------------------------'''

'''This main function calls all other functions and will maintain the 
function as 'active' until the user exits it.'''


def main():
    '''The below are all default values which will be altered when the
    user makes their fist pass of the program.'''
    password = '???'
    scrambled_message = '!!!'
    codex = gencode()
    x = " "
    count = 0
    while x != 'boom':
        if welcome():
            password = set_up()
            scrambled_message = new_message(codex, count)
            count = 1
        else:
            retrieve_message(password, scrambled_message, codex, count)
            scrambled_message = None
            count = 0
        x = input("To self-destruct type 'boom'. Otherwise, hit enter. ")
    self_destruct(5, 'KABOOM', "Yes")


'''---------------------SUPPORTING FUNCTIONS ------------------------'''

'''Welcomes the user and directs them to either write a new message or retrieve an existing message.'''


def welcome():
    today = date.today()
    print('Welcome Agent. The current date is:', today)
    desire = input(
        "Enter 'L' to leave a new message. Enter 'R' to retrieve message: ")
    while desire != 'L' and desire != 'R':
        desire = input(
            "Enter 'L' or leave a new message. Enter 'R' to retrieve message: ")
    if desire == 'L':
        return True
    else:
        return False


'''Uses count to check if a message already exists. If so, warns this will be overridden. 
    Takes message and puts it through codex to scramble and then override it.'''


def new_message(codex, count):
    if count > 0:
        print("Warning! You already have a message logged. "
              "Your new message will replace it. ")
        time.sleep(1)
        decision = input("Continue? Y/N: ")
        if decision == 'Y':
            entry = input(
                "Please give me your message. Note: Do not use numbers: ")
            scrambled_message = scramble(entry, codex)
            return scrambled_message
    if count < 1:
        entry = input(
            "Please give me your message. Note: Do not use numbers: ")
        scrambled_message = scramble(entry, codex)
        return scrambled_message


'''This function takes in an existing password, a coded message and the codex. 
    It determines whether the password is correct and if so unscrambles the message and prints it for the user.
    A count lets user know if no messages have been left. 
    It also erases the message automatically'''


def retrieve_message(password, coded_message, codex, count):
    if count == 0:
        print("Currently no saved messages.")
        return
    if check_identity(password):
        security_code = random.randint(0, 999999)
        verification_code = 0
        while verification_code != security_code:
            verification_code = email_verify(security_code)
        if verification_code == security_code:
            fixed_message = unscramble(coded_message, codex)
            print("Your message has been unscrambled!" + "\n" + "You message is: " + fixed_message +
                  "\n" + "This message will self-erase in 10 seconds.")
            self_destruct(10, "Message Erased", "no")
            os.system(SYSTEM)


'''This code sends an email to the user's email address which contains a random security password. It then asks the user
to input this code before progressing.'''


def email_verify(security_code):
    check = 'no'
    while check == 'no':
        email_address = str(
            input("Enter your email address for ID confirmation: "))
        sender_email = "cipsecretagency@gmail.com"
        receiver_email = email_address
        subject = "Agent Identity Confirmation"
        text = "Good Day: Your confirmation code is " + \
            str(security_code) + "!"
        message = 'Subject: {}\n\n{}'.format(subject, text)
        port = 465  # For SSL

        # Creates a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("cipsecretagency@gmail.com", 'bylwvkphuoopismg')
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
        print("Email Sent to: " + email_address)
        verification = int(
            input("Please enter only the numbers in your confirmation code: "))
        if verification == security_code:
            print("Correct")
            check = 'Yes'
            return verification
        else:
            print("Incorrect! Try again!")


'''
This function takes the previously scrambled message and flips the dictionary key and values. 
It then uses this new dictionary to unscramble the message'''


def unscramble(input, codex):
    print("Password Correct! Unscrambling now...")
    time.sleep(1.5)
    value = []
    inverse_codex = dict(zip(codex.values(), codex.keys()))
    # print(inverse_codex)
    for i in range(len(input)):
        value.append(inverse_codex[int(input[i])])
    value = ''.join(value)
    return value


def check_identity(password):
    # Ask for password
    if password != ' ':
        print("To retrieve your message I will need to confirm your password")
        checker = input("Enter Password: ")
        while checker != password:
            print("ACCESS DENIED STOP SNOOPING!")
            checker = input('Enter Password: ')
        return True
    return True


'''Function allocates a new password to the message the user is about to write.
Function will allow user to move forward without password if required. this could easily tbe changed'''


def set_up():
    x = input("If you would like to set up a password? Type Y or N: ")
    if x == 'Y':
        password = input("Please specify your password: ")
        print("Your password has been saved!")
        os.system(SYSTEM)
        return password
    else:
        doublecheck = input("Are you sure? Enter Y or N: ")
        while doublecheck != 'Y' and doublecheck != 'N':
            print(doublecheck)
            doublecheck = input(
                "Not a valid input! Please try again. Enter Y or N: ")
            print(doublecheck)
        if doublecheck == 'Y':
            print("OK")
            password = ' '
            return password
        elif doublecheck == 'N':
            password = input("Please enter password: ")
            return password


'''This takes the message and uses the unique codex. It assigns the string value of each key a new value'''


def scramble(info, codex):
    characters = list(info)
    value = []
    for i in range(len(characters)):
        test = characters[i]
        value.append(str(codex[test]))
    print("Your message has been saved and secured!")
    show_message(value)
    return value


'''This generates a dictionary of all letters and assigns them a random value between 1 and 1 million. 
    It then adds spaces.
    It then adds punctuation.'''


def gencode():
    codex_1 = dict.fromkeys(string.ascii_letters, 0)
    for i in codex_1:
        codex_1[i] = random.randint(0, 1000000)
    codex_1.update({' ': random.randint(0, 1000000)})
    codex_2 = dict.fromkeys(string.punctuation, 0)
    for i in codex_2:
        codex_2[i] = random.randint(0, 1000000)
    codex_1.update(codex_2)
    return codex_1


'''This asks the user if they would like to see the message in coded for and then sends it out. 
    Later I would use this ability to send the codex and the coded message to separate email addresses so that the they 
    could later be brought back together to decode the message elsewhere. '''


def show_message(message):
    approval = input("If you would like to see coded message type Y: ")
    if approval == 'Y' or approval == 'y':
        print(message)


'''This function takes in a time, saying and a decision on whether to count down. If countdown is 'Yes' it will count
 down from the specified time and print the saying'''


def self_destruct(countdown, saying, counter):
    colorama.init()
    red = '\033[31m'
    if counter == 'Yes':
        for i in range(countdown):
            print(countdown-i)
            time.sleep(1)
        os.system(SYSTEM)
        print(red + saying)

    else:
        time.sleep(countdown)
        print(saying)


if __name__ == '__main__':
    main()
