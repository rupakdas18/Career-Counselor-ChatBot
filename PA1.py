# -*- coding: utf-8 -*-
"""
Course: CS 5242: Natural Language Processing
Programming Assignment 1
Eliza the Career Counselor
@author: Rupak Kumar Das
"""

# import libraries (regular expression, random, ast and sys)
import re
import ast
import sys
import random

# Introduction
def intro():
    print("[Eliza]< This is Eliza program written by Rupak. I am a career counselor\
            for college students who are close to graduation.")
          
# Open a .txt file which has a dictionary that contains different patterns.
# This DIctionary is also attached at the end of the program.
with open('keywords.txt') as f:
    keywords = f.read()
keywords = ast.literal_eval(keywords)


# Memory to store name, major and city/place where the user lives
Memory = {'name':[],
          'depatmet':[],
          'place':[]}


# Some intermediate variables                      
user = '' 
dept = ''
username=[] 

        
#This is the response Functions based on user input
def respond(message):     
    
#if user says exit/bye/goodbye/see you later, it will leave the conversation.
    if re.search(r".*(exit|bye|goodbye|see you later).*",message):
        print("[Eliza]< Have a Nice day " + user )
        sys.exit()
        
#If the user talks about his living place it will store it in the memory        
    elif re.search(r".*([Ii] am from |[Ii] live|[My] famili lives|[iI]'m from).*",message):
# Store the city into memory
        Memory['place']= department(message)
        reply = ("You told me you are from {}. How it will impact on you careerr?").format(Memory['place'])
        more_topics['place'] = ([reply])
        

# This count variable is to avoid getting stuck in conversational loops           
    global count
    

# This loop is for searching keywords (if any) that matches with the user input.
# If it maches, then it prints the associated response.
    for pattern, value in keywords.items():
        match = re.search(pattern,message)
        if match:
            count = 0
            reply = (random.choice(value))
            reply = (reply+' {}')            
            print('[Eliza]< ' + reply.format(random.choice(Memory['name'])))
            break
        else:
            value = 'default'
            
            
# if the user input doesn't match with pattern, it will transform the sentence into simple 
# question for 2 times. After that it will ask a question randomly to the user. The "count" variable
# is used for this reason. "modify_user_input" function is for pronoun flipping.
             
    if value == 'default':
        count = count+1
        if count<2:
            print('[Eliza]< ' + random.choice(keywords[value]) + modify_user_input(message)) 
        else:
            value = random.choice(list(more_topics.keys()))
            print('[Eliza]< '+ random.choice(more_topics[value]))
                    
# This is the gibberish detector. It would be better if we could use any existing dictionary
#to detect gibberish word. But here if the length of the sentence is greater than 8 and if it 
#doesn't have any space, then I am considering it as a gibberish word. It will work for some cases but
# will fail for other cases.
                
def gibberish_detect(message):
    if len(message)>8:
        check = re.search(" ",message)
        if check:
             respond(message)
        else:
            print("[Eliza]< I don't understand. Can you please tell me in another way?")
    else:
         respond(message)


# This function is used to identify the name of the user. The name should start with Uppercase
# character. If the user input doesn't have any uppercase character, then it will ask for the name again.        
def find_name(): 
    user = None
    
    while(user == None):
        
        print("[Eliza]< " + "What is your name? ")
        message = input("[User]> ")

# if the user input starts with Ussercase "My" then it will ignore the first Uppercase word and
# will count from the 2nd one. Otherwise it will count from the first Uppercase character.       
        if message.startswith("My"):
            
            name_pattern = re.compile('[^A-z]+([A-Z][a-z]+)')
            name_words = name_pattern.findall(message)
        
        else:
            name_pattern = re.compile('([A-Z][a-z]+)')
            name_words = name_pattern.findall(message)
          
# This part is to add different parts of name           
        if len(name_words) > 0:
            user = ' '.join(name_words)
            Memory['name'] = ['', user,'']
            print('[Eliza]< '+ random.choice(keywords['name']).format(user)) 
        
    return user

# This function is used to identify the department and city of the user. Those should start with 
# character Uppercase.

def department(message): 
    dept = None
    
    if message.startswith("My"):
            
            name_pattern = re.compile('[^A-z]+([A-Z][a-z]+)')
            name_words = name_pattern.findall(message)
        
    else:
        name_pattern = re.compile('([A-Z][a-z]+)')
        name_words = name_pattern.findall(message)
        
 # This part is to add different parts of department name       
    if len(name_words) > 0:
        dept = ' '.join(name_words)
        print('[Eliza]< '+ random.choice(keywords['major']).format(dept))
        
    return dept

# This is the dictionary for the transformation. It is used as pronoun flipping.

def modify_user_input(user_input):
    key_word = { 
        "i" : "you",
        "you": "I",        
        "i'm" : "you're",
        "i am" : "you are",
        "I'm" : "you're",
        "I am" : "you are",        
        "am i" : "are you",
        "am I" : "are you",       
        "am" : "are",       
        "you are": "i am",       
        "are you": "am I",       
        "my" : "your",
        "your": "my",
        "yours": "mine",
        "you're": "I'm",       
        "mine": "yours",
        "me": "you",       
       "i'd": "you would",
       "i've": "you have",
       "i'll": "you will",
        }
    
    parts = user_input.lower().split()

    for item, value in enumerate(parts):
        if value in key_word:
            parts[item] = key_word.get(value)
    

    modify_input = " "
    return (modify_input.join(parts))
 

# This dictionary is used when there are more than 2 transformation. After 2 transformation, it will 
# randomly ask a question to the user.
more_topics = {'job': ["Tell me more about your expected job.","Elaborate please "],
              'family': ["What does your family say about your carrier?","Go on. I want to know more"],
              "place": ["Where are you from?", "Where do you live?"],
              "skill": ["what is your strong point?", "What is most important to get a better career?"]
    }

# This is the main function.
if __name__ == "__main__":
    message = ""
# Introduction
    intro()
# Find the user name
    user = find_name() 
    username = ['', user,'']
# Store the name into memory
    Memory['name'] = ['', user,'']
    print("[Eliza]< " + "What is your Major? ")
    message = input("["+ user +"]> ")
# Find the user major
    dept = department(message)
# Store the major into memory
    Memory['depatmet'] = dept
# Loop to start the conversation
    while (True):               
        message = input("["+user+"]> ")
        gibberish_detect(message)
          



