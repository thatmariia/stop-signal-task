from psychopy import parallel


class ParallelPorts:
    """
    The ParallelPorts class is responsible for configuring the parallel ports.
    """

    def __init__(self):
        # Write address EEG ports
        self.use = None

        self.write_address = None
        self.port_write = None
        self.read_address = None
        self.port_read = None

    def startup(
            self,
            use=True,
            write_address=0x4050,
            read_address=0x4051
    ):
        """
        Initialize the parallel ports.

        :param use: whether to use the parallel ports (default: True)
        :param write_address: write address of the parallel port (default: 0x4050)
        """

        # Write address EEG ports
        self.use = use

        if self.use:
            self.write_address = write_address
            self.read_address = read_address
            self.port_write = parallel.ParallelPort(address=self.write_address)
            self.port_read = parallel.ParallelPort(address=self.read_address)
