# Lexical Processing 
# @Mina Almasi, @Daniel Blumenkranz, @Matilde Sterup, @Anton Drasbæk Schiønning 
# @Aarhus University 2022

#### importing relevant packages #### 
from psychopy import visual, event, core, gui, data
import pandas as pd 
import os
import numpy as np
import random
from triggers import setParallelData

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 20  # Width of your monitor in cm
MON_SIZE = [1200, 1000]  # Pixel-dimensions of your monitor
FRAME_RATE = 60 # Hz  [120]
SAVE_FOLDER = 'faceWord_exp_data'  # Log is saved to this folder. The folder is created if it does not exist.
RUNS = 3 # Number of sessions to loop over (useful for EEG experiment)
MAX_DURATION_SEC = 20 #max duration of each trial 
MAX_FRAMES = FRAME_RATE * MAX_DURATION_SEC


#### preparing GUI ####
dialog = gui.Dlg(title = "Lexical Processing Experiment")
dialog.addField("Participant ID:")
dialog.addField("Age:")
dialog.addField("Gender:", choices = ["Female", "Male", "Other"])

dialog.show()  #showing the dialog box 

#saving the dialog box
if dialog.OK: #if the person presses OK
    ID = dialog.data[0]
    Age = dialog.data[1]
    Gender = dialog.data[2]
elif dialog.Cancel: #if the person presses Cancel 
    core.quit()

#defining columns and preparing the pandas data frame for recorded data 
columns = ["time_stamp", "id", "age", "gender","trial", "word", "wordtype", "reaction_time", "decision", "trigger_word", "trigger_decision"]
logfile = pd.DataFrame(columns=columns)

#### TEXTS ####
intro_text = """ Velkommen til eksperimentet. \n\n
Du vil blive præsenteret for nogle ord et ad gangen.  \n\n
Din opgave er at svare på, om ordet er et rigtigt dansk ord. 
Tast 'J' for ja, hvis det er et dansk ord og 'N' for nej, hvis det ikke er. \n\n
Alle rigtige ord er kendte danske ord.  \n\n
Du bedes indikere dit svar hurtigst muligt.\n\n
Før det rigtige eksperiment begynder, kommer der en prøverunde. \n\n
Tryk på en vilkårlig tast, når du er klar til at starte prøverunden. 
"""

outro_text = "Eksperimentet er nu færdigt. Tusind tak for din deltagelse."

trial_outro_text = """ Du har nu gennemført prøverunden.  \n\n 
Tryk på en vilkårlig tast, når du er klar til at begynde eksperimentet.
"""

#### WORDLISTS ####
# defining the words
real = ["krone", "penge", "minut", "grund", "måned", "skole", "aften", "parti", "antal", "musik", "kirke", "sæson", "kraft", "aktie", "medie", "firma", "hoved", "pause", "værdi", "butik", "fokus", "årsag", "april", "besøg", "ønske", "natur", "sprog", "bolig", "roman", "alvor", "titel"]
center_shuffle = ["knore", "pnege", "munit", "gnurd", "menåd", "sloke", "atfen", "patri", "atnal", "misuk", "krike", "sosæn", "karft", "atike", "meide", "frima", "hevod", "pasue", "vrædi", "bituk", "fukos", "åsarg", "arpil", "bøseg", "ønkse", "nutar", "sporg", "bilog", "ramon", "avlor", "tetil"]
fully_shuffle = ["rekon", "gepen", "nimtu", "drugn", "dåmen", "koles", "netaf", "irtap", "talan", "iksum", "ekkir", "næsno", "tarfk", "etiak", "emeid", "arfim", "vedoh", "sapeu", "ridæv", "iktub", "sofku", "garså", "lipra", "gøbes", "kønse", "urtan", "grops", "obgil", "omarn", "lavro", "letti"]
foreign = ["ᚴᚱᛟᚾᛖ", "ᛈᛖᚾᚷᛖ", "ᛗᛁᚾᚢᛏ", "ᚷᚱᚢᚾᛞ", "ᛗᚨᚾᛖᛞ", "ᛋᚴᛟᛚᛖ", "ᚨᚠᛏᛖᚾ", "ᛈᚨᚱᛏᛁ", "ᚨᚾᛏᚨᛚ", "ᛗᚢᛋᛁᚴ", "ᚴᛁᚱᚴᛖ", "ᛋᛖᛋᛟᚾ", "ᚴᚱᚨᚠᛏ", "ᚨᚴᛏᛁᛖ", "ᛗᛖᛞᛁᛖ", "ᚠᛁᚱᛗᚨ", "ᚺᛟᚡᛖᛞ", "ᛈᚨᚢᛋᛖ", "ᚡᛖᚱᛞᛁ", "ᛒᚢᛏᛁᚴ", "ᚠᛟᚴᚢᛋ", "ᚨᚱᛋᚨᚷ", "ᚨᛈᚱᛁᛚ", "ᛒᛖᛋᛟᚷ", "ᛟᚾᛋᚴᛖ", "ᚾᚨᛏᚢᚱ", "ᛋᛈᚱᛟᚷ", "ᛒᛟᛚᛁᚷ", "ᚱᛟᛗᚨᚾ", "ᚨᛚᚡᛟᚱ", "ᛏᛁᛏᛖᛚ"]

# combining the lists
unshuffled = real + center_shuffle + fully_shuffle + foreign
labels = ("real," * len(real) + "center_shuffle," * len(center_shuffle) + "fully_shuffle," * len(fully_shuffle)+ "foreign,"*len(foreign)).split(",")
labels = labels[0:-1]

# adding word type
word_dict_unshuffled = {key:value for key, value in zip(unshuffled, labels)}

# shuffling
l = list(word_dict_unshuffled.items()) #creating an ordered list of the items
random.shuffle(l) #shuffling the list
word_dict_shuffled = dict(l) #remaking the dictionary

# trial words
trial_words = ["debat", "dabet", "betad", "ᛞᛖᛒᚨᛏ"]
trial_wordtype = ["real", "center_shuffle", "fully_shuffle", "foreign"]
trial_fixation_time = [2, 4, 3, 2]

#### SETTING UP EXPERIMENT ####
# setting up window
win = visual.Window(fullscr = True, color = "black", monitor = "monitor")

# setting up text field
text = visual.TextStim(win, text='')

# getting the timestamp for unique logfile id
date = data.getDateStr()

# making sure there is a logfile directory
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

# setting up the log file
DATA = pd.DataFrame(columns = ["time_stamp", "global_time", "ID", "trigger", "Age", "Gender"])
filename = "logfiles/logfile_{}_{}.csv".format(ID, date)

# setting relative logfile path
path = "logfiles/"

# initialising clock and making sure trigger is off
clock = core.Clock()
pullTriggerDown = False

# setting up allowed keys 
keys = ["j", "n", "escape"] # "j" for "JA" and "n" for "NEJ"

##### SETTING UP FUNCTIONS #####
# displaying text
def info(string, height, wait = 0) :
    disp = visual.TextStim(win, text=string, height=height)
    disp.draw()
    win.flip()
    core.wait(wait)
    event.waitKeys()
    win.flip()

# displaying fixation cross
stim_fix = visual.TextStim(win, '+')
numbers = np.random.uniform(low=2.0, high=5.0, size=124) #defining the varying secs fixation crosses

def fix_cross(seconds):
    stim_fix.draw()
    win.flip()
    core.wait(seconds)

# drawing stimuli
def draw_stimuli(word):
    stim = visual.TextStim(win, text = word, height = 0.3)
    stim.draw()

# setting triggers
def word_trigger(wordtype):
    if wordtype == "real":
        TRIG_W = 1
    elif wordtype == "center_shuffle":
        TRIG_W = 2
    elif wordtype == "fully_shuffle":
        TRIG_W = 3
    elif wordtype == "foreign":
        TRIG_W = 4
    
    return TRIG_W

def decision_trigger(wordtype, decision):
    if wordtype == "real" and decision == "ja":
        TRIG_D = 11 #first number denotes the decision (1 = ja, 2 = nej), second number denotes the wordtype (1 = real, 2 = center_shuffle, 3 = fully_shuffle, 4 = foreign)
    elif wordtype == "real" and decision == "nej":
        TRIG_D = 21
    elif wordtype == "center_shuffle" and decision == "ja":
        TRIG_D = 12
    elif wordtype == "center_shuffle" and decision == "nej":
        TRIG_D = 22
    elif wordtype == "fully_shuffle" and decision == "ja":
        TRIG_D = 13
    elif wordtype == "fully_shuffle" and decision == "nej":
        TRIG_D = 23
    elif wordtype == "foreign" and decision == "ja":
        TRIG_D = 14
    elif wordtype == "foreign" and decision == "nej":
        TRIG_D = 24
    
    return TRIG_D

##### RUNNING THE EXPERIMENT #####
# info text 1
info(intro_text, 0.08)

# trial run
for n in range(len(trial_words)):
    fix_cross(trial_fixation_time[n])
    draw_stimuli(trial_words[n])
    win.flip()
    event.waitKeys(keyList = keys)

# end of trial run text
info(trial_outro_text, 0.1)

# real experiment
for n in range(len(word_dict_shuffled)):
    fix_cross(numbers[n])

    for frame in range(MAX_FRAMES): #for loop to ensure that the trigger is turned on the first frame that the stimuli is shown
        draw_stimuli(list(word_dict_shuffled.keys())[n])
        
        if frame == 1:
            win.callOnFlip(setParallelData, word_trigger(list(word_dict_shuffled.values())[n])) #word_trigger function with wordtype
            pullTriggerDown = True
            clock.reset()

        win.flip() #flipping the window to show the stimuli
        key = event.getKeys(keyList=keys)
        if pullTriggerDown:
            win.callOnFlip(setParallelData, 0)
            pullTriggerDown = False
        
        try: #try statement evaluating keypresses 
            if key[0] == "j":
                decision = "ja"
                win.callOnFlip(setParallelData, decision_trigger(list(word_dict_shuffled.values())[n], decision))
                pullTriggerDown = True
                reaction_time = clock.getTime()
                break
            elif key[0] == "n":
                decision = "nej"
                win.callOnFlip(setParallelData, decision_trigger(list(word_dict_shuffled.values())[n], decision))
                pullTriggerDown = True
                reaction_time = clock.getTime()
                break
            elif key[0] == "escape": # escape key to quit the programme
                core.quit()
        except:
            len(key) == 0 # if no key is pressed, the loop will continue
    
        if pullTriggerDown: 
            win.callOnFlip(setParallelData, 0)
            pullTriggerDown = False

    # appending the data from one trial to the logfile before the next loop starts
    logfile = logfile.append({
        "time_stamp": date,
        "id": ID,
        "trial": n,
        "age": Age,
        "gender": Gender,
        "word": list(word_dict_shuffled.keys())[n],
        "wordtype": list(word_dict_shuffled.values())[n],
        "decision": decision,
        "trigger_word": word_trigger(list(word_dict_shuffled.values())[n]),
        "trigger_decision": decision_trigger(list(word_dict_shuffled.values())[n], decision), #values() defined for wordtype
        "reaction_time": reaction_time}, ignore_index = True)

# Defining the logfile name (NB: this solution requires us to have a "logfiles folder")
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

# Saving the data our directory
logfile.to_csv(logfile_name)

# end of experiment text
info(outro_text, 0.1)
