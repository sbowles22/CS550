from turtle import *
import random as rd

def tree(depth=0):
    if depth!=8:
        d = rd.randint(20, (10-depth) * 10)
        a = rd.randint(5, (9-depth) * 7)
        b = rd.randint(5, (9-depth) * 7)
        pen.forward(d)
        pen.left(a)
        tree(depth+1)
        pen.right(a+b)
        tree(depth+1)
        pen.left(b)
        pen.back(d)

pen = Turtle()
pen.left(90)
pen.penup()
pen.back(300)
pen.pendown()
pen.forward(100)
pen.width(2)
tree()
while True:
    pen.left(1)