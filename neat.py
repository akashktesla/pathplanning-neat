class Node():
    def __init__(self,_input,output,weight,bias,is_disabled=False):
        self.input = _input
        self.output = output
        self.weight = weight 
        self.bias = bias
        self.is_disabled = is_disabled

    def calculate(self,value):
        return value*self.weight+self.bias

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
    # c_network connection network 
    def __init__(self,input_layer,output_layer,id_network,c_network):
        self.input_layer = input_layer # ids of input layer 
        self.output_layer = output_layer #ids of output layer
        self.id_network = id_network #dictionary of ids and values
        self.c_network = c_network 
    #returns output neural network
    def print(self):
        print(f'input layer: {self.input_layer}')
        print(f'output layer: {self.output_layer}')
        print(f'id network: {self.id_network}')
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
        if not str_to_bool(temp[4]):
            return_network.append(Node(temp[0],temp[1],temp[2],temp[3],is_disabled=False))
    return return_network

def mutation(nn):
    nn.print()
    #convert id network to list
    hidden_layer = []
    for i in nn.id_network:
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


def calculate(nn):
    nn.print()
    for i in nn.c_network:
        in_val = nn.id_network[str(i.input)]
        val = i.calculate(in_val)
        nn.id_network[str(i.output)] = val
    print("valzkai ae")
    nn.print()

def main():
    nn = NeuralNetwork(['1','2','3','4'], #input network
                       ['8','9'], #output network 
                       {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0}, # id_network 
                       [Node(1,5,1.2,2.3),Node(1,6,3.2,2.1),Node(1,7,3.2,1.4),
                        Node(2,5,5.2,1.7),Node(2,6,4.5,2.2),
                        Node(3,5,2.3,5.7),Node(3,7,1.2,3.2),
                        Node(4,6,8.3,7.2),
                        Node(5,8,4.3,2.2),
                        Node(6,8,9.3,3.2),Node(6,9,3.7,5.8),
                        Node(7,8,7.2,3.1),Node(7,9,7.2,4.7)])
    mutation(nn)

if __name__ == "__main__":
    main()
