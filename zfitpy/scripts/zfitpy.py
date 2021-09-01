#!/usr/bin/python3
"""zfitpy V0.3.2
Copyright (c) 2021 Michael P. Hayes, UC ECE, NZ

Usage: 

Here are some examples.

zfitpy --net net --draw
zfitpy --input data.csv --plot --output plotfilename
zfitpy --plot-fit --net net --ranges ranges --input data.csv --plot-error
"""

from __future__ import print_function
from matplotlib.pyplot import show, savefig, style
from argparse import ArgumentParser
from zfitpy.model import models, modelmake
from zfitpy import ZFitter
from zfitpy import Plotter
from zfitpy import impedancedata
import sys

def zfitpy_exception(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # We are not in interactive mode or we don't have a tty-like
      # device, so call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # We are in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print()
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

def model_make(args):

    if not args.net and not args.modelname:
        raise ValueError('Either need to specify model name with --modelname or network with --net')

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
            raise ValueError('Unknown model %s: known models: %s' % (args.modelname, modelnames))            

    return Model

def main():

    parser = ArgumentParser(description='Draw schematic of impedance model.')
    parser.add_argument('--version', action='version', version=__doc__.split('\n')[0])
    parser.add_argument('--modelname', type=str, help='model name')
    parser.add_argument('--net', type=str,
                        help="specify network, e.g., R('R1') + L('L1')")
    parser.add_argument('--input_filename', type=str, help='input filename')    
    parser.add_argument('--output_filename', type=str, help='output filename')
    parser.add_argument('--ranges', type=str, help="specify search ranges, e.g.,  {'R1':(0,1),'L1':(10,20)}")
    parser.add_argument('--draw', action='store_true', default=False, help='draw network')
    parser.add_argument('--layout', type=str, default='horizontal', help='drawing layout: vertical, horizontal, ladder')    
    parser.add_argument('--show', action='store_true', default=False, help='show plot')
    parser.add_argument('--nyquist', action='store_true', default=False, help='use Nyquist plot')    
    parser.add_argument('--plot-error', action='store_true', default=False, help='plot impedance error')
    parser.add_argument('--plot-fit', action='store_true', default=False, help='plot impedance data and fit')
    parser.add_argument('--plot-data', action='store_true', default=False, help='plot impedance data')    
    parser.add_argument('--magphase', action='store_true', default=False, help='plot magnitude and phase of impedance')            
    parser.add_argument('--title', type=str, help='title for plot')
    parser.add_argument('--method', type=str, help='optimization method: brute, trf, or dogbox', default='brute')    
    parser.add_argument('--steps', type=int, default=20,
                        help='the number of search steps per range')
    parser.add_argument('--fmin', type=float, default=None,
                        help='Minimum frequency to use for fitting')
    parser.add_argument('--fmax', type=float, default=None,
                        help='Maximum frequency to use for fitting')
    parser.add_argument('--finish', type=str, help='finishing search method: none or fmin')
    parser.add_argument('--verbose', type=int, default=0, help='set verbosity 0-2')
    parser.add_argument('--pdb', action='store_true',
                        default=False,
                        help='enter python debugger on exception')    
    parser.add_argument('--style', type=str, help='matplotlib style filename')

    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = zfitpy_exception
    
    if args.style:
        style.use(args.style)

    if args.draw:
        Model = model_make(args)
        model = Model()
        model.draw(args.output_filename, layout=args.layout)

        if args.show or args.output_filename is None:
            show()        
        return 0

    if args.input_filename is None:
        raise ValueError('Impedance data not specified')
    
    data = impedancedata(args.input_filename,
                         fmin=args.fmin, fmax=args.fmax)


    if False and args.ranges is None:
        raise ValueError('Search ranges not specified')

    if args.ranges is None:
        fitmodel = None
    else:

        ranges = args.ranges
        if ranges.endswith('.ranges'):
           ranges = open(ranges).read()
       
        Model = model_make(args)
        zfitter = ZFitter(Model, data.f, data.Z)            
        fitmodel = zfitter(ranges=ranges, Ns=args.steps,
                           method=args.method, verbose=args.verbose,
                           finish=args.finish)
        print('%s, error=%.3e' % (fitmodel, fitmodel.error))
    
    plotter = Plotter()
    if args.plot_error and fitmodel:
        plotter.Z_error(data, fitmodel, title=args.title)

    if args.plot_fit:
        if args.nyquist:
            plotter.Z_nyquist(data, fitmodel, title=args.title)
        else:
            plotter.Z_fit(data, fitmodel, title=args.title, magphase=args.magphase)

    if args.plot_data:
        if args.nyquist:
            plotter.Z_nyquist(data, None, title=args.title)
        else:
            plotter.Z_fit(data, None, title=args.title, magphase=args.magphase)

    if args.output_filename is not None:
        savefig(args.output_filename, bbox_inches='tight')

    if args.show or args.output_filename is None:        
        show()
    
    return 0


if __name__ == '__main__':
    main()
