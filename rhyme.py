import pronouncing
import re
import random

# The baseline to generate text
def generateRhymes(rhythm):
    while 1:
        r = random.randrange(len(rhythm.keys()))
        if len(rhythm[r]) >= 1:
            charLine = rhythm[r] + [r]
            return random.sample(set(charLine), 2)


# Generating the rhyme scheme for the first 4 lines
def generateQuatrain(rhythm):
    a = generateRhymes(rhythm)
    b = generateRhymes(rhythm)
    return [a[1], b[1], a[0], b[0]]

# Generating the rhyme scheme for the last 6 lines
def generateSetset(rhythm):
    c = generateRhymes(rhythm)
    d = generateRhymes(rhythm)
    e = generateRhymes(rhythm)
    return [c[0], d[0], e[0], c[1], d[1], e[1]]

# Generating the complete poem
def sonnet(rhythm):
    a = generateQuatrain(rhythm)
    c = generateSetset(rhythm)
    return a + c

# Seperating each poem
def layout(curr, select):
    sonnet = ""
    for i in curr:
        sonnet += select[i] + "\n"
    return sonnet


# Reading all text used from the model
outcome = {}
txt = open("poems.txt", "r")
lines = [line.strip() for line in txt.readlines()]
comp = [re.sub(r'[^\w\s]', '', line.split(" ")[-1]) for line in lines]
lineDiction = {i:w for i, w in enumerate(lines)}
wordDiction = {i:w for i, w in enumerate(comp)}

# Making sure not to use exact words for rhyming
for i, firstIndex in wordDiction.items():
    predicted = pronouncing.rhymes(firstIndex)
    rhymes = []
    for j, secondIndex in wordDiction.items():
        if firstIndex != secondIndex:
            if secondIndex in predicted:
                rhymes.append(j)
    outcome[i] = rhymes


# Generating all outcomes to the "results.txt" file
generate = open("results.txt", "w+")
num_of_sonnets = 5
for i in range(num_of_sonnets):
    ps = layout(sonnet(outcome), lineDiction)
    generate.write(ps)
    generate.write("\n")

generate.close()