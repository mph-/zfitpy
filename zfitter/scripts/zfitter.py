#!/usr/bin/python3
"""zfitter V0.1
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

def split(s, delimiter):
    """Split string by specified delimiter but not if delimiter is within
    parentheses."""

    parts = []
    current = []
    close_bracket = ''
    bracket_stack = []
    for c in (s + delimiter):
        if c == delimiter and len(bracket_stack) == 0:
            if len(current) > 0:
                parts.append(''.join(current))
            current = []
        else:
            if c == close_bracket:
                close_bracket = bracket_stack.pop()                
            elif c == '(':
                bracket_stack.append(close_bracket)
                close_bracket = ')'
            current.append(c)
    if close_bracket != '':
        raise ValueError('Missing %s in %s' % (close_bracket, s))
    return parts


def main():

    parser = ArgumentParser(description='Draw schematic of impedance model.')
    parser.add_argument('--version', action='version', version=__doc__.split('\n')[0])
    parser.add_argument('--modelname', type=str, help='model name')
    parser.add_argument('--net', type=str, help='treat model as network')
    parser.add_argument('--input_filename', type=str, help='input filename')    
    parser.add_argument('--output_filename', type=str, help='output filename')
    parser.add_argument('--ranges', type=str, help='search ranges')
    parser.add_argument('--draw', action='store_true', default=False, help='draw network')
    parser.add_argument('--show', action='store_true', default=False, help='show plot')
    parser.add_argument('--plot-error', action='store_true', default=False, help='plot impedance error')
    parser.add_argument('--plot-fit', action='store_true', default=False, help='plot impedance and fit')        
    parser.add_argument('--title', type=str, help='title for plot')
    

    args = parser.parse_args()

    if not args.net and not args.modelname:
        raise ValueError('Either need to specify model name with --modelname to network with --net')

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

        if args.show:
            show()        
        return 0

    if args.input_filename is None:
        raise ValueError('Impedance data not specified')
    
    data = impedancedata(args.input_filename)

    if args.ranges is None:
        raise ValueError('Search ranges not specified')

    zfitter = ZFitter(Model, data.f, data.Z)    

    fitmodel = zfitter(ranges=args.ranges)

    print('%s, error=%.3e' % (fitmodel, zfitter.error))
    
    plotter = Plotter()
    if args.plot_error:
        plotter.Z_error(data, fitmodel, title=args.title)

    if args.plot_fit:
        plotter.Z_fit(data, fitmodel, title=args.title)        

    if args.output_filename is not None:
        savefig(args.output_filename, bbox_inches='tight')

    if args.show:
        show()
    
    return 0


if __name__ == '__main__':
    main()
