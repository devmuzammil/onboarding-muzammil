import random
# EX Letter Grade
def grade(score):
    if(score >= 90):
        return 'A'
    elif(score >=80):
        return 'B'
    elif(score>=70):
        return 'C'
    elif(score >=60):
        return 'D'
    else:
        return 'F'

result=grade(79)

print(result)

# Ex FizzBuzz 1-100

def fizz_buzz():
        if number % 3 == 0 and number % 5 == 0:
            return 'FizzBuzz'
        elif number % 3 == 0:
            return 'Fizz'
        elif number % 5 == 0:
            return 'Buzz'
        else:
            return number

for number in range(1,101):
     play_fizz_buzz=fizz_buzz()
     print(play_fizz_buzz)

# EX 3 Password-strength checker

def check_password(password):

    problems = []

    if len(password) <8 :
        problems.append('Password is too short')

    if not any(char.isdigit() for char in password):
        problems.append('Password needs a digit')

    
    if not any(char.isupper() for char in password):
        problems.append('Password needs an uppercase letter')

    if not any(not char.isalpha() and not char.isdigit() for char in password):
        problems.append('Password needs a symbol')

    return problems

password=input('Enter the Password = ')
print (check_password(password))

def number_guessing_game():
    attempts=0
    computer_number=random.randint(1,100)
    while True:
        number=int(input('Enter the Number = '))
        attempts+=1
        if number>computer_number:
            print('High')
        elif number<computer_number:
            print('low')
        else:
            print('Correct !')
            print(f'Attempts: {attempts}')
            break

number_guessing_game()

def to_title_case():
    sentence=input('Enter the Sentence = ')
    words=sentence.split()

    title_words=[]
    for word in words:
        title_case= word[0].capitalize() + word[1:]
        title_words.append(title_case)

    result=" ".join(title_words)
    print(result)
to_title_case()