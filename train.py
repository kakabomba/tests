from model import Network, Configuration, Measure, SampleImage, Layer
import random, math

with Measure("Work"):
    configuration = Configuration(layer_sizes=[[50, 50], [20, 20], [1, 2]])

    with Measure("network initializing with config: " + configuration.__str__()):
        net = Network(configuration)


    def read_image_samples(path, apple_dog):
        from os import listdir
        from os.path import isfile, join
        return [SampleImage().
                    read_input(configuration.layer_sizes[0], path + f).
                    copy_output([[0, 1] if apple_dog else [1, 0]]) for f in listdir(path) if isfile(join(path, f))]


    with Measure("Reading samples: 'samples/images/apples,dogs/'"):
        samples = read_image_samples('samples/images/apples/', True) + read_image_samples('samples/images/dogs/', False)
        random.shuffle(samples)


    for sample in samples:
        with Measure("clasify sample"):
            result = net.clasify(sample.input, activation_function=lambda x: 1 / (1 + math.exp(-x))).get_result()
            print(result)






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
