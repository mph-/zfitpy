#!/usr/bin/python3
"""zfitter V0.2
Copyright (c) 2021 Michael P. Hayes, UC ECE, NZ

Usage: zfitter modelname input-filename output-filename
"""

from __future__ import print_function
from matplotlib.pyplot import show, savefig
from argparse import ArgumentParser
from zfitter.model import models, modelmake
from zfitter import ZFitter
from zfitter import Plotter
from zfitter import impedancedata

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
    parser.add_argument('--show', action='store_true', default=False, help='show plot')
    parser.add_argument('--plot-nyquist', action='store_true', default=False, help='show Nyquist plot')    
    parser.add_argument('--plot-error', action='store_true', default=False, help='plot impedance error')
    parser.add_argument('--plot-fit', action='store_true', default=False, help='plot impedance and fit')        
    parser.add_argument('--title', type=str, help='title for plot')
    parser.add_argument('--steps', type=int, default=20,
                        help='the number of search steps per range')

    args = parser.parse_args()

    if not args.net and not args.modelname:
        raise ValueError('Either need to specify model name with --modelname or network with --net')

    if args.net:
        Model = modelmake('Model', args.net)

    if args.modelname:        
        try:
            Model = models[args.modelname]
        except:
            modelnames = ', '.join(list(models.keys()))
            raise ValueError('Unknown model %s: known models: %s' % (args.modelname, modelnames))            

    if args.draw:
        model = Model()
        model.draw(args.output_filename)

        if args.show or args.output_filename is None:
            show()        
        return 0

    if args.input_filename is None:
        raise ValueError('Impedance data not specified')
    
    data = impedancedata(args.input_filename)

    if args.ranges is None:
        raise ValueError('Search ranges not specified')

    zfitter = ZFitter(Model, data.f, data.Z)    

    fitmodel = zfitter(ranges=args.ranges, Ns=args.steps)

    print('%s, error=%.3e' % (fitmodel, zfitter.error))
    
    plotter = Plotter()
    if args.plot_error:
        plotter.Z_error(data, fitmodel, title=args.title)

    if args.plot_fit:
        plotter.Z_fit(data, fitmodel, title=args.title)

    if args.plot_nyquist:
        plotter.Z_nyquist(data, fitmodel, title=args.title)                

    if args.output_filename is not None:
        savefig(args.output_filename, bbox_inches='tight')

    if args.show or args.output_filename is None:        
        show()
    
    return 0


if __name__ == '__main__':
    main()
