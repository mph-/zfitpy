from lcapy import R, L, C
from zfitter.model import Model, modelmake
        
SeriesRLModel = modelmake('SeriesRLModel', R('R1') + L('L1'), ('R1', 'L1'))
SeriesRCModel = modelmake('SeriesRCModel', R('R1') + C('C1'), ('R1', 'C1'))
SeriesLCModel = modelmake('SeriesLCModel', L('L1') + C('C1'), ('L1', 'C1'))

ParallelRLModel = modelmake('ParallelRLModel', R('R1') | L('L1'), ('R1', 'L1'))
ParallelRCModel = modelmake('ParallelRCModel', R('R1') | C('C1'), ('R1', 'C1'))
ParallelLCModel = modelmake('ParallelLCModel', L('L1') | C('C1'), ('L1', 'C1'))

SeriesRLCModel = modelmake('SeriesRLCModel', R('R1') + L('L1') + C('C1'), ('R1', 'L1', 'C1'))
ParallelRLCModel = modelmake('ParallelRLCModel', R('R1') | L('L1') | C('C1'), ('R1', 'L1', 'C1'))

Parallel2SeriesRLModel = modelmake('Parallel2SeriesRLModel',
                                   (R('R1') | L('L1')) | (R('R2') | L('L2')),
                                   ('R1', 'L1', 'R2', 'L2'))
Parallel3SeriesRLModel = modelmake('Parallel3SeriesRLModel',
                                   (R('R1') | L('L1')) | (R('R2') | L('L2')) | (R('R3') | L('L3')),
                                   ('R1', 'L1', 'R2', 'L2', 'R3', 'L3'))
Parallel4SeriesRLModel = modelmake('Parallel4SeriesRLModel',
                                   (R('R1') | L('L1')) | (R('R2') | L('L2')) | (R('R3') | L('L3')) | (R('R4') | L('L4')),
                                   ('R1', 'L1', 'R2', 'L2', 'R3', 'L3', 'R4', 'L4'))


