#Money
MoneyStr = input()
if MoneyStr[0] in ['R','r']:
    U = (eval(MoneyStr[3:]))/6.78
    print("USD{:.2f}".format(U))
elif MoneyStr[0] in ['U','u']:
    C = (eval(MoneyStr[3:]))*6.78
    print("RMB{:.2f}".format(C))
