from lcapy import f
import numpy as np

def build(net):
    
    Z = net.Z(f)

    paramnames = Z.symbols
    paramnames.pop('f')
    
    Zcodestr = str(Z)
    for p in paramnames:
        Zcodestr = Zcodestr.replace(p, 'self.' + p)
    Zcode = compile(Zcodestr, 'foo', 'eval')

    return net, Zcode


class Bar:

    def draw(self):

        self.net.draw()
    
    def Z(self, f):
        j = 1j
        pi = np.pi
        
        return eval(self.Zcode)
    
    def Y(self, f):

        return 1 / self.Z(f)
    
