def rectangle(height, width, holder="*", ender=""):
    for i in range(height):
        for j in range(width):
           print(holder, end=ender)
        print()

#rectangle(5,4,"G"," ")

def triangle(height, holder="*", ender=""):
    for i in range(height):
        for j in range(i + 1):
           print(holder, end=ender)
        print()

#triangle(5, "&", " ")

def rev_triangle(height, holder="*", ender=""):
    for i in range(height):
        for j in range(height - i):
           print(holder, end=ender)
        print()

#rev_triangle(5, "&", " ")

def hollow_triangle(height, holder="*", ender=""):
    for i in range(height):
        for j in range(i + 1):
            if j == 0 or i == 0 or i == height - 1 or j == i:
                print(holder, end = ender)
            else:
                print(" ", end = ender)
        print()

#hollow_triangle(20, "&", " ")

def hollow_square(height, holder="*", ender=""):
    for i in range(height):
        for j in range(height):
            if j == 0 or i == 0 or i == height - 1 or j == height - 1:
                print(holder, end = ender)
            else:
                print(" ", end = ender)
        print()

#hollow_square(5, "&", " ")

def hollow_rev_triangle(height, holder="*", ender=""):
    for i in range(height):
        for j in range(height - i):
            if j == 0 or i == 0 or i == height - 1 or j == (height-i-1):
                print(holder, end = ender)
            else:
                print(" ", end = ender)
        print()

#hollow_rev_triangle(5, "&", " ")

def fibbonauci(num, start1=0, start2=1):
    fib_list = []
    for i in range(num):
        start1, start2 = start2, start2 + start1
        fib_list.append(start1)
    
    return fib_list

#print(fibbonauci(5, 1, 1))

def factors(num):
    fact_list = []
    for i in range(1,int((num**1/2) + 1)):
        if num%i == 0:
            fact_list.append(i)
    
    fact_list.append(num)
    return fact_list

#print(factors(91))

def hcfandlcm(num1, num2):
    a, b = num1, num2
    while b != 0:
        a, b = b, a % b
    hcf = a
    lcm = (num1 * num2) // hcf

    return [hcf, lcm]

#print(hcfandlcm(6, 91))

def factorial(num):
    factorial = 1
    for i in range(1, num + 1):
        factorial *= i
    
    return factorial

#print(factorial(5))

def bogasort(li):
    import random

    while True:
        x = True
        random.shuffle(li)

        for i in range(1, len(li) - 1):
            if li[i] >= li[i - 1] and li[i] <= li[i + 1]:
                continue
            else:
                x = False

        if x:
            return (li)

#print(bogasort([1,9,7,8]))

def dictconst(keys, values):
    dict = {}
    for i in range(0, len(keys)):
        dict[keys[i]] = values[i]
    
    return dict

#print(dictconst("GOK", "123"))

def GetMYSQLCursor(dbname):
    import mysql.connector

    con = mysql.connector.MySQLConnection(
        host="localhost",
        user="root",
        password="password",
        database=dbname
    )

    cursor = con.cursor()

    return cursor