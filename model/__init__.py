import time
import logging
import os
import psutil

ident = 0


class Configuration:
    layer_sizes = []

    def __init__(self):
        self.layer_sizes = [[100, 100], [50, 50], [2, 1]]

    def __str__(self):
        return ', '.join(['Layer {} ({}x{})'.format(ind, c[0], c[1]) for ind, c in enumerate(self.layer_sizes)])


class Layer:
    vertices = [[]]

    def __init__(self, w=100, h=100):
        self.data = [[0 for x in range(w)] for y in range(h)]


class Network:
    Layers = []
    Edges = []

    def __init__(self, configuration: Configuration):
        for index, c in enumerate(configuration.layer_sizes):
            self.Layers.append(Layer(c[0], c[1]))
            if index > 0:
                prev_size = configuration.layer_sizes[index - 1]
                self.Edges.append(
                    [[[[0. for xp in range(prev_size[0])] for yp in range(prev_size[1])] for x in range(c[0])] for y in
                     range(c[1])])

    def train(self, sample: Layer):
        pass

    def clasify(self, sample: Layer):
        pass


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
    w = 0
    h = 0
    nodes = list()

    def __init__(self, w, h):
        self.w = w
        self.h = h
        return self


class SampleImage(Sample):
    def __init__(self, w, h):
        Sample.__init__(self, w, h)

    def read(self, filename):
        from PIL import Image
        im = Image.open(filename)
        pix = im.load()
        self.nodes = [[sum(pix[xp, yp]) / 255 / 3. for xp in range(self.w)] for yp in range(self.h)]
        return self

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
