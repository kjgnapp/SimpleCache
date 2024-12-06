
import argparse
import m5
from m5.objects import *
from caches import *  # Import the caches module

# Argument parser setup
# Tyler: Cache size handled via command-line arguments.
# Audrey: Associativity handled in the caches classes and passed via arguments.
# Peter: Block size parameter added for both L1 and L2 caches.
# Kurtis: Eviction policy parameter added for cache customization.

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')

# Tyler: Cache size handled via command-line arguments.
parser.add_argument("--l1i_size", default="16kB", help="L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", default="64kB", help="L1 data cache size. Default: 64kB.")
parser.add_argument("--l2_size", default="256kB", help="L2 cache size. Default: 256kB.")

# Audrey: Associativity handled in the caches classes and passed via arguments.
parser.add_argument("--l1i_assoc", type=int, default=2, help="L1 instruction cache associativity. Default: 2.")
parser.add_argument("--l1d_assoc", type=int, default=2, help="L1 data cache associativity. Default: 2.")
parser.add_argument("--l2_assoc", type=int, default=8, help="L2 cache associativity. Default: 8.")

# Peter: Block size parameter added for both L1I/L1D and L2 caches.
parser.add_argument("--block_size", type=int, default=64, help="Block size for L1 instruction cache in bytes. Default: 64.")

# Kurtis: Eviction policy parameter added for cache customization.
parser.add_argument("--eviction_policy", default="random", choices=["random", "lru", "fifo"],
                    help="Eviction policy for caches. Default: random.")
options = parser.parse_args()

# Create the system we are going to simulate
system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]
system.cpu = X86TimingSimpleCPU()

system.cache_line_size = options.block_size

# Set up caches with specified sizes and parameters
system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)
system.l2cache = L2Cache(options)

# Continue with the rest of the code to connect components
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Set up the workload to be a simple 'Hello World' program in SE mode
binary = 'configs/Lab1/matmult'
system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate and start the simulation
root = Root(full_system=False, system=system)
m5.instantiate()
print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
