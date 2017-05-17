import time
import logging
import os
import psutil


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
        process = psutil.Process(os.getpid())
        self.mem = process.memory_info().rss
        self.time = time.time()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('octolith')
        self.logger.info(' Starting ' + self.message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        process = psutil.Process(os.getpid())
        self.logger.info(' Finished ' + self.message)
        self.logger.info('Time consumed: %s sec, Memory consumed: %s MB', round(time.time() - self.time, 2),
                         round((process.memory_info().rss - self.mem) / 1024 / 1024, 2))


class SampleReader:
    pass
