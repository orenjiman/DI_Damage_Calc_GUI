sentinel = [((30, "BS"), (50, "HS"), (10, "E2", 1)), "Sentinel"]
vigilante = [((18, "BS"), (24, "HS"), (10, "E2", 1)), "Vigilante"]
duke = [((40, "BS"), (60, "HS"), (10, "E2", 1)), "Duke"]
chavez = ((sentinel, vigilante, duke), "Chavez")

queen_of_diamond = [((32, "BS"), (64, "HS"), (40, "CBS"), (80, "CHS")), "Queen of Diamond"]
jack_of_diamond = [((20, "BS"), (30, "HS"), (25, "CBS"), (38, "CHS")), "Jack of Diamond"]
king_of_diamond = [((40, "BS"), (80, "HS"), (50, "CBS"), (100, "CHS")), "King of Diamond"]
ace = ((queen_of_diamond, jack_of_diamond, king_of_diamond), "Ace")

lance = [((16, "BS"), (21, "HS")), "Lance"]
trident = [((9, "BS"), (13, "HS")), "Trident"]  # Bursts count as separate shots
javelin = [((24, "BS"), (34, "HS")), "Javelin"]
squire = ((lance, trident, javelin), "Squire")

silence = [((12, "BS"), (16, "HS"), (10, "Throw BS", 1), (20, "Throw HS", 1)), "Silence"]
cadence = [((12, "BS"), (16, "HS"), (9, "Throw BS"), (17, "Throw HS", 1)), "Cadence"]
violence = [((15, "BS"), (20, "HS"), (30, "WBS", 2), (60, "Throw HS", 2)), "Violence"]
larcin = ((silence, cadence, violence), "Larcin")

dragoons = [((14, "BS"), (19, "HS")), "dragoons"]
hydras = [((20, "BS"), (40, "HS")), "Hydras"]
wyverns = [((10, "BS"), (12, "HS")), "Wyverns"]
cav = ((dragoons, hydras, wyverns), "Cavalière")

zhulong = [((10, "BS"), (13, "HS")), "Zhulong"]
longshen = [((10, "BS"), (15, "HS")), "Longshen"]  # Bursts count as separate shots
xuan_wu = [((7, "BS"), (10, "HS")), "Xuan Wu"]
xiu = ((zhulong, longshen, xuan_wu), "Madame Xiu")

the_hook = [((40, "HF"), (25, "ADS BS"), (50, "ADS HS")), "The Hook"]
the_jab = [((25, "HF"), (18, "ADS BS"), (30, "ADS HS")), "The Jab"]
the_uppercut = [((40, "HF"), (30, "ADS BS"), (60, "ADS HS")), "The Uppercut"]
hans = ((the_hook, the_jab, the_uppercut), "Hans")

tactical_slingshot = [((22, "BS"), (34, "HS"), (34, "CBS"), (51, "CHS")), "Tactical Slingshot"]
experimental_splitshot = [((25, "BS"), (35, "CBS")), "Experimental Splitshot"]
heavy_longshot = [((18, "BS"), (30, "HS"), (50, "CBS"), (80, "CHS")), "Heavy Longshot"]
yumi = ((tactical_slingshot, experimental_splitshot, heavy_longshot), "Yu-Mi")

heartbreaker = [((10, "BS"), (12, "HS")), "Heartbreaker"]
jack_of_hearts = [((20, "BS"), (30, "HS")), "Jack of Hearts"]
lovebite = [((37, "BS"),), "Lovebite"]
red = ((heartbreaker, jack_of_hearts, lovebite), "Red")

# TODO: add sasori P2 (Give and take)
ame_kage = [((13, "BS"), (32, "HS"), (40, "Sword"), (5, "E3", 1)), "Ame & Kage"]
hyo_kanei = [((7, "BS"), (12, "HS"), (35, "CBS"), (60, "CHS"), (30, "Uncharged Sword"), (60, "Charged Sword"), (5, "E3", 1)), "Hyō & Kanei"]
yuki_hikari_0 = [((6, "BS"), (8, "HS"), (15, "Sword"), (5, "E3", 1)), "Yuki & Hikari 0 debuffs"]
yuki_hikari_1 = [((10, "BS"), (13, "HS"), (15, "Sword"), (5, "E3", 1)), "Yuki & Hikari 1 debuffs"]
yuki_hikari_2 = [((14, "BS"), (19, "HS"), (15, "Sword"), (5, "E3", 1)), "Yuki & Hikari 2 debuffs"]
yuki_hikari_3 = [((18, "BS"), (24, "HS"), (15, "Sword"), (5, "E3", 1)), "Yuki & Hikari 3 debuffs"]
yuki_hikari_4 = [((22, "BS"), (29, "HS"), (15, "Sword"), (5, "E3", 1)), "Yuki & Hikari 4 debuffs"]
sasori = ((ame_kage, hyo_kanei, yuki_hikari_0, yuki_hikari_1, yuki_hikari_2, yuki_hikari_3, yuki_hikari_4), "Sasori")

pulpo =[((15, "BS"), (20, "HS"), (23, "Intel BS")), "Pulpo"]
nautilo = [((5, "BS"), (8, "HS"), (50, "Fifty-Bomb")), "Nautilo"]
calamari = [((6, "BS"), (8, "HS"), (34, "Intel BS"), (60, "Intel HS")), "Calamari"]
octo = ((pulpo, nautilo, calamari), "Octo")

caliburn = [((8, "BS"), (11, "HS"), (5, "E1/E2", 3), (10, "P3", 1)), "Caliburn"]
galantine = [((10, "BS"), (13, "HS"), (5, "E1/E2", 3), (10, "P3", 1)), "Galantine"]
arondight = [((35, "BS"), (60, "HS"), (5, "E1/E2", 3), (10, "P3", 1)), "Arondight"]
vigil = ((caliburn, galantine, arondight), "Vigil")

agents = (chavez, ace, squire, larcin, cav, xiu, hans, yumi, red, sasori, octo, vigil)


if __name__ == "__main__":
    pass
