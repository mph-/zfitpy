"""This module provides named electrical models.

Copyright 2021 Michael Hayes, UCECE"""

from lcapy import R, L, C, Par, CPE
from .model import Model, modelmake
        
SeriesRLModel = modelmake('SeriesRLModel', R('R1') + L('L1'), ('R1', 'L1'))
SeriesRCModel = modelmake('SeriesRCModel', R('R1') + C('C1'), ('R1', 'C1'))
SeriesLCModel = modelmake('SeriesLCModel', L('L1') + C('C1'), ('L1', 'C1'))

ParallelRLModel = modelmake('ParallelRLModel', R('R1') | L('L1'), ('R1', 'L1'))
ParallelRCModel = modelmake('ParallelRCModel', R('R1') | C('C1'), ('R1', 'C1'))
ParallelLCModel = modelmake('ParallelLCModel', L('L1') | C('C1'), ('L1', 'C1'))

SeriesRLCModel = modelmake('SeriesRLCModel', R('R1') + L('L1') + C('C1'), ('R1', 'L1', 'C1'))
ParallelRLCModel = modelmake('ParallelRLCModel', Par(R('R1'),  L('L1'), C('C1')), ('R1', 'L1', 'C1'))

ParallelRSeriesRLModel = modelmake('ParallelRSeriesRLModel', R('R1') | (R('R2') + L('L1')), ('R1', 'R2', 'L1'))
ParallelCSeriesRLModel = modelmake('ParallelCSeriesRLModel', C('C1') | (R('R1') + L('L1')), ('C1', 'R1', 'L1'))
ParallelLSeriesRLModel = modelmake('ParallelLSeriesRLModel', L('L1') | (R('R1') + L('L2')), ('L1', 'R1', 'L2'))

ParallelRSeriesLCModel = modelmake('ParallelRSeriesLCModel', R('R1') | (L('L1') + C('C1')), ('R1', 'L1', 'C1'))
ParallelCSeriesLCModel = modelmake('ParallelCSeriesLCModel', C('C1') | (C('C2') + L('L1')), ('C1', 'C2', 'L1'))
ParallelLSeriesLCModel = modelmake('ParallelLSeriesLCModel', L('L1') | (C('C1') + L('L2')), ('L1', 'C1', 'L2'))

ParallelRSeriesRCModel = modelmake('ParallelRSeriesRCModel', R('R1') | (R('R1') + C('C1')), ('R1', 'R2', 'C1'))
ParallelCSeriesRCModel = modelmake('ParallelCSeriesRCModel', C('C1') | (R('R1') + C('C2')), ('C1', 'R1', 'C2'))
ParallelLSeriesRCModel = modelmake('ParallelLSeriesRCModel', L('L1') | (R('R1') + C('C1')), ('L1', 'R1', 'C1'))

SeriesRParallelRLModel = modelmake('SeriesRParallelRLModel', R('R1') + (R('R2') | L('L1')), ('R1', 'R2', 'L1'))
SeriesCParallelRLModel = modelmake('SeriesCParallelRLModel', C('C1') + (R('R1') | L('L1')), ('C1', 'R1', 'L1'))
SeriesLParallelRLModel = modelmake('SeriesLParallelRLModel', L('L1') + (R('R1') | L('L2')), ('L1', 'R1', 'L2'))

SeriesRParallelLCModel = modelmake('SeriesRParallelLCModel', R('R1') + (L('L1') | C('C1')), ('R1', 'L1', 'C1'))
SeriesCParallelLCModel = modelmake('SeriesCParallelLCModel', C('C1') + (C('C2') | L('L1')), ('C1', 'C2', 'L1'))
SeriesLParallelLCModel = modelmake('SeriesLParallelLCModel', L('L1') + (C('C1') | L('L2')), ('L1', 'C1', 'L2'))

SeriesRParallelRCModel = modelmake('SeriesRParallelRCModel', R('R1') + (R('R1') | C('C1')), ('R1', 'R2', 'C1'))
SeriesCParallelRCModel = modelmake('SeriesCParallelRCModel', C('C1') + (R('R1') | C('C2')), ('C1', 'R1', 'C2'))
SeriesLParallelRCModel = modelmake('SeriesLParallelRCModel', L('L1') + (R('R1') | C('C1')), ('L1', 'R1', 'C1'))

Parallel2SeriesRLModel = modelmake('Parallel2SeriesRLModel',
                                   (R('R1') + L('L1')) | (R('R2') + L('L2')),
                                   ('R1', 'L1', 'R2', 'L2'))
Parallel3SeriesRLModel = modelmake('Parallel3SeriesRLModel',
                                   (R('R1') + L('L1')) | (R('R2') + L('L2')) | (R('R3') + L('L3')),
                                   ('R1', 'L1', 'R2', 'L2', 'R3', 'L3'))
Parallel4SeriesRLModel = modelmake('Parallel4SeriesRLModel',
                                   (R('R1') + L('L1')) | (R('R2') + L('L2')) | (R('R3') + L('L3')) | (R('R4') + L('L4')),
                                   ('R1', 'L1', 'R2', 'L2', 'R3', 'L3', 'R4', 'L4'))

CPEModel = modelmake('CPEModel', CPE('K', 'alpha'), ('K', 'alpha'))
SeriesRCPEModel = modelmake('SeriesRCPEModel', R('R1') + CPE('K', 'alpha'), ('R1', 'K', 'alpha'))
ParallelRCPEModel = modelmake('ParallelRCPEModel', R('R1') | CPE('K', 'alpha'), ('R1', 'K', 'alpha'))

SeriesRParallelRCPEModel = modelmake('SeriesRParallelRCPEModel', R('R1') + (R('R2') | CPE('K', 'alpha')), ('R1', 'R2', 'K', 'alpha'))
ParallelRSeriesRCPEModel = modelmake('ParallelRSeriesRCPEModel', R('R1') | (R('R2') + CPE('K', 'alpha')), ('R1', 'R2', 'K', 'alpha'))

