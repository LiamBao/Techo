class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

def baseConverter(decNumber,base):
    digits = "0123456789ABCDEF"
    s = Stack()
    while True:



print(baseConverter(25,2))
print(baseConverter(25,16))
print(baseConverter(16,16))