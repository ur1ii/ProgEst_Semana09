stack = []

def push(item, capacity):
    if not is_full(capacity):
        stack.append(item)
        return "Elemento agregado"
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

def apilar():
    capacity = int(input("Ingrese el tamaño de la pila: "))
    while True:
        item = input("Ingrese un valor: ")
        print(push, item)
        answer = input("Desea ingresar otro valor? [S|N]: ")
        if answer.lower() == "n":
            print(f"La pila final es: {stack}")
            break

def desapilar():
    while True:
        answer = input("Desea desapilar? [S|N]: ")
        if answer.lower == "s":
            print(pop())
        elif answer.lower == "n":
            break
        else:
            print("Opcion invalida")

def menu():
    entrada()


