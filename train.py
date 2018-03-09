from model import Network, Configuration, Measure, SampleImage, Layer
import random, math
import numpy

image_folders = {'samples/images/apples/': {'expected_value': numpy.array([1., 0.])},
                 'samples/images/dogs/': {'expected_value': numpy.array([0., 1.])}}

with Measure("Work"):
    # configuration = Configuration(layer_sizes=[2500, 400, 2])

    # with Measure("network initializing with config: " + configuration.__str__()):
    #     net = Network(configuration)


    def read_image_samples(path, expected_value):
        from os import listdir
        from os.path import isfile, join

        # [print(path) for f in listdir(path) if isfile(join(path, f))]
        return [SampleImage().read(path + f).set_expected_value(expected_value
        ) for f in listdir(path) if isfile(join(path, f))]


    with Measure("Reading samples: 'samples/images/**"):
        samples = []
        for folder in image_folders:
            samples += read_image_samples(folder, image_folders[folder]['expected_value'])
        random.shuffle(samples)

    with Measure("Auto scaling images"):
        sizes = []
        for sample in samples:
            sizes.append(sample.get_w_h())
        average_size = SampleImage.calculate_average_w_h(sizes)
        for sample in samples:
            sample.scale(average_size).convert_to_data()

        configuration = Configuration(layer_sizes=[average_size[0]*average_size[1],
                                                   round((average_size[0]*average_size[1]*len(image_folders))**0.25)**2,
                                                   len(image_folders)])

        print("Configuration: %s" % (configuration, ))

    with Measure("Init network"):
        net = Network(configuration)

    with Measure("Forward propagation"):
        for sample in samples:
            with Measure("clasify sample"):
                net.set_layer(sample.data)
                net.forward_propagate()
                net.error_function(sample.expected_value, len(net.Layers)-1)



        # for sample in SampleReader():
        #     net.clasify(sample, 0)

        # output_config =.
        # read_input(configuration.layer_sizes[0], path + f).set_output(Layer())
        # for f in listdir(path) if isfile(join(path, f))]
        #
        #
        # with Measure("Reading samples: 'samples/images/apples,dogs/'"):
        #     samples = read_image_samples('samples/images/apples/') + read_image_samples('samples/images/dogs/')
        # random.shuffle(samples)

        # for sample in SampleReader():
        #     net.clasify(sample, 0)
