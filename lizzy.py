import random
import re

statement = input()

response_dict = ['I need (.*)', ["Why do you need %1?", "Would it really help you to get %1?", "Are you sure you need %1?"]]
regex = re.compile('(.*)(%\d)(.*)')
if (re.compile(response_dict[0]).match(statement)):
    random_choice = random.choice(response_dict[1])
    response = regex.search(random_choice)
    replacement = re.compile(response_dict[0]).match(statement).group(1)
    response = re.sub(str(response.group(2)), str(replacement), random_choice, flags=re.IGNORECASE)
    print(response)
