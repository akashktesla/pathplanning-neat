class Node():
    def __init__(self,_input,output,weight,bias,is_disabled=False):
        self.input = _input
        self.output = output
        self.weight = weight 
        self.bias = bias
        self.is_disabled = is_disabled

    def to_string(self):
        return f"{self.input}-{self.output}-{self.weight}-{self.bias}-{self.is_disabled}"

    def to_key(self):
        return f"{self.input}-{self.output}"

    def print(self):
        print(f"input:{self.input} : output:{self.output} : weight:{self.weight} : bias:{self.bias} : is_disabled:{self.is_disabled}")

def str_to_bool(_str):
    if _str == "True":
        return True
    return False

class NeuralNetwork():
    #id_network contains input layer values
    #c_nework connection network 
    def __init__(self,input_network,output_network,id_network,c_network):
        self.input_network = input_network # ids of input network 
        self.output_network = output_network #ids of output network
        self.id_network = id_network #dictionary of ids and values
        self.c_nework = c_network 
    #returns output neural network
    def print(self):
        for i in self.id_network:
            print(f"input:{i.input} : output:{i.output} : weight:{i.weight} : bias:{i.bias} : is_disabled:{i.is_disabled}")
        for i in self.id_network:
            print(f"")
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
        if not str_to_bool(temp[4]):
            return_network.append(Node(temp[0],temp[1],temp[2],temp[3],is_disabled=False))
    return return_network

def calculate(nn):
    nn.print()
    input_layer = nn.input_network

def main():
    nn = NeuralNetwork([1,2,3], #input network
                       [8,9], #output network 
                       {"1":3,"2":3,"3":3}, # id_network 
                       [Node(1,2,1.2,2.3),Node(2,3,3.2,2.1),Node(3,4,1.2,3.2)]) #c_network
    calculate(nn)

if __name__ == "__main__":
    main()






