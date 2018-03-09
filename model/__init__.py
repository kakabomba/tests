import time
import logging
import os
import psutil
import random
import numpy

ident = 0


class Configuration:
    layer_sizes = []

    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes

    def __str__(self):
        return ', '.join(['Layer {} = {} nodes'.format(ind, c) for ind, c in enumerate(self.layer_sizes)])


class Connections:
    prev_layer = None
    next_layer = None
    weights = None
    interceptions = None

    def __init__(self, prev_layer, next_layer, init_epsilon=10e-3):
        self.prev_layer = prev_layer
        self.next_layer = next_layer
        self.weights = numpy.random.rand(prev_layer.get_size(), next_layer.get_size())
        self.interceptions = numpy.random.rand(next_layer.get_size())
        f = numpy.vectorize(lambda a: a*init_epsilon)
        f(self.weights)
        f(self.interceptions)


class Layer:
    vertices = None
    size = None

    def set_vertices(self, data):
        self.size = len(data)
        self.vertices = numpy.zeros(self.size)
        for idx, val in enumerate(data):
            self.vertices[idx] = val
        return self

    def get_size(self):
        return self.size


def sigmoid(x):
    import math
    return 1 / (1 + math.exp(-x))


class Network:
    Layers = []
    Connections = []

    def __init__(self, configuration: Configuration):
        for index, c in enumerate(configuration.layer_sizes):
            self.Layers.append(Layer().set_vertices([0]*c))
            if index > 0:
                self.Connections.append(Connections(self.Layers[len(self.Layers)-2], self.Layers[len(self.Layers)-1]))

    def train(self, sample: Layer):
        pass

    def back_propagate(self, from_layer_number, activation_function):
        pass

    def set_layer(self, data, layer_index = 0):
        self.Layers[layer_index].set_vertices(data)
        return self

    def forward_propagate(self, activation_function = sigmoid):
        for i, layer in enumerate(self.Layers):
            if (i<len(self.Layers)-1):
                self.forward_propagate_from_layer(i, activation_function)

    def forward_propagate_from_layer(self, layer_index, activation_function = sigmoid):
        c = self.Connections[layer_index]
        from_layer = self.Layers[layer_index]
        to_layer = self.Layers[layer_index + 1]
        to_layer.vertices = numpy.vectorize(activation_function)(from_layer.vertices @ c.weights + c.interceptions)
        return self

    def error_function(self, expected_value, layer_index):
        return numpy.linalg.norm(expected_value - self.Layers[layer_index].vertices)


    def clasify(self, input: Layer, activation_function):
        self.Layers[0].set_vertices(input.vertices)
        for i, layer in enumerate(self.Layers):
            if i < len(self.Layers) - 1:
                print('Before propagation\n', self.Layers[i + 1])
                self.forward_propagate(i, activation_function)
                print('After propagation\n', self.Layers[i + 1])
        return self

    def get_result(self):
        return self.Layers[len(self.Layers) - 1]


class Measure:
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        global ident
        process = psutil.Process(os.getpid())
        self.mem = process.memory_info().rss
        self.time = time.time()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('octolith')
        self.logger.info(''.join(['__'] * ident) + ' >>> Starting ' + self.message)
        ident += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        global ident
        process = psutil.Process(os.getpid())
        ident -= 1
        self.logger.info(''.join(['__'] * ident) +
                         ' <<< Finished ' + self.message + ': Time consumed: %s sec, Memory consumed: %s MB',
                         round(time.time() - self.time, 2),
                         round((process.memory_info().rss - self.mem) / 1024 / 1024, 2))


class Sample:
    output = None
    input = None

    def __init__(self):
        return self


class SampleImage(Sample):
    image = None
    data = None
    w = None
    h = None
    expected_value = None

    def __init__(self):
        Sample.__init__(self)

    def scale(self, new_size):
        self.image = self.image.resize(new_size)
        self.w, self.h =new_size
        return self

    def read(self, filename):
        from PIL import Image
        im = Image.open(filename)
        self.image = im.convert('RGB')
        self.w, self.h = (self.image.width, self.image.height)
        im.close()
        return self

    def convert_to_data(self):
        self.data = [sum(self.image.getpixel((i % self.w, i // self.w)))/3./255. for i in range(self.w * self.h)]
        self.image.close()
        return self

    def get_data(self, index):
        return self.data

    def set_expected_value(self, expected_value):
        self.expected_value = expected_value
        return self

    def get_w_h(self):
        return self.image.width, self.image.height

    @staticmethod
    def calculate_average_w_h(sizes):
        area = 1
        aspect = 1

        for s in sizes:
            area = area * (s[0]*s[1])**(1/len(sizes))
            aspect = aspect * (s[0]/s[1])**(1/len(sizes))

        return round((area*aspect)**0.5), round((area/aspect)**0.5)


