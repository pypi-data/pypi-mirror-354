PyFunMath 🔢

PyFunMath is a lightweight and beginner-friendly Python library designed to perform fun and fundamental number theory operations. Whether you're a student, hobbyist, or Python learner, this library offers handy utilities to explore properties of numbers like primality, digit patterns, and mathematical characteristics.

---

✨ Features

- Check if a number is prime  
- Identify Armstrong numbers  
- Detect palindromes (numeric or string)  
- Check for perfect numbers  
- Count total number of digits in an integer  
- Calculate sum of digits  
- Check if a number is a happy number  
- List all divisors of a number  

---

In your Python project:

from pyfunmath import (
    is_prime,
    is_armstrong,
    count_digits,
    is_palindrome,
    is_perfect_number,
    sum_of_digits,
    is_happy_number,
    divisors,
)

---

How to Use

1. is_prime(n)  
   Checks if a number is prime.  
   Example:  
   is_prime(7)  # True

2. is_armstrong(n)  
   Checks if a number is an Armstrong number (e.g., 153 = 1³ + 5³ + 3³).  
   Example:  
   is_armstrong(153)  # True

3. count_digits(n)  
   Returns the total number of digits in a number.  
   Example:  
   count_digits(12345)  # 5

4. is_palindrome(x)  
   Checks if a number or string is a palindrome. Case-insensitive and ignores non-alphanumeric characters.  
   Example:  
   is_palindrome("Madam")  # True  
   is_palindrome(121)      # True

5. is_perfect_number(n)  
   Checks if a number is perfect (equal to the sum of its proper divisors).  
   Example:  
   is_perfect_number(28)  # True

6. sum_of_digits(n)  
   Returns the sum of all digits in a number.  
   Example:  
   sum_of_digits(123)  # 6

7. is_happy_number(n)  
   Determines if a number is a happy number.  
   Example:  
   is_happy_number(19)  # True

8. divisors(n)  
   Returns a list of all divisors of the number.  
   Example:  
   divisors(12)  # [1, 2, 3, 4, 6, 12]

---

🧑‍💻 Developer

Siva Naga Lakshmi Somepalli  
Artificial Intelligence & Data Science
