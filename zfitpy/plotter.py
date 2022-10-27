"""This module provides plotting support for impedance data.

Copyright 2021 Michael Hayes, UCECE"""

from matplotlib.pyplot import subplots
from numpy import degrees, angle


class Plotter(object):

    def set_title(self, axes, title=None, model=None, sfmax=2):

        if title is None:
            if model is None:
                return axes
            title = str(model)

        if model is not None:
            if r'%rmse' in title:
                title = title.replace(r'%rmse', '%.2e' % model._rmse)
            if r'%method' in title:
                title = title.replace(r'%method', str(model._method))
            if r'%model' in title:
                title = title.replace(r'%model', model.title(sfmax=sfmax))

        axes.set_title(title)
        return axes

    def Z_error(self, data, model, axes=None, title=None):

        Z = model.Z(data.f)

        if axes is None:
            fig, axes = subplots(1)

        axes.plot(data.f, (data.Z.real - Z.real), label=data.name + ' real')
        axes.plot(data.f, (data.Z.imag - Z.imag),
                  '--', label=data.name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance error (ohms)')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Z_fit(self, data, model=None, axes=None, title=None, magphase=False):

        if model is not None:
            Z = model.Z(data.f)
        else:
            Z = None

        if axes is None:
            fig, axes = subplots(1)

        if magphase:
            ax2 = axes.twinx()

            axes.plot(data.f, abs(data.Z), label=data.name + ' data mag')
            ax2.plot(data.f, degrees(angle(data.Z)), '--',
                     label=data.name + ' data phase')
            if Z is not None:
                axes.plot(data.f, abs(Z), label=data.name + ' model mag')
                ax2.plot(data.f, degrees(angle(Z)), '--',
                         label=data.name + ' model phase')
            ax2.legend()
            ax2.set_ylabel('Impedance phase (degrees)')

        else:
            axes.plot(data.f, data.Z.real, label=data.name + ' data real')
            axes.plot(data.f, data.Z.imag, '--',
                      label=data.name + ' data imag')

            if Z is not None:
                axes.plot(data.f, Z.real, label=data.name + ' model real')
                axes.plot(data.f, Z.imag, '--',
                          label=data.name + ' model imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance (ohms)')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Z_nyquist(self, data, model=None, axes=None, title=None):

        if model is not None:
            Z = model.Z(data.f)
        else:
            Z = None

        if axes is None:
            fig, axes = subplots(1)

        axes.plot(data.Z.real, data.Z.imag, label=data.name + ' data')
        if Z is not None:
            axes.plot(Z.real, Z.imag, label=data.name + ' model')

        axes.set_xlabel('Impedance real (ohms)')
        axes.set_ylabel('Impedance imag (ohms)')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Z(self, data, axes=None, title=None):

        if axes is None:
            fig, axes = subplots(1)

        axes.plot(data.f, data.Z.real, label=data.name + ' real')
        axes.plot(data.f, data.Z.imag, '--', label=data.name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance (ohms)')
        axes.grid(True)

        self.set_title(axes, title, model=None)
        axes.legend()
        return axes

    def Z_difference(self, data1, data2, axes=None, title=None):

        if axes is None:
            fig, axes = subplots(1)

        if not (data1.f == data2.f).all():
            raise ValueError('Mismatched frequencies')

        Z1 = data1.Z
        Z2 = data2.Z
        Zdiff = Z1 - Z2

        name = '(%s - %s)' % (data1.name, data2.name)

        axes.plot(data1.f, Zdiff.real, label=name + ' real')
        axes.plot(data1.f, Zdiff.imag, '--', label=name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel('Impedance error (ohms)')
        axes.grid(True)

        self.set_title(axes, title, model=None)
        axes.legend()
        return axes
