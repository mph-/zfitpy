#!/usr/bin/python3
"""zfitpy V0.6.1
Copyright (c) 2021--2025 Michael P. Hayes, UC ECE, NZ

Usage:

Here are some examples:

zfitpy --net net --draw
zfitpy --input data.csv --plot-data --output data.pdf
zfitpy --input data.csv --plot-fit --net net --ranges ranges --show
zfitpy --input data.csv --plot-error --net net --ranges ranges --show
zfitpy --input data.csv --plot-data --nyquist --plot_admittance --show
zfitpy --input data1.csv data2.csv --plot-data --nyquist --plot_admittance --show
zfitpy --net net --laplace
"""

from __future__ import print_function
from matplotlib.pyplot import show, savefig, style
from argparse import ArgumentParser, FileType
from zfitpy.model import models, modelmake
from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
import sys


# Plot types: real-imag, mag-phase, Ls-Rs, Cp-Gp, Nyquist, Nichols
# Plot formats: data, model, fit, error
# Plot data: impedance, admittance

def zfitpy_exception(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # We are not in interactive mode or we don't have a tty-like
        # device, so call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback
        import pdb
        # We are in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print()
        # ...then start the debugger in post-mortem mode.
        pdb.pm()


def model_make(args):

    if not args.net and not args.modelname:
        raise ValueError(
            'Either need to specify model name with --modelname or network with --net')

    if args.net:
        net = args.net
        if net.endswith('.net'):
            net = open(net).read()

        Model = modelmake('Model', net)

    if args.modelname:
        try:
            Model = models[args.modelname]
        except:
            modelnames = ', '.join(list(models.keys()))
            raise ValueError('Unknown model %s: known models: %s' %
                             (args.modelname, modelnames))

    return Model


def doit(filename, label, plotter, plot_type, plot_format, args):

    # TODO: tidy
    plotter.filename = filename
    plotter.label = label
    plotter.title = args.title

    data = impedancedata(filename,
                         fmin=args.fmin, fmax=args.fmax,
                         conjugate=args.conjugate,
                         admittance=args.data_admittance,
                         magphase=args.data_magphase)

    if args.fitfmin is not None or args.fitfmax is not None:

        if args.fitfmin is None:
            args.fitfmin = args.fmin
        if args.fitfmax is None:
            args.fitfmax = args.fmax

        fitdata = impedancedata(filename,
                                fmin=args.fitfmin, fmax=args.fitfmax,
                                conjugate=args.conjugate,
                                admittance=args.data_admittance,
                                magphase=args.data_magphase)
    else:
        fitdata = data

    if args.Zoffset != 0:
        data.Z += args.Zoffset

    if False and args.ranges is None:
        raise ValueError('Search ranges not specified')

    if args.ranges is None:
        fitmodel = None
    else:

        ranges = args.ranges
        if ranges.endswith('.ranges'):
            ranges = open(ranges).read()

        Model = model_make(args)
        zfitter = ZFitter(Model, fitdata.f, fitdata.Z)
        opt = 'Y' if args.fit_admittance else 'Z'
        fitmodel = zfitter(ranges=ranges, Ns=args.steps, opt=opt,
                           method=args.method, verbose=args.verbose,
                           finish=args.finish)
        if args.error:
            print('error=%.3e' % fitmodel.error)
        if args.defs:
            print(fitmodel.defs(args.sigfigs))
        if args.values:
            print(fitmodel)
        if not (args.error or args.defs or args.values):
            print('%s, error=%.3e' % (fitmodel, fitmodel.error))

    if plot_format is None:
        plot_format = 'fit' if fitmodel else 'data'

    if not fitmodel and plot_format in ('error', 'fit', 'model'):
        raise ValueError('Model not specified for plot')

    if plot_format not in ('data', 'model', 'fit', 'error'):
        raise ValueError(f'Unknown plot_format {plot_format}')

    if plot_type in ('real-imag', 'mag-phase'):
        if plot_format == 'error':
            plotter.error(data, fitmodel,
                          percent=args.percent,
                          magphase=plot_type=='mag-phase')
        elif plot_format == 'model':
            plotter.fit(None, fitmodel,
                        magphase=plot_type=='mag-phase')
        elif plot_format == 'fit':
            plotter.fit(data, fitmodel,
                        magphase=plot_type=='mag-phase')
        elif plot_format == 'data':
            plotter.fit(data, None,
                        magphase=plot_type=='mag-phase')

    elif plot_type == 'nyquist':
        plotter.nyquist(data, fitmodel, fmin=args.fmin,
                        fmax=args.fmax)
    elif plot_type == 'nichols':
        plotter.nichols(data, fitmodel, fmin=args.fmin,
                        fmax=args.fmax)
    elif plot_type == 'Ls-Rs':
        plotter.LsRs_fit(data, fitmodel, doLs=True, doRs=True)
    elif plot_type == 'Ls':
        plotter.LsRs_fit(data, fitmodel, doLs=True, doRs=False)
    elif plot_type == 'Rs':
        plotter.LsRs_fit(data, fitmodel, doLs=False, doRs=True)
    elif plot_type == 'Cp-Gp':
        plotter.CpGp_fit(data, fitmodel, doCp=True, doGp=True)
    elif plot_type == 'Cp':
        plotter.CpGp_fit(data, fitmodel, doCp=True, doGp=False)
    elif plot_type == 'Gp':
        plotter.CpGp_fit(data, fitmodel, doCp=False, doGp=True)
    elif plot_type == 'slice':
        plotter.slice(fitmodel, data, args.slice)
    else:
        raise ValueError(f'Unknown plot_type {plot_type}')


def main():

    parser = ArgumentParser(description='Draw schematic of impedance model.')
    parser.add_argument('--version', action='version',
                        version=__doc__.split('\n')[0])
    parser.add_argument('--modelname', type=str, help='model name')
    parser.add_argument('--net', type=str,
                        help="specify network, e.g., R('R1') + L('L1')")
    parser.add_argument('--input_filename', nargs='+')
    parser.add_argument('--output_filename', type=str, help='output filename')
    parser.add_argument(
        '--ranges', type=str, help="specify search ranges, e.g.,  {'R1':(0,1),'L1':(10,20)}")
    parser.add_argument('--label', nargs='+')
    parser.add_argument('--draw', action='store_true',
                        default=False, help='draw network')
    parser.add_argument('--layout', type=str, default='horizontal',
                        help='drawing layout: vertical, horizontal, ladder')
    parser.add_argument('--show', action='store_true',
                        default=False, help='show plot')
    parser.add_argument('--plot-admittance', action='store_true',
                        default=False,
                        help='plot admittance rather than impedance')
    parser.add_argument('--plot', type=str, default=None,
                        help='specify plot type: real-imag, mag-phase, Ls-Rs, Cp-Gp, nyquist, nichols, slice')
    parser.add_argument('--plot-format', type=str, default=None,
                        help='specify plot format: data, model, fit, error')
    parser.add_argument('--fit-admittance', action='store_true',
                        default=False,
                        help='fit admittance rather than impedance')
    parser.add_argument('--logf', action='store_true',
                        default=False, help='Plot log frequency')
    parser.add_argument('--plot-error', action='store_true',
                        default=False, help='plot impedance error')
    parser.add_argument('--plot-fit', action='store_true',
                        default=False, help='plot impedance data and fit')
    parser.add_argument('--plot-data', action='store_true',
                        default=False, help='plot impedance data')
    parser.add_argument('--magphase', action='store_true',
                        default=False, help='plot magnitude and phase of impedance')
    parser.add_argument('--title', type=str, help='title for plot')
    parser.add_argument(
        '--method', type=str, help='optimization method: brute, trf, or dogbox', default='brute')
    parser.add_argument('--steps', type=int, default=20,
                        help='the number of search steps per range')
    parser.add_argument('--fitfmin', type=float, default=None,
                        help='minimum frequency to use for fitting (default fmin)')
    parser.add_argument('--fitfmax', type=float, default=None,
                        help='maximum frequency to use for fitting (default fmax)')
    parser.add_argument('--fmin', type=float, default=None,
                        help='minimum frequency to use for plotting')
    parser.add_argument('--fmax', type=float, default=None,
                        help='maximum frequency to use for plotting')
    parser.add_argument('--finish', type=str,
                        help='finishing search method: none or fmin')
    parser.add_argument('--verbose', type=int, default=0,
                        help='set verbosity 0-2')
    parser.add_argument('--conjugate', action='store_true',
                        help='conjugate the impedance')
    parser.add_argument('--pdb', action='store_true', default=False,
                        help='enter python debugger on exception')
    parser.add_argument('--defs', action='store_true', default=False,
                        help='print component definitions as a dictionary')
    parser.add_argument('--error', action='store_true', default=False,
                        help='print the fitting error')
    parser.add_argument('--values', action='store_true', default=False,
                        help='print the fitted values')
    parser.add_argument('--style', type=str, help='matplotlib style filename')
    parser.add_argument('--laplace', action='store_true', default=False,
                        help='print impedance in Laplace domain')
    parser.add_argument('--Zoffset', type=float, default=0,
                        help='impedance offset to add')
    parser.add_argument('--sigfigs', type=int, default=10,
                        help='set number of significant figures when printing defs')
    parser.add_argument('--data-admittance', action='store_true',
                        default=False,
                        help='interpret data as admittance')
    parser.add_argument('--data-magphase', action='store_true',
                        default=False,
                        help='interpret data as magnitude/phase')
    parser.add_argument('--percent', action='store_true',
                        default=False,
                        help='show fitting error as percentage')
    parser.add_argument('--scale', type=float, default=1,
                        help='axis y-scale')

    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = zfitpy_exception

    if args.style:
        style.use(args.style)

    if args.laplace:
        Model = model_make(args)
        model = Model()
        print(model.net.Z.laplace())
        return 0

    if args.draw:
        Model = model_make(args)
        model = Model()
        model.draw(args.output_filename, layout=args.layout)

        if args.show or args.output_filename is None:
            show()
        return 0

    plot_type = args.plot
    if plot_type is None:
        plot_type = 'real-imag'

    plot_format = args.plot_format
    if args.plot_fit:
        if plot_format is not None:
            raise ValueError(f'Conflicting plot formats: {plot_format} and fit')
        plot_format = 'fit'
    if args.plot_error:
        if plot_format is not None:
            raise ValueError(f'Conflicting plot formats: {plot_format} and error')
        plot_format = 'error'
    if args.plot_data:
        if plot_format is not None:
            raise ValueError(f'Conflicting plot formats: {plot_format} and data')
        plot_format = 'data'

    plotter = Plotter(args.plot_admittance, args.logf, scale=args.scale)

    if args.input_filename is None:
        raise ValueError('No input filenames specified')

    if args.label is None:
        args.label = []
        for filename in args.input_filename:
            args.label.append(r'%filename')

    if len(args.label) != len(args.input_filename):
        raise ValueError('Number of labels is different from number of filenames')

    for filename, label in zip(args.input_filename, args.label):
        if args.verbose:
            print(filename)
        doit(filename, label, plotter, plot_type, plot_format, args)

    if args.output_filename is not None:
        savefig(args.output_filename, bbox_inches='tight')

    if args.show or args.output_filename is None:
        show()

    return 0


if __name__ == '__main__':
    main()
