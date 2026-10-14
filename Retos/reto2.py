def menu():
    print("=== Historial de navegacion ===")
    print("1. visitar pagina web ")
    print("2. mostrar historial ")

stack = []

def push(pagina):
    stack.append(pagina)
    return "Pagina agregada"

def isEmpty():
    return not len(stack)

def is_full(capacity):
    return len(stack) == capacity
def peek():
    if not isEmpty():
        return stack[-1]
    return "Pila vacia..."
