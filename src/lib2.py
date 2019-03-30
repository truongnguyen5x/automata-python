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


# check a string is langue of NFA, DFA
def checkString(root, string):
    if string == '':
        if root.isFinal:
            return True
    else:
        nexts = root.read(string[0])
        for state in nexts:
            if checkString(state, string[1:]):
                return True
    nexts = root.read('')
    for state in nexts:
        if checkString(state, string):
            return True
    return False


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


# union or intersection 2 DFA, input must be DFA
def unionIntersectionDFA(auto1, auto2, isUnion):
    states = []
    final1 = []
    final2 = []
    n2 = len(auto2["states"])
    chars = ['0', '1']
    id = 0
    for i in auto1["states"]:
        for j in auto2["states"]:
            state = State(str(id), i.name + ' ' + j.name)
            state.node1 = i
            state.node2 = j
            states.append(state)
            if i == auto1["init"] and j == auto2["init"]:
                init = state
            if i.isFinal or j.isFinal:
                final1.append(state)
            if i.isFinal and j.isFinal:
                final2.append(state)
            id += 1
    for state in states:
        for char in chars:
            i = int(state.node1.read(char)[0].id)
            j = int(state.node2.read(char)[0].id)
            temp = states[i * n2 + j]
            state.transitions.append(Transition(char, temp))
    finals = final1 if isUnion else final2
    return {"init": init, "states": states, "finals": finals}


# union 2 NFA
def unionNFA(auto1, auto2):
    initState = State()
    initState.transitions.append(Transition('', auto1["init"]))
    initState.transitions.append(Transition('', auto2["init"]))
    return {"init": initState, "finals": auto1["finals"] + auto2["finals"],
            "states": [initState] + auto1["states"] + auto2["states"]}


# concat 2 NFA
def concatNFA(automat1, automat2):
    auto1 = copy.deepcopy(automat1)
    auto2 = copy.deepcopy(automat2)
    for state in auto1["finals"]:
        state.isFinal = False
        state.transitions.append(Transition('', auto2["init"]))
    return {"init": auto1["init"], "finals": auto2["finals"], "states": auto1["states"] + auto2["states"]}


# star 1 NFA
def starNFA(automata):
    auto = copy.deepcopy(automata)
    init = State()
    init.isFinal = True
    auto["finals"].append(init)
    for final in auto["finals"]:
        final.transitions.append(Transition('', auto["init"]))
    auto["states"].append(init)
    return {"init": init, "finals": auto["finals"], "states": auto["states"]}


# check 2 list is same
def same(list1, list2):
    temp = [x for x in list1 if x not in list2]
    temp1 = [x for x in list2 if x not in list1]
    return True if temp == [] and temp1 == [] else False


# function E
def e(states, list):
    toFinal = False
    for state in states:
        toFinal = toFinal or state.isFinal
        nexts = state.read('')
        toFinal = e(nexts, list)[1] or toFinal
        if state not in list:
            list.append(state)
    return list, toFinal


# get all character in FA
def getChars(auto):
    chars = []
    for state in auto["states"]:
        for next in state.transitions:
            if next.char not in chars and next.char != '':
                chars.append(next.char)
    return chars


# nfa to dfa
def toDFA(auto, chars):
    states = []
    finals = []
    current = State()
    current.nodes, current.isFinal = e([auto["init"]], [])
    states.append(current)
    i = 1
    while True:
        for char in chars:
            next = []
            for node in current.nodes:
                next.extend(node.read(char))
            next, toFinal = e(next, [])
            temp = [x for x in states if same(next, x.nodes)]
            if not temp:
                temp.append(State())
                temp[0].nodes = next
                states.append(temp[0])
                temp[0].isFinal = toFinal
            current.transitions.append(Transition(char, temp[0]))
        if i == len(states):
            break
        else:
            current = states[i]
            i += 1
    for i in range(len(states)):
        name = ""
        for node in states[i].nodes:
            name += str(node.id)
        states[i].name = name
        states[i].id = str(i)
        if states[i].isFinal:
            finals.append(states[i])
    return {"init": states[0], "states": states, "finals": finals}


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

# merge 2 array
def mergeArray(arr1, arr2):
    for i in arr2:
        if i not in arr1:
            arr1.append(i)


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


# minimize way 2
def minimizeDFA2(auto, chars):
    equi = [auto["finals"], [x for x in auto["states"] if not x.isFinal]]
    stop = False
    while not stop:
        stop = True
        equi1 = []
        for set in equi:
            set1 = []
            for node in set:
                if not set1:
                    set1.append([node])
                else:
                    add = False
                    for sub in set1:
                        if equivalent(equi, sub[0], node, chars):
                            sub.append(node)
                            add = True
                    if not add:
                        stop = False
                        set1.append([node])
            equi1.extend(set1)
        equi = equi1
    return connect(auto, equi, chars)


# check nodeA is equivalent with nodeB
def equivalent(equi, nodeA, nodeB, chars):
    for char in chars:
        accept = False
        next = nodeA.read(char)
        next.extend(nodeB.read(char))
        for set in equi:
            if next[0] in set and next[1] in set:
                accept = True
        if not accept:
            return False
    return True
