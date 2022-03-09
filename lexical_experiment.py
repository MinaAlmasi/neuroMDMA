# Lexical Processing 
# @Mina Almasi, @Daniel Blumenkranz, @Matilde Sterup, @Anton Drasbæk Schiønning 
# @Aarhus University 2022

#### importing relevant packages #### 
import secrets
from psychopy import visual, event, core, gui, data
import pandas as pd 
import os
import numpy as np
import random


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

## Defining columns and preparing the pandas data frame for recorded data ##
columns = ["time_stamp", "id", "age", "gender","trial", "word", "wordtype", "reaction_time", "decision"]
logfile = pd.DataFrame(columns=columns)

#### TEXTS ####
intro_text = "Hello ..."
outro_text = "Thank you ..."

trial_text = "Welcome to the trial ..."

#### Wordlists ####
real = ["bread", "butter"]
center_shuffle = ["baerd","bettur"]
fully_shuffle = ["dreba","terbut"]

unshuffled = real + center_shuffle + fully_shuffle
word_list = random.sample(unshuffled, k = len(unshuffled))

trial_words = ["debat", "dabet", "betad"] #real, center_shuffle, fully_shuffle

#### SETTING UP EXPERIMENT #### 
# setting up window
win = visual.Window(fullscr = False, color = "black", monitor = "monitor")

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

# initialising clock 
clock = core.Clock()

##### SETTING UP FUNCTIONS ##### 
# displaying text 
def info(string, wait = 0):
    disp = visual.TextStim(win, text=string, height=0.2)
    disp.draw()
    win.flip()
    core.wait(wait)
    event.waitKeys()
    win.flip()

# displaying fixation cross 
stim_fix = visual.TextStim(win, '+')
numbers = np.random.uniform(low=2.0, high=5.0, size=63) #defining the varying secs fixation crosses 

def fix_cross(seconds):
    stim_fix.draw()
    win.flip()
    core.wait(seconds)

# displaying stimuli
def show_stimuli(word):
    stim = visual.TextStim(win, text = word, height = 0.3)
    stim.draw()
    win.flip()

def keypress():
    key = event.waitKeys(keyList = ["j", "n" "escape"]) [0] # "j" for "JA" and "n" for "NEJ"
    if key == "escape": #escape key to quit the programme
        core.quit()


##### RUNNING THE EXPERIMENT #####
# trial run
'''
for word in range(len(trial_words)):
    #fix_cross(numbers[word])
    show_stimuli(trial_words[word])
    if keypress() == "j":
        decision = "ja"
    elif keypress() == "n":
        decision = "nej"
'''

for n in range(len(word_list)):
    fix_cross(numbers[n])
    show_stimuli(word_list[n])
    clock.reset()
    if keypress() == "j":
        decision = "ja"
    elif keypress() == "n":
        decision = "nej" 
    reaction_time = clock.getTime()

    logfile = logfile.append({
        "time_stamp": date,
        "id": ID,
        "trial": n,
        "age": Age,
        "gender": Gender,
        "stimulus": word_list[n],
        "decision": decision,
        "reaction_time": reaction_time}, ignore_index = True)

# Defining the logfile name (NB: this solution requires us to have a "logfiles folder")
logfile_name = "logfiles/logfile_{}_{}.csv".format(ID, date)

# Saving the data our directory
logfile.to_csv(logfile_name)

