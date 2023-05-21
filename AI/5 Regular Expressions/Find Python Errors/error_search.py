import sys
import re
"""
-  A variable in python can contain any word character, [A-Za-z0-9_], but can’t begin with a digit.  Find variable 
names that begin with digits.  (Even cooler if you can exclude results between " or ' marks, to ignore strings.  
That doesn’t have to be done using regex, though it can be.) 
• Any variable in python followed by any number of spaces (including zero) and then an opening parenthesis can 
be assumed to be a function call or a function definition.  Find any function calls to undefined functions. 
• Look for java code by mistake - specifically, looking for variable declarations with the type infront of them
    i.e int num = 3;
    Char ch = "A";
    String str = "abc";
• Find situations where == has been used instead of =. 
• Find missing colons
"""
filename = sys.argv[1]
# open the file
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]
# read in the lines of code
# print(lines)


# check for variables starting with digits
# for each line: split the line by nonword characters and parse each word token:
    # if word matches [appropriate regex expression] - add specify line
isVar = r"^\w+$"
regvar = re.compile(isVar)
lineswitherrors = []
for index in range(len(lines)):
    line = lines[index]
    tokens = re.split("[^a-zA-Z0-9_\'\"]",line)
    for t in tokens:
        if len(t) > 0 and re.match(isVar,t):
            if not t.isdigit() and t[0].isdigit():
                # print("Line",index+1," has a variable ",t,"beginning with a digit.")
                if index+1 not in lineswitherrors:
                    lineswitherrors.append(index+1)
print("lines with variable names starting with digits: ",lineswitherrors)
print()
# check for undefined function calls
    # 1 find all defined functions
    # 2 if function call not in defined functions - specify line with error
# 1 look for defined functions
fcncall = r"\w*def\s*\w*\s*[(]"
regcall = re.compile(fcncall)
# defined function
fcns = set(["len","range","print"])

fcnname = r"\s*\w*[(]"
regname = re.compile(fcnname)
for line in lines:
    if re.match(regcall,line):
        # parse function name
        for result in re.finditer(regname,line):
            start,end = result.span()
            functionName = line[start:end-1].strip()
            fcns.add(functionName)
# 2 find undefined variable names 
errorlines = []
for i in range(len(lines)):
    line = lines[i]
    if not re.match(regcall,line):
        for result in re.finditer(regname,line):
            start,end = result.span()
            name = line[start:end-1].strip()
            if name not in fcns:
                errorlines.append(i+1)
print("Lines with undefined functions: ",errorlines)
print()
# check for type declaration in front of variable (aka space in variable name)
    # \s*something\s*varname = .* anything
wrongformat = r"\s*\w+\s+\w+\s*[=].*"
regex = re.compile(wrongformat)
badformatlines = []
for index in range(len(lines)):
    if re.match(regex, lines[index]):
        badformatlines.append(index+1)
print("Lines with type declaration in front of variable name: ",badformatlines)
print()
# check for == instead of =
    # look at all variable assignments
    # if uses == instead of = then error

varformat = r"(\s|\w)*[=]\s*[=].*(?!:)"
badvar = re.compile(varformat)
badvarlines = []
for index in range(len(lines)):
    if re.match(badvar,lines[index]):
        badvarlines.append(index+1)
print("Lines with == instead of = for variable assignment: ",badvarlines)
print()
# check for missing colons - at the end of lines with def, for, while, if, elif, else, try, except
keywords = {"def","for","while","elif","else","try","except","if"}
missingcolon = []
for index,line in enumerate(lines):
    tokens = re.split(r"\W",line)
    for t in tokens:
        if t in keywords and line[-1]!=":":
            missingcolon.append(index+1)
print("lines missing colons: ",missingcolon)