from tkinter import Tk,Label,TOP
from random import randint
from time import sleep

# nom, pv, armure, pa, pm, temps recharge special, degats - attq 1, degats + attq 1, degats - attq 2, degats + attq 2, pièces, clés, bombes, attaque active, level
# nom, x, y, pv
# x, y, nom item

def mouse_motion(event) :
    global texte
    global info
    if ecran == 8 :
        x,y = int(event.x//(421/46))+perso[-1][0]-22,int(event.y//(400/21))+perso[-1][1]-9
        if 0 < x < len(map[0]) and 0 < y < len(map) :
            if len(l_ennemis) > 0 :
                if perso[0] == "Barbarian" and (perso[10] == 0 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 or perso[10] == 1 and (abs(perso[-1][0]-x) == 0 and 2 <= abs(perso[-1][1]-y) <= 4 or 2 <= abs(perso[-1][0]-x) <= 4 and abs(perso[-1][1]-y) == 0) or perso[10] == 2 and perso[-1] == [x,y]) or perso[0] == "Archer" and (perso[10] == 0 and 2 <= abs(perso[-1][0]-x)+abs(perso[-1][1]-y) <= 3 or perso[10] == 1 and (abs(perso[-1][0]-x) == 0 and 3 <= abs(perso[-1][1]-y) <= 4 or 3 <= abs(perso[-1][0]-x) <= 4 and abs(perso[-1][1]-y) == 0) or perso[10] == 2 and (abs(perso[-1][0]-x) == 0 and abs(perso[-1][1]-y) == 2 or abs(perso[-1][0]-x) == 2 and abs(perso[-1][1]-y) == 0)) or perso[0] == "Assassin" and (perso[10] == 0 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 or perso[10] == 1 and ((abs(perso[-1][0]-x) == 0 and 1 <= abs(perso[-1][1]-y) <= 2 or 1 <= abs(perso[-1][0]-x) <= 2 and abs(perso[-1][1]-y) == 0)) or perso[10] == 2 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 2) or perso[0] == "Mage" and (perso[10] == 0 and 1 <= abs(perso[-1][0]-x)+abs(perso[-1][1]-y) <= 2 or perso[10] == 1 and perso[-1] == [x,y] or perso[10] == 2 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1) : texte["cursor"] = "target"
                else : texte["cursor"] = "tcross"
            elif abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 : texte["cursor"] = "target"
            else : texte["cursor"] = "tcross"
            info = ""
            if map[y][x] == "*" : info = "Next floor"
            elif map[y][x] == "¤" : info = "Trap"
            elif map[y][x] == "#" : info = "Web"
            elif map[y][x] == "§" : info = "Fire"
            elif map[y][x] == "█" : info = "Wall"
            elif map[y][x] == "▓" : info = "Door"
            for i in l_objets :
                if i[0] == x and i[1] == y and explore[i[1]//20][i[0]//20] == 1 :
                    a = {"♥" : "Heart","◙" : "Coin","y" : "Key","σ" : "Bomb"}[i[2]] if i[2] != "&" else i[3]
                    a += " "+str(cout_objets[i[2]]) if donjon[i[1]//20][i[0]//20] == "shop" else " "+str(cout_objets[i[3]]) if donjon[i[1]//20][i[0]//20] == "devildeal" else ""
                    info = a
            for i in l_fantomes :
                if i[0] == x and i[1] == y and explore[i[1]//20][i[0]//20] == 1 :
                    info = "Ghost"
                    break
            for i in l_ennemis :
                if i[1] == x and i[2] == y :
                    if i[0] in "OXWTM" : info = l_mobs[i[0]][0]+" "+str(i[3])+"/"+str(l_mobs[i[0]][1])
                    else : info = "Boss "+str(i[3])+"/"+str(l_mobs[i[0]][1])
                    break
            affich()

# pa : 24,24,23,26

def mouse_button_down(event) :
    global perso
    global l_ennemis
    global l_effets
    global l_objets
    global bombe
    if ecran == 8 and possib_mouv == 1 :
        x,y,e = int(event.x//(421/46))+perso[-1][0]-22,int(event.y//(400/21))+perso[-1][1]-9,""
        if len(l_ennemis) > 0 and 0 < x < len(map[0]) and 0 < y < len(map) :
            for i in range (len(l_ennemis)) :
                if l_ennemis[i][0] == "sq" and [x,y] in [[l_ennemis[i][1]+k,l_ennemis[i][2]+j] for j in range (4) for k in range (4)] :
                    e = i
                    break
                elif l_ennemis[i][0] == "gs" and l_ennemis[i][1] == x and l_ennemis[i][2] == y :
                    e = "gs"
                    break
                elif l_ennemis[i][1] == x and l_ennemis[i][2] == y :
                    e = i
                    break
            non = test_obstacle(perso[-1],[x,y])
            non,nb_p,nb_b,nb_t = non[0],non[1],non[2],non[3]
            if e != "" and e != "gs" :
                if perso[0] == "Barbarian" :
                    if perso[10] == 0 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 and perso[3][1] >= 2 : perso[3][1],l_ennemis[e][3] = perso[3][1]-2,l_ennemis[e][3]-randint(perso[6][0],perso[6][1])
                    elif perso[10] == 1 and (abs(perso[-1][0]-x) == 0 and 2 <= abs(perso[-1][1]-y) <= 4 or 2 <= abs(perso[-1][0]-x) <= 4 and abs(perso[-1][1]-y) == 0) and non == 0 and perso[3][1] >= 4 :
                        perso[3][1],l_ennemis[e][3] = perso[3][1]-4,l_ennemis[e][3]-randint(perso[6][2],perso[6][3])
                        if perso[-1][0] > x : perso[-1][0] = x+1
                        elif perso[-1][0] < x : perso[-1][0] = x-1
                        elif perso[-1][1] > y : perso[-1][1] = y+1
                        elif perso[-1][1] < y : perso[-1][1] = y-1
                        if perso[2][1] >= nb_p : perso[2][1] -= nb_p
                        else : perso[1][1],perso[2][1] = perso[1][1]-nb_p+perso[2][1],0
                        if perso[2][1] >= nb_b : perso[2][1] -= nb_b
                        else : perso[1][1],perso[2][1] = perso[1][1]-nb_b+perso[2][1],0
                        if nb_b > 0 : l_effets += ["Burn",2]
                        if nb_t > 0 : perso[4][1] = 0
                elif perso[0] == "Archer" :
                        if perso[10] == 0 and 2 <= abs(perso[-1][0]-x)+abs(perso[-1][1]-y) <= 3 and non == 0 and perso[3][1] >= 2 : perso[3][1],l_ennemis[e][3] = perso[3][1]-2,l_ennemis[e][3]-randint(perso[6][0],perso[6][1])
                        elif perso[10] == 1 and (abs(perso[-1][0]-x) == 0 and 3 <= abs(perso[-1][1]-y) <= 4 or 3 <= abs(perso[-1][0]-x) <= 4 and abs(perso[-1][1]-y) == 0) and non == 0 and perso[3][1] >= 4 : perso[3][1],l_ennemis[e][3] = perso[3][1]-4,l_ennemis[e][3]-randint(perso[6][2],perso[6][3])
                elif perso[0] == "Assassin" :
                        if perso[10] == 0 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 and non == 0 and perso[3][1] >= 2 : perso[3][1],l_ennemis[e][3] = perso[3][1]-2,l_ennemis[e][3]-randint(perso[6][0],perso[6][1])
                        elif perso[10] == 1 and ((abs(perso[-1][0]-x) == 0 and 1 <= abs(perso[-1][1]-y) <= 2 or 1 <= abs(perso[-1][0]-x) <= 2 and abs(perso[-1][1]-y) == 0)) and non == 0 and perso[3][1] >= 3 : perso[3][1],l_ennemis[e][3] = perso[3][1]-3,l_ennemis[e][3]-randint(perso[6][2],perso[6][3])
                elif perso[0] == "Mage" and perso[10] == 0 and 1 <= abs(perso[-1][0]-x)+abs(perso[-1][1]-y) <= 2 and non == 0 and perso[3][1] >= 2 : perso[3][1],l_ennemis[e][3] = perso[3][1]-2,l_ennemis[e][3]-randint(perso[6][0],perso[6][1])
            elif e != "gs" and perso[-1][0]//20 == x//20 and perso[-1][1]//20 == y//20 :
                if perso[0] == "Barbarian" and perso[10] == 2 and perso[-1] == [x,y] and perso[5][1] == 0 : perso[5][1],perso[6],l_effets = perso[5][0],[perso[6][0]*2,perso[6][1]*2,perso[6][2]*2,perso[6][3]*2],l_effets+[["Berserk",2]]
                elif perso[0] == "Archer" and perso[10] == 2 and (abs(perso[-1][0]-x) == 0 and abs(perso[-1][1]-y) == 2 or abs(perso[-1][0]-x) == 2 and abs(perso[-1][1]-y) == 0) and perso[5][1] == 0 and map[y][x] in "-¤§#" and map[int((perso[-1][1]+y)/2)][int((perso[-1][0]+x)/2)] :
                    perso[5][1],perso[-1] = perso[5][0],[x,y]
                    if perso[2][1] >= nb_p : perso[2][1] -= nb_p
                    else : perso[1][1],perso[2][1] = perso[1][1]-nb_p+perso[2][1],0
                    if perso[2][1] >= nb_b : perso[2][1] -= nb_b
                    else : perso[1][1],perso[2][1] = perso[1][1]-nb_b+perso[2][1],0
                    if nb_b > 0 : l_effets += ["Burn",2]
                    if nb_t > 0 : perso[4][1] = 0
                elif perso[0] == "Assassin" and perso[10] == 2 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 2 and perso[5][1] == 0 and map[y][x] in "-¤§#" : perso[5][1],perso[-1] = perso[5][0],[x,y]
                elif perso[0] == "Mage" :
                    if perso[10] == 1 and perso[-1] == [x,y] and perso[3][1] >= 6 :
                        perso[3][1] -= 6
                        for i in [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)] :
                            e = ""
                            for j in range (len(l_ennemis)) :
                                if l_ennemis[j][1] == x+i[0] and l_ennemis[j][2] == y+i[1] :
                                    e = j
                                    break
                            if e != "" :
                                l_ennemis[e][3] -= randint(perso[6][2],perso[6][3])
                                non = 0
                                for j in range (len(l_ennemis)) :
                                    if l_ennemis[j][1] == x+i[0]*2 and l_ennemis[j][2] == y+i[1]*2 :
                                        non = 1
                                        break
                                if map[y+i[1]*2][x+i[0]*2] in "-¤§#" and non == 0 :
                                    non = 0
                                    for j in range (len(l_ennemis)) :
                                        if l_ennemis[j][1] == x+i[0]*3 and l_ennemis[j][2] == y+i[1]*3 :
                                            non = 1
                                            break
                                    if map[y+i[1]*3][x+i[0]*3] in "-¤§#" and non == 0 : l_ennemis[e][1],l_ennemis[e][2] = l_ennemis[e][1]+i[0]*2,l_ennemis[e][2]+i[1]*2
                                    else : l_ennemis[e][1],l_ennemis[e][2] = l_ennemis[e][1]+i[0],l_ennemis[e][2]+i[1]
                    elif perso[10] == 2 and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 and perso[5][1] == 0 and map[y][x] == "-" : perso[5][1],map[x][y],l_effets = perso[5][0],"█",l_effets+[["Wall",3,x,y]]
            l = []
            for i in l_ennemis :
                if i[3] > 0 : l += [i]
                else :
                    n = randint(1,9)
                    if n > 3 : l_objets += [[i[1],i[2],["◙","◙","◙","♥","y","σ"][n-4]]]
            l_ennemis = list(l)
            if len(l_ennemis) == 0 :
                perso[2][1],perso[3][1],perso[4][1],perso[5][1] = perso[2][0],perso[3][0],perso[4][0],perso[5][0]
                for i in range (len(l_effets)) :
                    if l_effets[0][0] == "Berserk" : perso[6] = [int(perso[6][0]/2),int(perso[6][1]/2),int(perso[6][2]/2),int(perso[6][3]/2)]
                    elif l_effets[0][0] == "Wall" : map[l_effets[0][3]][l_effets[0][2]] = "-"
                    del l_effets[0]
                if map[perso[-1][1]//20*20][perso[-1][0]//20*20+7] == "▓" : map[perso[-1][1]//20*20][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["-","-"]
                if map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+15] == "▓" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+15],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20+15] = "-","-"
                if map[perso[-1][1]//20*20+15][perso[-1][0]//20*20+7] == "▓" : map[perso[-1][1]//20*20+15][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["-","-"]
                if map[perso[-1][1]//20*20+7][perso[-1][0]//20*20] == "▓" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20] = "-","-"
                if donjon[perso[-1][1]//20][perso[-1][0]//20] == "boss" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+7] = "*"
        elif len(l_ennemis) == 0 and 0 < x < len(map[0]) and 0 < y < len(map) :
            if map[y][x] in "-¤§#" and bombe == [] and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 and perso[9] > 0 :
                bombe,perso[9] = [x,y,0],perso[9]-1
                explosion(0)
            elif map[y][x] == "▓" and abs(perso[-1][0]-x)+abs(perso[-1][1]-y) == 1 and perso[8] > 0 :
                perso[8] -= 1
                if map[(y+1)//20*20][(x+1)//20*20+7] == "-" : map[(y+1)//20*20-1][(x+1)//20*20+7:(x+1)//20*20+9] = ["-","-"]
                if map[(y+1)//20*20+7][(x+1)//20*20+15] == "-" : map[(y+1)//20*20+7][(x+1)//20*20+16],map[(y+1)//20*20+8][(x+1)//20*20+16] = "-","-"
                if map[(y+1)//20*20+15][(x+1)//20*20+7] == "-" : map[(y+1)//20*20+16][(x+1)//20*20+7:(x+1)//20*20+9] = ["-","-"]
                if map[(y+1)//20*20+7][(x+1)//20*20] == "-" : map[(y+1)//20*20+7][(x+1)//20*20-1],map[(y+1)//20*20+8][(x+1)//20*20-1] = "-","-"
                explore[(y+1)//20][(x+1)//20] = 1
    affich()

def key_down(event) :
    global ecran
    global map
    global perso
    global l_ennemis
    global l_fantomes
    global l_effets
    global cooldown_armure
    global info2
    global info3
    global c
    global delai
    global fruit
    if ecran == 1 and event.keysym == "Return" : ecran = 2
    elif ecran == 2 :
        if event.keysym in ["Up","z"] and perso[0] != "Barbarian" : perso[0] = "Barbarian" if perso[0] == "Archer" else "Archer" if perso[0] == "Assassin" else "Assassin"
        elif event.keysym in ["Down","s"] and perso[0] != "Mage" : perso[0] = "Archer" if perso[0] == "Barbarian" else "Assassin" if perso[0] == "Archer" else "Mage"
        elif event.keysym == "h" : ecran = 3
        elif event.keysym == "Return" :
            ecran,perso = 7,[perso[0],[l_persos[perso[0]][0]]*2,[l_persos[perso[0]][1]]*2,[l_persos[perso[0]][2]]*2,[l_persos[perso[0]][3]]*2,[l_persos[perso[0]][4]]*2,[l_persos[perso[0]][5],l_persos[perso[0]][6],l_persos[perso[0]][7],l_persos[perso[0]][8]],0,0,0,0,0]
            crea_donjon(perso[11])
            ecran = 8
    elif ecran == 3 and event.keysym in "hd" : ecran = {"h" : 2,"d" : 4}[event.keysym]
    elif ecran == 4 and event.keysym in "hqd" : ecran = {"h" : 2,"q" : 3,"d" : 5}[event.keysym]
    elif ecran == 5 and event.keysym in "hqd" : ecran = {"h" : 2,"q" : 4,"d" : 6}[event.keysym]
    elif ecran == 6 and event.keysym in "hq" : ecran = {"h" : 2,"q" : 5}[event.keysym]
    elif ecran == 8 and possib_mouv == 1 :
        coords = list(perso[-1])
        if event.keysym == "Escape" : ecran,c = 11,0
        elif event.keysym == "Return" and len(l_ennemis) > 0 : nouveau_tour()
        elif event.keysym == "a" : ecran = 9
        elif event.keysym == "e" : crea_donjon(0)
        elif event.keysym in ["z","Up"] and perso[4][1] > 0 and not map[perso[-1][1]-1][perso[-1][0]] in "█▓" : perso[-1][1] -= 1
        elif event.keysym in ["s","Down"] and perso[4][1] > 0 and not map[perso[-1][1]+1][perso[-1][0]] in "█▓" : perso[-1][1] += 1
        elif event.keysym in ["q","Left"] and perso[4][1] > 0 and not map[perso[-1][1]][perso[-1][0]-1] in "█▓" : perso[-1][0] -= 1
        elif event.keysym in ["d","Right"] and perso[4][1] > 0 and not map[perso[-1][1]][perso[-1][0]+1] in "█▓" : perso[-1][0] += 1
        elif event.char in "&1" : perso[10] = 0
        elif event.char in "é2" : perso[10] = 1
        elif event.char in '"3' : perso[10] = 2
        if event.keysym in ["z","s","q","d","Up","Down","Left","Right"] and map[perso[-1][1]][perso[-1][0]] == "*" :
            ecran,perso[11] = 7,perso[11]+1
            crea_donjon(perso[11])
            ecran = 8
        else :
            if event.keysym in ["z","s","q","d","Up","Down","Left","Right"] :
                if len(l_ennemis) > 0 :
                    for i in l_ennemis :
                        if i[1] == perso[-1][0] and i[2] == perso[-1][1] or i[0] == "sq" and [perso[-1][0],perso[-1][1]] in [[i[1]+j,i[2]+k] for j in range (4) for k in range (4)] or i[0] == "gs" and [perso[-1][0],perso[-1][1]] in i[4] :
                            if event.keysym in ["z","Up"] : perso[-1][1] += 1
                            elif event.keysym in ["s","Down"] : perso[-1][1] -= 1
                            elif event.keysym in ["q","Left"] : perso[-1][0] += 1
                            elif event.keysym in ["d","Right"] : perso[-1][0] -= 1
                            break
                    if perso[4][1] > 0 and perso[-1] != coords : perso[4][1] -= 1
                    if map[perso[-1][1]][perso[-1][0]] == "¤" :
                        cooldown_armure = 2
                        if perso[2][1] > 0 : perso[2][1] -= 1
                        else : perso[1][1] -= 1
                    elif map[perso[-1][1]][perso[-1][0]] == "§" and len(l_ennemis) > 0 :
                        cooldown_armure,map[perso[-1][1]][perso[-1][0]],l_effets = 2,"-",l_effets+[["Burn",2]]
                        if perso[2][1] > 0 : perso[2][1] -= 1
                        else : perso[1][1] -= 1
                    elif map[perso[-1][1]][perso[-1][0]] == "#" and len(l_ennemis) > 0 : perso[4][1],cooldown_armure,map[perso[-1][1]][perso[-1][0]] = 0,2,"-"
                if len(l_fantomes) > 0 and perso[-1][0]//20 == l_fantomes[0][0]//20 and perso[-1][1]//20 == l_fantomes[0][1]//20 and 0 < perso[-1][0]%20 < 15 and 0 < perso[-1][1]%20 < 15 :
                    if perso[-1] in l_fantomes :
                        affich()
                        ecran = 12
                    else :
                        for i in range (len(l_fantomes)) :
                            if i == 0 : grille,b,m = path_finding(l_fantomes[i],perso[-1])
                            elif i in [1,2] :
                                p = list(perso[-1])
                                if event.keysym in ["z","Up"] and (p[1]%20 >= 3 and l_fantomes[i] == [p[0],p[1]-2] or p[1]%20 >= 2 and l_fantomes[i] == [p[0],p[1]-1]) or event.keysym in ["s","Down"] and (p[1]%20 <= 12 and l_fantomes[i] == [p[0],p[1]+2] or p[1]%20 <= 13 and l_fantomes[i] == [p[0],p[1]+1]) or event.keysym in ["q","Left"] and (p[0]%20 >= 3 and l_fantomes[i] == [p[0]-2,p[1]] or p[0]%20 >= 2 and l_fantomes[i] == [p[0]-1,p[1]]) or event.keysym in ["d","Right"] and (p[0]%20 <= 12 and l_fantomes[i] == [p[0]+2,p[1]] or p[0]%20 <= 13 and l_fantomes[i] == [p[0]+1,p[1]]) : grille,b,m = path_finding(l_fantomes[i],perso[-1])
                                else :
                                    if event.keysym in ["z","Up"] : p[1] = p[1]-2 if p[1]%20 >= 3 and not map[p[1]-2][p[0]] in "█▓" else p[1]-1 if p[1]%20 >= 2 and not map[p[1]-1][p[0]] in "█▓" else p[1]
                                    elif event.keysym in ["s","Down"] : p[1] = p[1]+2 if p[1]%20 <= 12 and not map[p[1]+2][p[0]] in "█▓" else p[1]+1 if p[1]%20 <= 13 and not map[p[1]+1][p[0]] in "█▓" else p[1]
                                    elif event.keysym in ["q","Left"] : p[0] = p[0]-2 if p[0]%20 >= 3 and not map[p[1]][p[0]-2] in "█▓" else p[0]-1 if p[0]%20 >= 2 and not map[p[1]][p[0]-1] in "█▓" else p[0]
                                    elif event.keysym in ["d","Right"] : p[0] = p[0]+2 if p[0]%20 <= 12 and not map[p[1]][p[0]+2] in "█▓" else p[0]+1 if p[0]%20 <= 13 and not map[p[1]][p[0+1]] in "█▓" else p[0]
                                    grille,b,m = path_finding(l_fantomes[i],p)
                            elif i == 3 :
                                if abs(perso[-1][0]-l_fantomes[i][0])+abs(perso[-1][1]-l_fantomes[i][1]) > 8 : grille,b,m = path_finding(l_fantomes[i],perso[-1])
                                else : grille,b,m = path_finding(l_fantomes[i],[l_fantomes[i][0]//20*20+1,l_fantomes[i][1]//20*20+14])
                            grille[b[0][1]][b[0][0]] = m+1
                            if b[0][0] != 0 and grille[b[0][1]][b[0][0]-1] == grille[b[0][1]][b[0][0]] or b[0][1] != 0 and grille[b[0][1]-1][b[0][0]] == grille[b[0][1]][b[0][0]] or b[0][0] != 13 and grille[b[0][1]][b[0][0]+1] == grille[b[0][1]][b[0][0]] or b[0][1] != 13 and grille[b[0][1]+1][b[0][0]] == grille[b[0][1]][b[0][0]] : grille[b[0][1]][b[0][0]] += 1
                            while grille[b[0][1]][b[0][0]] != 0 :
                                for j in [[0,-1],[0,1],[-1,0],[1,0]] :
                                    if 0 <= b[0][0]+j[0] <= 13 and 0 <= b[0][1]+j[1] <= 13 and grille[b[0][1]+j[1]][b[0][0]+j[0]] == grille[b[0][1]][b[0][0]]-1 :
                                        b = [[b[0][0]+j[0],b[0][1]+j[1]]]+b
                                        break
                            b = b[1:-1]
                            if len(b) > 0 : l_fantomes[i][0],l_fantomes[i][1] = l_fantomes[i][0]//20*20+1+b[0][0],l_fantomes[i][1]//20*20+1+b[0][1]
                            else :
                                l_fantomes[i] = perso[-1]
                                affich()
                                ecran = 12
                                break
                for i in range (len(l_objets)) :
                    if l_objets[i][0] == perso[-1][0] and l_objets[i][1] == perso[-1][1] :
                        non = 0
                        if l_objets[i][2] != "◙" :
                            if donjon[perso[-1][1]//20][perso[-1][0]//20] == "shop" and perso[7] >= cout_objets[l_objets[i][2]] : perso[7] -= cout_objets[l_objets[i][2]]
                            elif donjon[perso[-1][1]//20][perso[-1][0]//20] == "devildeal" and perso[1][0] > cout_objets[l_objets[i][3]] :
                                perso[1][0] -= cout_objets[l_objets[i][3]]
                                if perso[1][1] > perso[1][0] : perso[1][1] = perso[1][0]
                            elif donjon[perso[-1][1]//20][perso[-1][0]//20] in ["shop","devildeal"] : non = 1
                        if non == 0 :
                            if l_objets[i][2] == "♥" : perso[1][1] = perso[1][1]+1 if perso[1][1] < perso[1][0] else perso[1][1]
                            elif l_objets[i][2] == "◙" : perso[7] = perso[7]+1 if perso[7] < 99 else perso[7]
                            elif l_objets[i][2] == "y" : perso[8] = perso[8]+1 if perso[8] < 99 else perso[8]
                            elif l_objets[i][2] == "σ" : perso[9] = perso[9]+1 if perso[9] < 99 else perso[9]
                            else :
                                if l_objets[i][3] == "Health" : perso[1][0],perso[1][1] = perso[1][0]+1,perso[1][1]+1
                                elif l_objets[i][3] == "Protection" : perso[2][0],perso[2][1] = perso[2][0]+1,perso[2][1]+1
                                elif l_objets[i][3] == "Strong inside" and perso[2][0] > 0 : perso[1][0],perso[1][1],perso[2][0],perso[2][1] = perso[1][0]+1,perso[1][1]+1,perso[2][0]-1,perso[2][1]-1
                                elif l_objets[i][3] == "Strong outside" and perso[1][0] > 1 : perso[1][0],perso[1][1],perso[2][0],perso[2][1] = perso[1][0]-1,perso[1][1]-1 if perso[1][1] == perso[1][0] else perso[1][1],perso[2][0]+1,perso[2][1]+1
                                elif l_objets[i][3] == "Vampirism" and not ["Vampirism"] in l_effets : l_effets += [["Vampirism"]]
                                elif l_objets[i][3] == "Strenght" : perso[6] = [i+1 for i in perso[6]]
                                elif l_objets[i][3] == "Skillful" and perso[5][0] > 1 : perso[5][0],perso[5][1] = perso[5][0]-1,perso[5][1]-1
                                elif l_objets[i][3] == "Powerful" : perso[3][0],perso[3][1] = perso[3][0]+1,perso[3][1]+1
                                elif l_objets[i][3] == "Boots" : perso[4][0],perso[4][1] = perso[4][0]+1,perso[4][1]+1
                                elif l_objets[i][3] == "Strong but slow" and perso[4][0] > 1 : perso[3][0],perso[3][1],perso[4][0],perso[4][1] = perso[3][0]+1,perso[3][1]+1,perso[4][0]-1,perso[4][1]-1
                                elif l_objets[i][3] == "Fast but weak" and perso[3][0] > 1 : perso[3][0],perso[3][1],perso[4][0],perso[4][1] = perso[3][0]-1,perso[3][1]-1,perso[4][0]+1,perso[4][1]+1
                                ecran,info3 = 10,[l_objets[i][3],{"Health" : " +1 HP max ","Protection" : " +1 armor max ","Strong inside" : " +1 HP max / -1 armor max ","Strong outside" : " -1 HP max / +1 armor max ","Vampirism" : " Chance to recover HP when you kill ","Strenght" : " +1 damage ","Skillful" : " -1 cooldown special ","Powerful" : " +1 AP  ","Boots" : " +1 MP ","Strong but slow" : " +1 PA / -1 MP ","Fast but weak" : " -1 PA / +1 MP "}[l_objets[i][3]]]
                            del l_objets[i]
                        else :
                            if event.keysym in ["z","Up"] : perso[-1][1] += 1
                            elif event.keysym in ["s","Down"] : perso[-1][1] -= 1
                            elif event.keysym in ["q","Left"] : perso[-1][0] += 1
                            elif event.keysym in ["d","Right"] : perso[-1][0] -= 1
                        break
            if event.keysym in ["z","s","q","d","Up","Down","Left","Right"] and explore[perso[-1][1]//20][perso[-1][0]//20] == 0 and (perso[-1][1]-perso[-1][1]//20*20 == 15 and explore[(perso[-1][1]-1)//20][perso[-1][0]//20] == 0 or perso[-1][1]-perso[-1][1]//20*20 == 0 and explore[(perso[-1][1]+1)//20][perso[-1][0]//20] == 0 or perso[-1][0]-perso[-1][0]//20*20 == 15 and explore[perso[-1][1]//20][(perso[-1][0]-1)//20] == 0 or perso[-1][0]-perso[-1][0]//20*20 == 0 and explore[perso[-1][1]//20][(perso[-1][0]+1)//20] == 0) :
                explore[perso[-1][1]//20][perso[-1][0]//20] = 1
                if "fight" in donjon[perso[-1][1]//20][perso[-1][0]//20] or donjon[perso[-1][1]//20][perso[-1][0]//20] == "boss" :
                    if event.keysym in ["z","Up"] : perso[-1][1] -= 1
                    elif event.keysym in ["s","Down"] : perso[-1][1] += 1
                    elif event.keysym in ["q","Left"] : perso[-1][0] -= 1
                    elif event.keysym in ["d","Right"] : perso[-1][0] += 1
                    if perso[-1][1]//20 > 0 and donjon[perso[-1][1]//20-1][perso[-1][0]//20] != "" and (donjon[perso[-1][1]//20-1][perso[-1][0]//20] != "secretroom" or explore[perso[-1][1]//20-1][perso[-1][0]//20] == 1) : map[perso[-1][1]//20*20][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["▓","▓"]
                    if perso[-1][1]//20 < len(donjon)-1 and donjon[perso[-1][1]//20+1][perso[-1][0]//20] != "" and (donjon[perso[-1][1]//20+1][perso[-1][0]//20] != "secretroom" or explore[perso[-1][1]//20+1][perso[-1][0]//20] == 1) : map[perso[-1][1]//20*20+15][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["▓","▓"]
                    if perso[-1][0]//20 > 0 and donjon[perso[-1][1]//20][perso[-1][0]//20-1] != "" and (donjon[perso[-1][1]//20][perso[-1][0]//20-1] != "secretroom" or explore[perso[-1][1]//20][perso[-1][0]//20-1] == 1) : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20] = "▓","▓"
                    if perso[-1][0]//20 < len(donjon[0])-1 and donjon[perso[-1][1]//20][perso[-1][0]//20+1] != "" and (donjon[perso[-1][1]//20][perso[-1][0]//20+1] != "secretroom" or explore[perso[-1][1]//20][perso[-1][0]//20+1] == 1) : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+15],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20+15] = "▓","▓"
                    if "fight" in donjon[perso[-1][1]//20][perso[-1][0]//20] :
                        if perso[11] < 6 : n = randint(perso[11]+2,perso[11]+4)
                        else : n = randint(8,10)
                        l_p = [[1,1],[14,1],[1,14],[14,14],[7,6],[8,6],[7,9],[8,9],[6,7],[6,8],[9,7],[9,8]]
                        for i in range (n) :
                            p = l_p[randint(0,len(l_p)-1)]
                            l_ennemis += [["OXWTM"[randint(0,perso[11])] if perso[11] < 4 else "OXWTM"[randint(0,4)],perso[-1][0]//20*20+p[0],perso[-1][1]//20*20+p[1]]]
                            l_ennemis[-1] += [l_mobs[l_ennemis[-1][0]][1]]
                            del l_p[l_p.index(p)]
                    else :
                        b = ["dk","nw"] if perso[11] == 0 else ["dk","nw","sq","sq","gs","gs"] if perso[11] == 1 else ["dk","nw","sq","sq","gs","gs","pd","pd","pd"]
                        b = b[randint(0,len(b)-1)]
                        if b in ["dk","nw","pd"] : l_ennemis += [[b,perso[-1][0]//20*20+7,perso[-1][1]//20*20+7,l_mobs[b][1]]]
                        elif b == "sq" : l_ennemis += [[b,perso[-1][0]//20*20+6,perso[-1][1]//20*20+6,l_mobs[b][1],4]]
                        elif b == "gs" :
                            l_ennemis,fruit = l_ennemis+[[b,perso[-1][0]//20*20+7,perso[-1][1]//20*20+7,l_mobs[b][1],4,[[perso[-1][0]//20*20+8,perso[-1][1]//20*20+7],[perso[-1][0]//20*20+8,perso[-1][1]//20*20+8],[perso[-1][0]//20*20+7,perso[-1][1]//20*20+8]]]],[perso[-1][0]//20*20+randint(1,14),perso[-1][1]//20*20+randint(1,14)]
                            while 7 <= fruit[0]%20 <= 8 and 7 <= fruit[1]%20 <= 8 : fruit = [perso[-1][0]//20*20+randint(1,14),perso[-1][1]//20*20+randint(1,14)]
                    info2 = "You turn"
            if event.keysym in ["z","s","q","d","Up","Down","Left","Rigth"] and perso[1][1] <= 0 : ecran = 12
    elif ecran == 9 :
        if event.keysym == "a" : ecran = 8
        elif event.char in "&1" : perso[10] = 0
        elif event.char in "é2" : perso[10] = 1
        elif event.char in '"3' : perso[10] = 2
    elif ecran == 10 : ecran = 8
    elif ecran == 11 :
        if event.keysym in ["z","Up"] and c > 0 : c -= 1
        elif event.keysym in ["s","Down"] and c < 2 : c += 1
        elif event.keysym in ["q","Left"] and c == 2 and delai > 0 : delai = ((delai*10)-1)/10
        elif event.keysym in ["d","Right"] and c == 2 and delai < 2 : delai = ((delai*10)+1)/10
        elif event.keysym == "Return" :
            if c == 0 : ecran = 8
            elif c == 1 : ecran = 12
    affich()

def explosion(i) :
    global bombe
    bombe[2] = 1-bombe[2]
    affich()
    if i < 30 : fenetre.after(100,explosion,i+1)
    else :
        sleep(0.1)
        for i in [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)] :
            map[bombe[1]+i[1]][bombe[0]+i[0]] = {"█" : "m","-" : "s","¤" : "s","§" : "s","#" : "s"}[map[bombe[1]+i[1]][bombe[0]+i[0]]] if map[bombe[1]+i[1]][bombe[0]+i[0]] != "▓*" else map[bombe[1]+i[1]][bombe[0]+i[0]]
        for i in range (len(donjon)) :
            for j in range (len(donjon[i])) :
                if donjon[i][j] == "secretroom" and (i > 0 and (map[(i-1)*20+15][j*20+7] in "ms" or map[(i-1)*20+15][j*20+8] in "ms") or i < len(donjon)-1 and (map[(i+1)*20][j*20+7] in "ms" or map[(i+1)*20][j*20+8] in "ms") or j > 0 and (map[i*20+7][(j-1)*20+15] in "ms" or map[i*20+8][(j-1)*20+15] in "ms") or j < len(donjon[i])-1 and (map[i*20+7][(j+1)*20] in "ms" or map[i*20+8][(j+1)*20] in "ms")) :
                    explore[i][j] = 1
                    for k in range (6) :
                        if j > 0 and donjon[i][j-1] != "" : map[i*20+6][j*20-k],map[i*20+7][j*20-k],map[i*20+8][j*20-k],map[i*20+9][j*20-k] = "█","-","-","█"
                        if i > 0 and donjon[i-1][j] != "" : map[i*20-k][j*20+6:j*20+10] = ["█","-","-","█"]
                        if j < len(donjon[i])-1 and donjon[i][j+1] != "" : map[i*20+6][j*20+15+k],map[i*20+7][j*20+15+k],map[i*20+8][j*20+15+k],map[i*20+9][j*20+15+k] = "█","-","-","█"
                        if i < len(donjon)-1 and donjon[i+1][j] != "" : map[i*20+15+k][j*20+6:j*20+10] = ["█","-","-","█"]
        for i in [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)] :
            map[bombe[1]+i[1]][bombe[0]+i[0]] = "-" if map[bombe[1]+i[1]][bombe[0]+i[0]] == "s" else "█" if map[bombe[1]+i[1]][bombe[0]+i[0]] == "m" and not (map[bombe[1]+i[1]][bombe[0]+i[0]-1] != " " and map[bombe[1]+i[1]-1][bombe[0]+i[0]] != " " and map[bombe[1]+i[1]][bombe[0]+i[0]+1] != " " and map[bombe[1]+i[1]+1][bombe[0]+i[0]] != " ") else "-"
        bombe = []
        affich()

def test_obstacle(p1,p2) :
    non,nb_p,nb_b,nb_t,a = 0,0,0,0,[p1[0],p1[1],abs(p2[0]-p1[0])/abs(p2[1]-p1[1]) if abs(p2[1]-p1[1]) > abs(p2[0]-p1[0]) else abs(p2[0]-p1[0]),abs(p2[1]-p1[1])/abs(p2[0]-p1[0]) if abs(p2[0]-p1[0]) > abs(p2[1]-p1[1]) else abs(p2[1]-p1[1])]
    if p1[0] > p2[0] : a[2] = -a[2]
    if p1[1] > p2[1] : a[3] = -a[3]
    add_x,add_y = 0.5 if a[2] >= 0 else -0.5,0.5 if a[3] >= 0 else -0.5
    while int(a[0]+add_x) != p2[0] and int(a[1]+add_y) != p2[1] :
        if map[int(a[1]+add_y)][int(a[0]+add_x)] in "█▓" or 1 in [1 for i in l_ennemis if i[1] == int(a[0]+add_x) and i[2] == int(a[1]+add_y)] :
            non = 1
            break
        elif map[int(a[1]+add_y)][int(a[0]+add_x)] == "¤" : nb_p += 1
        elif map[int(a[1]+add_y)][int(a[0]+add_x)] == "§" : nb_b += 1
        elif map[int(a[1]+add_y)][int(a[0]+add_x)] == "#" : nb_t += 1
        a[0],a[1] = a[0]+a[2],a[1]+a[3]
    return non,nb_p,nb_b,nb_t

def nouveau_tour() :
    global ecran
    global map
    global l_ennemis
    global perso
    global l_effets
    global cooldown_armure
    global info2
    global possib_mouv
    global fruit
    possib_mouv = 0
    perso[2][1],perso[3][1],perso[4][1],perso[5][1],cooldown_armure = perso[2][1]+1 if cooldown_armure == 0 and perso[2][1] < perso[2][0] else perso[2][1],perso[3][0],perso[4][0],perso[5][1]-1 if perso[5][1] > 0 else perso[5][1],cooldown_armure-1 if cooldown_armure > 0 else cooldown_armure
    if map[perso[-1][1]][perso[-1][0]] == "¤" :
        if perso[2][1] > 0 : perso[2][1] -= 1
        else : perso[1][1] -= 1
    elif map[perso[-1][1]][perso[-1][0]] == "§" :
        if perso[2][1] > 0 : perso[2][1] -= 1
        else : perso[1][1] -= 1
        l_effet,map[perso[-1][1]][perso[-1][0]] = l_effets+[["Burn",2]],"-"
    i = 0
    while i < len(l_effets) :
        if l_effets[i][0] in ["Poison","Burn"] :
            cooldown_armure = 2
            if perso[2][1] > 0 : perso[2][1] -= 1
            else : perso[1][1] -= 1
        if len(l_effets[i]) > 1 : l_effets[i][1] -= 1
        if len(l_effets[i]) > 1 and l_effets[i][1] == 0 :
            if l_effets[i][0] == "Berserk" : perso[6] = [int(perso[6][0]/2),int(perso[6][1]/2),int(perso[6][2]/2),int(perso[6][3]/2)]
            elif l_effets[i][0] == "Wall" : map[l_effets[i][3]][l_effets[i][2]] = "-"
            del l_effets[i]
        else : i += 1
    if perso[1][1] <= 0 :
        ecran = 12
        sleep(1)
    else :
        for i in range (len(l_ennemis)) :
            if l_ennemis[i][0] in ["dn","sq","nw","gs","pd"] :
                if l_ennemis[i][0] == "dk" and abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 and l_ennemis[i][3] < l_mobs["dk"][1] :
                    l_ennemis[i][3] += l_mobs["dk"][5]
                    if l_ennemis[i][3] > l_mobs["dk"][1] : l_ennemis[i][3] = l_mobs["dk"][1]
                    info2 = "Boss : heals"
                    affich()
                    sleep(delai)
                elif l_ennemis[i][0] == "nw" and abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 :
                    cooldown_armure = 2
                    if perso[2][1] >= l_mobs["nw"][5] : perso[2][1] -= l_mobs["nw"][5]
                    else : perso[2][1],perso[1][1] = 0,perso[1][1]-(l_mobs["nw"][5]-perso[2][1])
                    if l_ennemis[i][1] > perso[-1][0] : d = [-1,0]
                    elif l_ennemis[i][1] < perso[-1][0] : d = [1,0]
                    elif l_ennemis[i][2] > perso[-1][1] : d = [0,-1]
                    elif l_ennemis[i][2] > perso[-1][1] : d = [0,1]
                    for j in range (2) :
                        if map[perso[-1][1]+d[1]][perso[-1][0]+d[0]] in "-¤§#" : perso[-1][0],perso[-1][1] = perso[-1][0]+d[0],perso[-1][1]+d[1]
                        else : break
                    info2 = "Boss : ejects"
                    affich()
                    sleep(delai)
                info2 = "Boss : moving"
                l_dep = path_finding(l_ennemis[i][1:3],perso[-1])
                for j in range (l_mobs[l_ennemis[i][0]][2]) :
                    pos_mobs = [[k[1],k[2]] for k in l_ennemis]
                    for k in l_ennemis :
                        if k[0] == "sq" : pos_mobs += [[k[1]+l,k[2]+m] for l in range (4) for m in range (4)]
                        elif k[0] == "gs" : pos_mobs += [[l[0],l[1]] for l in k[5]]
                    pos_mobs += list(perso[-1])
                    if l_ennemis[i][0] in ["dk","pd"] and len(l_dep) > 0 :
                        if l_ennemis[i][0] == "dk" : map[l_ennemis[i][2]][l_ennemis[i][1]] = "§"
                        l_ennemis[i][1:3] = l_dep[0]
                        del l_dep[0]
                    elif l_ennemis[i][0] == "nw" :
                        if len(l_dep) > 4 :
                            l_ennemis[i][1:3] = l_dep[0]
                            del l_dep[0]
                        elif abs(perso[-1][0]-l_ennemis[i][1])+abs(perso[-1][1]-l_ennemis[i][2]) < 4 :
                            if perso[-1][0] > l_ennemis[i][1] and map[l_ennemis[i][2]][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1]-1,l_ennemis[i][2]]
                            elif perso[-1][0] < l_ennemis[i][1] and map[l_ennemis[i][2]][l_ennemis[i][1]+1] in "-¤§#" and not [l_ennemis[i][1]+1,l_ennemis[i][2]] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1]+1,l_ennemis[i][2]]
                            elif perso[-1][1] > l_ennemis[i][2] and map[l_ennemis[i][2]-1][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]-1] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1],l_ennemis[i][2]-1]
                            elif perso[-1][1] < l_ennemis[i][2] and map[l_ennemis[i][2]+1][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]+1] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1],l_ennemis[i][2]+1]
                    elif l_ennemis[i][0] == "sq" :
                        if perso[-1][0] <= l_ennemis[i][1]+1 and perso[-1][1] < l_ennemis[i][2]+1 : direc = [-1,-1]
                        elif perso[-1][0] > l_ennemis[i][1]+1 and perso[-1][1] <= l_ennemis[i][2]+1 : direc = [1,-1]
                        elif perso[-1][0] >= l_ennemis[i][1]+1 and perso[-1][1] > l_ennemis[i][2]+1 : direc = [1,1]
                        elif perso[-1][0] < l_ennemis[i][1]+1 and perso[-1][1] >= l_ennemis[i][2]+1 : direc = [-1,1]
                        if abs(perso[-1][0]-l_ennemis[i][1]+1) >= abs(perso[-1][1]-l_ennemis[i][2]+1) : direc = 3+direc[0]*-1
                        else : direc = 2+direc[1]
                        if direc == 1 and map[l_ennemis[i][2]-1][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]-1] in pos_mobs and map[l_ennemis[i][2]-1][l_ennemis[i][1]+1] in "-¤§#" and not [l_ennemis[i][1]+1,l_ennemis[i][2]-1] in pos_mobs and map[l_ennemis[i][2]-1][l_ennemis[i][1]+2] in "-¤§#" and not [l_ennemis[i][1]+2,l_ennemis[i][2]-1] in pos_mobs and map[l_ennemis[i][2]-1][l_ennemis[i][1]+3] in "-¤§#" and not [l_ennemis[i][1]+3,l_ennemis[i][2]-1] in pos_mobs :
                            l_ennemis[i][2] -= 1
                            map[l_ennemis[2]+4][l_ennemis[1]+1:l_ennemis[1]+3] = ["#","#"]
                        elif direc == 2 and map[l_ennemis[i][2]][l_ennemis[i][1]+4] in "-¤§#" and not [l_ennemis[i][1]+4,l_ennemis[i][2]] in pos_mobs and map[l_ennemis[i][2]+1][l_ennemis[i][1]+4] in "-¤§#" and not [l_ennemis[i][1]+4,l_ennemis[i][2]+1] in pos_mobs and map[l_ennemis[i][2]+2][l_ennemis[i][1]+4] in "-¤§#" and not [l_ennemis[i][1]+4,l_ennemis[i][2]+2] in pos_mobs and map[l_ennemis[i][2]+3][l_ennemis[i][1]+4] in "-¤§#" and not [l_ennemis[i][1]+4,l_ennemis[i][2]+3] in pos_mobs :
                            l_ennemis[i][1] += 1
                            map[l_ennemis[2]+1][l_ennemis[1]-1],map[l_ennemis[2]+2][l_ennemis[1]-1] = "#","#"
                        elif direc == 3 and map[l_ennemis[i][2]+4][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]+4] in pos_mobs and map[l_ennemis[i][2]+4][l_ennemis[i][1]+1] in "-¤§#" and not [l_ennemis[i][1]+1,l_ennemis[i][2]+4] in pos_mobs and map[l_ennemis[i][2]+4][l_ennemis[i][1]+2] in "-¤§#" and not [l_ennemis[i][1]+2,l_ennemis[i][2]+4] in pos_mobs and map[l_ennemis[i][2]+4][l_ennemis[i][1]+3] in "-¤§#" and not [l_ennemis[i][1]+3,l_ennemis[i][2]+4] in pos_mobs :
                            l_ennemis[i][2] += 1
                            map[l_ennemis[2]-1][l_ennemis[1]+1:l_ennemis[1]+3] = ["#","#"]
                        elif direc == 4 and map[l_ennemis[i][2]][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]] in pos_mobs and map[l_ennemis[i][2]+1][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]+1] in pos_mobs and map[l_ennemis[i][2]+2][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]+2] in pos_mobs and map[l_ennemis[i][2]+3][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]+3] in pos_mobs :
                            l_ennemis[i][1] -= 1
                            map[l_ennemis[2]+1][l_ennemis[1]+4],map[l_ennemis[2]+2][l_ennemis[1]+4] = "#","#"
                        l_ennemis[i][4] = direc
                    elif l_ennemis[i][0] == "gs" :
                        if abs(perso[-1][0]-l_ennemis[i][1])+abs(perso[-1][1]-l_ennemis[i][2]) >= abs(fruit[0]-l_ennemis[i][1])+abs(fruit[1]-l_ennemis[i][2]) : l_dep = path_finding(l_ennemis[i][1:3],perso[-1])
                        else : l_dep = path_finding(l_ennemis[i][1:3],fruit)
                        if len(l_dep) > 0 :
                            if l_ennemis[i][1:3] == [l_dep[0][0],l_dep[0][1]+1] : l_ennemis[i][4] = 1
                            elif l_ennemis[i][1:3] == [l_dep[0][0]-1,l_dep[0][1]] : l_ennemis[i][4] = 2
                            elif l_ennemis[i][1:3] == [l_dep[0][0],l_dep[0][1]-1] : l_ennemis[i][4] = 3
                            elif l_ennemis[i][1:3] == [l_dep[0][0]+1,l_dep[0][1]] : l_ennemis[i][4] = 4
                            l_ennemis[i][5],l_ennemis[i][1:3] = l_ennemis[i][1:3]+l_ennemis[i][5],l_dep[0]
                            del l_ennemis[i][5][-1]
                            if perso[-1] == l_ennemis[i][1:3] : perso[1][1],perso[2][1] = 0,0
                        else :
                            if [l_ennemis[i][1],l_ennemis[i][2]-1] == perso[-1] : d = 1
                            elif [l_ennemis[i][1]+1,l_ennemis[i][2]] == perso[-1] : d = 2
                            elif [l_ennemis[i][1],l_ennemis[i][2]+1] == perso[-1] : d = 3
                            elif [l_ennemis[i][1]-1,l_ennemis[i][2]] == perso[-1] : d = 4
                            elif [l_ennemis[i][1],l_ennemis[i][2]-1] == fruit : d = 1
                            elif [l_ennemis[i][1]+1,l_ennemis[i][2]] == fruit : d = 2
                            elif [l_ennemis[i][1],l_ennemis[i][2]+1] == fruit : d = 3
                            elif [l_ennemis[i][1]-1,l_ennemis[i][2]] == fruit : d = 4
                            else :
                                p = []
                                if map[l_ennemis[i][1]][l_ennemis[i][2]-1] in "-¤§#" : p += [1]
                                elif map[l_ennemis[i][1]+1][l_ennemis[i][2]] in "-¤§#" : p += [2]
                                elif map[l_ennemis[i][1]][l_ennemis[i][2]+1] in "-¤§#" : p += [3]
                                elif map[l_ennemis[i][1]-1][l_ennemis[i][2]] in "-¤§#" : p += [4]
                                if len(p) == 0 : d = ""
                                else : d = p[randint(0,len(p)-1)]
                            if d == "" :
                                del l_ennemis[i]
                                perso[2][1],perso[3][1],perso[4][1],perso[5][1] = perso[2][0],perso[3][0],perso[4][0],perso[5][0]
                                for i in range (len(l_effets)) :
                                    if l_effets[0][0] == "Berserk" : perso[6] = [int(perso[6][0]/2),int(perso[6][1]/2),int(perso[6][2]/2),int(perso[6][3]/2)]
                                    elif l_effets[0][0] == "Wall" : map[l_effets[0][3]][l_effets[0][2]] = "-"
                                    del l_effets[0]
                                if map[perso[-1][1]//20*20][perso[-1][0]//20*20+7] == "▓" : map[perso[-1][1]//20*20][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["-","-"]
                                if map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+15] == "▓" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+15],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20+15] = "-","-"
                                if map[perso[-1][1]//20*20+15][perso[-1][0]//20*20+7] == "▓" : map[perso[-1][1]//20*20+15][perso[-1][0]//20*20+7:perso[-1][0]//20*20+9] = ["-","-"]
                                if map[perso[-1][1]//20*20+7][perso[-1][0]//20*20] == "▓" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20],map[perso[-1][1]//20*20+8][perso[-1][0]//20*20] = "-","-"
                                if donjon[perso[-1][1]//20][perso[-1][0]//20] == "boss" : map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+7] = "*"
                            else :
                                l_ennemis[i][1:3] = [[l_ennemis[i][1],l_ennemis[i][2]-1],[l_ennemis[i][1]+1,l_ennemis[i][2]],[l_ennemis[i][1],l_ennemis[i][2]]+1,[l_ennemis[i][1]-1,l_ennemis[i][2]]][d-1]
                                if l_ennemis[i][1:3] == fruit :
                                    fruit = [perso[-1][0]//20*20+randint(1,14),perso[-1][1]//20*20+randint(1,14)]
                                    while 7 <= fruit[0]%20 <= 8 and 7 <= fruit[1]%20 <= 8 : fruit = [perso[-1][0]//20*20+randint(1,14),perso[-1][1]//20*20+randint(1,14)]
                                else : del l_ennemis[i][5][-1]
                                if perso[-1] == l_ennemis[i][1:3] : perso[1][1],perso[2][1] = 0,0
                    affich()
                    sleep(delai)

                degats = 0
                if l_ennemis[i][0] == "dk" :
                    if abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 : degats,info2 = l_mobs["dk"][3],"Boss : hitting"
                    elif test_obstacle(l_ennemis[i][1:3],perso[-1])[0] == 0 and (abs(l_ennemis[i][1]-perso[-1][0]) == 0 and 2 <= abs(l_ennemis[i][2]-perso[-1][1]) <= 5 or abs(l_ennemis[i][2]-perso[-1][1]) == 0 and 2 <= abs(l_ennemis[i][1]-perso[-1][0]) <= 5) :
                        non = 0
                        for j in l_ennemis :
                            if perso[-1][0] > l_ennemis[i][1] and j[1] == perso[-1][0]-1 or perso[-1][0] < l_ennemis[i][1] and j[1] == perso[-1][0]+1 or perso[-1][1] > l_ennemis[i][2] and j[2] == perso[-1][1]-1 or perso[-1][1] < l_ennemis[i][2] and j[2] == perso[-1][1]+1 :
                                non = 1
                                break
                        if non == 0 :
                            degats,info2 = l_mobs["T"][4],"Boss : charge"
                            if perso[-1][0] > l_ennemis[i][1] : l_ennemis[i][1] = perso[-1][0]-1
                            elif perso[-1][0] < l_ennemis[i][1] : l_ennemis[i][1] = perso[-1][0]+1
                            elif perso[-1][1] > l_ennemis[i][2] : l_ennemis[i][2] = perso[-1][1]-1
                            elif perso[-1][1] < l_ennemis[i][2] : l_ennemis[i][2] = perso[-1][1]+1
                elif l_ennemis[i][0] == "nw" :
                    if test_obstacle(l_ennemis[i][1:3],perso[-1])[0] == 0 and 2 <= abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) <= 4 : degats,info2 = l_mobs["nw"][3],"Boss : fireball"
                    elif l_ennemis[i][3] < 10 and abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) < 5 :
                        non = 1
                        while non == 1 :
                            x = randint(-10,10)
                            y,non = randint(-10+abs(x),10-abs(y)),0
                            if 0 <= x <= len(map[0]) and 0 <= y <= len(map) : non = 1
                            if non == 0 and not map[l_ennemis[i][2]+y][l_ennemis[i][1]+x] in "-¤§#" : non = 1
                            if non == 0 :
                                for j in l_ennemis :
                                    if j[1:3] == [x,y] :
                                        non = 1
                                        break
                        l_ennemis[i][1:3],info2 = [l_ennemis[i][1]+x,l_ennemis[i][2]+y],"Boss : tp"
                elif l_ennemis[0] == "sq" :
                    non = 1
                    for j in [[0,-1],[1,-1],[2,-1],[3,-1],[4,0],[4,1],[4,2],[4,3],[0,4],[1,4],[2,4],[3,4],[-1,0],[-1,1],[-1,2],[-1,3]] :
                        if perso[-1] == [l_ennemis[i][1]+j[0],l_ennemis[i][2]+j[1]] :
                            non = 0
                            break
                    if non == 0 : degats,l_effets,info2 = l_mobs["sq"][3],l_effets+[["Poison",3]],"Boss : poisons"
                    elif randint(1,3) == 1 :
                        p = []
                        for j in [[0,-1],[1,-1],[2,-1],[3,-1],[4,0],[4,1],[4,2],[4,3],[0,4],[1,4],[2,4],[3,4],[-1,0],[-1,1],[-1,2],[-1,3]] :
                            if map[l_ennemis[i][2]+j[1]][l_ennemis[i][1]+j[0]] in "-¤§#" and not [l_ennemis[i][1]+j[0],l_ennemis[i][2]+j[1]] in pos_mobs : p += [j]
                        if len(p) >= 2 : t = 2
                        else : t = len(p)
                        for j in range (t) :
                            n = randint(0,len(p)-1)
                            l_ennemis += [["W",l_ennemis[i][1]+p[n][0],l_ennemis[i][2]+p[n][1],l_mobs["W"][1]]]
                            del p[n]
                        if t > 0 : info2 = "Boss : summons"
                elif l_ennemis[i][0] == "pd" :
                    if abs(l_ennemis[i][1]-perso[-1][0]) == 0 and 1 <= abs(l_ennemis[i][2]-perso[-1][1]) <= 4 :
                        a = 1 if l_ennemis[i][1] < perso[-1][0] else -1
                        for j in range (1,5,1) :
                            if 0 <= l_ennemis[i][1]+j*a < len(map[0]) and map[l_ennemis[i][2]][l_ennemis[i][1]+j*a] in "-¤#" : map[l_ennemis[i][2]][l_ennemis[i][1]+j*a] = "§"
                        degats,info2 = l_mobs["pd"][3],"Boss : fire"
                    elif abs(l_ennemis[i][2]-perso[-1][1]) == 0 and 1 <= abs(l_ennemis[i][1]-perso[-1][0]) <= 4 :
                        a = 1 if l_ennemis[i][2] < perso[-1][1] else -1
                        for j in range (1,5,1) :
                            if 0 <= l_ennemis[i][2]+j*a < len(map) and map[l_ennemis[i][2]+j*a][l_ennemis[i][1]] in "-¤#" : map[l_ennemis[i][2]+j*a][l_ennemis[i][1]] = "§"
                        degats,info2 = l_mobs["pd"][3],"Boss : fire"
                    elif randint(1,3) == 1 :
                        x,y = randint(perso[-1][0]//20*20+1,perso[-1][0]//20*20+14),randint(perso[-1][1]//20*20+1,perso[-1][1]//20*20+14)
                        for j in range (-2,3,1) :
                            for k in range (-2+abs(j),2-abs(j)) :
                                if 0 <= x+k < len(map[0]) and 0 <= y+j < len(map) and 0 < (x+k)%20 < 15 and 0 < (y+j)%20 < 15 : map[y+j][x+k] = "§"
                                if [x+k,y+j] == perso[-1] : degats = l_mobs["pd"][4]
                        info2 = "Boss : explosion"

                if degats > 0 : cooldown_armure = 2
                if perso[2][1] >= degats : perso[2][1] -= degats
                else : perso[2][1],perso[1][1] = 0,perso[1][1]-(degats-perso[2][1])
                if perso[1][1] <= 0 :
                    ecran = 12
                    sleep(1)
                    affich()
                else :
                    affich()
                    sleep(delai)

            else :
                info2 = l_mobs[l_ennemis[i][0]][0]+" : moving"
                l_dep = path_finding(l_ennemis[i][1:3],perso[-1])
                if l_dep != False :
                    l_dep = [[l_ennemis[i][1]//20*20+1+j[0],l_ennemis[i][2]//20*20+1+j[1]] for j in l_dep]
                    for j in range (l_mobs[l_ennemis[i][0]][2]) :
                        pos_mobs = [[k[1],k[2]] for k in l_ennemis]
                        for k in l_ennemis :
                            if k[0] == "sq" : pos_mobs += [[k[1]%20-1+l,k[2]%20-1+m] for l in range (4) for m in range (4)]
                            elif k[0] == "gs" : pos_mobs += [[l[0]%20-1,l[1]%20-1] for l in k[5]]
                        if l_ennemis[i][0] in "OWT" and len(l_dep) > 0 :
                            l_ennemis[i][1:3] = l_dep[0]
                            del l_dep[0]
                        elif not l_ennemis[i][0] in "OWT" :
                            if len(l_dep) >= {"X" : 3,"M" : 5}[l_ennemis[i][0]] and len(l_dep) > 0 :
                                l_ennemis[i][1:3] = l_dep[0]
                                del l_dep[0]
                            elif abs(perso[-1][0]-l_ennemis[i][1])+abs(perso[-1][1]-l_ennemis[i][2]) < {"X" : 2,"M" : 5}[l_ennemis[i][0]] :
                                if perso[-1][0] > l_ennemis[i][1] and map[l_ennemis[i][2]][l_ennemis[i][1]-1] in "-¤§#" and not [l_ennemis[i][1]-1,l_ennemis[i][2]] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1]-1,l_ennemis[i][2]]
                                elif perso[-1][0] < l_ennemis[i][1] and map[l_ennemis[i][2]][l_ennemis[i][1]+1] in "-¤§#" and not [l_ennemis[i][1]+1,l_ennemis[i][2]] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1]+1,l_ennemis[i][2]]
                                elif perso[-1][1] > l_ennemis[i][2] and map[l_ennemis[i][2]-1][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]-1] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1],l_ennemis[i][2]-1]
                                elif perso[-1][1] < l_ennemis[i][2] and map[l_ennemis[i][2]+1][l_ennemis[i][1]] in "-¤§#" and not [l_ennemis[i][1],l_ennemis[i][2]+1] in pos_mobs : l_ennemis[i][1:3] = [l_ennemis[i][1],l_ennemis[i][2]+1]
                        affich()
                        sleep(delai)

                    degats = 0
                    if l_ennemis[i][0] == "O" and abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 : degats,info2 = l_mobs["O"][3],"Slime : hitting"
                    elif l_ennemis[i][0] == "X" and test_obstacle(l_ennemis[i][1:3],perso[-1])[0] == 0 and 2 <= abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) <= 3 : degats,info2 = l_mobs["X"][3],"Skeleton : shoot"
                    elif l_ennemis[i][0] == "W" :
                        if abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 : degats,l_effets,info2 = l_mobs["W"][3],l_effets+[["Poison",2]],"Spider : poisons"
                        elif randint(1,3) != 3 :
                            non = 0
                            while non != -1 and non < 12 :
                                x = randint(-2,2)
                                y = randint(-2+abs(x),2-abs(x))
                                if map[l_ennemis[i][2]+y][l_ennemis[i][1]+x] == "-" : map[l_ennemis[i][2]+y][l_ennemis[i][1]+x],info2,non = "#","Spider : web",-1
                                else : non += 1
                    elif l_ennemis[i][0] == "T" :
                        if abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) == 1 : degats,info2 = l_mobs["T"][3],"Demon : hitting"
                        elif test_obstacle(l_ennemis[i][1:3],perso[-1])[0] == 0 and (abs(l_ennemis[i][1]-perso[-1][0]) == 0 and 2 <= abs(l_ennemis[i][2]-perso[-1][1]) <= 4 or abs(l_ennemis[i][2]-perso[-1][1]) == 0 and 2 <= abs(l_ennemis[i][1]-perso[-1][0]) <= 4) :
                            non = 0
                            for j in l_ennemis :
                                if perso[-1][0] > l_ennemis[i][1] and j[1] == perso[-1][0]-1 or perso[-1][0] < l_ennemis[i][1] and j[1] == perso[-1][0]+1 or perso[-1][1] > l_ennemis[i][2] and j[2] == perso[-1][1]-1 or perso[-1][1] < l_ennemis[i][2] and j[2] == perso[-1][1]+1 :
                                    non = 1
                                    break
                            if non == 0 :
                                degats,info2 = l_mobs["T"][4],"Demon : charge"
                                if perso[-1][0] > l_ennemis[i][1] : l_ennemis[i][1] = perso[-1][0]-1
                                elif perso[-1][0] < l_ennemis[i][1] : l_ennemis[i][1] = perso[-1][0]+1
                                elif perso[-1][1] > l_ennemis[i][2] : l_ennemis[i][2] = perso[-1][1]-1
                                elif perso[-1][1] < l_ennemis[i][2] : l_ennemis[i][2] = perso[-1][1]+1
                    elif l_ennemis[i][0] == "M" :
                        if test_obstacle(l_ennemis[i][1:3],perso[-1])[0] == 0 and 1 <= abs(l_ennemis[i][1]-perso[-1][0])+abs(l_ennemis[i][2]-perso[-1][1]) <= 2 : degats,info2 = l_mobs["M"][3],"Wizard : fireball"
                        else :
                            for j in range (len(l_ennemis)) :
                                if 1 <= abs(l_ennemis[i][1]-l_ennemis[j][1])+abs(l_ennemis[i][2]-l_ennemis[j][2]) <= 10 and l_ennemis[j][3] < l_mobs[l_ennemis[j][0]][1] :
                                    l_ennemis[j][3],info2 = l_mobs[l_ennemis[j][0]][1] if l_ennemis[j][3]+l_mobs["M"][4] > l_mobs[l_ennemis[j][0]][1] else l_ennemis[j][3]+l_mobs["M"][4],"Wizard : heal"
                                    break
                    if degats > 0 : cooldown_armure = 2
                    if perso[2][1] >= degats : perso[2][1] -= degats
                    else : perso[2][1],perso[1][1] = 0,perso[1][1]-(degats-perso[2][1])
                    if perso[1][1] <= 0 :
                        ecran = 12
                        sleep(1)
                        affich()
                    else :
                        affich()
                        sleep(delai)
    info2 = "You turn"
    affich()
    possib_mouv = 1

def path_finding(dep,fin) :
    non,m,grille,b,pos_mobs = 0,-1,[[-1 for j in range (14)] for i in range (14)],[],[[i[1]%20-1,i[2]%20-1] for i in l_ennemis]
    for i in l_ennemis :
        if i[0] == "sq" : pos_mobs += [[i[1]%20-1+j,i[2]%20-1+k] for j in range (4) for k in range (4)]
        elif i[0] == "gs" : pos_mobs += [[j[0]%20-1,j[1]%20-1] for j in i[5]]
    grille[dep[1]%20-1][dep[0]%20-1],grille[fin[1]%20-1][fin[0]%20-1] = 0,-2
    while non == 0 :
        non,m = 1,m+1
        for i in range (len(grille)) :
            for j in range (len(grille[i])) :
                if grille[i][j] == m :
                    if j != 0 and grille[i][j-1] == -1 and map[dep[1]//20*20+1+i][dep[0]//20*20+j] in "-¤§#" and not [j-1,i] in pos_mobs : grille[i][j-1],non = m+1,0
                    if i != 0 and grille[i-1][j] == -1 and map[dep[1]//20*20+i][dep[0]//20*20+1+j] in "-¤§#" and not [j,i-1] in pos_mobs : grille[i-1][j],non = m+1,0
                    if j != 13 and grille[i][j+1] == -1 and map[dep[1]//20*20+1+i][dep[0]//20*20+j+2] in "-¤§#" and not [j+1,i] in pos_mobs : grille[i][j+1],non = m+1,0
                    if i != 13 and grille[i+1][j] == -1 and map[dep[1]//20*20+i+2][dep[0]//20*20+1+j] in "-¤§#" and not [j,i+1] in pos_mobs : grille[i+1][j],non = m+1,0
                    if j != 0 and grille[i][j-1] == -2 : b = [[j-1,i]]
                    elif i != 0 and grille[i-1][j] == -2 : b = [[j,i-1]]
                    elif j != 13 and grille[i][j+1] == -2 : b = [[j+1,i]]
                    elif i != 13 and grille[i+1][j] == -2 : b = [[j,i+1]]
                if len(b) == 1 :
                    non = 1
                    break
    if donjon[perso[-1][1]//20][perso[-1][0]//20] != "secretroom" :
        if len(b) == 0 : return False
        else :
            grille[b[0][1]][b[0][0]] = m+1
            if b[0][0] != 0 and grille[b[0][1]][b[0][0]-1] == grille[b[0][1]][b[0][0]] or b[0][1] != 0 and grille[b[0][1]-1][b[0][0]] == grille[b[0][1]][b[0][0]] or b[0][0] != 13 and grille[b[0][1]][b[0][0]+1] == grille[b[0][1]][b[0][0]] or b[0][1] != 13 and grille[b[0][1]+1][b[0][0]] == grille[b[0][1]][b[0][0]] : grille[b[0][1]][b[0][0]] += 1
            while grille[b[0][1]][b[0][0]] != 0 :
                if b[0][0] != 0 and grille[b[0][1]][b[0][0]-1] == grille[b[0][1]][b[0][0]]-1 : b = [[b[0][0]-1,b[0][1]]]+b
                elif b[0][1] != 0 and grille[b[0][1]-1][b[0][0]] == grille[b[0][1]][b[0][0]]-1 : b = [[b[0][0],b[0][1]-1]]+b
                elif b[0][0] != 13 and grille[b[0][1]][b[0][0]+1] == grille[b[0][1]][b[0][0]]-1 : b = [[b[0][0]+1,b[0][1]]]+b
                elif b[0][1] != 13 and grille[b[0][1]+1][b[0][0]] == grille[b[0][1]][b[0][0]]-1 : b = [[b[0][0],b[0][1]+1]]+b
            b = b[1:-1]
            return b
    else : return grille,b,m

def crea_donjon(level) :
    global donjon
    global map
    global explore
    global perso
    global l_ennemis
    global l_fantomes
    global l_effets
    global l_objets
    global cooldown_armure
    global bombe
    global info
    global info2
    global possib_mouv
    # création du schéma du donjon
    donjon,l_pieces,p = [["depart"]],[3+level,2+level] if level < 3 else [6,5],[0,0]
    while l_pieces[0] > -1 :
        d,t = randint(1,4),"fight"+str(randint(0,4)) if l_pieces[0] > 0 else "boss"
        if d == 1 :
            if p[1] == 0 : donjon,p[1] = [["" for i in range (len(donjon[0]))]]+donjon,p[1]+1
            if donjon[p[1]-1][p[0]] == "" : donjon[p[1]-1][p[0]],p[1],l_pieces[0] = t,p[1]-1,l_pieces[0]-1
        elif d == 2 :
            if p[0] == len(donjon[0])-1 : donjon = [i+[""] for i in donjon]
            if donjon[p[1]][p[0]+1] == "" : donjon[p[1]][p[0]+1],p[0],l_pieces[0] = t,p[0]+1,l_pieces[0]-1
        elif d == 3 :
            if p[1] == len(donjon)-1 : donjon += [["" for i in range (len(donjon[0]))]]
            if donjon[p[1]+1][p[0]] == "" : donjon[p[1]+1][p[0]],p[1],l_pieces[0] = t,p[1]+1,l_pieces[0]-1
        elif d == 4 :
            if p[0] == 0 : donjon,p[0] = [[""]+i for i in donjon],p[0]+1
            if donjon[p[1]][p[0]-1] == "" : donjon[p[1]][p[0]-1],p[0],l_pieces[0] = t,p[0]-1,l_pieces[0]-1
    while l_pieces[1] > -3 :
        d,t,p = randint(1,4),"fight"+str(randint(0,4)) if l_pieces[1] > 0 else "itemroom" if l_pieces[1] > -1 else ["shop","shop","devildeal"][randint(0,2)] if l_pieces[1] > -2 else "secretroom",[randint(0,len(donjon[0])-1),randint(0,len(donjon)-1)]
        if "fight" in donjon[p[1]][p[0]] or donjon[p[1]][p[0]] == "depart" :
            if d == 1 :
                if p[1] == 0 : donjon,p[1] = [["" for i in range (len(donjon[0]))]]+donjon,p[1]+1
                if donjon[p[1]-1][p[0]] == "" : donjon[p[1]-1][p[0]],p[1],l_pieces[1] = t,p[1]-1,l_pieces[1]-1
            elif d == 2 :
                if p[0] == len(donjon[0])-1 : donjon = [i+[""] for i in donjon]
                if donjon[p[1]][p[0]+1] == "" : donjon[p[1]][p[0]+1],p[0],l_pieces[1] = t,p[0]+1,l_pieces[1]-1
            elif d == 3 :
                if p[1] == len(donjon)-1 : donjon += [["" for i in range (len(donjon[0]))]]
                if donjon[p[1]+1][p[0]] == "" : donjon[p[1]+1][p[0]],p[1],l_pieces[1] = t,p[1]+1,l_pieces[1]-1
            elif d == 4 :
                if p[0] == 0 : donjon,p[0] = [[""]+i for i in donjon],p[0]+1
                if donjon[p[1]][p[0]-1] == "" : donjon[p[1]][p[0]-1],p[0],l_pieces[1] = t,p[0]-1,l_pieces[1]-1

    # création des salles et couloirs vides
    map = [[" " for j in range (len(donjon[0])*20-4)] for i in range (len(donjon)*20-4)]
    for i in range (len(donjon)) :
        for j in range (len(donjon[0])) :
            if donjon[i][j] != "" :
                for k in range (16) :
                    map[i*20+k][j*20:j*20+16] = [["█"]+["-"]*14+["█"],["█"]*16][k in [0,15]]
    for i in range (len(donjon)) :
        for j in range (len(donjon[0])) :
            if "secretroom" != donjon[i][j] != "" :
                if j < len(donjon[0])-1 and "secretroom" != donjon[i][j+1] != "" :
                    for k in range (4) :
                        map[i*20+k+6][j*20+15:j*20+21] = [["-"]*6,["█"]*6][k in [0,3]]
                if i < len(donjon)-1 and "secretroom" != donjon[i+1][j] != "" :
                    for k in range (6) :
                        map[i*20+k+15][j*20+6:j*20+10] = ["█","-","-","█"]

    # remplissage des salles
    l_objets,l_fantomes = [],[]
    salles_fight = [[["¤","¤","¤","¤","¤","¤","-","-","¤","¤","¤","¤","¤","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","¤","¤","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["-","-","¤","-","-","-","¤","¤","-","-","-","¤","-","-"],["-","-","¤","-","-","-","¤","¤","-","-","-","¤","-","-"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","-","-","-","-","-","¤","¤","-","-","-","-","-","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","¤","¤","¤","¤","¤","-","-","¤","¤","¤","¤","¤","¤"]],
    [["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","█","-","█","-","-","█","-","█","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"]],
    [["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","█","█","█","-","-","-","-","█","█","█","█","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","█","█","-","-","-","-","-","-"],["-","-","-","-","-","-","█","█","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["-","█","█","█","█","-","-","-","-","█","█","█","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"]],
    [["¤","¤","-","-","-","-","-","-","-","-","-","-","¤","¤"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["-","-","-","-","¤","█","-","-","█","¤","-","-","-","-"],["-","-","█","█","█","█","-","-","█","█","█","█","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","█","█","█","█","-","-","█","█","█","█","-","-"],["-","-","-","-","¤","█","-","-","█","¤","-","-","-","-"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["¤","-","-","-","-","-","-","-","-","-","-","-","-","¤"],["¤","¤","-","-","-","-","-","-","-","-","-","-","¤","¤"]],
    [["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["-","-","-","-","█","-","-","-","-","█","-","-","-","-"],["-","-","-","█","-","-","-","-","-","-","█","-","-","-"],["-","-","█","-","-","-","-","-","-","-","-","█","-","-"],["-","-","-","-","-","-","¤","¤","-","-","-","-","-","-"],["-","-","-","-","-","-","¤","¤","-","-","-","-","-","-"],["-","-","█","-","-","-","-","-","-","-","-","█","-","-"],["-","-","-","█","-","-","-","-","-","-","█","-","-","-"],["-","-","-","-","█","-","-","-","-","█","-","-","-","-"],["-","-","-","-","-","█","-","-","█","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"]]]
    salles_secret = [[["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","█","-","█","█","█","█","█","█","-","█","█","-"],["-","-","-","-","-","-","█","█","-","-","-","-","-","-"],["-","█","█","-","-","-","-","-","-","-","-","█","█","-"],["-","-","-","-","█","█","-","-","█","█","-","-","-","-"],["-","█","█","-","█","-","-","-","-","█","-","█","█","-"],["-","█","█","-","█","█","█","█","█","█","-","█","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","█","█","-","█","█","-","-","█","█","-","█","█","-"],["-","-","█","-","-","-","-","-","-","-","-","█","-","-"],["█","-","█","-","-","-","█","█","-","-","-","█","-","█"],["-","-","-","-","█","-","-","-","-","█","-","-","-","-"],["-","█","█","█","█","█","-","-","█","█","█","█","█","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"]],
    [["-","█","-","-","-","-","-","-","-","-","-","-","█","-"],["█","█","-","-","-","-","-","-","-","-","-","-","█","█"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-","-","-","-","-","-","-"],["█","█","-","-","-","-","-","-","-","-","-","-","█","█"],["-","█","-","-","-","-","-","-","-","-","-","-","█","-"]]]
    for i in range (len(donjon)) :
        for j in range (len(donjon[0])) :
            if "fight" in donjon[i][j] :
                for k in range (len(salles_fight[int(donjon[i][j][5])])) :
                    map[i*20+k+1][j*20+1:j*20+15] = salles_fight[int(donjon[i][j][5])][k]
            elif donjon[i][j] == "secretroom" :
                n = randint(0,3)
                if n < 2 :
                    for k in range (len(salles_secret[n])) :
                        map[i*20+k+1][j*20+1:j*20+15] = salles_secret[n][k]
                if n == 0 :
                    for k in range (1,15) :
                        for l in range (1,15) :
                            if map[i*20+k][j*20+l] == "-" and not (k == 5 and 7 <= l <= 8 or k == 6 and 6 <= l <= 9) : l_objets += [[j*20+l,i*20+k,"◙"]]
                    l_fantomes += [[j*20+6,i*20+6],[j*20+7,i*20+6],[j*20+8,i*20+6],[j*20+9,i*20+6]]
                elif n == 1 : l_objets += [[j*20+1,i*20+1,"♥"],[j*20+14,i*20+1,"♥"],[j*20+1,i*20+14,"♥"],[j*20+14,i*20+14,"♥"]]
                elif n == 2 : l_objets += [[j*20+7,i*20+6,"♥"],[j*20+8,i*20+9,"♥"],[j*20+6,i*20+8,"y"],[j*20+9,i*20+7,"σ"],[j*20+7,i*20+7,"◙"],[j*20+8,i*20+7,"◙"],[j*20+7,i*20+8,"◙"],[j*20+8,i*20+8,"◙"]]
                elif n == 3 : l_objets += [[j*20+7,i*20+7,"&",objets[randint(0,len(objets)-1)]]]
    for i in range (len(donjon)) :
        for j in range (len(donjon[0])) :
            if donjon[i][j] == "shop" or donjon[i][j] == "devildeal" or donjon[i][j] == "itemroom" :
                if not (donjon[i][j] == "itemroom" and level == 0) :
                    if map[i*20][j*20+7] == "-" : map[i*20-1][j*20+7:j*20+9] = ["▓","▓"]
                    if map[i*20+7][j*20+15] == "-" : map[i*20+7][j*20+16],map[i*20+8][j*20+16] = "▓","▓"
                    if map[i*20+15][j*20+7] == "-" : map[i*20+16][j*20+7:j*20+9] = ["▓","▓"]
                    if map[i*20+7][j*20] == "-" : map[i*20+7][j*20-1],map[i*20+8][j*20-1] = "▓","▓"
                if donjon[i][j] == "shop" : l_objets += [[j*20+6,i*20+6,"♥"],[j*20+9,i*20+6,"&",objets[randint(0,len(objets)-1)]],[j*20+6,i*20+9,"y"],[j*20+9,i*20+9,"σ"]]
                elif donjon[i][j] == "devildeal" : l_objets += [[j*20+6,i*20+7,"&",objets[randint(0,len(objets)-1)]],[j*20+9,i*20+7,"&",objets[randint(0,len(objets)-1)]]]
                elif donjon[i][j] == "itemroom" : l_objets += [[j*20+7,i*20+7,"&",objets[randint(0,len(objets)-1)]]]

    # settings des variables du jeu
    explore,l_ennemis,l_effets,cooldown_armure,bombe,info,info2,possib_mouv = [],[],[],0,[],"","",1
    for i in range (len(donjon)) :
        explore += [[]]
        for j in range (len(donjon[i])) :
            if donjon[i][j] == "depart" : explore[-1],perso = explore[-1]+[1],perso+[[j*20+7,i*20+7]]
            else : explore[-1] += [0]
    affich()

def mort() :
    global texte
    global ecran
    l = ["            ██████████████            ","        ██████████████████████        ","      ██████████████████████████      ","    ██████████████████████████████    ","  ██████████████████████████████████  ","  ██████████████████████████████████  ","██████████████████████████████████████","██████████████████████████████████████","██████████████████████████████████████","████████      ██████████      ████████","██████          ██████          ██████","██████          ██████          ██████","  ████          ██████          ██████","  ██████      ██████████      ██████  ","  ████████████████  ████████████████  ","    ████████████      ████████████    ","        ████████  ██  ████████        ","        ██████████████████████        ","          ██████████████████          ","          ██████████████████          ","            ██  ██  ██  ██            "]
    for i in range (len(l)) :
        a,b = "" if i == 0 else "\n","" if i == len(l)-1 else "\n"
        texte["text"] = "\n".join(texte["text"].split("\n")[:i])+a+" "*14+l[i]+" "*14+b+"\n".join(texte["text"].split("\n")[i+1:])
        texte.update()
        sleep(0.025)
    for i in range (26) :
        for j in range (21) :
            a,b = "" if j == 0 else "\n","" if j == 20 else "\n"
            if j%2 == 0 : texte["text"] = "\n".join(texte["text"].split("\n")[:j])+a+texte["text"].split("\n")[j][2:]+b+"\n".join(texte["text"].split("\n")[j+1:])
            else : texte["text"] = "\n".join(texte["text"].split("\n")[:j])+a+"  "+texte["text"].split("\n")[j][:-2]+b+"\n".join(texte["text"].split("\n")[j+1:])
        texte.update()
    ecran = 1
    affich()

def affich() :
    if ecran == 1 : texte["text"] = "\n\n ▓█████   ▓██  ▓██ ▓███  ▓██   ▓████   ▓██████   ▓███   ▓███  ▓██\n ▓██  ▓██ ▓██  ▓██ ▓████ ▓██ ▓██       ▓██     ▓██  ▓██ ▓████ ▓██\n ▓██  ▓██ ▓██  ▓██ ▓██▓██▓██ ▓██  ▓███ ▓████   ▓██  ▓██ ▓██▓██▓██\n ▓██  ▓██ ▓██  ▓██ ▓██ ▓████ ▓██   ▓██ ▓██     ▓██  ▓██ ▓██ ▓████\n ▓█████     ▓███   ▓██  ▓███   ▓████   ▓██████   ▓███   ▓██  ▓███\n\n             ▓███   ▓██  ▓██ ▓██████   ▓█████ ▓████████\n           ▓██  ▓██ ▓██  ▓██ ▓██     ▓██         ▓██\n           ▓██  ▓██ ▓██  ▓██ ▓████     ▓███      ▓██\n           ▓██ ████ ▓██  ▓██ ▓██          ▓██    ▓██\n             ▓████    ▓███   ▓██████ ▓█████      ▓██\n\n\n\n                          [PRESS ENTER]\n\n\n\n"
    elif ecran == 2 : texte["text"] = " "*25+"CHARACTER CHOICE\n"+"-"*66+"\n"+{"Barbarian" : "[","Archer" : " ","Assassin" : " ","Mage" : " "}[perso[0]]+"Barbarian"+{"Barbarian" : "]","Archer" : " ","Assassin" : " ","Mage" : " "}[perso[0]]+"|\n"+{"Barbarian" : " ","Archer" : "[","Assassin" : " ","Mage" : " "}[perso[0]]+"Archer"+{"Barbarian" : " ","Archer" : "]","Assassin" : " ","Mage" : " "}[perso[0]]+"   |\n"+{"Barbarian" : " ","Archer" : " ","Assassin" : "[","Mage" : " "}[perso[0]]+"Assassin"+{"Barbarian" : " ","Archer" : " ","Assassin" : "]","Mage" : " "}[perso[0]]+" |\n"+{"Barbarian" : " ","Archer" : " ","Assassin" : " ","Mage" : "["}[perso[0]]+"Mage"+{"Barbarian" : " ","Archer" : " ","Assassin" : " ","Mage" : "]"}[perso[0]]+"     |\n"+"-"*10+"\nHP : "+str(l_persos[perso[0]][0])+"\nShield : "+str(l_persos[perso[0]][1])+"\nAttack points : "+str(l_persos[perso[0]][2])+"\nMovement points : "+str(l_persos[perso[0]][3])+"\nFirst attack : "+{"Barbarian" : "Sword (+) 1 2AP","Archer" : "Arrow shot (○) 2-3 2AP","Assassin" : "Dagger blow (+) 1 2AP","Mage" : "Fireball (○) 1-2 2AP"}[perso[0]]+"\nSecond Attack : "+{"Barbarian" : "Charge (+) 2-4 4AP","Archer" : "Mighty arrow (+) 3-4 4AP","Assassin" : "Throws a dagger (+) 1-2 3AP","Mage" : "Shock wave (□) 1 6AP"}[perso[0]]+"\nSpecial : "+{"Barbarian" : "Berserk, x2 damage for 2 turns","Archer" : "Dodge, move of two squares towards a direction","Assassin" : "Teleportation, teleport to a nearby square (range : 1-2)","Mage" : "Wall, create a wall which id destroyed after 3 turns"}[perso[0]]+"\n"*6+"-"*66+"\nSelect (enter) | Help (h)"
    elif ecran == 3 : texte["text"] = " "*28+"HELP (1/4)\n"+"-"*66+"\n█ -> wall\n# -> door\n@ -> player\n♥ -> heart\n◙ -> coin\ny -> key\nσ -> bomb\n¤ -> trap\n§ -> fire\n# -> spider web\n& -> item\n* -> end of level\nAttack style :\n   + -> crossed\n   ○ -> in circle around the character\n   □ -> touch the eight squares around the character\nAttack description : name/style/range/cost\n"+"-"*66+"\nNext page (d) | Main screen (h)"
    elif ecran == 4 : texte["text"] = " "*28+"HELP (2/4)\n"+"-"*66+"\nControls :\n\nMouve up -> z/Up\nMouve down -> s/Down\nMouve left -> q/Left\nMouve right -> d/Rigth\nSelect first attack -> 1\nSelect second attack -> 2\nSelect special -> 3\nVision mode on/off -> a\nFinish the turn -> Return\nPause -> Escape\n\nClick on the squares to use attacks or open doors with keys"+"\n"*4+"-"*66+"\nPrevious page (q) | Next page (d) | Main screen (h)"
    elif ecran == 5 : texte["text"] = " "*28+"HELP (3/4)\n"+"-"*66+"\nRooms types :\n\nHome (H) -> The room you appear in\nFight (F) -> The rooms in which there are monsters to kill\nItem room (I) -> The room in which you get a free item (only the\nfirst level is unlocked)\nShop (S) -> The room where you can buy items (it is locked every\ntime)\nDevil deal (D) -> It's similar to the shop except you pay with\nlife points and only two items are proposed\nSecret room (T) -> There is one in all levels but it is hidden, to\nfind it you have to put a bomb on the right wall to detonate it\nBoss room -> To go to the next level you have to beat the boss in\nthis room"+"\n"*4+"-"*66+"\nPrevious page (q) | Next page (d) | Main screen (h)"
    elif ecran == 6 : texte["text"] = " "*28+"HELP (4/4)\n"+"-"*66+"\nEnnemis types :\n\nSlime (O) : 10HP/2MP\n   Attack -> Hit with 1 of range (2 damages)\nSkeleton (X) : 10HP/2MP\n   Attack -> Shoot an arrow with 2-3 of range (2 damages)\nSpider (W) : 10HP/1MP\n   First attack -> Spiderweb with 1-2 of range (remove all MP)\n   Second attack -> Poison with 1 of range (1 damage for 2 turns)\nHorned demon (T) : 15HP/2MP\n   First attack -> Horn blow with 1 of range (2 damages)\n   Second attack -> Charge with 2-4 of range (1 damages)\nWizard (M) : 6HP/1MP\n   First attack -> Fireball with 1-2 of range (2 damage)\n   Second attack -> Heal with 1-10 of range\nGhost (U) : Contact with this enemy will kill you\n\n"+"-"*66+"\nPrevious page (q) | Main screen (h)"
    elif ecran in [8,9,10] :
        t = [[map[i][j] if -1 < i < len(map) and -1 < j < len(map[0]) and (0 <= i-i//20*20 < 16 and 0 <= j-j//20*20 < 16 and explore[i//20][j//20] == 1 or i-i//20*20 >= 16 and 0 <= j-j//20*20 < 16 and (explore[i//20][j//20] == 1 or i//20 < len(explore)-1 and explore[i//20+1][j//20] == 1) or 0 <= i-i//20*20 < 16 and j-j//20*20 >= 16 and (explore[i//20][j//20] == 1 or j//20 < len(explore[0])-1 and explore[i//20][j//20+1] == 1)) else " " for j in range (perso[-1][0]-22,perso[-1][0]+24,1)] for i in range (perso[-1][1]-7,perso[-1][1]+9,1)]
        t = [["HP : "+str(perso[1][1])+"/"+str(perso[1][0])+" | Armor : "+str(perso[2][1])+"/"+str(perso[2][0])+" | Coins : "+str(perso[7])+" | Keys : "+str(perso[8])+" | Bombs : "+str(perso[9])],["-"*66]]+t+[["-"*66],["AP : "+str(perso[3][1])+" | MP : "+str(perso[4][1])+" | Special : "+str(perso[5][1])+" turns left"],[["[","",""][perso[10]]+"(1) "+{"Barbarian" : "(+) 1 2AP ","Archer" : "(○) 2-3 2AP ","Assassin" : "(+) 1 2AP ","Mage" : "(○) 1-2 2AP "}[perso[0]]+str(perso[6][0])+"-"+str(perso[6][1])+["]","",""][perso[10]]+" | "+["","[",""][perso[10]]+"(2) "+{"Barbarian" : "(+) 2-4 4AP ","Archer" : "(+) 3-4 4AP ","Assassin" : "(+) 1-2 3AP ","Mage" : "(□) 1 6AP "}[perso[0]]+str(perso[6][2])+"-"+str(perso[6][3])+["","]",""][perso[10]]+" | "+["","","["][perso[10]]+"(3) "+{"Barbarian" : "Berserk","Archer" : "Dodge","Assassin" : "Teleportation","Mage" : "Wall"}[perso[0]]+["","","]"][perso[10]]]]
        t[9][22] = "@"
        for i in l_objets :
            if perso[-1][0]-22 <= i[0] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[1] <= perso[-1][1]+8 and explore[i[1]//20][i[0]//20] == 1 : t[i[1]-(perso[-1][1]-9)][i[0]-(perso[-1][0]-22)] = i[2]
        for i in l_ennemis :
            if i[0] in "OXWTM" and perso[-1][0]-22 <= i[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2] <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)][i[1]-(perso[-1][0]-22)] = i[0]
            elif i[0] == "dk" and perso[-1][0]-22 <= i[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2] <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)][i[1]-(perso[-1][0]-22)] = "K"
            elif i[0] == "nw" and perso[-1][0]-22 <= i[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2] <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)][i[1]-(perso[-1][0]-22)] = "S"
            elif i[0] == "pd" and perso[-1][0]-22 <= i[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2] <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)][i[1]-(perso[-1][0]-22)] = "Y"
            elif i[0] == "sq" :
                for j in range (4) :
                    for k in range (4) :
                        if perso[-1][0]-22 <= i[1]+k <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2]+j <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)+j][i[1]-(perso[-1][0]-22)+k] = [[["\\","-","-","/"],["-","o","o","-"],["-"," "," ","-"],["/","-","-","\\"]],[["\\","|","|","/"],["|"," ","o","|"],["|"," ","o","|"],["/","|","|","\\"]],[["\\","-","-","/"],["-"," "," ","-"],["-","o","o","-"],["/","-","-","\\"]],[["\\","|","|","/"],["|","o"," ","|"],["|","o"," ","|"],["/","|","|","\\"]]][i[4]-1][j][k]
            elif i[0] == "gs" :
                if perso[-1][0]-22 <= i[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[2] <= perso[-1][1]+8 : t[i[2]-(perso[-1][1]-9)][i[1]-(perso[-1][0]-22)] = "^>v<"[i[4]-1]
                for j in i[5] :
                    if perso[-1][0]-22 <= j[0] <= perso[-1][0]+23 and perso[-1][1]-7 <= j[1] <= perso[-1][1]+8 : t[j[1]-(perso[-1][1]-9)][j[0]-(perso[-1][0]-22)] = "O"
        for i in l_fantomes :
            if perso[-1][0]-22 <= i[0] <= perso[-1][0]+23 and perso[-1][1]-7 <= i[1] <= perso[-1][1]+8 and explore[i[1]//20][i[0]//20] == 1 : t[i[1]-(perso[-1][1]-9)][i[0]-(perso[-1][0]-22)] = "U"
        for i in range (2,len(t)-3,1) :
            t[i] += ["|"]
            if i == 2 :
                if info != "" : t[i] += " "+info
                else : t[i] += " "+info2
            elif i in [3,12] : t[i] += ["-------------------"]
            elif 4 <= i <= 11 and i-4 < len(l_effets) : t[i] += [" "+l_effets[i-4][0]+" ("+str(l_effets[i-4][1])+" turns)"] if len(l_effets[i-4]) > 1 else [" "+l_effets[i-4][0]]
            elif i in [13,15,17] :
                if 0 <= perso[-1][1]//20-1+(i-13)//2 < len(donjon) :
                    for j in range (-5,5,1) :
                        if j != -5 :
                            if 0 <= perso[-1][0]//20+j < len(donjon[0]) and (explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] == 1 or "" != donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] != "secretroom" and (0 <= perso[-1][1]//20-2+(i-13)//2 < len(donjon) and explore[perso[-1][1]//20-2+(i-13)//2][perso[-1][0]//20+j] == 1 or 0 <= perso[-1][1]//20+(i-13)//2 < len(donjon) and explore[perso[-1][1]//20+(i-13)//2][perso[-1][0]//20+j] == 1 or 0 <= perso[-1][0]//20+j-1 < len(donjon[0]) and explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j-1] == 1 or 0 <= perso[-1][0]//20+j+1 < len(donjon[0]) and explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j+1] == 1)) : t[i] += "F" if "fight" in donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] else {"depart" : "H","itemroom" : "I","shop" : "S","devildeal" : "D","boss" : "B","secretroom" : "T"}[donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j]]
                            else : t[i] += [" "]
                        if 0 <= perso[-1][0]//20+j < len(donjon[0])-1 and (donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] != "secretroom" != donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j+1] and donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] != "" != donjon[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j+1] and (explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] == 1 or explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j+1] == 1) or explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j] == 1 and explore[perso[-1][1]//20-1+(i-13)//2][perso[-1][0]//20+j+1] == 1) : t[i] += ["-"]
                        else : t[i] += [" "]
            elif i in [14,16] : t[i] += [" "]+["| " if 0 <= perso[-1][0]//20+j < len(donjon[0]) and 0 <= perso[-1][1]//20+(i-15) < len(donjon) and donjon[perso[-1][1]//20][perso[-1][0]//20+j] != "" != donjon[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] and ((donjon[perso[-1][1]//20][perso[-1][0]//20+j] == "secretroom" and explore[perso[-1][1]//20][perso[-1][0]//20+j] == 1 or explore[perso[-1][1]//20][perso[-1][0]//20+j] == 1 and not (donjon[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] == "secretroom" and explore[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] == 0)) or (donjon[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] == "secretroom" and explore[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] == 1 or explore[perso[-1][1]//20+(i-15)][perso[-1][0]//20+j] == 1 and not (donjon[perso[-1][1]//20][perso[-1][0]//20+j] == "secretroom" and explore[perso[-1][1]//20][perso[-1][0]//20+j] == 0))) else "  " for j in range (-4,5,1)]
        if len(bombe) > 0 and bombe[2] == 1 and perso[-1][0]-22 <= bombe[0] <= perso[-1][0]+23 and perso[-1][1]-7 <= bombe[1] <= perso[-1][1]+8 : t[bombe[1]-(perso[-1][1]-9)][bombe[0]-(perso[-1][0]-22)] = "σ"
        if ecran == 9 :
            a = {"Barbarian" : [["+",1,1],["+",2,4],["□"]],"Archer" : [["○",2,3],["+",3,4],["+",2,2]],"Assassin" : [["+",1,1],["+",1,2],["○",2,2]],"Mage" : [["○",1,2],["□",2,4],["+",1,1]]}[perso[0]][perso[10]]
            if a[0] == "+" :
                for i in range (a[1],a[2]+1,1) :
                    if test_obstacle(perso[-1],[perso[-1][0]-i,perso[-1][1]])[0] == 0 : t[9][22-i] = "░"
                    if test_obstacle(perso[-1],[perso[-1][0],perso[-1][1]-i])[0] == 0 : t[9-i][22] = "░"
                    if test_obstacle(perso[-1],[perso[-1][0]+i,perso[-1][1]])[0] == 0 : t[9][22+i] = "░"
                    if test_obstacle(perso[-1],[perso[-1][0],perso[-1][1]+i])[0] == 0 : t[9+i][22] = "░"
            elif a[0] == "○" :
                for i in range (-3,4,1) :
                    for j in range (-2+abs(i),3-abs(i),1) :
                        if not i == j == 0 and test_obstacle(perso[-1],[perso[-1][0]+j,perso[-1][1]+i])[0] == 0 : t[9+i][22+j] = "░"
            elif a[0] == "□" : t[9][22] = "░"
        elif ecran == 10 : t[8][21-int(len(info3[1])/2):23+int((len(info3[1])+1)/2)],t[9][21-int(len(info3[1])/2):23+int((len(info3[1])+1)/2)],t[10][21-int(len(info3[1])/2):23+int((len(info3[1])+1)/2)],t[11][21-int(len(info3[1])/2):23+int((len(info3[1])+1)/2)] = " "+"-"*(len(info3[1]))+" ","|"+" "*int((len(info3[1])-len(info3[0]))/2)+info3[0]+" "*int((len(info3[1])-len(info3[0])+1)/2)+"|","|"+info3[1]+"|"," "+"-"*(len(info3[1]))+" "
        texte["text"] = "\n".join(["".join(i) for i in t])
    elif ecran == 11 : texte["text"] = " "*30+"Pause :\n"+"-"*66+"\n"*8+" "*int((60-len(str(perso[11]+1)))/2)+"Floor "+str(perso[11]+1)+"\n"+" "*29+{0 : "[",1 : " ",2 : " "}[c]+"Resume"+{0 : "]",1 : " ",2 : " "}[c]+"\n"+" "*30+{0 : " ",1 : "[",2 : " "}[c]+"Quit"+{0 : " ",1 : "]",2 : " "}[c]+"\n"+" "*int((66-(26+len(str(delai))))/2-1)+{0 : "  ",1 : "  ",2 : "<["}[c]+"Delay of enemy actions : "+str(delai)+"s"+{0 : "  ",1 : "  ",2 : "]>"}[c]+"\n"*8
    elif ecran == 12 : mort()
    texte.update()

fenetre = Tk()
fenetre.title("Dungeon Quest")
fenetre.configure(bg="#000000")
fenetre.geometry("600x400")
fenetre.resizable(width=False,height=False)
fenetre.bind("<Key>",key_down)

# 66x20
texte,ecran,perso = Label(fenetre,text="",font="Consolas 12",fg="#ffffff",bg="#000000",justify="left",cursor="tcross"),1,["Barbarian"]
texte.pack(side=TOP,anchor="w",padx=0,pady=0)
texte.bind("<Motion>",mouse_motion)
texte.bind("<Button-1>",mouse_button_down)

# nom, pv, armure, pa, pm, temps recharge special, degats - attq 1, degats + attq 1, degats - attq 2, degats + attq 2
# pièces, clés, bombes
delai = 1.0

l_persos = {"Barbarian" : [5,8,8,2,4,2,3,1,2],
"Archer" : [3,5,6,2,3,2,3,3,4],
"Assassin" : [4,3,6,3,4,3,4,2,3],
"Mage" : [4,6,8,1,2,2,3,2,2]}

# nom, pv, pm, dégats 1, dégats 2, dégats 3
l_mobs = {"O" : ["Slime",10,2,2],
"X" : ["Skeleton",10,2,2],
"W" : ["Spider",10,1,1],
"T" : ["Demon",15,2,2,1],
"M" : ["Wizard",6,1,2,2],
"dk" : ["Dark Knight",50,2,2,2,2],
"nw" : ["Night Witch",50,3,2,3,2],
"sq" : ["Spider Queen",50,1,1],
"gs" : ["Giant Snake",50],
"pd" : ["Primordial Demon",50,2,3,2]}

objets = ["Health","Protection","Strong inside","Strong outside","Vampirism","Strenght","Skillful","Powerful","Boots","Strong but slow","Fast but weak"]
cout_objets = {"♥" : 3,"y" : 3,"σ" : 3,"&" : 10,"Health" : 1,"Protection" : 1,"Strong inside" : 1,"Strong outside" : 1,"Vampirism" : 2,"Strenght" : 1,"Powerful" : 1,"Boots" : 1,"Fast but weak" : 1,"Strong but slow" : 1}

affich()

fenetre.mainloop()


"""
écrans :
    - 1 : Title screen
    - 2 : Main screen
    - 3 : Help 1 (signification symboles)
    - 4 : Help 2 (controles)
    - 5 : Help 3 (types de salles)
    - 6 : Help 4 (types d'ennemis)
    - 7 : Loading dungeon
    - 8 : Dungeon
    - 9 : Vision
    - 10 : Effet item
    - 11 : Pause
    - 12 : Game Over

----------
A AJOUTER :
ENLEVER COMMANDE RESET DONJON
changer appellation ecran pour pouvoir mieux ajouter d'autres ecrans
boss :
    - dk/
    - nw/
    - sq/
    - gs/
    - pd/
item -1 degats min +1 degats max
item +1 degats min -1 degats max
item bottes anti-feu ~
----------
░ (176)
▒ (177)
▓ (178)
----------

Caractères :
mur -> █ (219)
porte -> ▓
joueur -> @
coeur -> ♥ (3)
argent -> ◙ (10)
clé -> y
bombe -> σ
piège -> ¤ (207)
toile d'araignée -> #
objet -> &

Pièces :
base
monstres
magasins
item room
devil deal
boss
secret room
enigme ~

Persos :
barbare (épée) 5PV 8B 8PA 2PM -> coup d'épée (+) 1 (2PA) / charge (+) 2-4 (4PA) // tape 2x plus fort pour les 3 prochains coups donnés (non cumulable) (4 coups)
rodeur (arc) 3PV 5B 6PA 2PM -> tire flèche (○) 2-3 (2PA) / flèche puissante (+) 3-4 (4PA) // roulade (2 case dans une direction) (3 coups)
assassin (dague) 4PV 3B 6PA 3PM -> coup de dague (+) 1 (2PA) / lance dague (+) 1-2 (3PA) // se tp (○) 2 (4 coups)
mage (baton de magicien) 4PV 6B 8PA 1PM -> boule de feu (○) 1-2 (2PA) / onde de choc (□) 1 (6PA) (repousse les ennemis d'une case) // créer un mur qui se détruit après 3 tours (2 coups)

Curseur :
cases où on peut tirer -> target
cases où on peut pas tirer -> tcross

███████--███████
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
----------------
----------------
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
███████--███████

fight rooms :

███████--███████
█¤¤¤¤¤¤--¤¤¤¤¤¤█
█¤------------¤█
█¤-----¤¤-----¤█
█¤------------¤█
█¤------------¤█
█¤------------¤█
---¤---¤¤---¤---
---¤---¤¤---¤---
█¤------------¤█
█¤------------¤█
█¤------------¤█
█¤-----¤¤-----¤█
█¤------------¤█
█¤¤¤¤¤¤--¤¤¤¤¤¤█
███████--███████

███████--███████
█--------------█
█-█-█-█--█-█-█-█
█--------------█
█-█-█-█--█-█-█-█
█--------------█
█-█-█-█--█-█-█-█
----------------
----------------
█-█-█-█--█-█-█-█
█--------------█
█-█-█-█--█-█-█-█
█--------------█
█-█-█-█--█-█-█-█
█--------------█
███████--███████

███████--███████
█--------------█
█-████----████-█
█-█----------█-█
█-█----------█-█
█-█----------█-█
█--------------█
-------██-------
-------██-------
█--------------█
█-█----------█-█
█-█----------█-█
█-█----------█-█
█-████----████-█
█--------------█
███████--███████

███████--███████
█¤¤----------¤¤█
█¤------------¤█
█-----█--█-----█
█-----█--█-----█
█----¤█--█¤----█
█--████--████--█
----------------
----------------
█--████--████--█
█----¤█--█¤----█
█-----█--█-----█
█-----█--█-----█
█¤------------¤█
█¤¤----------¤¤█
███████--███████

███████--███████
█--------------█
█--------------█
█-----█--█-----█
█----█----█----█
█---█------█---█
█--█--------█--█
-------¤¤-------
-------¤¤-------
█--█--------█--█
█---█------█---█
█----█----█----█
█-----█--█-----█
█--------------█
█--------------█
███████--███████

secret rooms :

███████--███████
█--------------█
█-██-██████-██-█
█------██------█
█-██--------██-█
█----██--██----█
█-██-█----█-██-█
--██-██████-██--
----------------
█-██-██--██-██-█
█--█--------█--█
██-█---██---█-██
█----█----█----█
█-█████--█████-█
█--------------█
███████--███████

███████--███████
█♥█----------█♥█
███----------███
█--------------█
█--------------█
█--------------█
█--------------█
----------------
----------------
█--------------█
█--------------█
█--------------█
█--------------█
███----------███
█♥█----------█♥█
███████--███████

███████--███████
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
█------♥-------█
-------◙◙σ------
------y◙◙-------
█-------♥------█
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
███████--███████

███████--███████
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
-------&--------
----------------
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
█--------------█
███████--███████
----------
script pour générer les listes des salles :

a = ""
b = [[j for j in a[i*16:(i+1)*16]][1:-1] for i in range (1,15)]
print("[",end="")
for i in range (len(b)) :
    print("[",end="")
    for j in range (len(b[i])) :
        if j < len(b[i])-1 : print('"'+b[i][j]+'",',end="")
        else : print('"'+b[i][j]+'"',end="")
    if i < len(b)-1 : print("],",end="")
    else : print("]",end="")
print("]")
----------
script affichage à chaque action au cas où :

t = [[map[k][l] if -1 < k < len(map) and -1 < l < len(map[0]) and (0 <= k-k//20*20 < 16 and 0 <= l-l//20*20 < 16 and explore[k//20][l//20] == 1 or k-k//20*20 >= 16 and 0 <= l-l//20*20 < 16 and (explore[k//20][l//20] == 1 or k//20 < len(explore)-1 and explore[k//20+1][l//20] == 1) or 0 <= k-k//20*20 < 16 and l-l//20*20 >= 16 and (explore[k//20][l//20] == 1 or l//20 < len(explore[0])-1 and explore[k//20][l//20+1] == 1)) else " " for l in range (perso[-1][0]-22,perso[-1][0]+24,1)] for k in range (perso[-1][1]-7,perso[-1][1]+9,1)]
t = [["HP : "+str(perso[1][1])+"/"+str(perso[1][0])+" | Armor : "+str(perso[2][1])+"/"+str(perso[2][0])+" | Coins : "+str(perso[7])+" | Keys : "+str(perso[8])+" | Bombs : "+str(perso[9])],["-"*66]]+t+[["-"*66],["AP : "+str(perso[3][1])+" | MP : "+str(perso[4][1])+" | Special : "+str(perso[5][1])+" turns left"],[["[","",""][perso[10]]+"(1) "+{"Barbare" : "(+) 1 2AP ","Rodeur" : "(○) 2-3 2AP ","Assassin" : "(+) 1 2AP ","Mage" : "(○) 1-2 2AP "}[perso[0]]+str(perso[6][4])+"-"+str(perso[6][5])+["]","",""][perso[10]]+" | "+["","[",""][perso[10]]+"(2) "+{"Barbare" : "(+) 2-4 4AP ","Rodeur" : "(+) 3-4 4AP ","Assassin" : "(+) 1-2 3AP ","Mage" : "(□) 1 6AP "}[perso[0]]+str(perso[6][6])+"-"+str(perso[6][7])+["","]",""][perso[10]]+" | "+["","","["][perso[10]]+"(3) "+{"Barbare" : "Berserk","Rodeur" : "Dodge","Assassin" : "Teleportation","Mage" : "Wall"}[perso[0]]+["","","]"][perso[10]]]]
t[9][22] = "@"
for k in l_ennemis :
    if perso[-1][0]-22 <= k[1] <= perso[-1][0]+23 and perso[-1][1]-7 <= k[2] <= perso[-1][1]+8 : t[k[2]-(perso[-1][1]-9)][k[1]-(perso[-1][0]-22)] = k[0]
for k in range (2,len(t)-3,1) :
    t[k] += ["|"]
    if k == 2 : t[k] += " "+info
    elif k in [3,12] : t[k] += ["-------------------"]
    elif 4 <= k <= 11 and k-4 < len(l_effets) : t[k] += [" "+l_effets[k-4][0]+" ("+str(l_effets[k-4][1])+" turns)"]
    elif k in [13,15,17] :
        if 0 <= perso[-1][1]//20-1+(k-13)//2 < len(donjon) :
            for l in range (-5,5,1) :
                if l != -5 :
                    if 0 <= perso[-1][0]//20+l < len(donjon[0]) and (explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] == 1 or "" != donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] != "secretroom" and (0 <= perso[-1][1]//20-2+(k-13)//2 < len(donjon) and explore[perso[-1][1]//20-2+(k-13)//2][perso[-1][0]//20+l] == 1 or 0 <= perso[-1][1]//20+(k-13)//2 < len(donjon) and explore[perso[-1][1]//20+(k-13)//2][perso[-1][0]//20+l] == 1 or 0 <= perso[-1][0]//20+l-1 < len(donjon[0]) and explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l-1] == 1 or 0 <= perso[-1][0]//20+l+1 < len(donjon[0]) and explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l+1] == 1)) : t[k] += "F" if "fight" in donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] else {"depart" : "H","itemroom" : "I","shop" : "S","devildeal" : "D","boss" : "B","secretroom" : "T"}[donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l]]
                    else : t[k] += [" "]
                if 0 <= perso[-1][0]//20+l < len(donjon[0])-1 and (donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] != "secretroom" != donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l+1] and donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] != "" != donjon[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l+1] and (explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] == 1 or explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l+1] == 1) or explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l] == 1 and explore[perso[-1][1]//20-1+(k-13)//2][perso[-1][0]//20+l+1] == 1) : t[k] += ["-"]
                else : t[k] += [" "]
    elif k in [14,16] : t[k] += [" "]+["| " if 0 <= perso[-1][0]//20+l < len(donjon[0]) and 0 <= perso[-1][1]//20+(k-15) < len(donjon) and donjon[perso[-1][1]//20][perso[-1][0]//20+l] != "" != donjon[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] and ((donjon[perso[-1][1]//20][perso[-1][0]//20+l] == "secretroom" and explore[perso[-1][1]//20][perso[-1][0]//20+l] == 1 or explore[perso[-1][1]//20][perso[-1][0]//20+l] == 1 and not (donjon[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] == "secretroom" and explore[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] == 0)) or (donjon[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] == "secretroom" and explore[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] == 1 or explore[perso[-1][1]//20+(k-15)][perso[-1][0]//20+l] == 1 and not (donjon[perso[-1][1]//20][perso[-1][0]//20+l] == "secretroom" and explore[perso[-1][1]//20][perso[-1][0]//20+l] == 0))) else "  " for l in range (-4,5,1)]
t = ["".join(k) for k in t]
texte["text"] = "\n".join(t)
texte.update()
----------
map[perso[-1][1]//20*20+7][perso[-1][0]//20*20+7] = "*"
----------

ennemis :
O -> slime (tape 1 de range / 2PM / HP)
X -> squelette (tire flèche 2-3 de range / 2PM / HP)
W -> araignée (toile 1-2 de range / poison 1 de range / 1PM / HP)
T -> demon à cornes (coup de corne 1 de range / charge 2-4 de range / 2PM / HP)
M -> sorcier (boule de feu 1-2 de range / soin 1-10 de range / 1PM / HP)

dk -> Dark Knight (tape 1 de range / charge 2-5 de range / +2HP si commence son tour au corps-à-corps / 2PM)
nw -> Nigth Witch (boule de feu 2-4 de range (fait du feu par terre) / TP 10 cases plus loin / repousse en faisant des dégats si commence son tour au corps-à-corps / 3PM)
sq -> Spider Queen (poison 1 de range (dure 3 tours) / invocation de 2 araignées / toiles d'araignées là où elle marche / 1PM)
gs -> Giant Snake (mécanique de snake / 1PM)
pd -> Primordial Demon (gerbe de flammes 1-4 de range (met du feu par terre) / explosion 3-5 de range (5 de diamètre et met du feu par terre) / feu là où il marche / 2PM)

objets :
strong inside : +1 pv max -1 armure max
strong outside : -1 pv max +1 armure max
strenght : +1 dégats
skillful : -1 couldown special
vampirism
boots : +1 PM
powerful : +1 PA
fast but weak : -1 PA +1 PM
strong but slow : -1 PM +1 PA
"""