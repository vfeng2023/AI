from colorama import init,Back,Fore
import re
import sys
init()

toMatch = sys.argv[1]
# text,flags = toMatch.split("/")[1:]
vals = toMatch.split("/")[1:]
text = vals[0]
flags = ""
if len(vals) > 1:
    flags = vals[-1]
flagArgs = None
for flag in flags:
    if flagArgs is None:
        if flag == "i":
            flagArgs = re.I
        elif flag == "m":
            flagArgs = re.M
        elif flag == "s":
            flagArgs = re.S
    else:
        if flag == "i":
            flagArgs = flagArgs|re.I
        elif flag == "m":
            flagArgs = flagArgs|re.M
        elif flag == "s":
            flagArgs = flagArgs|re.S
if flagArgs is None:
    exp = re.compile(text)
else:
    exp = re.compile(text,flagArgs)
# string to run re on
# string = "While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?"
string = sys.argv[2]
annotatedStr = ""
startIndex = 0
colors = [Back.LIGHTYELLOW_EX,Back.CYAN]
colorIndex = 0
matches = 0
for result in exp.finditer(string):
    matches += 1
    reStart,reEnd = result.span()
    annotatedStr += string[startIndex:reStart]
    highlightcolor = colors[colorIndex]
    if reStart == startIndex and startIndex!=0:
        colorIndex = (colorIndex+1)%2
        highlightcolor = colors[colorIndex]
    annotatedStr += highlightcolor + string[reStart:reEnd] + Back.RESET
    startIndex = reEnd
annotatedStr += string[startIndex:]
print(annotatedStr)
print("Total matches",matches)
