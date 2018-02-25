from model import Network, Configuration, Measure, SampleImage, Layer
import random, math

image_folders = ['samples/images/apples/', 'samples/images/dogs/']

with Measure("Work"):
    # configuration = Configuration(layer_sizes=[2500, 400, 2])

    # with Measure("network initializing with config: " + configuration.__str__()):
    #     net = Network(configuration)


    def read_image_samples(path, class_index):
        from os import listdir
        from os.path import isfile, join
        return [SampleImage().read(path + f).set_class(class_index) for f in listdir(path) if isfile(join(path, f))]


    with Measure("Reading samples: 'samples/images/**"):
        samples = []
        for index, folder in enumerate(image_folders):
            samples += read_image_samples(folder, index)
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
                # result = net.clasify(sample.input, activation_function=lambda x: 1 / (1 + math.exp(-x))).get_result()
                # print(sample.get_w_h())






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
