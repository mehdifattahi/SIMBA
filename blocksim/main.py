import time
import csv
from json import dumps as dump_json
from blocksim.world import SimulationWorld
from blocksim.node_factory import NodeFactory
from blocksim.transaction_factory import TransactionFactory
from blocksim.models.network import Network

def write_report(world):
    report_directory = 'report/'
    with open(report_directory + 'report.json', 'w') as f:
        f.write(dump_json(world.env.data))
    with open(report_directory + 'propagation-time.csv', 'w') as f:
        f.write('connection, count, sum, average\n')
        for connection in world.env.data['block_propagation']:
            propagation_values = world.env.data['block_propagation'][connection]
            if len(propagation_values) > 0:
                sum = 0
                for i in propagation_values:
                    sum = + propagation_values[i]
                avg = sum / len(propagation_values)
                f.write(connection + ', ' + str(len(propagation_values)) + ', ' + str(sum) + ', ' + str(avg) + '\n')
        # f.write(dump_json(world.env.data['block_propagation']))

    vf_node = {}
    with open(report_directory + 'block-verification-time.csv', 'w') as f:
        # f.write(str(world.report_verification_time()))
        writer = csv.writer(f)
        for block_vf in world.report_verification_time():
            split = block_vf.split(':')
            writer.writerow([split[1]])
            if split[0] in vf_node:
                value = vf_node[split[0]]
                split_value = value.split(',')
                split_value[0] = str(int(split_value[0]) + 1)
                split_value[1] = str(float(split[1]) + float(split_value[1]))
                split_value[2] = str(float(split_value[1]) / float(split_value[0]))
                vf_node[split[0]] = split_value[0] + ', ' + split_value[1] + ', ' + split_value[2]
            else:
                vf_node[split[0]] = '1, ' + split[1] + ', ' + split[1]
    with open(report_directory + 'node-verification-time-average.csv', 'w') as f:
        f.write('node, count, sum, average\n')
        for block_vf in vf_node:
            f.write(block_vf + ', ' + vf_node[block_vf] + '\n')
            # writer.writerow([block_vf + ', ' + vf_node[block_vf]])


def report_node_chain(world, nodes_list):
    for node in nodes_list:
        head = node.chain.head
        chain_list = []
        num_blocks = 0
        for i in range(head.header.number):
            b = node.chain.get_block_by_number(i)
            chain_list.append(str(b.header))
            num_blocks += 1
        chain_list.append(str(head.header))
        key = f'{node.address}_chain'
        world.env.data[key] = {
            'head_block_hash': f'{head.header.hash[:8]} #{head.header.number}',
            'number_of_blocks': num_blocks,
            'chain_list': chain_list
        }


def run_model():
    now = int(time.time())  # Current time
    duration = 400  # seconds
    verification_mode = "WithMerkle"
    # verification_mode = "WithoutMerkle"

    world = SimulationWorld(
        verification_mode,
        duration,
        now,
        '../input-parameters/config.json',
        '../input-parameters/latency.json',
        '../input-parameters/throughput-received.json',
        '../input-parameters/throughput-sent.json',
        '../input-parameters/delays.json')

    # Create the network
    network = Network(world.env, 'NetworkXPTO')

    miners = {
        'USA': {
            'how_many': 4,
            'mega_hashrate_range': "(20, 40)"
        },
        'Japan': {
            'how_many': 2,
            'mega_hashrate_range': "(20, 40)"
        },
        'Canada': {
            'how_many': 8,
            'mega_hashrate_range': "(20, 40)"
        }
    }
    non_miners = {
        'Japan': {
            'how_many': 1
        },
        'Canada': {
            'how_many': 10
        },
        'Ireland': {
            'how_many': 1
        }
    }

    node_factory = NodeFactory(world, network)
    # Create all nodes
    nodes_list = node_factory.create_nodes(miners, non_miners)
    # Start the network heartbeat
    world.env.process(network.start_heartbeat())
    # Full Connect all nodes
    for node in nodes_list:
        node.verification_mode = verification_mode
        node.connect(nodes_list)

    transaction_factory = TransactionFactory(world)
    transaction_factory.broadcast(100, 40, 15, nodes_list)
    # transaction_factory.broadcast(5000, 4000, 15, nodes_list)

    world.start_simulation()

    report_node_chain(world, nodes_list)
    write_report(world)


if __name__ == '__main__':
    run_model()
