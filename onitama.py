import sys
import math
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
import copy
import time
posicionesCentro = 469440
posicionCentral = 4096
posicionesBordes = 28886587
p1 = 11043370
p2 = 4539716 
p3 =141440
p4 = 4096
ponderacionPC = 2
ponderacionPCC = 3
tuplaZero = (0, 0)
limitInf = 1  ##0b1
limitSup = 16777216  ##0b2 a la 24
maskTempleMasters = [4194304, 4]  ##templo del jugador 0 estará en el bit 2 a la 22, y el templo
                                  ##del otro jugador en el bit 2 a la 2
baseMaster = [462, 15138816]
dictMaskPos = {
1: (0, 0), 2: (0, 1), 4 :(0, 2), 8:(0, 3), 16:(0, 4),
32 :(1, 0), 64 :(1, 1), 128 :(1, 2), 256 :(1, 3), 512 :(1, 4),
1024 :(2, 0), 2048 :(2, 1), 4096 :(2, 2), 8192:(2, 3), 16384:(2, 4),
32768:(3, 0), 65536:(3, 1), 131072:(3, 2), 262144:(3, 3), 524288:(3, 4),
1048576:(4, 0), 2097152:(4, 1), 4194304:(4, 2), 8388608:(4, 3), 16777216:(4, 4)
}
movimientoFinal = {
1: "A5", 2: "B5", 4 : "C5", 8:"D5", 16:"E5",
32 : "A4", 64 :"B4", 128 :"C4", 256 :"D4", 512 :"E4",
1024 :"A3", 2048 :"B3", 4096 :"C3", 8192:"D3", 16384:"E3",
32768:"A2", 65536:"B2", 131072:"C2", 262144:"D2", 524288:"E2",
1048576:"A1", 2097152:"B1", 4194304:"C1", 8388608:"D1", 16777216:"E1"
}
def parseListToDictCartas(listasLineas):
    dictionarioCartas = [{}, {}, {} ]
    for linea in listasLineas:
        cartaNueva = carta(linea[1], [(linea[2],linea[3]),(linea[4], linea[5]),(linea[6],linea[7]),(linea[8],linea[9])])
        if(linea[0] == -1):
            dictionarioCartas[2][linea[1]] = cartaNueva
        else:
            dictionarioCartas[linea[0]][linea[1]] = cartaNueva
    return dictionarioCartas
def intercambiarCarta(dictCartas,idCarta):
    nuevasCartas = copy.deepcopy(dictCartas)
    carta = None
    diccionarioNeutro = nuevasCartas[2]
    cartaIdNeutra = list(diccionarioNeutro.keys())[0]
    cartaNeutraDel = diccionarioNeutro[cartaIdNeutra]
    if(nuevasCartas[1].get(idCarta) != None):
        carta = nuevasCartas[1][idCarta]
        nuevasCartas[1].pop(idCarta)
        nuevasCartas[2][idCarta] = carta
        nuevasCartas[2].pop(cartaIdNeutra)
        nuevasCartas[1][cartaIdNeutra] = cartaNeutraDel
    if(nuevasCartas[0].get(idCarta) != None):
        carta = nuevasCartas[0][idCarta]
        nuevasCartas[0].pop(idCarta)
        nuevasCartas[2][idCarta] = carta
        nuevasCartas[2].pop(cartaIdNeutra)
        nuevasCartas[0][cartaIdNeutra] = cartaNeutraDel 
    return nuevasCartas
def bitboard_to_board(bitboard, mask_W, masks_w, mask_B, masks_b):
    board = [['.' for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            bit = i*5+j
            if bitboard & (1 << bit):
                if mask_W & (1 << bit):
                    board[i][j] = 'W'
                if masks_w & (1 << bit):
                    board[i][j] = 'w'
                if mask_B & (1 << bit):
                    board[i][j] = 'B'
                if masks_b & (1 << bit):
                    board[i][j] = 'b'
    return board
def board_to_bitboard(board):
    bitboard = 0
    mask_W = 0
    mask_B = 0
    masks_w = 0
    masks_b = 0
    for i in range(5):
        for j in range(5):
            bit = i*5+j
            if board[i][j] == 'b':
                bitboard |= 1 << bit
                masks_b |= 1 << bit
            if board[i][j] == 'B':
                bitboard |= 1 << bit
                mask_B = 1 << bit
            if board[i][j] == 'w':
                bitboard |= 1 << bit
                masks_w |= 1 << bit
            if board[i][j] == 'W':
                bitboard |= 1 << bit
                mask_W = 1 << bit
    return bitboard, mask_W, masks_w, mask_B, masks_b
class carta:
    def __init__(self, cartaId, movimientos):
        self.cartaId = cartaId
        self.movimientos = [movimiento for movimiento in movimientos if movimiento != tuplaZero]
    def setMovimientos(self, nuevosMov):
        self.movimientos = [movimiento for movimiento in nuevosMov if movimiento != tuplaZero]
    def getMovimientos(self):   
        return self.movimientos 
    def getIdCarta(self):
        return self.cartaId
class Movimiento:
    def __init__(self, dx, dy, idCartaUtilizada, movimientoAnt):
        self.dx = dx
        self.dy = dy
        self.idCartaUtilizada = idCartaUtilizada
        self.movimientoAnt = movimientoAnt
        self.movimientoDest = 0
    def getMascaraDestinoBit(self, idPlayer):
        # if(idPlayer):
        #     self.dx , self.dy = -self.dx, -self.dy
        x, y = dictMaskPos[self.movimientoAnt]
        nx = x-self.dy
        ny = y+self.dx
        if(0<= nx <= 4 and 0<= ny <= 4):
            self.movimientoDest = 1<<nx*5+ny
            return self.movimientoDest, limitInf <= self.movimientoDest <= limitSup
        return self.movimientoDest, False
    def getIdCarta(self):
        return self.idCartaUtilizada
    def getMovimientoDest(self):
        return self.movimientoDest
    def getMovimientoAnt(self):
        return self.movimientoAnt
class Nodo:
    def __init__(self, board, student0, master0, student1, master1):
        self.board = board
        self.student1 = student1
        self.master1 = master1
        self.student0 = student0
        self.master0 = master0
    def getBitBoard(self):
        return self.board
    def getStudentID(self, idPlayer):
        return self.student1 if idPlayer else self.student0
    def getMaster(self, idPlayer):
        return self.master1 if idPlayer else self.master0
    def setBitBoard(self, bitBoardNew):
        self.board = bitBoardNew
    def setStudentId(self, idPlayer, mascaraNueva):
        if idPlayer: self.student1 = mascaraNueva
        else: self.student0 = mascaraNueva
    def setMasterId(self, idPlayer, mascaraNueva):
        if idPlayer: self.master1 = mascaraNueva
        else: self.master0 = mascaraNueva

def esFinal(nodo, idPlayer):
    return  ((nodo.getMaster(int (not idPlayer)) == 0) or (nodo.getMaster(idPlayer) ==  maskTempleMasters[int(not idPlayer)]))

def make_move(board, p0_king, p0_pawns, p1_king, p1_pawns, from_mask, to_mask, player):
    # colocar la pieza en la posición final
    if player == 1:
        if from_mask & p1_pawns: p1_pawns |= to_mask
        else: p1_king = to_mask
    else:
        if from_mask & p0_pawns: p0_pawns |= to_mask
        else: p0_king = to_mask
    # eliminar la pieza de la posición inicial, no se elima al rey ya que esa mascara la hemos actualizado antes
    if((player == 1) and (from_mask & p1_pawns)): p1_pawns &= ~from_mask
    if((player == 0) and (from_mask & p0_pawns)): p0_pawns &= ~from_mask
    #actualizo la pieza contraria si es que se hace
    if player == 1:
        if to_mask == p0_king: p0_king = 0
        if to_mask & p0_pawns: p0_pawns &= ~to_mask
    else:
        if to_mask == p1_king: p1_king = 0
        if to_mask & p1_pawns: p1_pawns &= ~to_mask
    # actualizar el tablero
    board &= ~from_mask
    board |= to_mask
    return Nodo(board, p0_pawns, p0_king, p1_pawns, p1_king)

def get_piezas_board(master, students): ##encontrar fichas del player en un tablero dividiendolas una a una 
    def get_piezas_recursive(x1, y1, x2, y2, mask, piezas):   #4logn
        if x1 > x2 or y1 > y2 or len(piezas) == 4: return
        elif x1 == x2 and y1 == y2:
            if (mask & students): piezas.append(mask)
        else:
            xm = (x1+x2)//2
            ym = (y1+y2)//2
            mask1 = 1<<xm*5+ym
            mask2 = 1<<xm*5+y2
            mask3 = 1<<x2*5+ym
            mask4 = 1<<x2*5+y2
            get_piezas_recursive(x1, y1, xm, ym, mask1, piezas)
            get_piezas_recursive(x1, ym+1, xm, y2, mask2, piezas)
            get_piezas_recursive(xm+1, y1, x2, ym, mask3, piezas)
            get_piezas_recursive(xm+1, ym+1, x2, y2, mask4, piezas)
    piezas = []
    if(piezas != 0): get_piezas_recursive(0, 0, 4, 4, 0, piezas)
    if(master != 0): piezas.append(master)
    return piezas

def teComesAti(students, master, nuevoDest):
    return ((students & nuevoDest) | (master == nuevoDest))

def mascarasFilaCol(mask, x, y):
    fila_mask = 0b11111 << (5*x)
    col_mask = 0b1000010000100001000010000 >> 4-y
    diag_up = 0
    diag_down = 0
    # Generar la máscara de la diagonal superior
    if x >= 2 and y <= 2:
        diag_up |= 1 << ((x-2)*5 + y+2)
    if x >= 1 and y <= 3:
        diag_up |= 1 << ((x-1)*5 + y+1)
    if x <= 3 and y >= 1:
        diag_up |= 1 << ((x+1)*5 + y-1)
    if x <= 2 and y >= 2:
        diag_up |= 1 << ((x+2)*5 + y-2)
    
    # Generar la máscara de la diagonal inferior
    if x >= 2 and y >= 2:
        diag_down |= 1 << ((x-2)*5 + y-2)
    if x >= 1 and y >= 1:
        diag_down |= 1 << ((x-1)*5 + y-1)
    if x <= 3 and y <= 3:
        diag_down |= 1 << ((x+1)*5 + y+1)
    if x <= 2 and y <= 2:
        diag_down |= 1 << ((x+2)*5 + y+2)
    return fila_mask, col_mask, diag_up, diag_down
def evaluate(nodo, idPlayer): ## se evaluara con el nodo anterior es decir con el player anterior
                                  ## entonces el idPlayer será el de la anterior llamada
                                  ## el contrario de el que esta ahora
    # print(idPlayer)
    misStudents = nodo.getStudentID(idPlayer)
    susStudents = nodo.getStudentID(int (not idPlayer))
    miMaster = nodo.getMaster(idPlayer)
    suMaster = nodo.getMaster(int (not idPlayer))
    ##comerse al rey o llegar a la posicion destino
    #900
    #65 students->puesto 62
    if(0 == miMaster): return -700
    if(0 & misStudents): return -100
    if(suMaster == maskTempleMasters[idPlayer]): return -700
    if(0 == suMaster): return 700
    if(0 & susStudents): return 100
    if(miMaster == maskTempleMasters[int(not idPlayer)]): return 700
    
    pMe = 0
    pYou = 0
    ##posiciones maestro
    Mx, My = dictMaskPos[miMaster]
    Yx, Yy = dictMaskPos[suMaster]
    ##distancia de los maestros
    pFin = (abs(Mx - Yx) + abs(My - Yy))*-0.5
    ##mascaras fila, columna
    fila, columna, diag_up, diag_down = mascarasFilaCol(miMaster, Mx, My)
    filaY, columnaY, diag_upY, diag_downY = mascarasFilaCol(suMaster, Yx, Yy)
    pYou += (bin((fila & susStudents) | (fila & suMaster)).count('1'))*0.5
    pYou += (bin((columna & susStudents) | (columna & suMaster)).count('1'))*0.5
    pMe += (bin((filaY & misStudents) | (filaY & miMaster)).count('1'))*0.5
    pMe += (bin((columnaY & misStudents) | (columnaY & miMaster)).count('1'))*0.5
    ##añadido ahora hasta sin esto puesto 64
    pYou += (bin((diag_up & susStudents) | (diag_up & suMaster)).count('1'))*0.5
    pYou += (bin((diag_down & susStudents) | (diag_down & suMaster)).count('1'))*0.5
    pMe += (bin((diag_upY & misStudents) | (diag_upY & miMaster)).count('1'))*0.5
    pMe += (bin((diag_downY & misStudents) | (diag_downY & miMaster)).count('1'))*0.5
    ##mis puntuaciones
    #dom el centro
    pMe += bin(misStudents & posicionesCentro).count('1')*7
    pMe += bin(misStudents &  posicionCentral).count('1')*7
    ##dom de los bordes
    #1.3
    pMe += bin(misStudents & posicionesBordes).count('1')
    pMe += bin(miMaster & posicionesBordes).count('1')*0.5
    #fichas que nos quedan
    pMe += (bin(misStudents).count('1') + bin(miMaster).count('1'))*8
    ##sus puntuaciones
    #dom el centro
    pYou += bin(susStudents & posicionesCentro).count('1')*7
    pYou += bin(susStudents &  posicionCentral).count('1')*7
    ##dom de los bordes
    pYou += bin(susStudents & posicionesBordes).count('1')
    pYou += bin(suMaster & posicionesBordes).count('1')*0.5
    #fichas que le quedan
    pYou += (bin(susStudents).count('1') + bin(suMaster).count('1'))*8

    pYou += bin(suMaster & posicionesCentro).count('1')*0.5
    pYou += bin(suMaster &  posicionCentral).count('1')*0.5
    pMe += bin(miMaster & posicionesCentro).count('1')*0.5
    pMe += bin(miMaster &  posicionCentral).count('1')*0.5
    pFin  += pMe - pYou
    return pFin



def get_possible_moves(p0_king, p0_pawns, p1_king,  p1_pawns, cartas, idPlayer):
    misCartas = cartas[idPlayer]
    if(idPlayer):
        students = p1_pawns
        master = p1_king
    else:
        students = p0_pawns
        master = p0_king
    fichas = get_piezas_board(master, students)
    movimientosFichas = []
    for ficha in fichas:
        for carta in misCartas.values():
            for (dx, dy) in carta.getMovimientos():
                movimiento = Movimiento(dx, dy, carta.getIdCarta(), ficha)
                maskDest, entraEnRango = movimiento.getMascaraDestinoBit(idPlayer)
                if(entraEnRango and not teComesAti(students, master, maskDest)): 
                    movimientosFichas.append((ficha, maskDest, carta.getIdCarta()))
                    #, dx, dy
    return movimientosFichas



def alpha_beta_timeout(nodo, depth, cartas, alpha, beta, maximizing_player, idPlayer, time_limit, start_time):
    if depth == 0 or esFinal(nodo,int (not idPlayer)) or (time.time() - start_time) * 1000 >= time_limit:
        return evaluate(nodo,  int( not idPlayer))
    if maximizing_player:
        value = float('-inf')
        for move in sorted(get_possible_moves(nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), cartas, idPlayer), key=lambda x: -evaluate(make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), x[0], x[1], idPlayer), int(not idPlayer))):
            nuevo_nodo = make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), move[0], move[1], idPlayer)
            value = max(value, alpha_beta_timeout(nuevo_nodo, depth-1, intercambiarCarta(cartas, move[2]), alpha, beta, False, int(not idPlayer), time_limit, start_time))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
            if (time.time() - start_time) * 1000 >= time_limit:
                break
        return value
    else:
        value = float('inf')
        for move in sorted(get_possible_moves(nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), cartas, idPlayer), key=lambda x: +evaluate(make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), x[0], x[1], idPlayer), int(not idPlayer))):
            nuevo_nodo = make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), move[0], move[1], idPlayer)
            value = min(value, alpha_beta_timeout(nuevo_nodo, depth-1, intercambiarCarta(cartas, move[2]), alpha, beta, True, int(not idPlayer), time_limit, start_time))
            beta = min(beta, value)
            if alpha >= beta:
                break
            if (time.time() - start_time) * 1000 >= time_limit:
                break
        return value

def obtenerElMejorMovimiento(nodo, depth, idPlayer, cartas, time_Limit,start_time):
    best_move = (0, 0, 0)
    best_value = float('-inf')
    possible_moves = get_possible_moves(nodo.getMaster(0), nodo.getStudentID(0),nodo.getMaster(1), nodo.getStudentID(1), cartas, idPlayer)
    for move in sorted(possible_moves, key=lambda x: evaluate(make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0), nodo.getMaster(1), nodo.getStudentID(1), x[0], x[1], idPlayer), int(not idPlayer))):
        if (time.time() - start_time) * 1000 >= time_Limit:
            return best_move
        NuevoNodo = make_move(nodo.getBitBoard(), nodo.getMaster(0), nodo.getStudentID(0),nodo.getMaster(1), nodo.getStudentID(1),move[0], move[1], idPlayer)
        value = alpha_beta_timeout(NuevoNodo, depth-1, intercambiarCarta(cartas, move[2]),float('-inf'), float('inf'), False, int (not idPlayer), time_Limit, start_time)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move
player_id = int(input())
# game loop
while True:
    start = time.time()*1000
    boarD = []
    for i in range(5):
        board = input()
        boarD.append(board)
    # print(boarD)
    boardBit, mask_W, masks_w, mask_B, masks_b = board_to_bitboard(boarD)
    nodo = Nodo(boardBit, masks_w, mask_W, masks_b,mask_B)
    carDs = []
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        carDs.append([owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4])
    ##print(carDs)
    dictionarioCartasDelJuego = parseListToDictCartas(carDs)
    action_count = int(input())
    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]
    depth = 3
    movimiento = obtenerElMejorMovimiento(nodo,depth,player_id,dictionarioCartasDelJuego, 47.98766, time.time())
    print(str(movimiento[2])+" "+movimientoFinal[movimiento[0]]+movimientoFinal[movimiento[1]]+" tengo un  Bug")
    

