import math
def is_prime(n):
    if n <= 1:
      return False
    count = 0
    for i in range(2,int(math.sqrt(n))+1):
        if n % i == 0:
            count += 1
    if count >=1:
        return False
    else:
        return True

def is_armstrong(n):
    n1 = n
    Sum = 0
    digits = len(str(n))
    for i in range(digits):
        digit = n % 10
        Sum += math.pow(digit , digits)
        n = n // 10 
    return Sum == n1

def count_digits(n):
    return len(str(n))

def is_palindrome(x):
    x = str(x)
    x = x.lower()
    filtered = ''.join(c for c in x if c.isalnum())
    return filtered == filtered[::-1]

def is_perfect_number(x):
    divisors = [n for n in range(1,x) if x % n ==0]
    return sum(divisors) == x

def sum_of_digits(num):
    num = str(abs(num))
    return sum(int(digit) for digit in str(num))

def is_happy_number(num):
    seen = set()
    while  num != 1 and num not in seen:
      seen.add(num)
      num = sum(int(digit) ** 2  for digit in str(num))
    return num == 1

def divisors(num):
    num = abs(num)
    div = [n for n in range(1,num+1) if num % n == 0]
    return div

    




    
