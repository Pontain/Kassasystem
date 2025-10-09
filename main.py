

produkt_lista = {"100": {"produkt_id": 100, "produkt_namn": "kaffe", "pris_typ": "st", "pris": 75}}

class Produkt:
    
    def __init__(self, produkt_id, produkt_namn, pris_typ, pris):

        self.produkt_id = produkt_id
        self.produkt_namn = produkt_namn
        self.pris_typ = pris_typ
        self.pris = pris

################################################################################


def huvud_meny():

    option_list = ["1", "2", "0"]
        
    print("KASSA")
    print("1. Ny kund")
    print("2. Administrera")
    print("0. Avsluta")
    val = input(">> ")
    if val not in option_list:
        print("Fel val")
    else:
        return val
    
################################################################################


def admin_meny():

    option_list = ["1", "2", "3", "0"]

    while True:

        print("1. Hantera produkt")
        print("2. Lägg till produkt")
        print("3. Hantera kampanjer")
        print("0. Gå tillbaka till huvudmenyn.")
        val = input(">> ")
        if val not in option_list:
            print("Fel val")
        else:
            return val

################################################################################

def ny_kund():



################################################################################


while True:    

    val = huvud_meny()

    if val == "1":
        #ny_kund()

    elif val == "2":
        #administration()

    elif val == "0":
        print("System avslutat.")
        break





    