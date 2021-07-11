import argparse
import logging, json
import datetime, time, os, sys, shutil
import inspect
from docx2python import docx2python
from docx2csv import extract_tables, extract
from SystemVerilogModel import VerilogModel

class SpecModel(object):
    """"
    classdocs
    """

    staticdir = None
    serverstart = 0

    interfacetable = ['Signal Name', 'Direction', 'Description']

    def __init__(self, staticdir=None, spec=None, modulename=None):
        """

        :param staticdir:
        :param spec:
        """
        if os.path.exists(spec):
            #self.dmodel = docx2python(spec)
            self.tables = extract_tables(spec)
            intftbl = self.extractInterfaceTable()
            print("Interfacce Table: {}".format(intftbl))
            self.vmodel = VerilogModel(modulename=modulename)

        else:
            print("Specification Document does not exist, {}".format(spec))

    def extractInterfaceTable(self):
        """
        :return:
        """
        intftbl = None
        for tbl in self.tables:
            header_match = 0
            logging.info("Parsing table header: {}".format(tbl[0]))
            for idx, thdr in enumerate(tbl[0]):
                tcell = thdr.decode('utf-8')
                if tcell == self.interfacetable[idx]:
                    header_match += 1
            if header_match == len(self.interfacetable):
                print("Header Found: {}".format(self.interfacetable))
                intftbl = tbl
                break

        return intftbl

    def writeVerilog(self, vfile=None, modulename=None):
        """
        Writes the Verilog Model
        :param vfile:
        :param modulename:
        :return:
        """
        vlog = VerilogModel(modulename=modulename)



## main code section
if __name__ == '__main__':
    cascPath = os.path.abspath(os.getcwd())
    port = 9005
    www = os.path.join(os.getcwd(), 'ui_www_classis')
    ipaddr = '127.0.0.1'
    dbip = '127.0.0.1'
    logpath = os.path.join(os.getcwd(), 'log', 'openhdl.log')
    logdir = os.path.dirname(logpath)

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port", required=False, default=port,
                help="Port number to start HTTPServer." )

    ap.add_argument("-i", "--ipaddress", required=False, default='127.0.0.1',
                help="IP Address to start HTTPServer")

    ap.add_argument("-s", "--static", required=False, default=www,
                help="Static directory where WWW files are present")

    ap.add_argument("-d", "--dbaddress", required=False, default=dbip,
                    help="Database (MongoDB) IP address, defaults to %s" % (dbip))

    ap.add_argument("-f", "--logfile", required=False, default=logpath,
                    help="Directory where application logs shall be stored, defaults to %s" % (logpath) )
    modulename = "ipmodule"
    ap.add_argument("-m", "--module", required=False, default="{}".format(modulename),
                    help="Module name to be used for code-generation, defaults to %s" % (modulename))

    if not os.path.exists(logdir):
        print("Log directory does not exist, creating %s" % (logdir))
        os.makedirs(logdir)

    logging.basicConfig(filename=logpath, level=logging.DEBUG, format='%(asctime)s %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    logging.getLogger().addHandler(handler)

    ##Handle Agrs
    args = vars(ap.parse_args())
    if args['logfile']:
        logpath = os.path.abspath(args['logfile'])

    if args['module']:
        modulename = args['module']

    docx = os.path.join(os.getcwd(), 'sample', 'Example-Core1.docx')
    spec = SpecModel(spec=docx, modulename=modulename)
