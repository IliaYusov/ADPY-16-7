class Stack:

    def __init__(self, *args):
        self.stack = list(args)

    def __str__(self):
        return str(self.stack)

    def isEmpty(self):
        return not self.stack

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


brackets = input('input brackets sequence: ')
open_br = '({[<'
close_br = ')}]>'
stack = Stack()
for bracket in brackets:
    if bracket in open_br:
        stack.push(bracket)
    elif bracket in close_br:
        if stack.isEmpty() or close_br.index(bracket) != open_br.index(stack.pop()):
            print('Несбалансированно')
            break
    else:
        print(f'Неверный символ {bracket}')
        break
else:
    print('Сбалансированно' if stack.isEmpty() else 'Несбалансированно')
