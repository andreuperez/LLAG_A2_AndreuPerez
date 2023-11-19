from art import tprint

pref = "\033["
reset = f"{pref}0m"

class gramatica_class:

    def __init__(self):
        self.noterminals = []
        self.terminals = []
        self.produccions = []
        self.simbol_arranc = None


def lectura():
    gramatica = gramatica_class()
    print("\n\n     Introduïu una gramàtica G: ")
    gramatica.noterminals = input("\n         Σn: ").split(",")
    gramatica.terminals = input("\n         Σt: ").split(",")
    for element in gramatica.terminals:
        if element in gramatica.noterminals:
            print("\033[1;31m\n     ATENCIÓ: El símbol" , element, "pertany a l'alfabet de no terminals." + reset)
            print("\n")
            exit(0)
    print("\n         Introduïu les produccions:\n")
    for simbol in gramatica.noterminals:
        produccions = input("             "+simbol + " --> " ).split("|")
        gramatica.produccions.append([simbol])
        for lletra in produccions:
            gramatica.produccions[len(gramatica.produccions) - 1].append(lletra)
    gramatica.simbol_arranc = input("\n         Símbol d'arranc: ")[0]
    return gramatica
    
def inicial(llista, gramatica):
    for simbol in llista:
        if (simbol not in gramatica.terminals) and (simbol != "λ"):
            return False
    return True

def itsfecund(llista, omega, gramatica):
    for simbol in llista:
        if (simbol not in gramatica.terminals) and (simbol not in omega) and (simbol != "λ"):
            return False
    return True


def comparador(llista1, llista2):
    for simbol in llista1:
        if simbol not in llista2:
            return False
    return True

if __name__ == '__main__':
    tprint("Eliminador  de  simbols  inutils")
    tprint("Andreu  Perez  Torra")

    print("\n     ===========================================================================================")
    print("     ||                                     INSTRUCCIONS                                      ||")
    print("     ===========================================================================================")
    print("     || · Intoduïu els elements dels alfabets separats per comes i sense espais (Σn: S,A,B,C) ||")
    print("     || · Intoduïu els elements de les projeccions separats per una barra. (S --> aAa|B)      ||")
    print("     || · En cas de voler utilitzar la paraula buida copieu i enganxeu el següent simbol: λ   ||")
    print("     || · El programa és sensible amb les lletres minúscules i majúscules                     ||")
    print("     ===========================================================================================")

    fecunds = []
    omega = []
    gramatica = lectura()
    for y in range(len(gramatica.produccions)):
        for x in range(1, len(gramatica.produccions[y])):
            if (inicial(gramatica.produccions[y][x],gramatica)):
                fecunds.append(gramatica.produccions[y][0])
                break

    print("\n\n     Calcul dels Símbols Fecunds:     ")
    print("\n         Iteració 0     ", ", ".join(fecunds))

    contador = 1
    while comparador(fecunds,omega) == False:
        omega = fecunds
        fecunds = []
        for y in range(len(gramatica.produccions)):
            for x in range(1, len(gramatica.produccions[y])):
                if (itsfecund(gramatica.produccions[y][x],omega, gramatica)):
                    fecunds.append(gramatica.produccions[y][0])
                    break
        print("         Iteració", contador,"    ", ", ".join(fecunds))
        contador += 1

    print("\n         Els simbols fecunds trobats en la gramàtica introduida són: ", "Σf = {",", ".join(fecunds),"}")
    print("\n\n     Gramàtica equivalent sense simbols fecunds:     \n")

    nofecunds = []
    for simbol in gramatica.noterminals:
        if simbol not in fecunds:
            nofecunds.append(simbol)

    elementremove = []
    produccionsremove = []

    for produccio in gramatica.produccions:
        for x in range(len(produccio)):
            for lletra in produccio[x]:
                if lletra in nofecunds:
                    if x == 0:
                        produccionsremove.append(produccio)
                    else:
                        elementremove.append(produccio[x])
                    break
            else:
                continue
            break

    for produccio in produccionsremove:
        gramatica.produccions.remove(produccio)

    for element in elementremove:
        for y in gramatica.produccions:
            if element in y:
                y.remove(element)
                break

    for produccio in gramatica.produccions:
        print("         "  + produccio[0] + " -->", "|".join(produccio[1:]))

    accessibles = [gramatica.simbol_arranc]
    omega = []

    print("\n\n     Calcul dels Símbols Accessibles:     ")
    print("\n         Iteració 0     ", ", ".join(accessibles))

    contador = 1
    while comparador(accessibles, omega) == False:
        omega = []
        for element in accessibles:
            omega.append(element)

        for y in range(len(gramatica.produccions)):
            if gramatica.produccions[y][0] in omega:
                for x in range(1, len(gramatica.produccions[y])):
                    for lletra in gramatica.produccions[y][x]:
                        if lletra not in accessibles and lletra != "λ":
                            accessibles.append(lletra)
        print("         Iteració", contador, "    ", ", ".join(accessibles))
        contador += 1


    print("\n         Els simbols accessibles trobats en la gramàtica introduïda són: ", "Σac = {", ", ".join(accessibles), "}")

    produccionsremove = []
    for produccio in gramatica.produccions:
        if produccio[0] not in accessibles:
            produccionsremove.append(produccio)

    for element in produccionsremove:
        gramatica.produccions.remove(element)

    print("\n\n     Gramàtica equivalent sense simbols inútils:     \n")
    for produccio in gramatica.produccions:
        print("         "  + produccio[0] + " -->", "|".join(produccio[1:]))
    print("\n")