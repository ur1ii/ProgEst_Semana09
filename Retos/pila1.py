stack = []

def push(item, capacity):
    if not is_full(capacity):
        stack.append(item)
        return "Elemento apilado..."
    return "Pila llena..."

def isEmpty():
    return not len(stack)

def is_full(capacity):
    return len(stack) == capacity

def peak():
    if not isEmpty():
        return stack[-1]
    return "Pila vacia..."

def pop():
    if not isEmpty():
        return(stack.pop())
    return "Pila vacia..."\

def  show():
    message = ""
    for item in reversed(stack):
        message += f" ----------- \n"
        message += f"| {item:>6} |\n"
        message += f" ----------- \n"
    return message

capacity = int(input("Ingresa el tamaño de la pila: "))
while True:
    item = input("Ingresa un valor: ")
    print(push(item, capacity))
    answer = input("Desea ingresa otro dato? [S|N]: ")
    if answer.lower() == "n":
        print(f"La pila final es: {stack}")
        break

print("Mostrar tope")
print(peak())
print(peak())

while True:
    answer = input("Desea desapilar? [S|N]: ")
    if answer.lower() == "s":
        print(pop())
    elif answer.lower() == "n":
        break
    else:
        print("Opcion invalida...")





