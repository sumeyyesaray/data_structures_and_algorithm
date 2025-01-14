class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
def balance_checker(symbol_string):
    s = Stack()

    for symbol in symbol_string:
        if symbol in "([{":
            s.push(symbol)
        else:
            if s.is_empty():
                return False
            else:
                if not matches(s.pop(), symbol):
                    return False
    return s.is_empty()

def matches(sym_left, sym_right):
    all_lefts = "([{"
    all_rights = ")]}"
    return all_lefts.index(sym_left) == all_rights.index(sym_right)

test1 = "({[()]})"  # Dengeli parantezler
test2 = "({[([)()]})"  # Dengesiz parantezler
test3 = "(({}))"  # Dengeli parantezler
test4 = "[({})]"  # Dengeli parantezler
test5 = "((("  # Dengesiz parantezler
test6 = "{[()]}"  # Dengeli parantezler
test7 = "{[}"  # Dengesiz parantezler
test8 = "" 

print(balance_checker(test1))  # True
print(balance_checker(test2))  # False
print(balance_checker(test3))  # True
print(balance_checker(test4))  # True
print(balance_checker(test5))  # False
print(balance_checker(test6))  # True
print(balance_checker(test7))  # False
print(balance_checker(test8))  # True