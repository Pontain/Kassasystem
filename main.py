import ast
import os
from datetime import datetime

#produkt_lista = {"100": {"produkt_id": 100, "produkt_namn": "kaffe", "pris_typ": "st", "pris": 75}}

produkt_lista = {}
PRODUKT_FIL = "produkter.txt"
KVITTO_MAPP = "Kvitton"
KVITTO_NR = "kvittonr.txt"

################################################################################

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
        
        self.varor = [] # Med en vara kan det se ut såhär:
                        # [{"produkt": {"produkt_id": "1", "produkt_namn": "Kaffe", "pris_typ": "st", "pris": 50.0}, "antal": 2}]

    def add_item(self, produkt, antal=1): # Tar emot färdiga produktobjekt från ny_kund-funktionen. variablen produkt är produkt_lista[produkt_id] från
                                          # varukorg.add_item i ny_kund()
        self.varor.append({"produkt": produkt, "antal": antal})
        print(f"{antal} x {produkt['produkt_namn']}")

    def get_price(self, item):
        produkt = item["produkt"]
        antal = item["antal"]
        return produkt["pris"] * antal

    def skapa_kvittorader(self):

        kvittorader = []
        total = 0

        for item in self.varor: # loopar igenom self.varor-listan och kör get_price-funktionen på varje item för att räkna ut totalen.
            produkt = item["produkt"]           # Skapar en lista med varorna till kvittot i kvittorader.
            antal = item["antal"]
            pris = self.get_price(item)
            total += pris
            
            kvittorader.append(f"{produkt['produkt_namn']} ({antal} {produkt['pris_typ']}) - {pris:.2f} kr.") # .2f gör att priset alltid visas med två decimaler
                                                                                                              # : i f-sträng startar formateringsregeln.
        return kvittorader, total

            # produkt_lista = butikens lagerhylla
            # add_item() = du plockar en vara från hyllan och lägger den i din kundvagn
            # self.varor = själva kundvagnen
            # item = ett av föremålen i din kundvagn
            # get_price(item) = kassörens uträkning av priset för just den varan
            # Butikshyllan (produkt_lista) rörs aldrig – du tar bara kopior till din vagn.

################################################################################

class Kvitto:

    def __init__(self, varukorg):
        
        self.varukorg = varukorg
        self.datum_tid = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.datum = datetime.now().strftime("%Y-%m-%d")
        self.tid = datetime.now().strftime("%H-%M-%S")
        self.kvitto_nummer = self._next_nr() # _ = ska bara användas inuti klassen.

    def _next_nr(self):

        if not os.path.exists(KVITTO_NR):
            with open(KVITTO_NR, "w") as f:
                f.write("0")

        with open(KVITTO_NR, "r") as f:
            nr = int(f.read().strip() or 0) # .strip tar bort mellanslag och radbrytnigar, alltid bra att ha med.
                                            # Då filens str typas om till int är "or 0" bra ifall filen är tom, så det finns en int i filen, annars krasch.
            next_nr = nr + 1

        with open(KVITTO_NR, "w") as f:
            f.write(str(next_nr))

        return next_nr
    
    def skapa_kvitto(self):

        kvitto_fil = f"RECEIPTS_{self.datum}.txt" # Namn på kvittofilen, går tyvärr ej att ha kolon i filnamnet för tiden.
        kvitto_path = os.path.join(KVITTO_MAPP, kvitto_fil) # Sökväg till vart kvittofilerna ska lagras
        kvittorader, total = self.varukorg.skapa_kvittorader()

        if not os.path.exists(KVITTO_MAPP): 
            os.mkdir(KVITTO_MAPP) # Skapar mapp för kvitton

        # Skapar en lista för kvittot som ska skapas, börjar med kvittonummer och datum

        kvitto = []
        kvitto.append("~" * 30)
        kvitto.append(f"Kvitto # {self.kvitto_nummer}")
        kvitto.append(self.datum_tid)
        kvitto.append("-" * 30)
        kvitto.extend(kvittorader) # Lägger till alla element från listan: kvittorader
        kvitto.append("-" * 30)
        kvitto.append(f"Totalt: {total:.2f} kr")
        kvitto.append("~" * 30)
        kvitto.append("\n")

        terminal_kvitto = "\n".join(kvitto)

        with open(kvitto_path, "a", encoding="utf-8") as f:
            f.write("\n".join(kvitto)) # \n innan .join gör en radbrytning som separator. Blir som en for-loop med \n efter varje radkörning i loopen.

        print(f"\nKvittot sparat i {kvitto_path}")

        return terminal_kvitto

################################################################################

def ny_kund():

    varukorg = Varukorg()
    
    print("\nNy kund\n\n< för att gå tillbaka, PAY för betalning.\n")

    while True:

        print("Ange PLU och antal med mellanslag emellan: ")
        kassa_input = input(">> ").strip().upper() # .strip är bra ifall man råkar tex skriva in ett mellanslag, strip tar bort sånt.

        if kassa_input == "PAY":
            if not varukorg.varor:
                print("Varukorgen är tom.")
                continue
            else:
                kvitto = Kvitto(varukorg) # Kör konstruktorn i kvitto så att kvittonumret ökas.
                terminal_kvitto = kvitto.skapa_kvitto()
                print(f"\n{terminal_kvitto}")

                varukorg = Varukorg() # Nollställer varukorgen då klassen anropas på nytt.
                print("Ny kund\n\n< för att gå tillbaka, PAY för betalning.\n")
                continue

        elif kassa_input == "<":
            break

        else:
            produkt_id, antal = kassa_input.split()
            antal = int(antal)

        if produkt_id in produkt_lista:
            varukorg.add_item(produkt_lista[produkt_id], antal) # Skickar vald produkt till add_item-funktionen i Varukorg-klassen.

        else:
            print("Produkt finns ej.")
            continue

################################################################################

def lägg_till_produkt():

    produkt_id = input("Ange produkt-id: ")
    produkt_namn = input("Ange namn på produkt: ")
    pris_typ = input("Ange pristyp, st eller kg: ")
    pris = float(input("Ange pris: "))

    produkt = Produkt(produkt_id, produkt_namn, pris_typ, pris)

    spara_produkt(produkt)

################################################################################

def visa_produkter(): # Kanske kan köra en .join här istället.

    for produkt_id, info in produkt_lista.items():
        print(f"Id {produkt_id}: {info['produkt_namn']} ({info['pris_typ']}) - {info['pris']} kr.")
    input("Tryck enter för att gå tillbaka.")    

################################################################################

def spara_produkt(produkt: Produkt): # : Produkt är en hint, en ledtråd, ej ett krav. Då variablen produkt är satt till klassen Produkt kan det verka förvirrande.

    with open(PRODUKT_FIL, "a", encoding="utf-8") as f:
        f.write(str(produkt.skapa_produkt_i_listan()) + "\n") # Behöver konvertera dictionaryt till sträng då f.write enbart kan skriva text till fil.
                                                              # Gör en radbrytning, \n i slutet för att skapa rader.
 
################################################################################

def ladda_produktlistan():

    try:

        with open(PRODUKT_FIL, "r", encoding="utf-8") as f:
            for rad in f:
                produkt = ast.literal_eval(rad.strip()) # ast.literal_eval gör om text-strängen till en dictionary. strip tar bort onödiga tecken, typ \n, och mellanslag.
                produkt["pris"] = float(produkt["pris"]) # Säkerställer att priset blir en float och ej en str.
                produkt_lista[produkt["produkt_id"]] = produkt # Om produkt_id är 100 lägger den in 100 som huvudnyckel för produkten.
    except FileNotFoundError:
        print("Ingen produktlista hittad.")
    return produkt_lista

################################################################################

def huvud_meny():

    option_list = ["1", "2", "0"]
        
    print("KASSA")
    print("1. Ny kund")
    print("2. Administrera")
    print("0. Avsluta")
    val = input("\n>> ")
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
        print("<. Gå tillbaka till huvudmenyn.")
        val = input(">> ")
        if val not in option_list:
            print("Fel val")
        elif val == "1":
            pass
        elif val == "2":
            lägg_till_produkt()
        elif val == "3":
            visa_produkter()
        elif val == "4":
            pass
        elif val == "0":
            return

################################## Kör programmet ##############################################

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



