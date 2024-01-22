def modifications_dico_valeurs_dynamiques(dico) :
    
#####################################################################
# pass     #pour pas de variables dynamiques 
####################### A programmer en fonction des capteurs #############
    #simulation mesure capteurs
    import random
    valeur_distance = random.randint(1,100)
    valeur_position_ligne = random.randint(1,7)
    
    # modification  de la variable temperature  
    dico["distance"] = str(valeur_distance)    #str car texte
    dico["position_ligne"] = str(valeur_position_ligne)    #str car texte
    #####################################################################
    return(dico)
