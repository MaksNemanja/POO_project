import math
import pygame
import numpy as np
import random
MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

class AI():
    move_counter = -1
    def __init__(self):
        self.kart = None
        self.n=2                           #pour la division de ma matrice(matrix) en matrice de poids (voir map de poids)
        self.etape=-1                       #pour savoir dans quelle direction marcher(voir move)
        self.relative_x,self.relative_y=0,0 #combien je suis loin de ma cible
        self.ai_id=0                        #check point id pour l'ia 
        
        
    def set_kart(self, Kart):               #instnce de kart dans ia  pour utililse les attributs de kart necessaire
        self.kart = Kart
        
    
    def devise_string(self,string):         #methode qui prend le string de ma map et l'importe dans la matrice(matrix)
        matrix = string.strip().split('\n')
        BLOCK_SIZE=50
        width=len(matrix[0])*BLOCK_SIZE
        height=len(matrix)*BLOCK_SIZE
        return matrix,width,height
        
            
    def premiere_occurrence(self,matrix,n):   #methode pour savoir la position de mes checkpoint sur la map 
        premier_C = None
        premier_D = None
        premier_E = None
        premier_F = None

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'C' and premier_C is None:
                    y=i//n
                    x=j//n
                    premier_C = [y, x]
                elif matrix[i][j] == 'D' and premier_D is None:
                    y=i//n
                    x=j//n
                    premier_D = [y, x]
                elif matrix[i][j] == 'E' and premier_E is None:
                    y=i//n
                    x=j//n
                    premier_E = [y, x]
                elif matrix[i][j] == 'F' and premier_F is None:
                    y=i//n
                    x=j//n
                    premier_F = [y, x]
        checkpoints = [premier_C, premier_D, premier_E, premier_F]
        return checkpoints


    def map_de_poids(self,matrix,width, height,check_id,n):  #une methode qui me fait passer de ma matrice de string (matrix)
        larg = height // (n * BLOCK_SIZE)                    #a une matrice de poids ou chaque block constituant ma map 
        long = width // (n * BLOCK_SIZE)                     #a son propre poid, va etre utiliser pour trouver le chemin 
        h = 0                                                # le moin resistif
        poids = [[0] * long for _ in range(larg)]

        for i in range(larg):  # lignes, les y
            for j in range(long):  # colonnes, les x
                a = 0
                for k in range(i * n, (i * n) + n):  # lignes, parcours les y
                    for l in range(j * n, (j * n) + n):  # colonnes, les x
                        h += 1
                        if matrix[k][l] == 'G':
                            a += 1
                            
                        elif matrix[k][l] == 'L':
                            a+=2000
                            
                        elif matrix[k][l] == 'B':
                            pass
                            
                        elif (matrix[k][l] == 'C' and check_id==0):
                            a+=-20
                            
                        elif (matrix[k][l] == 'D' and check_id==1):
                            a+=-20
                            
                        elif (matrix[k][l] == 'E' and check_id==2):
                            a+=-20
                            
                        elif (matrix[k][l] == 'F' and check_id==3):
                            a+=-20

                poids[i][j] = a

        return poids




    def radar2(self,entree, matrice_poids):         #methode qui me renvoie une liste des voisins dans une matrice 
        def get_value(y_offset, x_offset):          #n'importe le type des voisins et les stocks 
            x, y = int(entree[1] + x_offset), int(entree[0] + y_offset)
            if 0 <= x < len(matrice_poids[0]) and 0 <= y < len(matrice_poids):
                return matrice_poids[y][x]
            else:
                return 2000  
        if entree is not None:
            n = get_value(-1, 0)  # (yoffset, xoffset)
            s = get_value(1, 0)
            e = get_value(0, 1)
            w = get_value(0, -1)
            ne = get_value(-1, 1)
            nw = get_value(-1, -1)
            se = get_value(1, 1)
            sw = get_value(1, -1)
        else:
            # Set default values if entree is None
            n, s, w, e, ne, nw, se, sw = 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000

        return n, s, w, e, ne, nw, se, sw
    
    
    def path_finder(self,og_path,sortie,matrice_poids):#methode stochastic qui cherche le chemin le moin resistif 
        visited=[]                                     #en se basant sur la matrice de poids et renvoie une liste 
        min_path=[]                                    #des directions a suivre pour arriver a ma destination
        min_path_global = []
        ancien_path=1000
        nouv_path=100
        
        for i in range (100):
            nouv_path=0
            entree=og_path.copy()
            min_path=[]
            
            while(entree[0]!=sortie[0] or  entree[1]!=sortie[1]):#entree[0]=y,entree[1]=x
                n, s, w, e, ne, nw, se, sw=self.radar2(entree,matrice_poids)
                min_value = min(n, s, w, e, ne, nw, se, sw)
                min_direction=[]
                #je marche dans la direction du checkpoint et du minimum
                
                if(entree[0]<sortie[0] and entree[1]<sortie[1]):
                    min_direction.append('se')
                        
                if(entree[0]>sortie[0] and entree[1]<sortie[1]):
                    min_direction.append('ne')
                    
                if(entree[0]<sortie[0] and entree[1]>sortie[1]):
                    min_direction.append('sw')
                
                if(entree[0]>sortie[0] and entree[1]>sortie[1]):
                    min_direction.append('nw')
                        
                if(entree[0]<sortie[0]):
                    min_direction.append('s')
                        
                if(entree[0]>sortie[0]):
                    min_direction.append('n')
                        
                if(entree[1]<sortie[1]):
                    min_direction.append('e')
                        
                if(entree[1]>sortie[1]):
                    min_direction.append('w')
                
                if len(min_direction) >= 1:
                    random_number = random.randint(0, len(min_direction) - 1)
                    # print(min_direction)
                    direction = min_direction[random_number]
                    # print('diredtion choiisi=',direction)
                    min_path.append(direction)
                    # print("minimum path=", min_path)

                
                if(direction=='e'):
                    entree[1]=entree[1]+1
                
                if(direction=='w'):
                    entree[1]=entree[1]-1
                    
                if(direction=='s' ):
                    entree[0]=entree[0]+1
                    
                if(direction=='n'):
                    entree[0]=entree[0]-1
                    
                if(direction=='ne'):
                    entree[1]=entree[1]+1
                    entree[0]=entree[0]-1
                
                if(direction=='nw'):
                    entree[1]=entree[1]-1
                    entree[0]=entree[0]-1   
                if(direction=='se'):
                    entree[1]=entree[1]+1
                    entree[0]=entree[0]+1
                if(direction=='sw'):
                    entree[1]=entree[1]-1
                    entree[0]=entree[0]+1
                # print(entree)
                
                a,b=int(entree[0]),int(entree[1])
                # print(matrice_poids[a][b])
                nouv_path+=matrice_poids[a][b]
            # print(min_path)
                if(nouv_path<ancien_path):
                    min_path_global=min_path
                    ancien_path=nouv_path
            if not min_path_global and min_path:
                min_path_global = min_path
                
        return min_path_global

    
    

    def path_totale(self,entree,checkpoints,matrix, width, height,n):
        paths=[]
        check_id=0
        for i in range (len(checkpoints)):
            poids=self.map_de_poids(matrix, width, height, check_id,n)
            paths.append(self.path_finder(entree,checkpoints[i],poids))
            entree=checkpoints[i].copy()
            check_id+=1
        return paths
    
    def next_pos(self,entree,direction,n, width, height):
        
        x=entree[1]
        y=entree[0]
        if(direction=='e'):
            x=x+BLOCK_SIZE*n
        
        if(direction=='w'):
            print(x)
            x=x-BLOCK_SIZE*n
            print(x)
            print(-BLOCK_SIZE*n)
            
        if(direction=='s' ):
            y=y+BLOCK_SIZE*n
            
        if(direction=='n'):
            y=y-BLOCK_SIZE*n
            
        if(direction=='ne'):
            x=x+BLOCK_SIZE*n
            y=y-BLOCK_SIZE*n
        
        if(direction=='nw'):
            x=x-BLOCK_SIZE*n
            y=y-BLOCK_SIZE*n
        if(direction=='se'):
            x=x+BLOCK_SIZE*n
            y=y+BLOCK_SIZE*n
        if(direction=='sw'):
            x=x-BLOCK_SIZE*n
            y=y+BLOCK_SIZE*n
        x=x+ BLOCK_SIZE*width%n
        y=y+ BLOCK_SIZE*height%n
        x=round(x)
        y=round(y)
        return [y,x]
    
    
    
    def bloc_verif(self,sortie,matrix):
        checkpoints=['C','D','E','F']
        lava=['L']
        x=int(sortie[1]//BLOCK_SIZE)
        y=int(sortie[0]//BLOCK_SIZE)
        x_entr=sortie[1]
        y_entr=sortie[0]
        foundcheck=False
        foundlava=False
        # indices=None
        indices=[y,x]
        a=self.radar2(indices,matrix)
        
        if any(block_type in a for block_type in checkpoints):
            foundcheck=True
        if any(block_type in a for block_type in lava):
            foundlava=True
        n, s, w, e, ne, nw, se, sw=self.radar2(indices,matrix)
        
        if foundcheck :
            
            if(n in checkpoints):
                y=indices[0]-1
                x=indices[1]
                
            elif(s in checkpoints):
                y=indices[0]+1
                x=indices[1]
                
            elif w  in checkpoints:
                y = indices[0]
                x = (indices[1] - 1)
                
            elif e  in checkpoints:
                y = indices[0] 
                x = (indices[1] + 1)
                
            elif ne  in checkpoints:
                y = (indices[0] - 1) 
                x = (indices[1] + 1) 
                
            elif nw  in checkpoints:
                y = (indices[0] - 1) 
                x = (indices[1] - 1) 
                
            elif se  in checkpoints:
                y = (indices[0] + 1) 
                x = (indices[1] + 1) 
                
            elif sw  in checkpoints:
                y = (indices[0] + 1) 
                x = (indices[1] - 1)
            x=x*BLOCK_SIZE+0.5*BLOCK_SIZE
            y=y*BLOCK_SIZE+0.5*BLOCK_SIZE
        else :
            y=y_entr
            x=x_entr
        return[y,x]
    
    def move(self, string):
        
        
        if(AI.move_counter>0):
            pass
        else:
            
            self.matrix,self.width,self.height=self.devise_string(string)
            checkpoints=self.premiere_occurrence(self.matrix,self.n)
            entree_principale=[self.kart.y//(BLOCK_SIZE*self.n),self.kart.x//(BLOCK_SIZE*self.n)]
            self.path_tot=self.path_totale(entree_principale,checkpoints,self.matrix, self.width, self.height,self.n)
            
        AI.move_counter += 1
        
        
    
            
        
        
        if(self.ai_id!=self.kart.checkpoint):
            self.etape=-1
            print('check_point atteneint reinitialisations de etapes et direction vers nv check')
            print('ai id=',self.ai_id)
            print('kart id=',self.kart.checkpoint)
            print('---------------------------------')
            self.ai_id=self.kart.checkpoint
        
        if(abs(self.relative_x)<=2 and abs(self.relative_y)<=2):
            print('x=',self.kart.x)
            print('y=',self.kart.y)
            self.etape+=1
            direction=self.path_tot[self.ai_id][self.etape]
            self.entree=[self.kart.y,self.kart.x]
            self.sortie=self.next_pos(self.entree,direction,self.n,self.width, self.height)
            print('sortie1=',self.sortie)
            self.sortie=self.bloc_verif(self.sortie,self.matrix)
        
            print('==========etape=============',self.etape)
            print('ma sortie doit etre :',self.sortie)
            print('prochaine checkpoint direction  =',self.path_tot[self.ai_id])
            print('prochaine direction =',self.path_tot[self.ai_id][self.etape])
            
            print('entree=',self.entree)
            print('ai id=',self.ai_id)
            print('kart id=',self.kart.checkpoint)
            
        
        self.relative_x = self.sortie[1] - self.kart.x 
        self.relative_y = self.sortie[0] - self.kart.y
        
        
        
        
        next_checkpoint_angle = math.atan2(self.relative_y, self.relative_x)
        
        # L'angle relatif correspond a la rotation que doit faire le kart pour se trouver face au checkpoint
        # On applique l'operation (a + pi) % (2*pi) - pi pour obtenir un angle entre -pi et pi
        relative_angle = (next_checkpoint_angle - self.kart.orientation + math.pi) % (2 * math.pi) - math.pi
        
        # =================================================
        # Enfin, commander le kart en fonction de l'angle
        # =================================================
        if relative_angle > MAX_ANGLE_VELOCITY:
            # On tourne a droite
            command = [False, False, False, True]
        elif relative_angle < -MAX_ANGLE_VELOCITY:
            # On tourne a gauche
            command = [False, False, True, False]
        else:
            # On avance
            command = [True, False, False, False]
            
        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = {key: command[i] for i, key in enumerate(key_list)}
        return keys

            
        