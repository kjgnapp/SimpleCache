import m5
from m5.objects import Cache, RandomRP, LRURP, MRURP, FIFORP

# General L1 Cache Template (Base Class for L1I and L1D Caches)
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def connectCPU(self, cpu):
        raise NotImplementedError  # To be implemented by L1I or L1D cache classes

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# L1 Instruction Cache (L1I)
class L1ICache(L1Cache):
    def __init__(self, options=None):
        super(L1ICache, self).__init__()
        self.size = options.l1i_size if options and options.l1i_size else '16kB'
        # self.block_size = options.l1i_block_size if options and options.l1i_block_size else 64  # Default block size
        self.assoc = options.l1i_assoc if options and options.l1i_assoc else 2  # Default associativity

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

# L1 Data Cache (L1D)
class L1DCache(L1Cache):
    def __init__(self, options=None):
        super(L1DCache, self).__init__()
        self.size = options.l1d_size if options and options.l1d_size else '64kB'
        # self.block_size = options.l1d_block_size if options and options.l1d_block_size else 64  # Default block size
        self.assoc = options.l1d_assoc if options and options.l1d_assoc else 2  # Default associativity

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

# General Cache Class with Eviction Policy Support
class CustomCache(m5.objects.Cache):
    def __init__(self, options=None):
        super(CustomCache, self).__init__()
        # Set the replacement policy based on the options
        if options and options.eviction_policy:
            if options.eviction_policy == 'random':
                self.replacement_policy = RandomRP()
            elif options.eviction_policy == 'lru':
                self.replacement_policy = LRURP()
            elif options.eviction_policy == 'fifo':
                self.replacement_policy = FIFORP()
            else:
                raise ValueError(f"Unsupported eviction policy: {options.eviction_policy}")
        else:
            self.replacement_policy = RandomRP()  # Default is random

# L2 Cache
class L2Cache(CustomCache):
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(L2Cache, self).__init__()
        self.size = options.l2_size if options and options.l2_size else '256kB'
        # self.block_size = options.l2_block_size if options and options.l2_block_size else 64  # Default block size
        self.assoc = options.l2_assoc if options and options.l2_assoc else 8  # Default associativity

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports
