"""This module provides plotting support for impedance data.

Copyright 2021 Michael Hayes, UCECE"""

from matplotlib.pyplot import subplots
from numpy import degrees, angle, pi


class Plotter:

    def __init__(self, admittance=False, logf=False):

        self.admittance = admittance
        self.logf = logf

        if self.admittance:
            self.label = 'Admittance'
            self.units = 'siemens'
        else:
            self.label = 'Impedance'
            self.units = 'ohms'

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

    def error(self, data, model, axes=None, title=None):

        mZ = model.Z(data.f)
        dZ = data.Z
        if self.admittance:
            mZ = 1 / mZ
            dZ = 1 / dZ

        if axes is None:
            fig, axes = subplots(1)

        if self.logf:
            plot = axes.semilogx
        else:
            plot = axes.plot

        plot(data.f, (dZ.real - mZ.real), label=data.name + ' real')
        plot(data.f, (dZ.imag - mZ.imag),
             '--', label=data.name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{self.label} error ({self.units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def data(self, data, axes=None, title=None, magphase=False):

        self.fit(data, None, axes, title, magphase)

    def fit(self, data, model=None, axes=None, title=None, magphase=False):

        if model is not None:
            mZ = model.Z(data.f)
            if self.admittance:
                mZ = 1 / mZ
        else:
            mZ = None

        dZ = data.Z
        if self.admittance:
            dZ = 1 / dZ

        if axes is None:
            fig, axes = subplots(1)

        if self.logf:
            plot = axes.semilogx
        else:
            plot = axes.plot

        if magphase:
            axes2 = axes.twinx()

            if self.logf:
                plot2 = axes2.semilogx
            else:
                plot2 = axes2.plot

            plot(data.f, abs(dZ), label=data.name + ' data mag')
            plot2(data.f, degrees(angle(dZ)), '--',
                  label=data.name + ' data phase')
            if mZ is not None:
                plot(data.f, abs(mZ), label=data.name + ' model mag')
                plot2(data.f, degrees(angle(mZ)), '--',
                      label=data.name + ' model phase')
            axes2.legend()
            axes2.set_ylabel(f'{self.label} phase (degrees)')

        else:
            plot(data.f, dZ.real, label=data.name + ' data real')
            plot(data.f, dZ.imag, '--',
                 label=data.name + ' data imag')

            if mZ is not None:
                plot(data.f, mZ.real, label=data.name + ' model real')
                plot(data.f, mZ.imag, '--',
                     label=data.name + ' model imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{self.label} ({self.units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def nyquist(self, data, model=None, axes=None, title=None):

        dZ = data.Z
        if self.admittance:
            dZ = 1 / dZ

        if model is not None:
            mZ = model.Z(data.f)
            if self.admittance:
                mZ = 1 / mZ
        else:
            mZ = None

        if axes is None:
            fig, axes = subplots(1)

        axes.plot(dZ.real, dZ.imag, label=data.name + ' data')
        if mZ is not None:
            axes.plot(mZ.real, mZ.imag, label=data.name + ' model')

        axes.set_xlabel(f'{self.label} real ({self.units})')
        axes.set_ylabel(f'{self.label} imag ({self.units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def difference(self, data1, data2, axes=None, title=None):

        dZ1 = data1.Z
        dZ2 = data2.Z
        if self.admittance:
            dZ1 = 1 / dZ1
            dZ2 = 1 / dZ2

        if axes is None:
            fig, axes = subplots(1)

        if not (data1.f == data2.f).all():
            raise ValueError('Mismatched frequencies')

        Zdiff = dZ1 - dZ2

        name = '(%s - %s)' % (data1.name, data2.name)

        axes.plot(data1.f, Zdiff.real, label=name + ' real')
        axes.plot(data1.f, Zdiff.imag, '--', label=name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{self.label} error ({self.units})')
        axes.grid(True)

        self.set_title(axes, title, model=None)
        axes.legend()
        return axes

    def LsRs_fit(self, data, model=None, axes=None, title=None,
                 doLs=True, doRs=True):

        if model is not None:
            Z = model.Z(data.f)
        else:
            Z = None

        if axes is None:
            fig, axes = subplots(1)

        if doLs and doRs:
            Lsaxes = axes

            # Handle multiple calls with specified axes
            if not hasattr(axes, '_twinx'):
                axes._twinx = axes.twinx()

            Rsaxes = axes._twinx
        elif doLs:
            Lsaxes = axes
            Rsaxes = None
        else:
            Rsaxes = axes
            Lsaxes = None

        if Rsaxes is not None:
            Rs = data.Z.real
            Rsaxes.plot(data.f, Rs, '--', label=data.name + ' data Rs')
            Rsaxes.set_ylabel('Resistance (ohm)')
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Z is not None:
            if Rsaxes is not None:
                Rs = Z.real
                Rsaxes.plot(data.f, Rs, '--', label=data.name + ' model Rs')
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Lsaxes is not None:
            Ls = data.Z.imag / (2 * pi * data.f)
            Lsaxes.plot(data.f, Ls * 1e3, label=data.name + ' data Ls')
            Lsaxes.set_ylabel('Inductance (mH)')

        if Z is not None:
            if Lsaxes is not None:
                Ls = Z.imag / (2 * pi * data.f)
                Lsaxes.plot(data.f, Ls * 1e3, label=data.name + ' model Ls')

        axes.set_xlabel('Frequency (Hz)')
        axes.grid(True)

        self.set_title(axes, title, model)

        if Lsaxes is not None:
            Lsaxes.legend()
        if Rsaxes is not None:
            Rsaxes.legend()
        return axes
