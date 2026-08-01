import random
import math
from settings import DEFAULT_HIDDEN_NODES, DEFAULT_MUTATION_RATE, MUTATION_MAG

mut_mag = MUTATION_MAG
mut_rate = DEFAULT_MUTATION_RATE

class NeuralNetwork:
    def __init__(self, input_nodes=4, hidden_nodes=DEFAULT_HIDDEN_NODES, output_nodes=1):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.ih_weights = [[random.uniform(-1, 1) for _ in range(input_nodes)] for _ in range(hidden_nodes)]
        self.ho_weights = [[random.uniform(-1, 1) for _ in range(hidden_nodes)] for _ in range(output_nodes)]

        self.h_bias = [random.uniform(-1, 1) for _ in range(hidden_nodes)]
        self.o_bias = [random.uniform(-1, 1) for _ in range(output_nodes)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def tanh(self, x):
        return math.tanh(x)

    def predict(self, input_arr):
        hidden = []
        for h in range(self.hidden_nodes):
            total = self.h_bias[h]
            for i in range(self.input_nodes):
                total += self.ih_weights[h][i] * input_arr[i]
            hidden.append(self.tanh(total))

        output = []
        for o in range(self.output_nodes):
            total = self.o_bias[o]
            for h in range(self.hidden_nodes):
                total += self.ho_weights[o][h] * hidden[h]
            output.append(self.sigmoid(total))

        return output[0]

    def mutate(self):
        global mut_mag, mut_rate

        def mutate_val(v):
            if random.random() < mut_rate:
                return v + random.gauss(0, mut_mag)
            return v

        mut_rate *= 0.99998
        mut_mag *= 0.99998

        self.ih_weights = [[mutate_val(v) for v in row] for row in self.ih_weights]
        self.ho_weights = [[mutate_val(v) for v in row] for row in self.ho_weights]
        self.h_bias = [mutate_val(v) for v in self.h_bias]
        self.o_bias = [mutate_val(v) for v in self.o_bias]