from model import Network, Configuration, Measure, SampleImage

with Measure("Work"):

    configuration = Configuration()

    with Measure("network initializing with config: " + configuration.__str__()):
        net = Network(configuration)

    def read_image_samples(path):
        from os import listdir
        from os.path import isfile, join
        return [SampleImage(*configuration.layer_sizes[0]).read(path + f) for f in listdir(path) if isfile(join(path, f))]

    with Measure("Reading samples: 'samples/images/apples,dogs/'"):
        apples = read_image_samples('samples/images/apples/')
        dogs = read_image_samples('samples/images/dogs/')


# for sample in SampleReader():
#     net.clasify(sample, 0)

