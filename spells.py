import math


#True Reflection
#Adds True to the top of the stack
def true_reflection(currentstack):
	currentstack.append(True)


#False Reflection
#Adds False to the top of the stack
def false_reflection(currentstack):
	currentstack.append(False)


#Nullary Reflection
#Adds Null to the top of the stack
def nullary_reflection(currentstack):
	currentstack.append(Null)


#Vector Reflection Zero
#Adds (0, 0, 0) to the top of the stack
def vector_reflection_zero(currentstack):
	currentstack.append((0, 0, 0))


#Vector Reflection +X
#Adds (1, 0, 0) to the top of the stack
def vector_reflection_px(currentstack):
	currentstack.append((1, 0, 0))


#Vector Reflection -X
#Adds (-1, 0, 0) to the top of the stack
def vector_reflection_nx(currentstack):
	currentstack.append((-1, 0, 0))



#Vector Reflection +Y
#Adds (0, 1, 0) to the top of the stack
def vector_reflection_py(currentstack):
	currentstack.append((0, 1, 0))



#Vector Reflection -Y
#Adds (0, -1, 0) to the top of the stack
def vector_reflection_ny(currentstack):
	currentstack.append((0, -1, 0))



#Vector Reflection +Z
#Adds (0, 0, 1) to the top of the stack
def vector_reflection_pz(currentstack):
	currentstack.append((0, 0, 1))


#Vector Reflection -Z
#Adds (0, 0, -1) to the top of the stack
def vector_reflection_nz(currentstack):
	currentstack.append((0, 0, -1))


#Circle's Reflection
#Adds τ, the radial representation of a complete circle, to the stack.
def circle_reflection(currentstack):
	currentstack.append(math.tau)


#Arc's Reflection
#Adds π, the radial representation of half a circle, to the stack.
def arc_reflection(currentstack):
	currentstack.append(math.pi)



#Euler's Reflection
#Adds e, the base of natural logarithms, to the stack.
def euler_reflection(currentstack):
	currentstack.append(math.e)



#Additive Distillation
#Performs Addition
def additive_distillation(currentstack):
	a = currentstack.pop()
	atype = type(a)
	b = currentstack.pop()
	btype = type(b)
	if atype in [int, float] and btype in [int,float]:
	    currentstack.append(a+b)
	elif atype in [int,float] and btype == tuple:
	    currentstack.append(tuple([value+a for value in b]))
	elif atype == tuple and btype in [int,float]:
	    currentstack.append(tuple([value+b for value in b]))
	elif atype == tuple and btype == tuple:
	    currentstack.append(tuple([a[i]+b[i] for i in range(3)]))
	else:
	    print(f"spell not able to handle types {atype} and {btype}!")
	

#Subtractive Distillation
#Performs Subtraction
def subtractive_distillation(currentstack):
	a = currentstack.pop()
	atype = type(a)
	b = currentstack.pop()
	btype = type(b)
	if atype in [int, float] and btype in [int,float]:
	    currentstack.append(b-a)
	elif atype in [int,float] and btype == tuple:
	    currentstack.append(tuple([value-a for value in b]))
	elif atype == tuple and btype == tuple:
	    currentstack.append(tuple([b[i]-a[i] for i in range(3)]))
	else:
	    print(f"spell not able to handle types {atype} and {btype}!")

#DEBUG Number
#number thingy
def debug_num(currentstack):
	pass


#DEBUG nNumber
#negative number thingy
def debug_nnum(currentstack):
	pass


