import math
import numpy as np

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
	    currentstack.append(tuple([value+b for value in a]))
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


#Multiplicative Distillation
#Perform multiplication or the dot product.
def multiplicative_distillation(currentstack):
    a = currentstack.pop()
    atype = type(a)
    b = currentstack.pop()
    btype = type(b)
    if atype in [int, float] and btype in [int,float]:
        currentstack.append(a*b)
    elif atype in [int,float] and btype == tuple:
        currentstack.append(tuple([value*a for value in b]))
    elif atype == tuple and btype in [int,float]:
        currentstack.append(tuple([value*b for value in a]))
    elif atype == tuple and btype == tuple:
        #dot product
        currentstack.append(sum([a[i]*b[i] for i in range(3)]))
    else:
        print(f"spell not able to handle types {atype} and {btype}!")

#Division Distillation
#Perform division or the cross product.
def division_distillation(currentstack):
    a = currentstack.pop()
    atype = type(a)
    b = currentstack.pop()
    btype = type(b)
    if atype in [int, float] and btype in [int,float]:
        currentstack.append(b/a)
    elif atype in [int,float] and btype == tuple:
        currentstack.append(tuple([value/a for value in b]))
    elif atype == tuple and btype == tuple:
        #cross product
        s1 = b[1]*a[2] - b[2]*a[1]
        s2 = b[2]*a[0] - b[0]*a[2]
        s3 = b[0]*a[1] - b[1]*a[0]
        currentstack.append((s1, s2, s3))
    else:
        print(f"spell not able to handle types {atype} and {btype}!")




#Length Purification
#Compute the absolute value or length.
def length_purification(currentstack):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        currentstack.append(abs(num))
    elif numtype == tuple:
        currentstack.append(math.sqrt(sum([x**2 for x in num])))


#Power Distillation
#Perform exponentiation or vector projection.
def power_distillation(currentstack):
    a = currentstack.pop()
    atype = type(a)
    b = currentstack.pop()
    btype = type(b)
    if atype in [int, float] and btype in [int,float]:
        currentstack.append(b**a)
    elif atype in [int, float] and btype == tuple:
        currentstack.append(tuple([value**a for value in b]))
    elif atype == tuple and btype == tuple:
        u = np.array(b)
        v = np.array(a)
        v_norm = np.sqrt(sum(v**2))
        currentstack.append(tuple((np.dot(u, v)/v_norm**2)*v))



#Floor Purification
#"Floors" a number, cutting off the fractional component and leaving an integer value. If passed a vector, instead floors each of its components.
def floor_purification(currentstack):
	pass


#Ceiling Purification
#"Ceilings" a number, raising it to the next integer value if it has a fractional componen. If passed a vector, instead ceils each of its components.
def ceiling_purification(currentstack):
	pass


#Vector Exaltation
#Combine three numbers at the top of the stack into a vector's X, Y, and Z components (bottom to top).
def vector_exaltation(currentstack):
    z = currentstack.pop()
    y = currentstack.pop()
    x = currentstack.pop()
    currentstack.append((x, y, z))


#Vector Disintegration
#Split a vector into its X, Y, and Z components (bottom to top).
def vector_disintegration(currentstack):
	pass


#Modulus Distillation
#Takes the modulus of two numbers.
def modulus_distillation(currentstack):
	pass


#Axial Purification
#Coerce vector to nearest axial direction or return sign of number
def axial_purification(currentstack):
	pass


#Entropy Reflection
#Creates a random number between 0 and 1
def entropy_reflection(currentstack):
	pass


#Jester's Gambit
#Swaps the top two iotas on the stack
def jesters_gambit(currentstack):
	pass


#Rotation Gambit
#Yanks the iota third from the top of the stack to the top
def rotation_gambit(currentstack):
	pass


#Rotation Gambit
#Yanks the iota third from the top of the stack to the top
def rotation_gambit(currentstack):
	pass


#Rotation Gambit II
#Yanks the top iota to the third position
def rotation_gambit_ii(currentstack):
	pass


#Gemini Decomposition
#Duplicates the top iota
def gemini_decomposition(currentstack):
	pass


#Prospector's Gambit
#Copy the second-to-last iota to the top
def prospectors_gambit(currentstack):
	pass


#Undertaker's Gambit
#Copy the top iota of the stack, put it under the second
def undertakers_gambit(currentstack):
	pass


#Gemini Gambit
#Removes the number at the top of the stack, copies the next iota that number of times
def gemini_gambit(currentstack):
	pass


#Dioscuri Gambit
#Copy the top two iotas of the stack
def dioscuri_gambit(currentstack):
	pass


#Flock's Reflection
#Pushes the size of the stack 
def flocks_reflection(currentstack):
	pass


#Fisherman's Gambit
#Grabs the element in the stack indexed by the number and brings it to the top. If the number is negative, instead moves the top iota down that many elements
def fishermans_gambit(currentstack):
	pass


#Fisherman's Gambit II
#Like Fisherman's Gambit, but copies instead of moving
def fishermans_gambit_ii(currentstack):
	pass


#Swindler's Gambit
#Rearranges the top elements based on the provided Lehmer Code
def swindlers_gambit(currentstack):
	pass


