class VerilogModel(object):
    """"
    Builds a Verilo g
    """

    _modulename = None
    _ports = []
        #port dictionary, {'name', 'direction', 'width', 'Description'}

    def __init__(self, modulename=None):
        """

        :param modulename:
        """
        if not modulename:
            print("Module Name is missing. ")
        else:
            self._modulename = modulename

    def push_input_port(self, signaltuple):
        print("Signal Tuple, {}".format(signaltuple))
        #self._ports.append(signaltuple)

    def parseInterfaceTable(self, itable):
        """
        Parse and process interface table
        :param itable:
        :return:
        """
        
