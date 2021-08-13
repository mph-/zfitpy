from lcapy import *
import numpy as np

class Foo:

    net = R('R1') + L('L1')

    Z = net.Z(f)

    p = ('R1', 'L1')

    codestr = 'j = 1j; pi = np.pi; ' + str(Z)
    for param in p:
        codestr = codestr.replace(param, 'self.' + param)

    code = compile(codestr, 'foo', 'single')
    

    def __init__(self, R1, L1):

        self.R1 = R1
        self.L1 = L1

    
    def Z(self, f):

        return eval(self.code)
    
