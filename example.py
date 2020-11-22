import chains
from pprint import pprint
import json


def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding

# Load training data and build the model
#data, table = chains.process_corpus("train.csv", 100)
#print(table.pmi("move", "nsubj", "move", "nsubj"))

#function to go through the dependency pairs and find the highest "amount of information" given the first option/ second option
def gothroughdeps(deps,option):
    result=[]
    for x in deps:
        if x[0] != option[0]:
            information = table.pmi(x[0],x[1],option[0],option[1])
            result.append(information)
    
    return result

# load the pre-built model
with open("all.json") as fp:
    table = chains.ProbabilityTable(json.load(fp))


#this is my cloze test  (system passes has 45% success rate approx.)
# load testing data
test = chains.load_data("val.csv")
correct=0
total=0
for t in test:
    one, two = parse_test_instance(t)
    prot=chains.protagonist(one)
    prot2=chains.protagonist(two)

    #in case prot is not found
    try:
        testing=prot[1]
        testing2=prot2[1]
    except TypeError as ex:
        total+=1
        continue

    one_deps = chains.coreferring_pairs(one,prot[1].root)
    two_deps = chains.coreferring_pairs(two,prot2[1].root)
    
    #in case my system cant parse the dependecy pairs properly (fail the line and move on)
    if len(one_deps)==0 or len (two_deps)==0:
        total+=19
        continue
    
    oneoption = one_deps[-1]
    twooption = two_deps[-1]
    oneresult=gothroughdeps(one_deps,oneoption)
    tworesult=gothroughdeps(two_deps,twooption)
    
    #in case my system cant parse the dependecy pairs properly (fail the line and move on)  
    if len(oneresult)==0 or len (tworesult)==0:
        total+=1
        continue
    
    
    ''' my logic is that i get X amount of info by relating each of the verbs with the optional verb
        and to choose between option one and two i just need to find the average of how much information I get from each
        option and choose the option that gives more information
    '''
    # got this code from     https://careerkarma.com/blog/python-average/#:~:text=We%20can%20find%20the%20average,the%20Python%20mean()%20function.
    # average = sum(orders) / len(orders)
    oneaverage = sum(oneresult) / len(oneresult)
    twoaverage = sum(tworesult) / len(tworesult)

    if oneaverage>twoaverage:
        result = 1
    else:
        result = 2



    if result == story_answer(t)[1]:
        correct+=1
    total+=1

print ("Out of {} trials {} were succesful with {} success rate".format(total,correct,correct/total*100))




