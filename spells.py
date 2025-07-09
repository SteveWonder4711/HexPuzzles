import math
import numpy as np
import copy
import main

#TODO: Add more safety and mishap detection


#True Reflection
#Adds True to the top of the stack
def true_reflection(currentstack, gameobj):
	currentstack.append(True)


#False Reflection
#Adds False to the top of the stack
def false_reflection(currentstack, gameobj):
	currentstack.append(False)


#Nullary Reflection
#Adds Null to the top of the stack
def nullary_reflection(currentstack, gameobj):
	currentstack.append(None)


#Vector Reflection Zero
#Adds (0, 0, 0) to the top of the stack
def vector_reflection_zero(currentstack, gameobj):
	currentstack.append((0, 0, 0))


#Vector Reflection +X
#Adds (1, 0, 0) to the top of the stack
def vector_reflection_px(currentstack, gameobj):
	currentstack.append((1, 0, 0))


#Vector Reflection -X
#Adds (-1, 0, 0) to the top of the stack
def vector_reflection_nx(currentstack, gameobj):
	currentstack.append((-1, 0, 0))



#Vector Reflection +Y
#Adds (0, 1, 0) to the top of the stack
def vector_reflection_py(currentstack, gameobj):
	currentstack.append((0, 1, 0))



#Vector Reflection -Y
#Adds (0, -1, 0) to the top of the stack
def vector_reflection_ny(currentstack, gameobj):
	currentstack.append((0, -1, 0))



#Vector Reflection +Z
#Adds (0, 0, 1) to the top of the stack
def vector_reflection_pz(currentstack, gameobj):
	currentstack.append((0, 0, 1))


#Vector Reflection -Z
#Adds (0, 0, -1) to the top of the stack
def vector_reflection_nz(currentstack, gameobj):
	currentstack.append((0, 0, -1))


#Circle's Reflection
#Adds τ, the radial representation of a complete circle, to the stack.
def circle_reflection(currentstack, gameobj):
	currentstack.append(math.tau)


#Arc's Reflection
#Adds π, the radial representation of half a circle, to the stack.
def arc_reflection(currentstack, gameobj):
	currentstack.append(math.pi)



#Euler's Reflection
#Adds e, the base of natural logarithms, to the stack.
def euler_reflection(currentstack, gameobj):
	currentstack.append(math.e)



#Additive Distillation
#Performs Addition
def additive_distillation(currentstack, gameobj):
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
        currentstack.append(b)
    else:
        print(f"spell not able to handle types {atype} and {btype}!")
        currentstack.append("ERROR")
	

#Subtractive Distillation
#Performs Subtraction
def subtractive_distillation(currentstack, gameobj):
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
        currentstack.append("ERROR")


#Multiplicative Distillation
#Perform multiplication or the dot product.
def multiplicative_distillation(currentstack, gameobj):
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
        currentstack.append("ERROR")

#Division Distillation
#Perform division or the cross product.
def division_distillation(currentstack, gameobj):
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
        currentstack.append("ERROR")




#Length Purification
#Compute the absolute value or length.
def length_purification(currentstack, gameobj):
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
        currentstack.append("ERROR")

#Power Distillation
#Perform exponentiation or vector projection.
def power_distillation(currentstack, gameobj):
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
        currentstack.append("ERROR")



#Floor Purification
#"Floors" a number, cutting off the fractional component and leaving an integer value. If passed a vector, instead floors each of its components.
def floor_purification(currentstack, gameobj):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        currentstack.append(math.floor(num))
    elif numtype == tuple:
        currentstack.append(tuple([math.floor(element) for element in num]))
    else:
        print(f"spell not able to handle type {numtype}!")
        currentstack.append("ERROR")

#Ceiling Purification
#"Ceilings" a number, raising it to the next integer value if it has a fractional componen. If passed a vector, instead ceils each of its components.
def ceiling_purification(currentstack, gameobj):
    num = currentstack.pop()
    numtype = type(num)
    if numtype in [int,float]:
        currentstack.append(math.ceil(num))
    elif numtype == tuple:
        currentstack.append(tuple([math.ceil(element) for element in num]))
    else:
        print(f"spell not able to handle type {numtype}!")
        currentstack.append("ERROR")


#Vector Exaltation
#Combine three numbers at the top of the stack into a vector's X, Y, and Z components (bottom to top).
def vector_exaltation(currentstack, gameobj):
    z = currentstack.pop()
    y = currentstack.pop()
    x = currentstack.pop()
    currentstack.append((x, y, z))


#Vector Disintegration
#Split a vector into its X, Y, and Z components (bottom to top).
def vector_disintegration(currentstack, gameobj):
	x, y, z = currentstack.pop()
	currentstack.append(x)
	currentstack.append(y)
	currentstack.append(z)


#Modulus Distillation
#Takes the modulus of two numbers.
def modulus_distillation(currentstack, gameobj):
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
def axial_purification(currentstack, gameobj):
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
        currentstack.append("ERROR")


#Entropy Reflection
#Creates a random number between 0 and 1
def entropy_reflection(currentstack, gameobj):
	currentstack.append(np.random.rand())


#Jester's Gambit
#Swaps the top two iotas on the stack
def jesters_gambit(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a)
    currentstack.append(b)

#Rotation Gambit
#Yanks the iota third from the top of the stack to the top
def rotation_gambit(currentstack, gameobj):
	a = currentstack.pop()
	b = currentstack.pop()
	c = currentstack.pop()
	currentstack.append(b)
	currentstack.append(a)
	currentstack.append(c)

#Rotation Gambit II
#Yanks the top iota to the third position
def rotation_gambit_ii(currentstack, gameobj):
	a = currentstack.pop()
	b = currentstack.pop()
	c = currentstack.pop()
	currentstack.append(a)
	currentstack.append(c)
	currentstack.append(b)


#Gemini Decomposition
#Duplicates the top iota
def gemini_decomposition(currentstack, gameobj):
    currentstack.append(copy.deepcopy(currentstack[-1]))	


#Prospector's Gambit
#Copy the second-to-last iota to the top
def prospectors_gambit(currentstack, gameobj):
	currentstack.append(copy.deepcopy(currentstack[-2]))


#Undertaker's Gambit
#Copy the top iota of the stack, put it under the second
def undertakers_gambit(currentstack, gameobj):
	a = currentstack.pop()
	b = currentstack.pop()
	currentstack.append(a)
	currentstack.append(b)
	currentstack.append(copy.deepcopy(a))


#Gemini Gambit
#Removes the number at the top of the stack, copies the next iota that number of times
def gemini_gambit(currentstack, gameobj):
    num = currentstack.pop()
    item = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        currentstack.append("ERROR")
        return
    for _ in range(num):
        currentstack.append(copy.deepcopy(item))


#Dioscuri Gambit
#Copy the top two iotas of the stack
def dioscuri_gambit(currentstack, gameobj):
	currentstack.append(copy.deepcopy(currentstack[-2]))
	currentstack.append(copy.deepcopy(currentstack[-2]))


#Flock's Reflection
#Pushes the size of the stack 
def flocks_reflection(currentstack, gameobj):
	currentstack.append(len(currentstack))


#Fisherman's Gambit
#Grabs the element in the stack indexed by the number and brings it to the top. If the number is negative, instead moves the top iota down that many elements
def fishermans_gambit(currentstack, gameobj):
    num = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        currentstack.append("ERROR")
        return
    if num >= 0:
        item = copy.deepcopy(currentstack[-num-1])
        del currentstack[-num-1]
        currentstack.append(item)
    else:
        item = currentstack.pop()
        currentstack.insert(len(currentstack)+num, item)


#Fisherman's Gambit II
#Like Fisherman's Gambit, but copies instead of moving
def fishermans_gambit_ii(currentstack, gameobj):
    num = currentstack.pop()
    if type(num) != int:
        print("this spell needs a number at the top of the stack")
        currentstack.append("ERROR")
        return
    if num >= 0:
        item = currentstack[-num-1]
        currentstack.append(copy.deepcopy(item))
    else:
        item = currentstack[-1]
        currentstack.insert(len(currentstack)+num-1, copy.deepcopy(item))


#Swindler's Gambit
#Rearranges the top elements based on the provided Lehmer Code
def swindlers_gambit(currentstack, gameobj):
    code = currentstack.pop()
    if type(code) != int:
        print("lehmer code needs to be an integer")
        currentstack.append("ERROR")
        return
    #factorials up to 720
    factorials = [1, 2, 6, 24, 120, 720]
    i = 0
    while factorials[i] <= code:
        i += 1
    if i > len(currentstack):
        print("not enough iotas on stack for lehmer code")
        currentstack.append("ERROR")
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
def augurs_purification(currentstack, gameobj):
    argument = currentstack.pop()
    if argument in [0, None, False]:
        currentstack.append(False)
    else:
        currentstack.append(True)


#Negation Purification
#Inverts the boolean argument
def negation_purification(currentstack, gameobj):
    argument = currentstack.pop()
    if type(argument) == bool:
        currentstack.append(False if argument else True)
    elif type(argument) == int:
        currentstack.append(argument*-1-1)
    else:
        print("argument needs to be bool!")
        currentstack.append("ERROR")
        return
    


#Disjunction Distillation
#Performs boolean OR
def disjunction_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) == bool or type(b) == bool:
        currentstack.append(True if a or b else False)
    elif type(a) == int and type(b) == int:
        bitsa = a.to_bytes(4, signed=True)
        bitsb = b.to_bytes(4, signed=True)
        outbits = [bitsa[i] | bitsb[i] for i in range(4)]
        currentstack.append(outbits)
    elif type(a) == list and type(b) == list:
        outlist = a
        for element in b:
            if element not in outlist:
                outlist.append(element)
        currentstack.append(outlist)
    else:
        print(f"spell cannot handle types {type(a)} and {type(b)}!")
        currentstack.append("ERROR")
        return
    

#Conjunction Distillation
#Performs boolean AND
def conjunction_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) == bool and type(b) == bool:
        currentstack.append(True if a and b else False)
    elif type(a) == int and type(b) == int:
        bitsa = a.to_bytes(4, signed=True)
        bitsb = b.to_bytes(4, signed=True)
        outbits = [bitsa[i] & bitsb[i] for i in range(4)]
        currentstack.append(outbits)
    elif type(a) == list and type(b) == list:
        outlist = []
        for element in a:
            if element in b:
                outlist.append(element)
        currentstack.append(outlist)
    else:
        print(f"spell cannot handle types {type(a)} and {type(b)}!")
        currentstack.append("ERROR")
        return


#Exclusion Distillation
#Performs boolean XOR
def exclusion_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) == bool or type(b) == bool: 
        currentstack.append(True if (a ^ b) else False)
    elif type(a) == int and type(b) == int:
        bitsa = a.to_bytes(4, signed=True)
        bitsb = b.to_bytes(4, signed=True)
        outbits = [bitsa[i] ^ bitsb[i] for i in range(4)]
        currentstack.append(outbits)
    elif type(a) == list and type(b) == list:
        outlist = []
        for element in a:
            if element not in b:
                outlist.append(element)
        for element in b:
            if element not in a:
                outlist.append(element)
        currentstack.append(outlist)

    else:
        print("both arguments need to be booleans")
        currentstack.append("ERROR")
        return


#Augur's Exaltation
#If the first argument is True, keep the second and discard the third. Otherwise vice versa
def augurs_exaltation(currentstack, gameobj):
    sel = currentstack.pop()
    if type(sel) != bool:
        print("needs a boolean value as selector")
        currentstack.append("ERROR")
        return
    if sel:
        del currentstack[-2]
    else:
        del currentstack[-1]


#Equality Distillation
#If the first two arguments are equal, return True, otherwise False
def equality_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a == b)


#Inequality Distillation
#If the first two arguments are not equal, return True, otherwise False
def inequality_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    currentstack.append(a != b)



#Maximus Distillation
#If the first argument is greater than the second, return True, otherwise False
def maximus_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        currentstack.append("ERROR")
        return
    else:
        currentstack.append(b>a)


#Minimus Distillation
#If the first argument is lesser than the second, return True, otherwise False
def minimus_distillation(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        currentstack.append("ERROR")
        return
    else:
        currentstack.append(b<a)


#Maximus Distillation II
#If the first argument is greater or equal to the second, return True, otherwise False
def maximus_distillation_ii(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        currentstack.append("ERROR")
        return
    else:
        currentstack.append(b>=a)


#Minimus Distillation II
#If the first argument is lenn or equal to the second, return True, otherwise False
def minimus_distillation_ii(currentstack, gameobj):
    a = currentstack.pop()
    b = currentstack.pop()
    if type(a) not in [int,float] or type(b) not in [int,float]:
        print("needs two numbers")
        currentstack.append("ERROR")
        return
    else:
        currentstack.append(b<=a)


#Selection Distillation
#Remove the number at the top of the stack an get the element indexed by that number from the list on the top of the stack. Return None if out of bounds
def selection_distillation(currentstack, gameobj):
    num = currentstack.pop()
    if type(num) != int:
        print("needs an integer")
        currentstack.append("ERROR")
        return
    container = currentstack.pop()
    if type(container) != list:
        print("expected a list")
        currentstack.append("ERROR")
        return
    currentstack.append(container[num])


#Selection Exaltation
#Remove the two numbers at the top of the stack, replace the list on top with a sublist between those indices, both inclusive
def selection_exaltation(currentstack, gameobj):
    num1 = currentstack.pop()
    num2 = currentstack.pop()
    container = currentstack.pop()
    if type(num1) != int or type(num2) != int:
        print("needs two integers and a list")
        currentstack.append("ERROR")
        return
    if num1 > num2:
        num1, num2 = num2, num1
    currentstack.append(container[num1:num2+1])


#Integration Distillation
#Remove the element on top of the stack and add it to the list on top of the stack
def integration_distillation(currentstack, gameobj):
    element = currentstack.pop()
    container = currentstack[-1]
    if type(container) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    container.append(element)


#Derivation Decomposition
#Remove the last element of the list on top of the stack and add it onto the stack
def derivation_decomposition(currentstack, gameobj):
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    currentstack.append(container.pop())


#Vacant Reflection
#Push an empty list to the top of the stack.
def vacant_reflection(currentstack, gameobj):
    currentstack.append([])


#Single's Purification
#Remove the top of the stack and push a list containing only that element.
def singles_purification(currentstack, gameobj):
    element = currentstack.pop()
    currentstack.append([element])


#Retrograde Purification
#Reverse the list at the top of the stack
def retrograde_purification(currentstack, gameobj):
    container = currentstack.pop()
    if type(container) != list:
        print("need a list")
        currentstack.append("ERROR")
        return
    currentstack.append(container.reverse())


#Locator's Distillation
#Remove the top element and list on the stack and push the index of that element in the list, -1 if it does not exist.
def locators_distillation(currentstack, gameobj):
    element = currentstack.pop()
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    if element not in container:
        currentstack.append(-1)
    else:
        currentstack.append(container.index(element))


#Excisor's Distillation
#Remove the number at the top of the stack, then remove the element indexed by the number of the list on the top of the stack.
def excisors_distillation(currentstack, gameobj):
    num = currentstack.pop()
    container = currentstack.pop()
    if type(num) != int or type(container) != list:
        print("needs an integer and a list")
        currentstack.append("ERROR")
        return
    del container[num]


#Surgeon's Exaltation
#Remove the top element and a number from the stack, then set the nth element of the list on top of the stack with that element
def surgeons_exaltation(currentstack, gameobj):
    element = currentstack.pop()
    index = currentstack.pop()
    if type(index) != int or type(currentstack[-1]) != list: 
        print("needs an integer, an element and a list")
        currentstack.append("ERROR")
        return
    currentstack[-1][index] = element


#Flock's Gambit
#Remove a number and then that number many elements from the stack, push a list with all those elements.
def flocks_gambit(currentstack, gameobj):
    num = currentstack.pop()
    if type(num) != int:
        print("needs an integer")
        currentstack.append("ERROR")
        return
    outlist = []
    for _ in range(num):
        outlist.append(currentstack.pop())
    outlist.reverse()
    currentstack.append(outlist)


#Flock's Disintegration
#Remove the list at the top of the stack and push each element of it to the stack
def flocks_disintegration(currentstack, gameobj):
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    for element in container:
        currentstack.append(element)


#Speaker's Distillation
#Remove the top element of the stack, add it as the first element to the list on top of the stack.
def speakers_distillation(currentstack, gameobj):
    element = currentstack.pop()
    if type(currentstack[-1]) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    currentstack[-1].insert(0, element)


#Speaker's Decomposition
#Remove the first element of the list at the top of the stack and push it to the stack.
def speakers_decomposition(currentstack, gameobj):
    if type(currentstack[-1]) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    element = currentstack[-1]
    del currentstack[-1]
    currentstack.append(element)


#Scribe's Reflection
#Pushes an iota from the level input onto the stack
def scribes_reflection(currentstack, gameobj):
    if len(gameobj.levelinputs) == 0:
        print("Level inputs empty!")
        currentstack.append("ERROR")
        return
    currentstack.append(gameobj.levelinputs[0])
    del gameobj.levelinputs[0]


#Scribe's Gambit
#Removes the top iota and outputs it
def scribes_gambit(currentstack, gameobj):
    element = currentstack.pop()
    gameobj.leveloutputs.append(element)


#Huginn's Gambit
#Removes the top iota from the stack and saves it to my ravenmind.
def huginns_gambit(currentstack, gameobj):
    element = currentstack.pop()
    gameobj.ravenmind = element


#Munnin's Reflection
#Copy the iota out of my ravenmind and push it onto the stack.
def munnins_reflection(currentstack, gameobj):
    currentstack.append(gameobj.ravenmind) 


#Sine Purification
#Takes the sine of an angle in radians.
def sine_purification(currentstack, gameobj):
    angle = currentstack.pop()
    if type(angle) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    currentstack.append(math.floor(math.sin(angle)*1e+10)/1e+10)


#Cosine Purification
#Takes the cosine of an angle in radians.
def cosine_purification(currentstack, gameobj):
    angle = currentstack.pop()
    if type(angle) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    currentstack.append(math.floor(math.cos(angle)*1e+10)/1e+10)


#Tanent Purification
#Takes the tangent of an angle in radians.
def tanent_purification(currentstack, gameobj):
    angle = currentstack.pop()
    if type(angle) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    currentstack.append(math.floor(math.tan(angle)*1e+10)/1e+10)


#Inverse Sine Purification
#Takes the inverse sine value of a value bbetween -1 and 1
def inverse_sine_purification(currentstack, gameobj):
    value = currentstack.pop()
    if type(value) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    if value > 1 or value < -1:
        print("needs a value between -1 and 1!")
        currentstack.append("ERROR")
    currentstack.append(math.floor(math.asin(value)*1e+10)/1e+10)


#Inverse Cosine Purification
#Takes the inverse cosine value of a number between -1 and 1
def inverse_cosine_purification(currentstack, gameobj):
    value = currentstack.pop()
    if type(value) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    if value > 1 or value < -1:
        print("needs a value between -1 and 1!")
        currentstack.append("ERROR")
    currentstack.append(math.floor(math.acos(value)*1e+10)/1e+10)


#Takes the inverse tangent of a value
#Takes the inverse tangent of a value
def inverse_tangent_purification(currentstack, gameobj):
    value = currentstack.pop()
    if type(value) not in [int,float]:
        print("needs a number!")
        currentstack.append("ERROR")
        return
    currentstack.append(math.floor(math.atan(value)*1e+10)/1e+10)


#Inverse Tangent Distillation
#Takes the inverse tangent of a Y and X value
def inverse_tangent_distillation(currentstack, gameobj):
    y = currentstack.pop()
    x = currentstack.pop()
    if type(x) not in [int,float] or type(y) not in [int, float]:
        print("needs two numbers!")
        currentstack.append("ERROR")
        return
    value = y/x
    currentstack.append(math.floor(math.atan(value)*1e+10)/1e+10)


#Logarithmic Distillation
#Takes the logarithm with the base on the top of the stack of the number second to the top of the stack.
def logarithmic_distillation(currentstack, gameobj):
    base = currentstack.pop()
    x = currentstack.pop()
    if type(x) not in [int,float] or type(base) not in [int, float]:
        print("needs two numbers!")
        currentstack.append("ERROR")
        return
    currentstack.append(math.floor(math.log(x, base)*1e+10)/1e+10)


#Uniqueness Purification
#Removes duplicate entries from a list
def uniqueness_purification(currentstack, gameobj):
    container = currentstack.pop()
    if type(container) != list:
        print("needs a list")
        currentstack.append("ERROR")
        return
    newlist = []
    for element in container:
        if element not in newlist:
            newlist.append(element)
    currentstack.append(newlist)


def elementtospell(element):
    if type(element) != str:
        return None
    elif not element.startswith("<") or not element.endswith(">"):
        print("wrong formatted pattern")
        return None
    else:
        spell = []
        for letter in element:
            if letter not in ["<", ">"]:
                spell.append(int(letter))
        return spell


#Hermes' Gambit
#Remove a pattern or list of petterns and cast them, escaped patterns get pushed to the stack.
def hermes_gambit(currentstack, gameobj):
    gameobj.executiondepth += 1
    currentdepth = gameobj.executiondepth
    patterns = currentstack.pop()
    if type(patterns) == str:
       spell = elementtospell(patterns)
       main.executespell(spell, currentstack, gameobj)
    elif type(patterns) == list:
        for pattern in patterns:
            if type(pattern) == str:
                if gameobj.executiondepth < currentdepth:
                    return
                spell = elementtospell(pattern)
                main.executespell(spell, currentstack, gameobj)
    gameobj.executiondepth -= 1


#Iris' Gambit
#Like Hermes' Gambit, but push a Jump iota that when executed jumps directly to the end of the pattern list.
def iris_gambit(currentstack, gameobj):
    print("sorry did not implement that yet")


#Thot's Gambit
#Cast the list of patterns atthe top of the stack once for every element of the second list. Push Iotas remaining after every element on the main stack
def thots_gambit(currentstack, gameobj):
    container = currentstack.pop()
    patterns = currentstack.pop()
    if type(patterns) != list or type(container) != list:
        print("needs a list of patterns and another list")
        currentstack.append("ERROR")
        return
    output = []
    for element in container:
        print(f"thotting {element}")
        skip = False
        gameobj.executiondepth += 1
        currentdepth = gameobj.executiondepth
        tempstack = copy.deepcopy(currentstack)
        tempstack.append(element)
        for pattern in patterns:
            if gameobj.executiondepth < currentdepth:
                skip = True
                break
            spell = elementtospell(pattern)
            main.executespell(spell, tempstack, gameobj)
        if not skip:
            for element in tempstack:
                output.append(element)
    print(output)
    currentstack.append(output)
        







#Charon's Gambit
#Forcibly halts a Hex. Only exits one Iteration of Thot's Gambit
def charons_gambit(currentstack, gameobj):
    gameobj.executiondepth -= 1


