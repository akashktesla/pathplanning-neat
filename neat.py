from random import randint
import random
import copy

# class Node():
#     def __init__(self,_id,value):
#         self.id = _id
#         self.value = value

class Connect():
    def __init__(self,innovation_number,_input,output,weight,is_disabled=False):
        self.innovation_number = innovation_number
        self.input = _input #input node
        self.output = output #output node
        self.weight = weight 
        self.is_disabled = is_disabled

    def calculate(self,value):
        return value*self.weight

    def to_string(self):
        return f"{self.innovation_number}-{self.input}-{self.output}-{self.weight}-{self.is_disabled}"

    def to_key(self):
        return f"{self.input}-{self.output}"

    def print(self):
        print(f"innovation number:{self.innovation_number} : input:{self.input} : output:{self.output} : weight:{self.weight} : is_disabled:{self.is_disabled}")

def str_to_bool(_str):
    if _str == "True":
        return True
    return False

class NeuralNetwork():
    #node_map contains input layer values
    # c_network connection network 
    def __init__(self,input_layer,output_layer,hidden_layer,node_map,c_network,stepsize,next_in,next_nn,min_weight=0,max_weight=0):
        self.input_layer = input_layer # ids of input layer 
        self.output_layer = output_layer #ids of output layer
        self.hidden_layer = hidden_layer
        self.node_map = node_map #dictionary of ids and values
        self.c_network = c_network 
        self.next_in = next_in
        self.next_nn = next_nn
        self.mutation_stepsize = stepsize
        #calculate maximum weight
        weight_list = []
        for i in c_network:
            weight_list.append(i.weight)
        if min_weight!=0:
            self.min_weight = min_weight
        else:
            self.min_weight = min(weight_list)
        if max_weight!=0:
            self.max_weight = max_weight
        else:
            self.max_weight = max(weight_list)



    #returns output neural network
    def print(self):
        print(f'input layer: {self.input_layer}')
        print(f'output layer: {self.output_layer}')
        print(f'id network: {self.node_map}')
        for i in self.c_network:
            i.print()

    def evaluate(self):
        pass


#sigmoid
def sigmoid(x):
    pass

def relu(x):
	return max(0.0, x)

def network_to_string(nn):
    returns = set()
    for i in nn.c_network:
        returns.add(f"{i.input}-{i.output}")
    return returns

def crossover(a,b):
    aset = network_to_string(a)
    bset = network_to_string(b)
    node_hm = {}
    for i in a.c_network:
        node_hm[i.to_key()] = i.to_string()
    for i in b.c_network:
        node_hm[i.to_key()] = i.to_string()
    asi = aset.union(bset)
    # print(f'node-hashmap: {node_hm}')
    return_network = []
    for i in asi:
        key = node_hm[i]
        temp = key.split("-")
        #checking if thery are disabled 
        if not str_to_bool(temp[3]):
            return_network.append(Connect(temp[0],temp[1],temp[2],temp[3],is_disabled=False))
    return return_network

def mutation(nn):
    nl = [nn]
    tl = [copy.deepcopy(nn)]
    cl = []
    for i in tl:
        temp = mutation_c(i)
        cl.append(temp)

    nl = nl+cl

    tl = clone_list(nl)
    cl = []
    for i in tl:
        cl.append(mutation_cw(i))
    nl = nl+cl

    # tl = clone_list(nl)
    # cl = []
    # for i in tl:
    #     cl.append(mutation_c(i))
    # nl = nl+cl

    # tl = clone_list(nl)
    # cl = []
    # for i in tl:
    #     cl.append(mutation_cw(i))
    # nl = nl+cl

    return nl

#mutation connecting a possible connection
def mutation_c(nn):
    hidden_layer = nn.hidden_layer
    ith = []
    for i in nn.input_layer:
        for j in hidden_layer:
            ith.append(f'{i}-{j}')
    # print(f"{ith}")
    #hiddenlayer to  output layer
    hto = []
    for i in hidden_layer:
        for j in nn.output_layer:
            hto.append(f'{i}-{j}')
    pc = ith+hto
    exsisting_connections = []
    # print(f"possible connections :{pc}")
    for i in nn.c_network:
        exsisting_connections.append(f"{i.input}-{i.output}")
    # print(f"exsisting connections: {exsisting_connections}")
    for i in exsisting_connections:
        try:
            pc.remove(i)
        except:
            pass
    # print(f"possible connections: {pc}")

    index = randint(0,len(pc)-1)
    # print(f"index: {index}")
    connection = pc[index]
    # print(connection)
    _split = connection.split("-")
    _input = _split[0]
    _output = _split[1]
    con_node = Connect(nn.next_in,_input,_output,random.uniform(nn.min_weight,nn.max_weight))

    #updates
    nn.c_network.append(con_node)
    #update next innovation number
    nn.next_in +=1
    return nn

# mutation add new node
def mutation_an(nn):
    #create new node
    node_id = nn.next_nn 
    #input to node
    rin = nn.input_layer[randint(0,len(nn.input_layer)-1)]
    #node to output
    rout = nn.output_layer[randint(0,len(nn.output_layer)-1)]
    #connection 
    #input to node connection
    itn_node = Connect(nn.next_in,rin,node_id,random.uniform(nn.min_weight,nn.max_weight))
    #node to output connection
    nto_node = Connect(nn.next_in+1,node_id,rout,random.uniform(nn.min_weight,nn.max_weight))
    #updates
    #updating connection network
    nn.c_network.append(itn_node)
    nn.c_network.append(nto_node)
    #updating next innovation number
    nn.next_in+=2
    #initializing node in node map
    nn.node_map[str(node_id)] = 0
    nn.next_nn +=1
    # print("mutation an end ")
    return nn

def mutation_cw(nn):
    if len(nn.c_network) >0:
        random_node = nn.c_network[randint(0,len(nn.c_network)-1)]
        random_node.weight = random.uniform(random_node.weight-nn.mutation_stepsize,random_node.weight+nn.mutation_stepsize)
    return nn

#disables random node... mayb use it in cross over ig...
def mutation_dn(nn):
    if len(nn.c_network) >0:
        random_node = nn.c_network[randint(0,len(nn.c_network)-1)]
        random_node.is_disabled = True
    return nn


def clone_list(nl):
    cl = []
    for i in nl:
        cl.append(copy.deepcopy(i))
    return cl

def calculate(nn):
    # nn.print()
    for i in nn.c_network:
        in_val = nn.node_map[str(i.input)]
        val = i.calculate(in_val)
        nn.node_map[str(i.output)] = val
    # nn.print()
    # for i in nn.output_layer:
        # print(f"output at node:{i} is {nn.node_map[str(i)]}")


def calculate_2(nn):
    pass

def crossover_test():
    parent1 = NeuralNetwork(['1','2','3','4'], #input network
                       ['8','9'], #output network 
                       {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0}, # node_map 
                       [Connect(1,1,5,1.2),Connect(2,1,6,3.2),Connect(3,1,7,3.2),
                        Connect(4,2,5,5.2),Connect(5,2,6,4.5),
                        Connect(6,3,5,2.3),
                        Connect(8,4,6,8.3),
                        Connect(9,5,8,4.3),
                        Connect(10,6,8,9.3),
                        Connect(12,7,8,7.2),Connect(13,7,9,4.2)],
                       2.5,#weights stepsize
                       13, #next innovation number
                       10, #next node number
                       )
    parent2 = NeuralNetwork(['1','2','3','4'], #input network
                       ['8','9'], #output network 
                       {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0}, # node_map 
                       [Connect(1,1,5,1.2),Connect(2,1,6,3.2),Connect(3,1,7,3.2),
                        Connect(4,2,5,5.2),Connect(5,2,6,4.5),
                        Connect(6,3,5,2.3),Connect(7,3,7,1.2),
                        Connect(8,4,6,8.3),
                        Connect(9,5,8,4.3),
                        Connect(10,6,8,9.3),Connect(11,6,9,3.7),
                        Connect(12,7,8,7.2),Connect(13,7,9,4.2)],
                       2.5,#weights stepsize
                       13, #next innovation number
                       10, #next node number
                       )
    offspring = crossover(parent1,parent2)
    print(offspring)
    for i in offspring:
            i.print()




def main():
    nn = NeuralNetwork(['1','2','3','4'], #input network
                       ['8','9'], #output network 
                       {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0}, # node_map 
                       [Connect(1,1,5,1.2),Connect(2,1,6,3.2),Connect(3,1,7,3.2),
                        Connect(4,2,5,5.2),Connect(5,2,6,4.5),
                        Connect(6,3,5,2.3),Connect(7,3,7,1.2),
                        Connect(8,4,6,8.3),
                        Connect(9,5,8,4.3),
                        Connect(10,6,8,9.3),Connect(11,6,9,3.7),
                        Connect(12,7,8,7.2),Connect(13,7,9,4.2)],
                       2.5,#weights stepsize
                       13, #next innovation number
                       10, #next node number
                       )

    # calculate(nn)
    # crossover_test()
    # mutation(nn)

def main2():
    nn = NeuralNetwork(
        [1,2,3,4,5,6,7,8,9,10],#input layer
        [11,12,13,14],#output layer
        [15],#hidden layer
        {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,},#node map
        [],#connection network
        2.5,#stepsize
        1,#next innovation number
        16,#next node number
        1,#min weight 
        100 #max weight
    )
    #end
    nl = mutation(nn)
    # print(nl)
    # for i in nl:
    #     i.print()


if __name__ == "__main__":
    main2()
