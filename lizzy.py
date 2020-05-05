import re
import string

class Key:
    def __init__(self):
        self.keyword = ""
        self.decomps = []

    def add_decomp(self, decomp):
        self.decomps.append(decomp)

    def set_keyword(self, keyword):
        self.keyword = keyword

    def get_keyword(self):
        return self.keyword

    def get_decomps(self):
        return self.decomps

class Decomp:
    def __init__(self):
        self.decomp_rule = ""
        self.responses = []
        self.index = 0

    def add_response(self, response):
        self.responses.append(response)

    def set_decomp_rule(self, decomp_rule):
        self.decomp_rule = decomp_rule

    def set_index(self, index):
        self.index = index

    def get_decomp_rule(self):
        return self.decomp_rule

    def get_responses(self):
        return self.responses

    def get_index(self):
        return self.index


class Eliza:
    #def __init__(self):

    def response_select(self, decomp):

        if decomp.get_index() < len(decomp.get_responses())-1:
            decomp.set_index(decomp.get_index() + 1)
        else:
            decomp.set_index(0)
        response = decomp.get_responses()[decomp.get_index()]
        return response

    def find_decomp(self, decomp_rule, response, user_input):
        result_sub = user_input
        m = re.findall("(\*|[a-z ]*)", decomp_rule)
        num = re.findall("[0-9]", response)
        num = num[0]
        new_list = [i.lstrip().rstrip() for i in m if i != ""]
        for i in range(0, len(new_list)):
            if i < int(num):
                if new_list[i] != "*":
                    if new_list[i] in result_sub:
                        result_sub = result_sub.partition(new_list[i])[2].lstrip().rstrip()
                elif new_list[i] == "*":
                    continue
            elif i >= int(num):
                if new_list[i] == "*":
                    if i >= len(new_list)-1:
                        continue
                    elif i < len(new_list)-1:
                        if new_list[i + 1] != "*" and new_list[i + 1] in result_sub:
                            result_sub = result_sub.partition(new_list[i + 1])[0].lstrip().rstrip()
                    else:
                        print("Error: invalid response file")
                else:
                    if new_list[i][0] == "/":
                        result_sub = str(new_list[i + 1]).strip("/")
        r = response.replace(num, result_sub)
        return r

    def decomp_match(self, decomps, user_input):
        for j in decomps:
            m = re.findall("([a-z ]*)", j.get_decomp_rule())
            my_list = [i.lstrip().rstrip() for i in m]
            my_list = [i for i in my_list if i]
            # if every item in the decomp list is in the user input
            if all(str(i) in user_input for i in my_list):
                response = self.response_select(j)
                if any(char.isdigit() for char in response):
                    result_sub = self.find_decomp(j.get_decomp_rule(), response, user_input)
                    return result_sub
                else:
                    return response


    def respond(self, keys, user_input):
        response = ""
        for i in keys:
            if i.get_keyword() in user_input:
                response = self.decomp_match(i.get_decomps(), user_input)
        if response != "" and response != None:
            return response
        else:
            response = self.response_select(keys[0].get_decomps()[0])
            return response

    def preprocessing(self, substitutions, user_input):

        if user_input.lower().find("i am") >= 0:
            user_input = user_input.lower().replace("i am", "iam")
        if user_input.lower().find("you are") >= 0:
            user_input = user_input.lower().replace("you are", "youare")
        if user_input.lower().find("i was") >= 0:
            user_input = user_input.lower().replace("i was", "iwas")
        if user_input.lower().find("you were") >= 0:
            user_input = user_input.lower().replace("you were", "youwere")
        split_string = user_input.split(" ")

        for i in range(0, len(split_string)):
            for j in substitutions.items():
                if split_string[i] in j[1]:
                    split_string[i] = j[0]
                    break
                else:
                    continue

        string = ' '.join(word for word in split_string)
        return string

    def load(self):
        with open("substitutions.txt") as f:
            lines = [line.rstrip('\n') for line in f]
        dictionary = {}
        for i in lines:
            dictionary[i.split(" = ")[0]] = (i.split(" = ")[1].split(" ; "))
        f.close()

        with open("responses.txt") as f:
            s = []
            keys = []
            for line in f:
                line = line.rstrip()
                x = len(line)
                line = line.lstrip()
                indent = x - len(line)
                div = int(indent / 2)
                s = s[:div] + [line]
                if len(s) == 1:
                    key = Key()
                    key.set_keyword(s[0].replace("key = ", ""))
                    keys.append(key)
                if len(s) == 2:
                    decomp = Decomp()
                    decomp.set_decomp_rule(s[1].lstrip().replace("decomp = ", ""))
                    key.add_decomp(decomp)
                if len(s) == 3:
                    decomp.add_response(s[2].lstrip().replace("resp = ", ""))
        f.close()
        return keys, dictionary

def main():

    user_input = ""
    lizzy = Eliza()
    #substitutions = lizzy.load_subs("substitutions.txt")
    keys, substitutions = lizzy.load()

    while user_input != "quit" and user_input != "goodbye":
        user_input = input()

        user_input = user_input.translate(str.maketrans('', '', string.punctuation))
        user_input = user_input.lower()


        prep_input = lizzy.preprocessing(substitutions, user_input)
        respond = lizzy.respond(keys, prep_input)
        print(respond)

if __name__ == '__main__':
    main()