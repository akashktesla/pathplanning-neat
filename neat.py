from random import randint
import random

class Node():
    def __init__(self,_id,value):
        self.id = _id
        self.value = value

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
    def __init__(self,input_layer,output_layer,node_map,c_network,next_ii,min_weight=0,max_weight=0):
        self.input_layer = input_layer # ids of input layer 
        self.output_layer = output_layer #ids of output layer
        self.node_map = node_map #dictionary of ids and values
        self.c_network = c_network 
        self.next_ii = next_ii
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

class Agent():
    def __init__(self,inn):
        self.nn = inn
        self.tof = 0
        self.distance = 0
        self.displacement = 0
        self.fitness = 0

    def update_fitness(self):
        #updates fitness according to the parameters
        pass 

#sigmoid
def sigmoid(x):
    pass

def relu(x):
	return max(0.0, x)

def network_io_string(nn):
    returns = set()
    for i in nn:
        returns.add(f"{i.input}-{i.output}")
    return returns

def crossover(a,b):
    aset = network_io_string(a.input_network)
    bset = network_io_string(b.input_network)
    node_hm = {}
    for i in a.input_network:
        node_hm[i.to_key()] = i.to_string()
    for i in b.input_network:
        node_hm[i.to_key()] = i.to_string()
    asi = aset.union(bset)
    print(f'node-hashmap: {node_hm}')
    return_network = []
    for i in asi:
        key = node_hm[i]
        temp = key.split("-")
        #checking if thery are disabled 
        if not str_to_bool(temp[3]):
            return_network.append(Connect(temp[0],temp[1],temp[2],temp[3],is_disabled=False))
    return return_network

def mutation(nn):
    nn.print()
    #convert id network to list
    hidden_layer = []
    for i in nn.node_map:
        hidden_layer.append(i)
    print(hidden_layer) 
    for i in nn.input_layer:
        hidden_layer.remove(i)
    for i in nn.output_layer:
        hidden_layer.remove(i)
    print(f"hiddenlayer: {hidden_layer}")
    # input to hiddenlayer
    ith = []
    for i in nn.input_layer:
        for j in hidden_layer:
            ith.append(f'{i}-{j}')
    print(f"{ith}")
    #hiddenlayer to  output layer
    hto = []
    for i in hidden_layer:
        for j in nn.output_layer:
            hto.append(f'{i}-{j}')
    possible_connections = ith+hto
    exsisting_connections = []

    #exsisting connections
    for i in nn.c_network:
        exsisting_connections.append(f"{i.input}-{i.output}")
    print(f"possible_connections: {possible_connections}")
    print(f"exsisting connection: {exsisting_connections}")
    for i in exsisting_connections:
        try:
            possible_connections.remove(i)
        except:
            pass
    print(f"possible connections: {possible_connections}")

    #connecting the possible connection
    mutation_c(nn,possible_connections)
    #adding new node
    #modifing exsisting weights sooo... mayb like with step size or some shit idk


#connecting a possible connection
def mutation_c(nn,pc):
    connection = pc[randint(0,len(pc)-1)]
    print(connection)
    _split = connection.split("-")
    _input = _split[0]
    _output = _split[1]
    con_node = Connect(nn.next_ii,_input,_output,random.uniform(nn.min_weight,nn.max_weight))
    #don't forget to update next_ii da
    con_node.print()

# add new node
def mutation_an(nn):
   pass 




def calculate(nn):
    nn.print()
    for i in nn.c_network:
        in_val = nn.node_map[str(i.input)]
        val = i.calculate(in_val)
        nn.node_map[str(i.output)] = val
    print("valzkai ae")
    nn.print()

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
                        Connect(12,7,8,7.2),Connect(13,7,9,7.2)],
                       13 #next innovation number
                       )
    mutation(nn)

if __name__ == "__main__":
    main()
