import numpy as np
from pandas import DataFrame
import math
import copy

class Salesman():
    def __init__(self, route_list):
        self.route_df = DataFrame(route_list)
        self.stack_search_nodes = [] #A group of nodes stacked with solutions to mitigation problems
        self.present_nodes = [] #Just the node you are searching for(1 or 2)
        self.suitable_val = math.inf #Provisional value
        self.suitable_ans = [] #Provisional solution
        self.node_num = self.route_df.shape[0] #Number of nodes

    #The minimum value of the given DataFrame[index, column]Return a pair
    def __minimumRoute(self, target_route_df):
        min_index = target_route_df.idxmin(axis=1) #Minimum column for each row
        minimum = math.inf #Initial value of the minimum value
        loc = [-1, -1] #Initial value of position
        for index, column in zip(min_index.index, min_index.values):
            if math.isnan(column): #NaN when all lines are inf,This is not the minimum
                continue
            if minimum > target_route_df[column][index]:
                minimum = target_route_df[column][index] #Minimum value update
                loc = [index, column] # index,Update column position
        return loc

    #Given a default DataFrame and an array of route selections, it returns the optimal value
    def __calcSuitableSum(self, route_list):
        route_df_tmp = copy.deepcopy(self.route_df)
        route_length = 0
        for route in route_list:
            if route[2] == 0: #When selecting this route
                route_length += route_df_tmp[route[1]][route[0]] #Added to route length
                if (route[1] in route_df_tmp.index and route[0] in route_df_tmp.columns): #When the corresponding element still exists in the DataFrame of the reduced path
                    route_df_tmp[route[0]][route[1]] = math.inf # DataFrame[column][index],Reverse route of the corresponding road(1->When 2 2->1)Will not be adopted, so inf
                route_df_tmp = route_df_tmp.drop(route[0], axis=0) #Delete line of the corresponding route
                route_df_tmp = route_df_tmp.drop(route[1], axis=1) #Delete the column of the corresponding route
            else: #When not selecting this route
                if (route[0] in route_df_tmp.index and route[1] in route_df_tmp.columns): #When the corresponding element still exists in the DataFrame of the reduced path
                    route_df_tmp[route[1]][route[0]] = math.inf #Since it is not adopted, let the corresponding route be inf

        min_sum = 0 #Add the path lengths of mitigation problems
        next_route = copy.deepcopy(route_df_tmp) #DataFrame at this point is next_Keep on route
        for index in route_df_tmp.index: #Run on each line
            min_tmp = route_df_tmp.ix[index, :].min() #Get the minimum value of a row
            min_sum += min_tmp #Add the minimum value
            route_df_tmp.ix[index, :] = route_df_tmp.ix[index, :] - min_tmp #Subtract the minimum value from each element in the row
        for column in route_df_tmp.columns: #Run on each column
            min_tmp = route_df_tmp.ix[:, column].min() #Get column minimum
            min_sum += min_tmp #Add the minimum value
            route_df_tmp.ix[:, column] = route_df_tmp.ix[:, column] - min_tmp #Subtract the minimum value from each element in that column
        route_length += min_sum #Added to route length
        return route_length, next_route #DataFrame of the route length and the route at the time of the node

    #Check if the cycle is closed
    def __checkClosedCircle(self, route_list, route_df_tmp):
        # route_df_Assuming tmp is 2x2
        mini_route = self.__minimumRoute(route_df_tmp) # route_df_Of the smallest element of tmp[index, coumn]
        if mini_route == [-1, -1]: #route_df_When all tmp are inf
            return False
        mini_route.append(0) #Add 0 because it is the route to be adopted
        route_list.append(mini_route) #Add to route list
        route_df_tmp = route_df_tmp.drop(mini_route[0], axis=0) #Delete row
        route_df_tmp = route_df_tmp.drop(mini_route[1], axis=1) #Delete column
        last_route = [route_df_tmp.index[0], route_df_tmp.columns[0]] #Get the rest of the elements
        last_route.append(0) #Add 0 because it is the route to be adopted
        route_list.append(last_route) #Add to route list

        label, counter = 0, 0 #label is the current position,counter is the number of moves
        for i in range(self.node_num): #Maximum number of iterations is number of nodes
            for route in route_list:
                if route[0] == label and route[2] == 0: #If the starting point is label and the adopted route
                    new_label = route[1] #Label update
                    counter += 1 #counter increment
            label = new_label
            if label == 0: #If label is 0, the round is over
                break
        if counter == self.node_num: #If the number of movements matches the number of nodes, the cycle is closed.
            return True
        else:
            return False

    #Add a new route to the route to a certain node and present_Add to nodes
    def __setPresentNodes(self, target_route, target_branch):
        for status in range(2):
            target_route_tmp = copy.deepcopy(target_route) # target_Copy ele
            target_route_tmp.append(status) # status(Approval) added
            target_branch_tmp = copy.deepcopy(target_branch) # target_Copy branch
            target_branch_tmp.append(target_route_tmp) #Add route
            self.present_nodes.append(target_branch_tmp) # present_Added to nodes

    #Evaluate the relevant node,Evaluate the node if branching is possible,If the branch ends, compare with the provisional value
    def __evaluateNode(self, target_node):
        if (False if target_node[1].shape == (2, 2) else True):  #When you can still branch,Judgment is target_DataFrame of node has not reached 2x2
            next_route = self.__minimumRoute(target_node[1]) #Get the smallest element[index, column]
            if next_route != [-1, -1]: # [-1, -1]In the case of, the distance becomes inf, so it is not suitable., present_Add nothing to nodes
                self.__setPresentNodes(next_route, target_node[0])
        else: #At the end of the branch
            if self.__checkClosedCircle(target_node[0], target_node[1]): #Is it a one-round cycle?
                if self.suitable_val > target_node[2]: #Is it smaller than the provisional value?
                    self.suitable_val = target_node[2] #Update of provisional value
                    self.suitable_ans = target_node[0] #Update of provisional solution

    #Convert a list of routes to path
    def __displayRoutePath(self, route_list):
        label, counter, route_path = 0, 0, "0" #label is the current position,counter is the number of moves, route_path is the route
        for i in range(self.node_num): #Maximum number of iterations is number of nodes
            for route in route_list:
                if route[0] == label and route[2] == 0: #If the starting point is label and the adopted route
                    new_label = route[1] #Label update
                    route_path += " -> " + str(new_label)
                    counter += 1 #counter increment
            label = new_label
            if label == 0: #If label is 0, the round is over
                break
        return route_path

    #Calculate the optimum value and the optimum solution(Main method)
    def getSuitableAns(self):
        target_route = self.__minimumRoute(self.route_df) #Get the minimum element of DataFrame of route
        self.__setPresentNodes(target_route, []) # present_Set to nodes

        while True:
            if self.suitable_val != math.inf: #When the provisional value of the optimal solution is set
                self.stack_search_nodes = list(filter(lambda node: node[2] < self.suitable_val, self.stack_search_nodes)) #Exclude if the solution of the mitigation problem of stacked nodes exceeds the provisional value

            while len(self.present_nodes) != 0: #If there is a list of searches, ask the solution of the mitigation problem and stack
                first_list = self.present_nodes[0] # present_Get to evaluate nodes
                self.present_nodes.pop(0) #I will evaluate it so present_Exclude from nodes
                route_length, next_route = self.__calcSuitableSum(first_list) #Get the solution to the mitigation problem
                self.stack_search_nodes.insert(0, [first_list, next_route, route_length]) #stack

            if len(self.stack_search_nodes) == 0: #Exit when there are no more stacks
                break;

            #When the number of stacked nodes is 1, or when the solution of the first mitigation problem of the stacked nodes is smaller than the solution of the second mitigation problem(To confirm from the solution that seems to be good)
            if len(self.stack_search_nodes) == 1 or self.stack_search_nodes[0][2] <= self.stack_search_nodes[1][2]:
                self.__evaluateNode(self.stack_search_nodes[0]) #Evaluate the first node
                self.stack_search_nodes.pop(0) #Delete the first node
            else:
                self.__evaluateNode(self.stack_search_nodes[1]) #Evaluate the second node
                self.stack_search_nodes.pop(1) #Delete the second node

        return self.suitable_val, self.__displayRoutePath(self.suitable_ans) #Returns the optimum value and the optimum route
