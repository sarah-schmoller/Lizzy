import re
import random
import string


class eliza:
    #def __init__(self):

    def respond(self, responses, user_input):

        regex = re.compile('(.*)(%\d)(.*)')

        resp = ""
        for key in responses:
            random_choice = random.choice(responses[key])
            key_regex = re.compile(key)
            if (key_regex.match(user_input)):
                resp = regex.search(random_choice)
                repl = key_regex.match(user_input).group(1)
                resp = re.sub(str(resp.group(2)), str(repl), random_choice, flags=re.IGNORECASE)
                return resp

    def preprocessing(self, synonyms, user_input):
        split_string = user_input.split(" ")
        for i in range(0, len(split_string)):
            for j in synonyms.items():
                if split_string[i] in j[1]:
                    split_string[i] = j[0]
        string = ' '.join(word for word in split_string)
        return string

    #def postprocessing(self, reflections):

    def load_dicts(self, file_name):
        with open(file_name) as f:
            lines = [line.rstrip('\n') for line in f]
        dictionary = {}
        for i in lines:
            dictionary[i.split(":")[0]] = (i.replace(":", "").split(" "))
        return dictionary

    def load_resps(self, file_name):
        f = open(file_name, "r").read()
        f = f.split("key: ")
        dictionary = {}
        for i in f:
            if i != "":
                i = i.replace("\n", "").split("  resp: ")
                dictionary[i[0]] = i[1:]
        return dictionary

def main():

    user_input = ""
    while user_input != "quit" and user_input != "goodbye":
        user_input = input()

        user_input = user_input.translate(str.maketrans('', '', string.punctuation))
        user_input = user_input.lower()

        lizzy = eliza()
        synonyms = lizzy.load_dicts("synonyms.txt")
        reflections = lizzy.load_dicts("reflections.txt")
        responses = lizzy.load_resps("responses.txt")

        prep_input = lizzy.preprocessing(synonyms, user_input)

        respond = lizzy.respond(responses, prep_input)
        print(respond)

if __name__ == '__main__':
    main()