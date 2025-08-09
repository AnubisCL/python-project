#重叠
import turtle as t
t.setup(400,400)
t.pendown()
t.pensize(2)
t.pencolor("black")
for i in range(9):
    t.seth(100*(i+1))
    t.fd(100)
    #t.seth(i*100+80)
t.done()

    
