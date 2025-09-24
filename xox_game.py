import os
import random
import time

random.seed(time.time())

gameTable = [[" "]*3 for _ in range(3)]
dolumu = [[0]*3 for _ in range(3)]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def showtable():
    print(f"""
       1   2   3
    A| {gameTable[0][0]} | {gameTable[0][1]} | {gameTable[0][2]} |
     |___|___|___|
    B| {gameTable[1][0]} | {gameTable[1][1]} | {gameTable[1][2]} |
     |___|___|___|
    C| {gameTable[2][0]} | {gameTable[2][1]} | {gameTable[2][2]} |
     |___|___|___|
    """)

hamle_map = {
    "A1": (0,0), "A2": (0,1), "A3": (0,2),
    "B1": (1,0), "B2": (1,1), "B3": (1,2),
    "C1": (2,0), "C2": (2,1), "C3": (2,2)
}

def kazananvarmi(simge=None):
    for i in range(3):
        if all(gameTable[i][j] == (simge if simge else gameTable[i][0]) and gameTable[i][j] != " " for j in range(3)):
            return True
        if all(gameTable[j][i] == (simge if simge else gameTable[0][i]) and gameTable[j][i] != " " for j in range(3)):
            return True
    if all(gameTable[k][k] == (simge if simge else gameTable[0][0]) and gameTable[k][k] != " " for k in range(3)):
        return True
    if all(gameTable[k][2-k] == (simge if simge else gameTable[0][2]) and gameTable[k][2-k] != " " for k in range(3)):
        return True
    return False

def oyuncu_hamlesi(simge):
    while True:
        hamle = input(f"{simge} oyuncusunun hamlesi (A1-C3): ").upper()
        if hamle in hamle_map:
            i,j = hamle_map[hamle]
            if dolumu[i][j] == 0:
                gameTable[i][j] = simge
                dolumu[i][j] = 1
                break
        print("Geçersiz hamle, tekrar deneyin.")

def bilgisayar_hamlesi():
    # 1. Kazanma hamlesi
    for i in range(3):
        for j in range(3):
            if dolumu[i][j] == 0:
                gameTable[i][j] = "O"
                if kazananvarmi("O"):
                    dolumu[i][j] = 1
                    return
                gameTable[i][j] = " "
    # 2. Rakibi engelleme
    for i in range(3):
        for j in range(3):
            if dolumu[i][j] == 0:
                gameTable[i][j] = "X"
                if kazananvarmi("X"):
                    gameTable[i][j] = "O"
                    dolumu[i][j] = 1
                    return
                gameTable[i][j] = " "
    # 3. Orta kare
    if dolumu[1][1] == 0:
        gameTable[1][1] = "O"
        dolumu[1][1] = 1
        return
    # 4. Köşeler
    for (i, j) in [(0,0), (0,2), (2,0), (2,2)]:
        if dolumu[i][j] == 0:
            gameTable[i][j] = "O"
            dolumu[i][j] = 1
            return
    # 5. Rastgele boş kare
    boslar = [(i,j) for i in range(3) for j in range(3) if dolumu[i][j] == 0]
    if boslar:
        i, j = random.choice(boslar)
        gameTable[i][j] = "O"
        dolumu[i][j] = 1

def oyun():
    skor_tek = {"X":0, "O":0, "Berabere":0}
    skor_iki = {"X":0, "O":0, "Berabere":0}
    while True:
        # Tahtayı sıfırla
        for i in range(3):
            for j in range(3):
                gameTable[i][j] = " "
                dolumu[i][j] = 0
        clear_screen()
        showtable()

        mod = ""
        while mod not in ["1", "2"]:
            mod = input("Tek oyuncu için 1, iki oyuncu için 2 yazınız: ")

        oyuncu_sirasi = "X"
        while True:
            if mod == "1" and oyuncu_sirasi == "O":
                bilgisayar_hamlesi()
            else:
                oyuncu_hamlesi(oyuncu_sirasi)

            clear_screen()
            showtable()

            if kazananvarmi(oyuncu_sirasi):
                print(f"{oyuncu_sirasi} kazandı!")
                if mod == "1":
                    skor_tek[oyuncu_sirasi] += 1
                else:
                    skor_iki[oyuncu_sirasi] += 1
                break
            if all(dolumu[i][j] == 1 for i in range(3) for j in range(3)):
                print("Berabere!")
                if mod == "1":
                    skor_tek["Berabere"] += 1
                else:
                    skor_iki["Berabere"] += 1
                break

            oyuncu_sirasi = "O" if oyuncu_sirasi == "X" else "X"

        print("\nSkorlar:")
        print(f"Tek oyuncu modu - X: {skor_tek['X']}, O: {skor_tek['O']}, Berabere: {skor_tek['Berabere']}")
        print(f"İki oyuncu modu - X: {skor_iki['X']}, O: {skor_iki['O']}, Berabere: {skor_iki['Berabere']}")

        devam = input("Yeni maç oynamak ister misiniz? (E/H): ").upper()
        if devam != "E":
            print("Oyundan cikiliyor.")
            break

oyun()