"""This module provides plotting support for impedance data.

Copyright 2021--2025 Michael Hayes, UCECE"""

from matplotlib.pyplot import subplots
from numpy import degrees, angle, pi, linspace, log
from os.path import basename, splitext


class Plotter:

    def __init__(self, admittance=False, logf=False, axes=None):

        self.admittance = admittance
        self.logf = logf

        if axes is None:
            fig, axes = subplots(1)
        self.axes = axes

        self.filename = ''
        self.label = ''
        self.title = ''

    def _plot(self, axes):

        if self.logf:
            plot = axes.semilogx
        else:
            plot = axes.plot

        return plot

    def make_label(self, which=''):

        label = self.label
        if r'%filename' in label:
            filename = basename(self.filename)
            name, ext = splitext(filename)
            label = label.replace(r'%filename', name)

        if which != '':
            label = label + ' ' + which

        latex_name = '$\\mathrm{' + label.replace('_', '\_').replace(' ', '\ ') + '}$'
        return latex_name

    def make_title(self, model=None, sfmax=2):

        title = self.title
        if title is None:
            if model is None:
                return
            title = str(model)

        if model is not None:
            if r'%rmse' in title:
                title = title.replace(r'%rmse', '%.2e' % model._rmse)
            if r'%method' in title:
                title = title.replace(r'%method', str(model._method))
            if r'%model' in title:
                title = title.replace(r'%model', model.title(sfmax=sfmax))

        title = title.replace('_', '\_')
        return title

    def set_title(self, model=None, sfmax=2):

        title = self.make_title(model, sfmax)
        self.axes.set_title(title)

    def Y_error(self, data, model, percent=False):

        return self.error(data, model, percent, admittance=True)

    def Z_error(self, data, model, percent=False):

        return self.error(data, model, percent, admittance=False)

    def error(self, data, model, percent=False,
              admittance=None, magphase=False):

        if magphase:
            raise ValueError('TODO: error magphase')

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
            units = 'ohms'

        mZ = model.Z(data.f)
        dZ = data.Z
        if admittance:
            mZ = 1 / mZ
            dZ = 1 / dZ

        axes = self.axes

        plot = self._plot(axes)

        ereal = dZ.real - mZ.real
        eimag = dZ.imag - mZ.imag
        if percent:
            ereal = ereal / dZ.real * 100
            eimag = eimag / dZ.imag * 100

        plot(data.f, ereal, label=self.make_label('real'))
        plot(data.f, eimag, '--', label=self.make_label('imag'))

        axes.set_xlabel('Frequency (Hz)')
        if percent:
            axes.set_ylabel('Percent error')
        else:
            axes.set_ylabel(f'{ylabel} error ({units})')
        axes.grid(True)

        self.set_title(model)
        axes.legend()
        return axes

    def Y_data(self, data, magphase=False):

        return self.data(data, magphase, True)

    def Z_data(self, data, magphase=False):

        return self.data(data, magphase, False)

    def data(self, data, magphase=False,
             admittance=None):

        return self.fit(data, None, magphase, admittance)

    def Y_fit(self, data, model=None, magphase=False):

        return self.fit(data, model, magphase, True)

    def Z_fit(self, data, model=None, magphase=False):

        return self.fit(data, model, magphase, False)

    def fit(self, data, model=None, magphase=False,
            admittance=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
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

        axes = self.axes

        plot = self._plot(axes)

        if magphase:
            axes2 = axes.twinx()

            plot2 = self._plot(axes2)

            plot(data.f, abs(dZ), label=self.make_label('data mag'))
            plot2(data.f, degrees(angle(dZ)), '--',
                  label=self.make_label('data phase'))
            if mZ is not None:
                plot(data.f, abs(mZ), label=self.make_label('model mag'))
                plot2(data.f, degrees(angle(mZ)), '--',
                      label=self.make_label('model phase'))
            axes2.legend()
            axes2.set_ylabel(f'{ylabel} phase (degrees)')

        else:
            plot(data.f, dZ.real, label=self.make_label('data real'))
            plot(data.f, dZ.imag, '--',
                 label=self.make_label('data imag'))

            if mZ is not None:
                plot(data.f, mZ.real, label=self.make_label('model real'))
                plot(data.f, mZ.imag, '--',
                     label=self.make_label('model imag'))

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{ylabel} ({units})')
        axes.grid(True)

        self.set_title(model)
        axes.legend()
        return axes

    def Y_nyquist(self, data, model=None, title=None,
                  fmin=None, fmax=None):

        return self.nyquist(data, model, True, fmin, fmax)

    def Z_nyquist(self, data, model=None, title=None,
                  fmin=None, fmax=None):

        return self.nyquist(data, model, False, fmin, fmax)

    def nyquist(self, data, model=None, title=None,
                admittance=None, fmin=None, fmax=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
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

        axes = self.axes

        axes.plot(dZ[mf].real, dZ[mf].imag, label=self.make_label('data'))
        if mZ is not None:
            axes.plot(mZ[mf].real, mZ[mf].imag,
                      label=self.make_label('model'))

        axes.set_xlabel(f'{ylabel} real ({units})')
        axes.set_ylabel(f'{ylabel} imag ({units})')
        axes.grid(True)

        self.set_title(model)
        axes.legend()
        return axes

    def Y_nichols(self, data, model=None, title=None,
                  fmin=None, fmax=None):

        return self.nichols(data, model, True, fmin, fmax)

    def Z_nichols(self, data, model=None, title=None,
                  fmin=None, fmax=None):

        return self.nichols(data, model, False, fmin, fmax)

    def nichols(self, data, model=None, title=None,
                admittance=None, fmin=None, fmax=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
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

        axes = self.axes

        axes.plot(angle(dZ[mf]), log(abs(dZ[mf])),
                  label=self.make_label('data'))
        if mZ is not None:
            axes.plot(angle(mZ[mf]), log(abs(mZ[mf])),
                      label=self.make_label('model'))

        axes.set_xlabel('Phase (rad)')
        axes.set_ylabel(f'log {ylabel} (log {units})')
        axes.grid(True)

        self.set_title(model)
        axes.legend()
        return axes

    def Y_difference(self, data1, data2, title=None):

        return self.difference(data1, data2, True)

    def Z_difference(self, data1, data2, title=None):

        return self.difference(data1, data2, False)

    def difference(self, data1, data2, admittance=None):

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
            units = 'ohms'

        dZ1 = data1.Z
        dZ2 = data2.Z
        if admittance:
            dZ1 = 1 / dZ1
            dZ2 = 1 / dZ2

        axes = self.axes

        if not (data1.f == data2.f).all():
            raise ValueError('Mismatched frequencies')

        Zdiff = dZ1 - dZ2

        name = '(%s - %s)' % (data1.latex_name, data2.latex_name)

        axes.plot(data1.f, Zdiff.real, label=self.make_label('real'))
        axes.plot(data1.f, Zdiff.imag, '--', label=self.make_label('imag'))

        axes.set_xlabel('Frequency (Hz)')
        axes.set_ylabel(f'{ylabel} error ({units})')
        axes.grid(True)

        self.set_title(model=None)
        axes.legend()
        return axes

    def LsRs_fit(self, data, model=None, title=None,
                 doLs=True, doRs=True):

        if model is not None:
            Z = model.Z(data.f)
        else:
            Z = None

        axes = self.axes

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
            Rsaxes.plot(data.f, Rs, '--', label=self.make_label('data Rs'))
            Rsaxes.set_ylabel('Resistance (ohm)')
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Z is not None:
            if Rsaxes is not None:
                Rs = Z.real
                Rsaxes.plot(data.f, Rs, '--', label=self.make_label('model Rs'))
            if Lsaxes is not None:
                # Dummy plot to advance colour.
                # Lsaxes.plot([], [])
                pass

        if Lsaxes is not None:
            Ls = data.Z.imag / (2 * pi * data.f)
            Lsaxes.plot(data.f, Ls * 1e3, label=self.make_label('data Ls'))
            Lsaxes.set_ylabel('Inductance (mH)')

        if Z is not None:
            if Lsaxes is not None:
                Ls = Z.imag / (2 * pi * data.f)
                Lsaxes.plot(data.f, Ls * 1e3, label=self.make_label('model Ls'))

        axes.set_xlabel('Frequency (Hz)')
        axes.grid(True)

        self.set_title(model)

        if Lsaxes is not None:
            Lsaxes.legend()
        if Rsaxes is not None:
            Rsaxes.legend()
        return axes


    def Y_slice(self, model=None, data=None, paramname=None, axes=None,
                title=None):

        return self.slice(model, data, paramname, True)

    def Z_slice(self, model=None, data=None, paramname=None, axes=None,
                title=None):

        return self.slice(model, data, paramname, False)

    def slice(self, model=None, data=None, paramname=None,
              admittance=None):

        if paramname not in model.paramnames:
            s = ', '.join(model.paramnames)
            raise ValueError(f'Unknown param {paramname}.  Known params {s}')

        ranges = model._ranges
        rmin = ranges[paramname][0]
        rmax = ranges[paramname][1]

        index = model.paramnames.index(paramname)
        params = model.params

        x = linspace(rmin, rmax, 200)
        rmse = x * 0

        Model = model.__class__

        if admittance is None:
            admittance = self.admittance

        if admittance:
            ylabel = 'Admittance'
            units = 'S'
        else:
            ylabel = 'Impedance'
            units = 'ohms'

        if admittance:
            for m, x1 in enumerate(x):
                params[index] = x1
                model1 = Model(*params)
                rmse[m] = model1.Yrmse(data.f, data.Y)
        else:
            for m, x1 in enumerate(x):
                params[index] = x1
                model1 = Model(*params)
                rmse[m] = model1.Zrmse(data.f, data.Z)

        axes = self.axes

        axes.plot(x, rmse)
        axes.set_xlabel('$' + paramname + '$')
        axes.set_ylabel(f'{ylabel} rmse ({units})')

        axes.grid(True)

        self.set_title(model)
        return axes
