import time
import logging
import os
import psutil
import random

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
    weights = []
    interceptions = []

    def __init__(self, prev_layer, next_layer, init_epsilon=10e-3):
        self.prev_layer = prev_layer
        self.next_layer = next_layer
        self.weights = [[random.random()*init_epsilon for i in [None]*prev_layer.get_size()] for j in [None]*next_layer.get_size()]
        self.interceptions = [random.random()*init_epsilon for i in [None] * next_layer.get_size()]


class Layer:
    vertices = None
    size = None

    def set_vertices(self, data):
        self.vertices = [y for y in data]
        self.size = len(self.vertices)
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
            self.forward_propagate_from_layer(i, activation_function)

    def forward_propagate_from_layer(self, layer_index, activation_function = sigmoid):
        import numpy
        c = self.Connections[layer_index]
        for i in range(c.next_layer.get_size()):
            c.next_layer.vertices[i] = activation_function(numpy.array(c.weights[layer_index]) @
                                                           numpy.array(c.next_layer.vertices) + numpy.array(c.interceptions))

        return self

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

    # def set_output(self, output: Layer):
    #     self.output = output
    #     return self

    # def set_input(self, input: Layer):
    #     self.input = input
    #     return self

    # def copy_output(self, data):
    #     self.output = Layer(len(data), len(data[0]))
    #     self.output.set_vertices(data)
    #     return self

    # def copy_input(self, data):
    #     self.input = Layer(len(data), len(data[0]))
    #     self.input.set_vertices(data)
    #     return self

    def __init__(self):
        return self


class SampleImage(Sample):
    image = None
    data = None
    w = None
    h = None
    class_index = None

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

    def set_class(self, class_index):
        self.class_index = class_index
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


# class SampleReader:
#     def __init__(self, path, sample_class, net_config):
#         from os import listdir
#         from os.path import isfile, join
#         self._config = net_config
#         self._sample_class = sample_class
#         self._path = path
#         self._current = 0
#         self._list = [f for f in listdir(self._path) if isfile(join(self._path, f))]
#         self._list.sort()
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self._current >= len(self._list):
#             raise StopIteration
#         else:
#             self._current += 1
#             return self._sample_class(self._config).read(self._list[self._current - 1])
#
#     pass
