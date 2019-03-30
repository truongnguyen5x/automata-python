import xml.etree.ElementTree as ET
import copy
# class state of automata
class State:
    def __init__(self, id=" ", name=" "):
        self.transitions = []
        self.isFinal = False
        self.id = id
        self.name = name

    def read(self, char):
        return [x.next for x in self.transitions if x.char == char]


# class transition from a state to the other state
class Transition:
    def __init__(self, char, next):
        self.char = char
        self.next = next


# indent the xml tree
def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# read file .JFF
def importJFF(fileName):
    states = []
    finals = []
    tree = ET.parse(fileName)
    tags = tree.findall(".//state")
    for tag in tags:
        state = State(tag.get("id"), tag.get("name"))
        if tag.find("initial") is not None:
            init = state
        if tag.find("final") is not None:
            finals.append(state)
            state.isFinal = True
        states.append(state)
    tags = tree.findall(".//transition")
    for tag in tags:
        From = [x for x in states if x.id == tag.find("from").text][0]
        to = [x for x in states if x.id == tag.find("to").text][0]
        read = tag.find("read").text
        tran = Transition('' if read is None else read, to)
        From.transitions.append(tran)
    for i in range(len(states)):
        states[i].id = str(i)
    return {"init": init, "finals": finals, "states": states}

# export 1 automata to jff
def export(auto, fileName):
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "fa"
    automaton = ET.SubElement(root, "automaton")
    for i in range(len(auto["states"])):
        state = auto["states"][i]
        state.element = ET.SubElement(automaton, "state", {"name": state.name, "id": str(i)})
    ET.SubElement(auto["init"].element, "initial")
    for state in auto["finals"]:
        ET.SubElement(state.element, "final")
    for i in auto["states"]:
        for j in i.transitions:
            tran = ET.SubElement(automaton, "transition")
            ET.SubElement(tran, "from").text = i.id
            ET.SubElement(tran, "to").text = j.next.id
            ET.SubElement(tran, "read").text = j.char
    indent(root)
    ET.ElementTree(root).write(fileName, encoding='UTF-8', xml_declaration=True)

def removeUnreachable(auto):
    for i in range(len(auto['states'])):
        auto['states'][i].reachable = False;
    auto['init'].reachable = True
    stop = False
    while (not stop):
        stop = True
        for i in range(len(auto["states"])):
            for tran in auto['states'][i].transitions:
                if (auto['states'][i].reachable == True and tran.next.reachable == False):
                    stop = False
                    tran.next.reachable = True
    for i in range(len(auto['states']) - 1, -1, -1):
        obj = auto['states'][i]
        if (obj.reachable == False):
            if (obj in auto['finals']):
                auto['finals'].remove(obj)
            auto['states'].remove(obj)

# get all character in FA
def getChars(auto):
    chars = []
    for state in auto["states"]:
        for next in state.transitions:
            if next.char not in chars and next.char != '':
                chars.append(next.char)
    return chars

# merge 2 array
def mergeArray(arr1, arr2):
    for i in arr2:
        if i not in arr1:
            arr1.append(i)

# check 2 list is same
def same(list1, list2):
    temp = [x for x in list1 if x not in list2]
    temp1 = [x for x in list2 if x not in list1]
    return True if temp == [] and temp1 == [] else False

# minimize way 1
def minimizeDFA(auto, chars):
    mark = []
    unmark = []
    for i in range(len(auto["states"])):
        stateI = auto["states"][i]
        for j in range(i + 1, len(auto["states"])):
            stateJ = auto["states"][j]
            if stateI.isFinal != stateJ.isFinal:
                mark.append([stateI, stateJ])
            else:
                unmark.append([stateI, stateJ])
    loop = True
    while loop:
        loop = False
        for pair in unmark:
            for char in chars:
                next = pair[0].read(char)
                next.extend(pair[1].read(char))
                temp1 = [x for x in mark if same(next, x)]
                if temp1:
                    mark.append(pair)
                    unmark.remove(pair)
                    loop = True
                    break
    list = []
    for state in auto["states"]:
        list.append([state])
    for pair in unmark:
        a = [x for x in list if pair[0] in x][0]
        b = [x for x in list if pair[1] in x][0]
        if a != b:
            a.extend(b)
            list.remove(b)
    return connect(auto, list, chars)


# create dfa from list equivalent states
def connect(auto, list, chars):
    states = []
    finals = []
    for i in range(len(list)):
        node = list[i]
        name = ""
        for j in node:
            name += j.id
        temp = State(str(i), name)
        temp.nodes = node
        states.append(temp)
        if auto["init"] in node:
            init = temp
        if node[0] in auto["finals"]:
            finals.append(temp)
    for state in states:
        for char in chars:
            node = state.nodes[0].read(char)[0]
            temp = [x for x in states if node in x.nodes][0]
            state.transitions.append(Transition(char, temp))
    return {"init": init, "states": states, "finals": finals}


file = 'dfa.jff'
dfa = importJFF(file)
chars = getChars(dfa)
removeUnreachable(dfa)
dfa2 = minimizeDFA(dfa, chars)
export(dfa2,"mindfa.jff")