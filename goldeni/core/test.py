def square(x):
	return x*x

def doSquare(s,y):
	return s(y)

print doSquare(square,5)
