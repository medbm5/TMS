from .helper import get_matrix_distances
from .branchAndBound import Salesman
from .nearestNeighbor import Prch_Vsn
from .clarckAndWright import Clarke_Wright
from .rl_tsp.tsp_solver import tsp_solver
import numpy as np

def get_bnb(df):
    print(df.dtypes)
    route_list =get_matrix_distances(df)
    #Instantiate and use method
    salesman = Salesman(route_list)
    suitable_val, suitable_route = salesman.getSuitableAns()
    return(suitable_route)


def get_NN(df):
    route_list =get_matrix_distances(df)
    return(Prch_Vsn(route_list))

def get_CW(df):
    route_list=get_matrix_distances(df)
    return(Clarke_Wright(route_list))

def get_RL(df):
    route_liste=get_matrix_distances(df)
    dist_mat=np.array(route_liste)
    best_pctg = 100
    alpha = 0.012
    gamma = 0.4
    #for alpha in np.linspace(0.012,0.012,1):
    #    for gamma in np.linspace(0.4 ,0.4,100):
    for _ in range(15):
            slow_pctg, rl_route, rl_dist, google_route, google_dist = tsp_solver(dist_mat, alpha=alpha, gamma=gamma)
            if slow_pctg < best_pctg:
                best_pctg = slow_pctg
                if slow_pctg < 0:
                    print(f"\nBest solution so far with parameters alpha:{alpha}, gamma:{gamma}, is {-np.around(slow_pctg,decimals=1)}% FASTER than google's solution")
                    print(f"RL route:     {rl_route}; distance: {rl_dist}")
                    print(f"Google route {google_route}; distance: {google_dist}\n")
                else:
                    print(f"\nBest solution so far with parameters alpha:{alpha}, gamma:{gamma}, is {np.around(slow_pctg,decimals=1)}% slower than google's solution")
                    
    final_result=rl_route

    print('final===>',final_result)
    return(final_result)