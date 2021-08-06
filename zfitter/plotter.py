from matplotlib.pyplot import subplots

class Plotter(object):

    def Z_error(self, data, model, axes=None, title=None):

        Z = model.Z(data.f)
        
        if axes is None:
            fig, axes = subplots(1)

        axes.plot(data.f, (data.Z.real - Z.real), label=data.name + ' real')
        axes.plot(data.f, (data.Z.imag - Z.imag), '--', label=data.name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance error (ohms)')
        axes.grid(True)

        if title is None:
            title = str(model)
        axes.set_title(title)
        axes.legend()

    def Z(self, data, axes=None, title=None):
        
        if axes is None:
            fig, axes = subplots(1)

        axes.plot(data.f, data.Z.real, label=data.name + ' real')
        axes.plot(data.f, data.Z.imag, '--', label=data.name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance (ohms)')
        axes.grid(True)

        if title is None:
            title = data.name
        axes.set_title(title)
        axes.legend()        
        
            
