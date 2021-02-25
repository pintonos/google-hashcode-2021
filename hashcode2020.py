import sys
from random import randint, shuffle
import numpy as np
import os
import selenium


class Book:
    def __init__(self, id, points):
        self.id = id
        self.points = points


class Library:
    def __init__(self, id, number_of_books, signup, books_per_day, books):
        self.id = id
        self.signup = signup
        self.number_of_books = number_of_books
        self.books_per_day = books_per_day
        self.books = books
        self.points_over_days = 0

    def get_points_of_all_books(self):
        sum = 0
        for book in self.books:
            sum = sum + book.points
        return sum

    def points_in_days(self, days):
        useful_days = days - self.signup
        points = 0

        text = "Hallo"

        x = useful_days*self.books_per_day
        if useful_days*self.books_per_day > len(books):
            x = len(books)

        for d in range(0, x):
            points = points + int(books[d].points)

        return points

    def get_ratio_books_signup(self):
        return self.get_points_of_all_books / (self.number_of_books / self.books_per_day)

    def add_result_book(self, book):
        if not self.result_books:
            self.result_books = [book]
        else:
            self.result_books.append(book)


x = 2
filename_in = ["input/a_example.txt",
               "input/b_read_on.txt",
               "input/c_incunabula.txt",
               "input/d_tough_choices.txt",
               "input/f_libraries_of_the_world.txt"]
print(filename_in[x])

filename_out = filename_in[x].split('.txt')[0] + '.out'

with open(filename_in[x]) as f:
    line = f.readline().split(" ")

    amount_books = line[0]
    amount_libraries = line[1]
    days = int(line[2])

    line = f.readline().split(" ")

    books = []

    for x in range(0, int(amount_books)):
        book = Book(x, line[x])
        books.append(book)

    libraries = []

    for l in range(2, int(amount_libraries) + 2):
        line_lib = f.readline().split(" ")
        line_lib = list(map(int, line_lib))

        line_books = f.readline().split(" ")
        line_books = list(map(int, line_books))

        books_in_lib = [books[book_id] for book_id in line_books]
        books_in_lib.sort(key=lambda b: b.points, reverse=True)

        libraries.append(Library(l - 2, line_lib[0], line_lib[1], line_lib[2], books_in_lib))

    libs = []

    for lib in libraries:
        lib.points_over_days = lib.points_in_days(days)

    libraries.sort(key=lambda y: y.points_over_days, reverse=True)

    print(str(libraries[0].points_over_days) + " in " + str(days) + " days")

    days = days - libraries[0].signup
    libs.append(libraries[0])
    libraries.remove(libraries[0])

    for i, lib in enumerate(libraries):
        uniques = lib.books
        print(str(i) + " / " + str(len(libraries)))
        for j, lib_other in enumerate(libraries):
            if i > j:
                uniques = [v for v in uniques if v not in lib_other.books]
        lib.books = uniques

    '''
    while days > 0 and len(libraries) > 0:
        for lib in libraries:
            lib.points_over_days = lib.points_in_days(days)

        libraries.sort(key=lambda y: y.points_over_days, reverse=True)

        print(str(libraries[0].points_over_days) + " in " + str(days) + " days")

        days = days - libraries[0].signup

        for i in range(0, 201):
            libs.append(libraries[i])
            libraries.remove(libraries[i])
            '''



#write to file
outputfile = os.path.join(filename_out)
o = open(outputfile, "w+")
o.write(str(len(libs)) + "\n")

for lib in libs:
    o.write(str(lib.id) + " " + str(len(lib.books)) + "\n")
    for b in lib.books:
        o.write(str(b.id) + " ")

    o.write("\n")

o.close()
