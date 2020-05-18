import re
import string

class Key:
    def __init__(self):
        self.keyword = ""
        self.decomps = []
        self.weight = int(0)

    def add_decomp(self, decomp):
        self.decomps.append(decomp)

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_weight(self, weight):
        self.weight = weight

    def get_keyword(self):
        return self.keyword

    def get_decomps(self):
        return self.decomps

    def get_weight(self):
        return self.weight

    def is_related_decomp(self, decomp):
        return decomp in self.decomps

class Decomp:
    def __init__(self):
        self.decomp_rule = ""
        self.responses = []
        # current index of the response we are using
        self.response_index = 0

    def add_response(self, response):
        self.responses.append(response)

    def set_decomp_rule(self, decomp_rule):
        self.decomp_rule = decomp_rule

    def set_response_index(self, response_index):
        self.response_index = response_index

    def get_decomp_rule(self):
        return self.decomp_rule

    def get_responses(self):
        return self.responses

    def get_response_index(self):
        return self.response_index

    def get_components(self):
        m = re.findall("(\*|[a-z ]*)", self.decomp_rule)
        new_list = [i.lstrip().rstrip() for i in m if i != "" and i != " "]
        return new_list

    def get_weight(self, keys):
        for key in keys:
            if key.is_related_decomp(self):
                return key.get_weight()
        return None

class Eliza:
    def __init__(self):
        self.keys = []
        self.substitutions = {}
        self.stack = []

    def response_select(self, decomp):
        if decomp.get_response_index() < len(decomp.get_responses())-1:
            decomp.set_response_index(decomp.get_response_index() + 1)
        else:
            decomp.set_response_index(0)
        response = decomp.get_responses()[decomp.get_response_index()]
        return response

    def response_swap(self, decomp_rule, response, user_input):
        result_sub = user_input
        m = re.findall("(\*|[/a-z' ]*)", decomp_rule)
        num = re.findall("[0-9]", response)
        # the digit telling what position to use
        num = num[0]
        new_list = [i.lstrip(" ").rstrip(" ") for i in m if i != "" and i != " "]
        for i in range(0, len(new_list)):
            if i < int(num):
                if new_list[i] != "*":
                    if new_list[i].strip("/") in result_sub.lower():
                        result_sub = result_sub.lower().partition(new_list[i].strip("/"))[2].lstrip().rstrip()
                    else:
                        pass
                else:
                    pass
            elif i >= int(num):
                if new_list[i][0] == "/":
                    result_sub = new_list[i].strip("/")
                elif new_list[i] == "*":
                    if i >= len(new_list)-1:
                        pass
                    elif i < len(new_list)-1:
                        if new_list[i + 1] != "*" and new_list[i + 1] in result_sub.lower():
                            result_sub = result_sub.lower().partition(new_list[i + 1])[0].lstrip().rstrip() #if isinstance(result_sub, list) else result_sub][0]
                    else:
                        print("Error: invalid response file")
                else:
                    if new_list[i][0] == "/":
                        result_sub = str(new_list[i + 1]).strip("/")
            else:
                pass
        r = response.replace(num, result_sub)

        return r

    def decomp_match(self, key, user_input):

        decomps = key.get_decomps()
        selected_decomp = None
        max_num = len(user_input)
        current_list = []
        user_input = user_input.lower().split(" ")

        response = ""
        for j in decomps:
            m = re.findall("([a-z' ]*)", j.get_decomp_rule())
            my_list = [i.lstrip().rstrip() for i in m]
            my_list = [i for i in my_list if i]
            my_list = [i.split(" ") for i in my_list]

            iterator = iter(user_input)
            test = [all(j in iterator for j in i) for i in my_list]

            test = test.count(False)

            if test > 0:
                truth = False
            else:
                truth = True

            if truth:
                # what if all the elements in that last decomp list you looked at (current_list) are also in this new list?
                if current_list == []:
                    current_list = my_list
                    selected_decomp = j
                elif all(elem in my_list for elem in current_list) and len(my_list) > len(current_list):
                    current_list = my_list
                    selected_decomp = j

        if selected_decomp != None:
            return selected_decomp
        else:
            return None

    def best_match(self, decomp1, decomp2):
        if decomp1 == None:
            return decomp2
        elif decomp2 == None:
            return decomp1
        elif decomp1.get_weight(self.keys) > decomp2.get_weight(self.keys):
            return decomp1
        elif decomp2.get_weight(self.keys) > decomp1.get_weight(self.keys):
            return decomp2
        elif len(decomp1.get_decomp_rule().split(" ")) > len(decomp2.get_decomp_rule().split(" ")):
            return decomp1
        elif len(decomp2.get_decomp_rule().split(" ")) > len(decomp1.get_decomp_rule().split(" ")):
            return decomp2
        else:
            list_1 = decomp1.get_components()
            list_2 = decomp2.get_components()
            if len(list_1[0].split(" ")) > len(list_2[0].split(" ")):
                return decomp1
            elif len(list_2[0].split(" ")) > len(list_1[0].split(" ")):
                return decomp2
            else:
                return decomp1

    def cleanup_stack(self):
        if len(self.stack) >= 5:
            self.stack.pop(len(self.stack)-1)

    def respond(self, keys, user_input):
        # Get decomp for None. We do it this way so that None could be anywhere in the file.
        key = next((x for x in keys if x.get_keyword() == "None"), None)
        decomp = key.get_decomps()[0]
        key_weight = 0
        for i in keys:
            if i.get_keyword() != "" and (i.get_keyword() in user_input):
                if self.decomp_match(i, user_input) is not decomp:
                    if i.get_weight() >= key_weight:
                        decomp = self.best_match(decomp, self.decomp_match(i, user_input))
                        key = i
                        key_weight = i.get_weight()

        if key.get_keyword() == "None":
            if self.stack != []:
                key = next((x for x in keys if x.get_keyword() == "your"), None)
                decomp = next((x for x in key.get_decomps() if x.get_decomp_rule().split(" ")[0] == "MEM"), None)
                user_input = self.stack.pop()
        elif key.get_keyword() == "your":
            self.stack.append(user_input)
            self.cleanup_stack()

        response = self.response_select(decomp)
        if any(char.isdigit() for char in response):
            response = self.response_swap(decomp.get_decomp_rule(), response, user_input)
            return response
        else:
            return response

    def preprocessing(self, substitutions, user_input):
        join_list = ["i am", "am i", "you are", "are you", "i was", "was i", "you were", "were you"]
        truth_list = []
        for i in join_list:
            iterator = iter(user_input.split(" "))
            truth_list.append(all(j in iterator for j in i.split(" ")))
        test = truth_list.count(True)
        if test > 0:
            result = True
        else:
            result = False
        if bool(result):
            user_input = [user_input.replace(i, i.replace(" ", "")) for i in join_list if i in user_input][0]

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

        for i in lines:
            self.substitutions[i.split(" = ")[0]] = (i.split(" = ")[1].split(" ; "))
        f.close()

        with open("responses.txt") as f:
            s = []

            for line in f:
                line = line.rstrip()
                x = len(line)
                line = line.lstrip()
                indent = x - len(line)
                div = int(indent / 2)
                s = s[:div] + [line]
                if len(s) == 1:
                    key = Key()
                    weight = int(str([i for i in re.findall("[0-9]*", s[0]) if i][0]))
                    key.set_keyword(re.sub("[0-9]", "", s[0].replace("key = ", "").replace(" ", "")))
                    key.set_weight(weight)
                    self.keys.append(key)
                if len(s) == 2:
                    decomp = Decomp()
                    decomp.set_decomp_rule(s[1].lstrip().replace("decomp = ", ""))
                    key.add_decomp(decomp)
                if len(s) == 3:
                    decomp.add_response(s[2].lstrip().replace("resp = ", ""))
        f.close()

def main():

    user_input = ""
    lizzy = Eliza()
    lizzy.load()

    while user_input != "quit" and user_input != "goodbye":
        user_input = input()

        user_input = user_input.translate(str.maketrans('', '', string.punctuation))
        user_input = user_input.lower()

        prep_input = lizzy.preprocessing(lizzy.substitutions, user_input)
        respond = lizzy.respond(lizzy.keys, prep_input)
        print(respond)

if __name__ == '__main__':
    main()