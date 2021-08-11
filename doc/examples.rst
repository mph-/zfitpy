Examples
========

To plot the error between the best fit and the measure data use::

   $ zfitpy --net "L('L1') + (R('R1') | (L('L2') + R('R2')))" --ranges="{'R1':(0,5e3),'L1':(1e-3,20e-3),'R2':(0,0.1),'L2':(1e-3,20e-3)}" --input demo/E4990A-example1.csv --plot-error


To draw the model use::

   $ zfitpy --net "L('L1') + (R('R1') | (L('L2') + R('R2')))" --draw
   

.. image:: Parallel2SeriesRLModel.png
   :width: 7cm

.. image:: ../demo/E4990A-example1a.png
   :width: 15cm           
           

.. image:: ParallelRCPEModel.png
   :width: 7cm

.. image:: ../demo/E4990A-example1d.png
   :width: 15cm           
           

.. image:: SeriesRParallelRCPEModel.png
   :width: 7cm

.. image:: ../demo/E4990A-example1h.png
   :width: 15cm           
           
      
