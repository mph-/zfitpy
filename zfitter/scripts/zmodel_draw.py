#!/usr/bin/python3
"""zmodel-draw V0.2
Copyright (c) 2021 Michael P. Hayes, UC ECE, NZ

Usage: zmodel-draw modelname output-filename
"""

from __future__ import print_function
from argparse import ArgumentParser
from zfitter.model import models

def main():

    parser = ArgumentParser(description='Draw schematic of impedance model.')
    parser.add_argument('modelname', type=str, help='model name')
    parser.add_argument('--version', action='version', version=__doc__.split('\n')[0])
    parser.add_argument('output_filename', type=str, help='output filename')

    args = parser.parse_args()

    if args.modelname not in models:
        modelnames = ', '.join(list(models.keys()))
        raise ValueError('Unknown model %s: known models: %s' % (args.modelname, modelnames))

    model = models[args.modelname]()
    
    model.draw(args.output_filename)

    return 0


if __name__ == '__main__':
    main()
