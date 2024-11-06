import time
import random
import colorsys
from dataclasses import dataclass
from colorama import Fore, Back, Style, init

init()

@dataclass
class LightState:
    on: bool = False
    brightness: int = 0
    hue: int = 0
    saturation: int = 0
    name: str = "Valo"

class VirtualHueBridge:
    def __init__(self, ip='127.0.0.1'):
        self.ip = ip
        self.connected = False
        self.lights = {
            1: LightState(name="Olohuone"),
            2: LightState(name="LED-nauha")
        }

    def connect(self):
        if not self.connected:
            print(f"{Fore.YELLOW}⚡ Paina Bridge-nappia yhdistääksesi...{Style.RESET_ALL}")
            input("Paina Enter...")
            self.connected = True
            print(f"{Fore.GREEN}✓ Yhdistetty virtuaaliseen siltaan osoitteessa {self.ip}{Style.RESET_ALL}")

    def get_light_status(self, light_id):
        light = self.lights[light_id]
        h = light.hue / 65535.0
        s = light.saturation / 254.0
        v = light.brightness / 254.0
        r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)]
        
        if not light.on:
            return f"{Fore.RED}●{Style.RESET_ALL} Pois päältä"
        else:
            intensity = "█" * (light.brightness // 51 + 1)
            return f"{Fore.GREEN}●{Style.RESET_ALL} Päällä [{intensity:<5}] RGB({r},{g},{b})"

    def display_status(self):
        print("\n=== Virtuaalisen Hue bridgen status ===")
        for light_id, light in self.lights.items():
            status = self.get_light_status(light_id)
            print(f"Valo {light_id} ({light.name}): {status}")
        print("================================\n")

    def set_light(self, light_id, **kwargs):
        if not self.connected:
            raise Exception("Siltaan ei ole yhdistetty! Suorita connect() ensin.")
        
        light = self.lights[light_id]
        for key, value in kwargs.items():
            setattr(light, key, value)
        self.display_status()

    def morse_code(self, light_id, text):
        MORSE = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', ' ': ' '
        }
        
        for char in text.upper():
            if char not in MORSE:
                continue
                
            morse = MORSE[char]
            print(f"\nMorsetetaan merkki '{char}': {morse}")
            
            for symbol in morse:
                if symbol == '.':
                    self.set_light(light_id, on=True, brightness=254)
                    time.sleep(0.2)
                elif symbol == '-':
                    self.set_light(light_id, on=True, brightness=254)
                    time.sleep(0.6)
                
                self.set_light(light_id, on=False, brightness=0)
                time.sleep(0.2)
            
            time.sleep(0.6)

    def disco_mode(self, light_id, duration=5):
        print(f"\n🪩 Käynnistetään disko-moodi {duration} sekunniksi!")
        end_time = time.time() + duration
        
        while time.time() < end_time:
            self.set_light(light_id,
                on=True,
                brightness=random.randint(50, 254),
                hue=random.randint(0, 65535),
                saturation=random.randint(150, 254)
            )
            time.sleep(1)
            
        self.set_light(light_id, on=False, brightness=0)

def main():
    bridge = VirtualHueBridge()
    bridge.connect()

    while True:
        print("\nVirtualinen Hue-ohjain")
        print("1. Kytke valo päälle/pois")
        print("2. Säädä kirkkautta")
        print("3. Muuta LED-nauhan väriä")
        print("4. Disco-tila")
        print("5. Morse-viesti")
        print("6. Näytä valojen tila")
        print("0. Lopeta")

        valinta = input("\nValitse toiminto (0-6): ")

        if valinta == "0":
            print("Suljetaan ohjelma...")
            break
        elif valinta == "1":
            valo_id = int(input("Valitse valo (1-2): "))
            tila = input("Päälle (k/e)? ").lower() == 'k'
            bridge.set_light(valo_id, on=tila)
        elif valinta == "2":
            valo_id = int(input("Valitse valo (1-2): "))
            kirkkaus = int(input("Anna kirkkaus (0-254): "))
            bridge.set_light(valo_id, brightness=kirkkaus)
        elif valinta == "3":
            vari = input("Valitse väri (punainen/vihreä/sininen/keltainen): ").lower()
            varit = {
                'punainen': (0, 254),
                'vihreä': (21845, 254),
                'sininen': (43690, 254),
                'keltainen': (10922, 254)
            }
            if vari in varit:
                hue, sat = varit[vari]
                bridge.set_light(2, on=True, brightness=254, hue=hue, saturation=sat)
        elif valinta == "4":
            valo_id = int(input("Valitse valo (1-2): "))
            kesto = int(input("Anna kesto sekunneissa: "))
            bridge.disco_mode(valo_id, kesto)
        elif valinta == "5":
            valo_id = int(input("Valitse valo (1-2): "))
            viesti = input("Kirjoita morse viesti: ")
            bridge.morse_code(valo_id, viesti)
        elif valinta == "6":
            bridge.display_status()
        else:
            print("Virheellinen valinta!")

if __name__ == "__main__":
    main()