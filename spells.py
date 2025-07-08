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
    elif atype == list and btype == list:
        for element in a:
            b.append(element)
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
    elif numtype == bool:
        currentstack.append(1 if num else 0)
    elif numtype == list:
        currentstack.append(len(num))
    else:
        print(f"spell not able to handle type {numtype}!")

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
    else:
        print(f"spell not able to handle types {atype} and {btype}!")



#Floor Purification
#"Floors" a number, cutting off the fractional component and leaving an integer value. If passed a vector, instead floors each of its components.
def floor_purification(currentstack):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        currentstack.append(math.floor(num))
    elif numtype == tuple:
        currentstack.append(tuple([math.floor(element) for element in num]))
    else:
        print(f"spell not able to handle type {numtype}!")

#Ceiling Purification
#"Ceilings" a number, raising it to the next integer value if it has a fractional componen. If passed a vector, instead ceils each of its components.
def ceiling_purification(currentstack):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        currentstack.append(math.ceil(num))
    elif numtype == tuple:
        currentstack.append(tuple([math.ceil(element) for element in num]))
    else:
        print(f"spell not able to handle type {numtype}!")


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
	x, y, z = currentstack.pop()
	currentstack.append(x)
	currentstack.append(y)
	currentstack.append(z)


#Modulus Distillation
#Takes the modulus of two numbers.
def modulus_distillation(currentstack):
    a = currentstack.pop()
    atype = type(a)
    b = currentstack.pop()
    btype = type(b)
    if atype in [int, float] and btype in [int,float]:
        currentstack.append(b%a)
    elif atype in [int,float] and btype == tuple:
        currentstack.append(tuple([value%a for value in b]))
    elif atype == tuple and btype == tuple:
        currentstack.append(tuple([b[i]%a[i] for i in range(3)]))
    else:
        print(f"spell not able to handle types {atype} and {btype}!")


#Axial Purification
#Coerce vector to nearest axial direction or return sign of number
def axial_purification(currentstack):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        if num == 0:
            currentstack.append(0)
        else:
            currentstack.append(num/abs(num))
    elif numtype == tuple:
        length = math.sqrt(sum([x**2 for x in num]))
        currentstack.append(tuple([element/length for element in num]))
    else:
        print(f"spell not able to handle type {numtype}!")


#Entropy Reflection
#Creates a random number between 0 and 1
def entropy_reflection(currentstack):
	currentstack.append(np.random.rand())


#Jester's Gambit
#Swaps the top two iotas on the stack
def jesters_gambit(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a)
    currentstack.append(b)

#Rotation Gambit
#Yanks the iota third from the top of the stack to the top
def rotation_gambit(currentstack):
	a = currentstack.pop()
	b = currentstack.pop()
	c = currentstack.pop()
	currentstack.append(b)
	currentstack.append(a)
	currentstack.append(c)

#Rotation Gambit II
#Yanks the top iota to the third position
def rotation_gambit_ii(currentstack):
	a = currentstack.pop()
	b = currentstack.pop()
	c = currentstack.pop()
	currentstack.append(a)
	currentstack.append(c)
	currentstack.append(b)


#Gemini Decomposition
#Duplicates the top iota
def gemini_decomposition(currentstack):
    currentstack.append(currentstack[-1])	


#Prospector's Gambit
#Copy the second-to-last iota to the top
def prospectors_gambit(currentstack):
	currentstack.append(currentstack[-2])


#Undertaker's Gambit
#Copy the top iota of the stack, put it under the second
def undertakers_gambit(currentstack):
	a = currentstack.pop()
	b = currentstack.pop()
	currentstack.append(a)
	currentstack.append(b)
	currentstack.append(a)


#Gemini Gambit
#Removes the number at the top of the stack, copies the next iota that number of times
def gemini_gambit(currentstack):
    num = currentstack.pop()
    item = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        return
    for _ in range(num):
        currentstack.append(item)


#Dioscuri Gambit
#Copy the top two iotas of the stack
def dioscuri_gambit(currentstack):
	currentstack.append(currentstack[-2])
	currentstack.append(currentstack[-2])


#Flock's Reflection
#Pushes the size of the stack 
def flocks_reflection(currentstack):
	currentstack.append(len(currentstack))


#Fisherman's Gambit
#Grabs the element in the stack indexed by the number and brings it to the top. If the number is negative, instead moves the top iota down that many elements
def fishermans_gambit(currentstack):
    num = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        return
    if num >= 0:
        item = currentstack[-num]
        del currentstack[-num]
        currentstack.append(item)
    else:
        item = currentstack.pop()
        currentstack.insert(len(currentstack)+num, item)


#Fisherman's Gambit II
#Like Fisherman's Gambit, but copies instead of moving
def fishermans_gambit_ii(currentstack):
    num = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        return
    if num >= 0:
        item = currentstack[-num-1]
        currentstack.append(item)
    else:
        item = currentstack[-1]
        currentstack.insert(len(currentstack)+num-1, item)


#Swindler's Gambit
#Rearranges the top elements based on the provided Lehmer Code
#My god this one will be silly
def swindlers_gambit(currentstack):
    code = currentstack.pop()
    if type(code) != int:
        print("lehmer code needs to be an integer")
        return
    #factorials up to 720
    factorials = [1, 2, 6, 24, 120, 720]
    i = 0
    while factorials[i] <= code:
        i += 1
    if i > len(currentstack):
        print("not enough iotas on stack for lehmer code")
        return
    choices = [currentstack.pop() for _ in range(i+1)]
    print(f"i: {i}")
    print(choices)
    out = [] 
    while i > 0:
        distance = factorials[i]-code
        size = factorials[i] - factorials[i-1]
        choice = math.ceil((i)*distance/size)-1
        out.append(choices[choice])
        del choices[choice]
        code %= factorials[i-1]
        while factorials[i-1] > code and i > 0:
            i -= 1
    for element in choices[::-1]:
        out.append(element)
    for element in out:
        currentstack.append(element)

	


#Augurs Purification
#Convert an argument to a boolean: 0, None and False become False, everything else becomes True
def augurs_purification(currentstack):
    argument = currentstack.pop()
    if argument in [0, None, False]:
        currentstack.append(False)
    else:
        currentstack.append(True)


#Negation Purification
#Inverts the boolean argument
def negation_purification(currentstack):
    argument = currentstack.pop()
    if type(argument) != bool:
        print("argument needs to be bool!")
        return
    currentstack.append(False if argument else True)


#Disjunction Distillation
#Performs boolean OR
def disjunction_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) != bool or type(b) != bool:
        print("both arguments need to be booleans")
        return
    currentstack.append(True if a or b else False)



#Conjunction Distillation
#Performs boolean AND
def conjunction_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) != bool or type(b) != bool:
        print("both arguments need to be booleans")
        return
    currentstack.append(True if a and b else False)


#Exclusion Distillation
#Performs boolean XOR
def exclusion_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) != bool or type(b) != bool:
        print("both arguments need to be booleans")
        return
    currentstack.append(True if (a ^ b) else False)


#Augur's Exaltation
#If the first argument is True, keep the second and discard the third. Otherwise vice versa
def augurs_exaltation(currentstack):
    sel = currentstack.pop()
    if type(sel) != bool:
        print("needs a boolean value as selector")
        return
    if sel:
        del currentstack[-2]
    else:
        del currentstack[-1]


#Equality Distillation
#If the first two arguments are equal, return True, otherwise False
def equality_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a == b)


#Inequality Distillation
#If the first two arguments are not equal, return True, otherwise False
def inequality_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a != b)



#Maximus Distillation
#If the first argument is greater than the second, return True, otherwise False
def maximus_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        return
    else:
        currentstack.append(b>a)


#Minimus Distillation
#If the first argument is lesser than the second, return True, otherwise False
def minimus_distillation(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        return
    else:
        currentstack.append(b<a)


#Maximus Distillation II
#If the first argument is greater or equal to the second, return True, otherwise False
def maximus_distillation_ii(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        return
    else:
        currentstack.append(b>=a)


#Minimus Distillation II
#If the first argument is lenn or equal to the second, return True, otherwise False
def minimus_distillation_ii(currentstack):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        return
    else:
        currentstack.append(b<=a)


#Selection Distillation
#Remove the number at the top of the stack an get the element indexed by that number from the list on the top of the stack. Return None if out of bounds
def selection_distillation(currentstack):
    num = currentstack.pop()
    if type(num) != int:
        print("needs an integer")
        return
    container = currentstack.pop()
    if type(container) != list:
        print("expected a list")
        return
    currentstack.append(container[num])


#Selection Exaltation
#Remove the two numbers at the top of the stack, replace the list on top with a sublist between those indices, both inclusive
def selection_exaltation(currentstack):
    num1 = currentstack.pop()
    num2 = currentstack.pop()
    container = currentstack.pop()
    if type(num1) != int or type(num2) != int:
        print("needs two integers and a list")
        return
    if num1 > num2:
        num1, num2 = num2, num1
    currentstack.append(container[num1:num2+1])


#Integration Distillation
#Remove the element on top of the stack and add it to the list on top of the stack
def integration_distillation(currentstack):
    element = currentstack.pop()
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        return
    container.append(element)


#Derivation Decomposition
#Remove the last element of the list on top of the stack and add it onto the stack
def derivation_decomposition(currentstack):
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        return
    currentstack.append(container.pop())


#Vacant Reflection
#Push an empty list to the top of the stack.
def vacant_reflection(currentstack):
    currentstack.append([])


#Single's Purification
#Remove the top of the stack and push a list containing only that element.
def singles_purification(currentstack):
    element = currentstack.pop()
    currentstack.append([element])


#Retrograde Purification
#Reverse the list at the top of the stack
def retrograde_purification(currentstack):
    container = currentstack.pop()
    if type(container) != list:
        print("need a list")
        return
    currentstack.append(container.reverse())


#Locator's Distillation
#Remove the top element and list on the stack and push the index of that element in the list, -1 if it does not exist.
def locators_distillation(currentstack):
    element = currentstack.pop()
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        return
    if element not in container:
        currentstack.append(-1)
    else:
        currentstack.append(container.index(element))


#Excisor's Distillation
#Remove the number at the top of the stack, then remove the element indexed by the number of the list on the top of the stack.
def excisors_distillation(currentstack):
    num = currentstack.pop()
    container = currentstack.pop()
    if type(num) != int or type(container) != list:
        print("needs an integer and a list")
        return
    del container[num]


#Surgeon's Exaltation
#Remove the top element and a number from the stack, then set the nth element of the list on top of the stack with that element
def surgeons_exaltation(currentstack):
    element = currentstack.pop()
    index = currentstack.pop()
    if type(index) != int or type(currentstack[-1]) != list: 
        print("needs an integer, an element and a list")
        return
    currentstack[-1][index] = element


#Flock's Gambit
#Remove a number and then that number many elements from the stack, push a list with all those elements.
def flocks_gambit(currentstack):
    num = currentstack.pop()
    if type(num) != int:
        print("needs an integer")
        return
    outlist = []
    for _ in range(num):
        outlist.append(currentstack.pop())
    currentstack.append(outlist)


#Flock's Disintegration
#Remove the list at the top of the stack and push each element of it to the stack
def flocks_disintegration(currentstack):
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        return
    for element in container:
        currentstack.append(element)


#Speaker's Distillation
#Remove the top element of the stack, add it as the first element to the list on top of the stack.
def speakers_distillation(currentstack):
    element = currentstack.pop()
    if type(currentstack[-1]) != list:
        print("needs a list")
        return
    currentstack[-1].insert(0, element)


#Speaker's Decomposition
#Remove the first element of the list at the top of the stack and push it to the stack.
def speakers_decomposition(currentstack):
    if type(currentstack[-1]) != list:
        print("needs a list")
        return
    element = currentstack[-1]
    del currentstack[-1]
    currentstack.append(element)


