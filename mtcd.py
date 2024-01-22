
def traitement_commandes_dynamiques (commande): 
    try : 
        commande_split=commande.split('=')
        if commande_split[0] == 'LED' and commande_split[1]== 'ON' :
            print("led on")
            #action...  

        elif commande_split[0] == 'LED' and commande_split[1]== 'OFF' :
            print("led off")
            #action...
        
        elif commande_split[0] == 'pot1' :
            print('potentiometre = ',commande_split[1])
            #action
    except :
        pass
  