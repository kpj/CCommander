CCommander
==========

A wrapper for cirrus7_'s LightCommander python API.

Examples
--------
CCommander features a couple of usage examples:

* Music Visualization

Use it in your python code

.. code:: python

  >>> from ccommander.examples import music_visualizer as mv
  >>> mv.main('foo.mp3')
  
or run it from the command-line

.. code:: bash

  $ ccommander foo.mp3

Dependencies
------------

* pyserial_


.. _cirrus7: http://www.cirrus7.com/
.. _pyserial: http://pyserial.sourceforge.net/
