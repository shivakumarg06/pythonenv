# Maintaining Two Lists 
# Maininting Two Lists will work, but it might get messy while running the program, alternative choice will be dictionary...

acronyms = ['LOL', 'IDK', 'TBH']
translations = [ 'laugh out loud', "I don't know", 'to be honest']

print(acronyms)
print(translations)

del acronyms[0]
del translations[0]

print(acronyms)
print(translations)

# Example Dictionary 
# key, assing to , value 
acronyms = { 'LOL': 'laugh out loud', 
            'IDK': "I don't know", 
            'TBH': 'to be honest'
            } 
print(acronyms['LOL'])

# Types of Dictionaries
# string
acronyms = { 'LOL': 'laugh out loud', 
            'IDK': "I don't know", 
            'TBH': 'to be honest'
            }

# string to numbers 
menu = {
    'Soup': 5, 
    'Salad':6
}

# anything 
my_dict = { 10: 'hello', 2: 6.5 }

# Exmaple 
# Create an Empty dictionary 
# Adding new dictionary items 

acronyms = {}

acronyms['LOL'] = "laugh out loud"
acronyms['IDK'] = "I don't know"
acronyms['TBH'] = "to be honest"

print(acronyms)

del acronyms['LOL']
print(acronyms)

# Exmaple
definition = acronyms['BTW'] # the value doesn't exist in the list, which throws an Key error, 
print(definition)
definition = acronyms.get('BTW')
print(definition)

# Exmaple 
acronyms = { 'LOL': 'laugh out loud', 
            'IDK': "I don't know", 
            'TBH': 'to be honest'
            } 
definition = acronyms.get('BTW')

if definition: 
    print(definition)
else:
    print("Key doesn't exists..")



# Exmaple 
acronyms = { 'LOL': 'laugh out loud', 
            'IDK': "I don't know", 
            'TBH': 'to be honest'
            } 
sentence = = 'IDK' + ' what happened ' + 'TBH'
translation = acronyms.get('IDK') + 'what happened' + acronyms.get('TBH')

print('sentence:' sentence)
print('translation:', translation)
