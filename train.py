from model import Network, Configuration, Measure, SampleReader

configuration = Configuration()

with Measure("network initializing with config: " + configuration.__str__()):
    net = Network(Configuration())

for sample, output in SampleReader():
    net.train(sample, output)

for sample in SampleReader():
    net.clasify(sample, output)

