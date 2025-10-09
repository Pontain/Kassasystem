import ast

#produkt_lista = {"100": {"produkt_id": 100, "produkt_namn": "kaffe", "pris_typ": "st", "pris": 75}}

produkt_lista = {}
FILNAMN = "produkter.txt"



class Produkt:
    
    def __init__(self, produkt_id, produkt_namn, pris_typ, pris):

        self.produkt_id = produkt_id
        self.produkt_namn = produkt_namn
        self.pris_typ = pris_typ
        self.pris = pris

    def skapa_produkt_i_listan(self):

        return {"produkt_id": self.produkt_id, "produkt_namn": self.produkt_namn, "pris_typ": self.pris_typ, "pris": self.pris}
    
################################################################################

class Varukorg:

    def __init__(self):
        
        self.varor = []

    def add_item(self, produkt, antal=1):

        self.varor.append({"produkt": produkt, "antal": antal})
        print(f"{antal} x {produkt['produkt_namn']}")

    def get_price(self, item):
        produkt = item["produkt"]

    def PAY(self):

        total = 0

        for 



################################################################################


def ladda_produktlistan():

    try:

        with open(FILNAMN, "r", encoding="utf-8") as f:
            for rad in f:
                produkt = ast.literal_eval(rad.strip()) # ast.literal_eval gör om text-strängen till en dictionary. strip tar bort onödiga tecken, typ \n, och mellanslag.
                produkt_lista[produkt["produkt_id"]] = produkt # Om produkt_id är 100 lägger den in 100 som huvudnyckel för produkten.
    except FileNotFoundError:
        print("Ingen produktlista hittad.")
    return produkt_lista



################################################################################


def spara_produkt(produkt: Produkt): # : Produkt är en hint, en ledtråd, ej ett krav. Då variablen produkt är satt till klassen Produkt kan det verka förvirrande.

    with open(FILNAMN, "a", encoding="utf-8") as f:
        f.write(str(produkt.skapa_produkt_i_listan()) + "\n") # Behöver konvertera dictionaryt till sträng då f.write enbart kan skriva text till fil.
                                                              # Gör en radbrytning, \n i slutet för att skapa rader.
 
################################################################################


def lägg_till_produkt():

    produkt_id = input("Ange produkt-id: ")
    produkt_namn = input("Ange namn på produkt: ")
    pris_typ = input("Ange pristyp, st eller kg: ")
    pris = float(input("Ange pris: "))

    produkt = Produkt(produkt_id, produkt_namn, pris_typ, pris)

    spara_produkt(produkt)

################################################################################

def visa_produkter():

    print(produkt_lista)
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

    option_list = ["1", "2", "3", "4", "0"]

    while True:

        print("1. Hantera produkt")
        print("2. Lägg till produkt")
        print("3. Visa alla produkter")
        print("4. Hantera kampanjer")
        print("0. Gå tillbaka till huvudmenyn.")
        val = input(">> ")
        if val not in option_list:
            print("Fel val")
        if val == "1":
            pass
        if val == "2":
            lägg_till_produkt()
        if val == "3":
            visa_produkter()




################################################################################

def ny_kund():

    while True:

        varukorg = Varukorg()

        produkt_id = input(">> ")

        if produkt_id in produkt_lista:
            antal = int(input("antal: "))
            varukorg.add_item(produkt_lista[produkt_namn], antal)

        if produkt_id == "PAY":
            Varukorg.PAY(varukorg)

        if produkt_id == "<":
            break

        else:
            print("Produkt finns ej.")
            continue





################################################################################
ladda_produktlistan()

while True:    

    val = huvud_meny()

    if val == "1":
        ny_kund()

    elif val == "2":
        admin_meny()

    elif val == "0":
        print("System avslutat.")
        break



