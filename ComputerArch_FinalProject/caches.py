
# Kurtis: Added eviction policy parameter to Cache class.
# Peter: Added block size handling for L1ICache and L1DCache.
# Audrey: Extended associativity control to L1DCache and L2Cache.
from m5.objects import Cache

# Pretty sure L1Cache class is not used, ignore for now unless needed. (L1I and L1D classes are used)
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def connectCPU(self, cpu):
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# L1I Cache Parameters
class L1ICache(L1Cache):
    def __init__(self, options=None):
        super(L1ICache, self).__init__()
        self.size = options.l1i_size if options and options.l1i_size else '16kB'
        self.block_size = options.l1i_block_size if options and options.l1i_block_size else 64  # Default block size
        self.assoc = options.l1i_assoc if options and options.l1i_assoc else 2 

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

# L1D Cache Parameters
class L1DCache(L1Cache):
    def __init__(self, options=None):
        super(L1DCache, self).__init__()
        self.size = options.l1d_size if options and options.l1d_size else '64kB'
        self.block_size = options.l1d_block_size if options and options.l1_block_size else 64  # Default block size
        self.assoc = options.l1d_assoc if options and options.l1d_assoc else 2  # Default associativity

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

# Add eviction policy handling
class Cache(m5.objects.Cache):
    def __init__(self, options=None):
        super(Cache, self).__init__()
        if options and options.eviction_policy:
            self.eviction_policy = options.eviction_policy
        else:
            self.eviction_policy = 'random'  

# L2 Cache Parameters
class L2Cache(Cache):
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        self.size = options.l2_size if options and options.l2_size else '256kB'
        self.assoc = options.l2_assoc if options and options.l2_assoc else 8  # Default associativity
        self.block_size = options.l2_block_size if options and options.l2_block_size else 64  # Default block size

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
