from pyNN.utility import get_script_args

simulator_name = get_script_args(1)[0]
exec("import pyNN.%s as p" % simulator_name)

import pylab

p.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
nNeuronsPerCore = 10
nNeurons = 15 * 4 * nNeuronsPerCore

if simulator_name == "spiNNaker":
    p.set_number_of_neurons_per_core("IF_curr_exp", nNeuronsPerCore)

# Synfire Cell parameters
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

# Input Parameters
spikeArray = {'spike_times': [[0]]}

# Connection Parameters
weight_to_spike = 2.0
delay = 2
loopConnections = list()
for i in range(0, nNeurons):
    singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, delay)
    loopConnections.append(singleConnection)
injectionConnection = [(0, 0, weight_to_spike, 1)]

# Setup Populations
synfire_population = p.Population(nNeurons, p.IF_curr_exp, cell_params_lif,
        label='loop')
input_population = p.Population(1, p.SpikeSourceArray, spikeArray,
        label='input')

# Setup Projections
synfire_projection = p.Projection(synfire_population, synfire_population,
        p.FromListConnector(loopConnections))
input_projection = p.Projection(input_population, synfire_population,
        p.FromListConnector(injectionConnection))

# Record and run
synfire_population.record()
p.run(3000)

# Get and plot spikes
spikes = synfire_population.getSpikes(compatible_output=True)
pylab.figure()
pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], ".")
pylab.xlabel('Time/ms')
pylab.ylabel('spikes')
pylab.title('spikes')
pylab.savefig("synfire_spikes.pdf", format="PDF")

# End the Simulation
p.end()
