.. _relax:

Structure Relaxation
====================

This recipe is used to test the performance of different models in performing structure relaxation.


.. mdinclude:: ../../../mlipx-hub/relax/mp-1143/README.md

.. note::

   If you relax a non-periodic system and your model yields a stress tensor of :code:`[inf, inf, inf, inf, inf, inf]` you have to add the :code:`--convert-nan` flag to the :code:`mlipx compare` or :code:`zndraw` command to convert them to :code:`None`.

.. jupyter-execute::
   :hide-code:

   from mlipx.doc_utils import get_plots

   plots = get_plots("*StructureOptimization", "../../mlipx-hub/relax/mp-1143/")
   plots["adjusted_energy_vs_steps"].show()

This recipe uses the following Nodes together with your provided model in the :term:`models.py` file:

* :term:`StructureOptimization`

.. dropdown:: Content of :code:`main.py`

   .. literalinclude:: ../../../mlipx-hub/relax/mp-1143/main.py
      :language: Python


.. dropdown:: Content of :code:`models.py`

   .. literalinclude:: ../../../mlipx-hub/relax/mp-1143/models.py
      :language: Python
