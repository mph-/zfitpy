from lcapy import f, R, C, L, CPE
import numpy as np

models = {}

def modelmake(name, net, paramnames=None):

    if isinstance(net, str):
        net = eval(net)
    
    if paramnames is None:
        Z = eval('(%s).Z(f)' % net)
        paramnames = Z.symbols
        paramnames.pop('f')
    
    params = ', '.join(paramnames)
    
    docstring = name + '(' + params + '): ' + str(net)
    newclass = type(name, (Model, ), {'__doc__': docstring})
    newclass.net = net
    newclass.paramnames = paramnames
    models[name] = newclass
    return newclass


class Model(object):

    Zcode = None

    def __init__(self, *args):
        """Create model instance."""

        if len(args) == 0:
            return
        
        for m, p in enumerate(self.paramnames):
            setattr(self, p, args[m])
    
    def __repr__(self):
        return self.__str__()

    def __call__(self, i, t):

        return self.v(i, t)

    def v(self, i, t):        

        h, d, dd = self.zimpulse(t - t[0])

        v = 0
        if not h is 0:
            dt = t[1] - t[0]
            v = v + np.convolve(i, h, mode='full')[0:len(t)] * dt

        if not d is 0:
            v = v + d * i

        if not dd is 0:

            if False:
                I = np.fft.rfft(i)
                dt = t[1] - t[0]            
                f = np.fft.rfftfreq(len(i), dt)
                didt = np.fft.irfft(I * 2j * np.pi * f)
                v = v + dd * didt                
            else:
                if True:
                    # Central differences
                    didt = np.gradient(i, t)
                else:
                    dt = t[1] - t[0]                                
                    didt = np.diff(i, append=0) / dt
                v = v + dd * didt

        return v
    
    def i(self, v, t):

        h, d, dd = self.yimpulse(t - t[0])

        i = 0
        if not h is 0:
            dt = t[1] - t[0]
            i = i + np.convolve(v, h, mode='full')[0:len(t)] * dt

        if not d is 0:
            i = i + d * v

        if not dd is 0:
            dvdt = np.gradient(v, t)
            i = i + dd * dvdt

        return i

    def zimpulse(self, t):    

        raise ValueError('Method zimpulse not defined for %s' % self.__class__.__name__)

    def yimpulse(self, t):    

        raise ValueError('Method yimpulse not defined for %s' % self.__class__.__name__)    


    def draw(self, filename=None):

        self.net.draw(filename)

    def _Zbuild(self):
    
        Z = self.net.Z(f)
        
        paramnames = Z.symbols
        paramnames.pop('f')
        
        Zcodestr = str(Z)
        for p in paramnames:
            Zcodestr = Zcodestr.replace(p, 'self.' + p)
        Zcode = compile(Zcodestr, 'Z', 'eval')

        return Zcode
        
    def Z(self, f):
        """Return impedance at frequency `f`; `f` can be an ndarray."""

        if self.Zcode is None:
            # Cache result for class
            self.__class__.Zcode = self._Zbuild()
        
        j = 1j
        pi = np.pi
        
        return eval(self.Zcode)
    
    def Y(self, f):
        """Return admittance at frequency `f`; `f` can be an ndarray."""        

        return 1 / self.Z(f)

    def __str__(self):

        parts = []
        for var, val in vars(self).items():
            units = {'R': ' ohms', 'C': ' F', 'L': ' H', 'K':'', 'a':''}[var[0]]

            # Could convert units to have SI prefixes
            parts.append('%s=%.2e%s' % (var, val, units))

        return ', '.join(parts)
