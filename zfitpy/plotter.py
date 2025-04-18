"""This module provides plotting support for impedance data.

Copyright 2021--2025 Michael Hayes, UCECE"""

from matplotlib.pyplot import subplots
from numpy import degrees, angle, pi


class Plotter:

    def __init__(self, admittance=False, logf=False):

        self.admittance = admittance
        self.logf = logf

    def _plot(self, axes):

        if self.logf:
            plot = axes.semilogx
        else:
            plot = axes.plot

        return plot

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

        title = title.replace('_', '\_')

        axes.set_title(title)
        return axes

    def Y_error(self, data, model, axes=None, title=None, percent=False):

        return self.error(data, model, axes, title, percent, admittance=True)

    def Z_error(self, data, model, axes=None, title=None, percent=False):

        return self.error(data, model, axes, title, percent, admittance=False)

    def error(self, data, model, axes=None, title=None, percent=False,
              admittance=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            label = 'Admittance'
            units = 'S'
        else:
            label = 'Impedance'
            units = 'ohms'

        mZ = model.Z(data.f)
        dZ = data.Z
        if admittance:
            mZ = 1 / mZ
            dZ = 1 / dZ

        if axes is None:
            fig, axes = subplots(1)

        plot = self._plot(axes)

        ereal = dZ.real - mZ.real
        eimag = dZ.imag - mZ.imag
        if percent:
            ereal = ereal / dZ.real * 100
            eimag = eimag / dZ.imag * 100

        plot(data.f, ereal, label=data.latex_name + ' real')
        plot(data.f, eimag, '--', label=data.latex_name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        if percent:
            axes.set_ylabel('Percent error')
        else:
            axes.set_ylabel(f'{label} error ({units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Y_data(self, data, axes=None, title=None, magphase=False):

        return self.data(data, axes, title, magphase, True)

    def Z_data(self, data, axes=None, title=None, magphase=False):

        return self.data(data, axes, title, magphase, False)

    def data(self, data, axes=None, title=None, magphase=False,
             admittance=None):

        return self.fit(data, None, axes, title, magphase, admittance)

    def Y_fit(self, data, model=None, axes=None, title=None, magphase=False):

        return self.fit(data, model, axes, title, magphase, True)

    def Z_fit(self, data, model=None, axes=None, title=None, magphase=False):

        return self.fit(data, model, axes, title, magphase, False)

    def fit(self, data, model=None, axes=None, title=None, magphase=False,
            admittance=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            label = 'Admittance'
            units = 'S'
        else:
            label = 'Impedance'
            units = 'ohms'

        if model is not None:
            mZ = model.Z(data.f)
            if admittance:
                mZ = 1 / mZ
        else:
            mZ = None

        dZ = data.Z
        if admittance:
            dZ = 1 / dZ

        if axes is None:
            fig, axes = subplots(1)

        plot = self._plot(axes)

        if magphase:
            axes2 = axes.twinx()

            plot2 = self._plot(axes2)

            plot(data.f, abs(dZ), label=data.latex_name + ' data mag')
            plot2(data.f, degrees(angle(dZ)), '--',
                  label=data.latex_name + ' data phase')
            if mZ is not None:
                plot(data.f, abs(mZ), label=data.latex_name + ' model mag')
                plot2(data.f, degrees(angle(mZ)), '--',
                      label=data.latex_name + ' model phase')
            axes2.legend()
            axes2.set_ylabel(f'{label} phase (degrees)')

        else:
            plot(data.f, dZ.real, label=data.latex_name + ' data real')
            plot(data.f, dZ.imag, '--',
                 label=data.latex_name + ' data imag')

            if mZ is not None:
                plot(data.f, mZ.real, label=data.latex_name + ' model real')
                plot(data.f, mZ.imag, '--',
                     label=data.latex_name + ' model imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{label} ({units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Y_nyquist(self, data, model=None, axes=None, title=None,
                  fmin=None, fmax=None):

        return self.nyquist(data, model, axes, title, True, fmin, fmax)

    def Z_nyquist(self, data, model=None, axes=None, title=None,
                  fmin=None, fmax=None):

        return self.nyquist(data, model, axes, title, False, fmin, fmax)

    def nyquist(self, data, model=None, axes=None, title=None,
                admittance=None, fmin=None, fmax=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            label = 'Admittance'
            units = 'S'
        else:
            label = 'Impedance'
            units = 'ohms'

        dZ = data.Z
        if admittance:
            dZ = 1 / dZ

        f = data.f
        if fmin is None:
            fmin = f[0]
        if fmax is None:
            fmax = f[-1]
        mf = (f >= fmin) & (f <= fmax)

        if model is not None:
            mZ = model.Z(f)
            if admittance:
                mZ = 1 / mZ
        else:
            mZ = None

        if axes is None:
            fig, axes = subplots(1)

        axes.plot(dZ[mf].real, dZ[mf].imag, label=data.latex_name + ' data')
        if mZ is not None:
            axes.plot(mZ[mf].real, mZ[mf].imag,
                      label=data.latex_name + ' model')

        axes.set_xlabel(f'{label} real ({units})')
        axes.set_ylabel(f'{label} imag ({units})')
        axes.grid(True)

        self.set_title(axes, title, model)
        axes.legend()
        return axes

    def Y_difference(self, data1, data2, axes=None, title=None):

        return self.difference(data1, data2, axes, title, True)

    def Z_difference(self, data1, data2, axes=None, title=None):

        return self.difference(data1, data2, axes, title, False)

    def difference(self, data1, data2, axes=None, title=None, admittance=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            label = 'Admittance'
            units = 'S'
        else:
            label = 'Impedance'
            units = 'ohms'

        dZ1 = data1.Z
        dZ2 = data2.Z
        if admittance:
            dZ1 = 1 / dZ1
            dZ2 = 1 / dZ2

        if axes is None:
            fig, axes = subplots(1)

        if not (data1.f == data2.f).all():
            raise ValueError('Mismatched frequencies')

        Zdiff = dZ1 - dZ2

        name = '(%s - %s)' % (data1.latex_name, data2.latex_name)

        axes.plot(data1.f, Zdiff.real, label=name + ' real')
        axes.plot(data1.f, Zdiff.imag, '--', label=name + ' imag')

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{label} error ({units})')
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
            Rsaxes.plot(data.f, Rs, '--', label=data.latex_name + ' data Rs')
            Rsaxes.set_ylabel('Resistance (ohm)')
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Z is not None:
            if Rsaxes is not None:
                Rs = Z.real
                Rsaxes.plot(data.f, Rs, '--', label=data.latex_name + ' model Rs')
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Lsaxes is not None:
            Ls = data.Z.imag / (2 * pi * data.f)
            Lsaxes.plot(data.f, Ls * 1e3, label=data.latex_name + ' data Ls')
            Lsaxes.set_ylabel('Inductance (mH)')

        if Z is not None:
            if Lsaxes is not None:
                Ls = Z.imag / (2 * pi * data.f)
                Lsaxes.plot(data.f, Ls * 1e3, label=data.latex_name + ' model Ls')

        axes.set_xlabel('Frequency (Hz)')
        axes.grid(True)

        self.set_title(axes, title, model)

        if Lsaxes is not None:
            Lsaxes.legend()
        if Rsaxes is not None:
            Rsaxes.legend()
        return axes
