import pygame as pg 

width = 600
height = 600 
size = 75
thk = 3

win = pg.display.set_mode((width, height))
pg.display.set_caption("TIC TAC TOE")

def distance(c1,c2):
    return ((c1[0]-c2[0])**2 + (c1[1] - c2[1])**2)**0.5

def draw_x(cord):
    x = cord[0]
    y = cord[1]
    x_size = size*0.9
    pg.draw.line(win,(255,255,255),(x+x_size,y+x_size),(x-x_size,y-x_size),thk)
    pg.draw.line(win,(255,255,255),(x-x_size,y+x_size),(x+x_size,y-x_size),thk)

def draw_o(cord):
    pg.draw.circle(win,(255,255,255),cord,size,thk)

def draw_gb():
    for i in range(1,3):
       pg.draw.line(win,(255,255,255),(i*(width/3),0),(i*(width/3),height),thk+1) 
       pg.draw.line(win,(255,255,255),(0,i*(height/3)),(width,i*(height/3)),thk+1) 

def win_chk(gb_pos):
    for win_pos in win_pos_lst:
        for ply in (1,-1):
            if gb_pos[win_pos[0]]==ply and gb_pos[win_pos[1]]==ply and gb_pos[win_pos[2]]==ply:
                return (ply,win_pos)
    flg = True
    for i in range(9): 
        if gb_pos[i]==0: flg = False
    if flg: return 0
    return -1

def draw_pc(cord,ply):
    if ply==-1:
        draw_x(cord)
    elif ply==1:
        draw_o(cord)   

def comp(gb_pos,ply,x=0):
    if win_chk(gb_pos)==0: return 0
    if win_chk(gb_pos)!=-1: return ply*-1

    if ply==-1:
        for i in range(9):
            if gb_pos[i]==0:
                gb_pos[i]=ply
                if win_chk(gb_pos)!=-1:gb_pos[i]=0; return [i]
                gb_pos[i] = 0
        for i in range(9):
            if gb_pos[i]==0:
                gb_pos[i]=ply
                tmp = comp(gb_pos,ply*-1,x+1)
                gb_pos[i]=0
                if tmp!=1:
                    return [i]
        return 1
    else:
        for i in range(9):
            if gb_pos[i]==0:
                gb_pos[i]=ply 
                tmp = comp(gb_pos,ply*-1,x+1)
                gb_pos[i] = 0
                if tmp==1:
                    return 1
        return -1

run = True
ply = 1
pos = (0,0)
delay = 0
click = False
allow = True
gb_pos = [0]*9
cell_lst = [(100+200*j,100+200*i) for i in range(3) for j in range(3)]
win_pos_lst = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
while run:
    win.fill((0,0,0))
    #To check the events done in the window  
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        pos = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            click = True
        elif event.type == pg.MOUSEBUTTONUP:
            click = False


    min_dst = 100000
    cell_ind = 0
    for cord in cell_lst:
        if distance(pos,cord) < min_dst:
            min_dst = distance(pos,cord)
            cell_ind = cell_lst.index(cord)

    if gb_pos[cell_ind]==0:
        draw_pc(cell_lst[cell_ind],ply)

    if win_chk(gb_pos)!=-1:
        pg.time.delay(500)
        win.fill((0,0,0))
        draw_gb()
        win_ply = win_chk(gb_pos)[0]
        for cord in cell_lst:
            pg.time.delay(200)
            draw_pc(cord,win_ply)
            pg.display.update()
        quit()

    if click and allow and ply==1:
        allow = False
        if ply==1 and gb_pos[cell_ind]==0:
            gb_pos[cell_ind] = ply
            ply*=-1
        elif gb_pos[cell_ind]==0:
            gb_pos[cell_ind] = ply
            ply*=-1
    if ply==-1 and allow:
        mv = comp(gb_pos,ply)[0]
        gb_pos[mv] = ply
        ply*=-1
        pg.time.delay(200)


    for ind in range(9):
        draw_pc(cell_lst[ind],gb_pos[ind])
        
    
    # For delay B/W two clicks
    if not allow:
        delay+=1
        if delay == 60:
            allow = True
            delay = 0

    draw_gb()
    pg.display.update()