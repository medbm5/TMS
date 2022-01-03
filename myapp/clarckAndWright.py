import math
import operator

def Clarke_Wright(M):
    # Notre liste de chemin, on fixe le premier noeud (1)
    Result=[1,1]
    
    #Calculer les économies
    SavingsList={}
    s=0
    for i in range(1,len(M)):
        for j in range(i+1,len(M[0])):
            s=(M[i][0]+M[0][j])-M[i][j]
            SavingsList[(i+1,j+1)]=s
    
    #Trier les économies en ordre décroissante
    SavingsList = sorted(SavingsList.items(), key=operator.itemgetter(1), reverse=True)
    print('economistes=>',SavingsList[0])
    #first tour
    Result=[1,SavingsList[0][0][0],SavingsList[0][0][1],1]
    print(Result,'\n')

    for i in range(1,len(SavingsList)):
        route=SavingsList[i]
        route=route[0]
        if(route[0] in Result and route[1] in Result):
            continue
        elif(route[0] in Result and route[1] not in Result):
            index=Result.index(route[0])
            Result.insert(index+1,route[1])

        elif(route[1] in Result and route[0] not in Result):
            index=Result.index(route[1])
            Result.insert(index+1,route[0])

        else:
            continue

        print(route,Result,'\n')
    return Result