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