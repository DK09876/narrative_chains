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

# load testing data
test = chains.load_data("oop.csv")
for t in test:
    one, two = parse_test_instance(t)
    # one_deps = chains.extract_dependency_pairs(one)
    prot=chains.protagonist(one)
    prot2=chains.protagonist(two)
    one_deps = chains.coreferring_pairs(one,prot[1].root)
    print (one_deps)
    two_deps = chains.coreferring_pairs(two,prot2[1].root)
    oneoption = one_deps[-1]
    twooption = two_deps[-1]
    oneresult=gothroughdeps(one_deps,oneoption)
    tworesult=gothroughdeps(two_deps,twooption)
    print (oneresult)
    
    ''' my logic is that i get X amount of info by relating each of the verbs with the optional verb
        and to choose between option one and two i just need to find the average of how much information I get from each
        option and choose the option that gives more information
    '''
    # got this code from     https://careerkarma.com/blog/python-average/#:~:text=We%20can%20find%20the%20average,the%20Python%20mean()%20function.
    # average = sum(orders) / len(orders)
    #oneaverage = sum(oneresult) / len(oneresult)
    #twoaverage = sum(tworesult) / len(tworesult)

    # if oneaverage>twoaverage:
    #     result = 1
    # else:
    #     result = 2

    # print (result)
   # pprint(one[2:])
    #pprint(two[2:])
    
    #pprint("answer:"+ str(story_answer(t)))




