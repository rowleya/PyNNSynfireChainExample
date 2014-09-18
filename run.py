import pyNN.spiNNaker as p
import pylab

p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
nNeuronsPerCore = 10
nNeurons = 15 * 4 * nNeuronsPerCore
p.set_number_of_neurons_per_core("IF_curr_exp", nNeuronsPerCore)
p.set_number_of_neurons_per_core("DelayExtension", nNeuronsPerCore)

cell_params_lif = {
    'cm': 0.25,
    'i_offset': 0.0,
    'tau_m': 20.0,
    'tau_refrac': 2.0,
    'tau_syn_E': 5.0,
    'tau_syn_I': 5.0,
    'v_reset': -70.0,
    'v_rest': -65.0,
    'v_thresh': -50.0
    }

populations = list()
projections = list()

weight_to_spike = 2.0
delay = 10

loopConnections = list()
for i in range(0, nNeurons):
    singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, delay)
    loopConnections.append(singleConnection)

injectionConnection = [(0, 0, weight_to_spike, 1)]
spikeArray = {'spike_times': [[0]]}
populations.append(
        p.Population(nNeurons, p.IF_curr_exp, cell_params_lif, label='pop_1'))
populations.append(
        p.Population(1, p.SpikeSourceArray, spikeArray, label='inputSpikes_1'))

projections.append(p.Projection(populations[0], populations[0],
        p.FromListConnector(loopConnections)))
projections.append(p.Projection(populations[1], populations[0],
        p.FromListConnector(injectionConnection)))

populations[0].record()

p.run(10000)

spikes = populations[0].getSpikes(compatible_output=True)

pylab.figure()
pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], ".")
pylab.xlabel('Time/ms')
pylab.ylabel('spikes')
pylab.title('spikes')
pylab.savefig("synfire_spikes.pdf", format="PDF")

p.end()
