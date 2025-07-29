Concept
=======

``mlipx`` is a tool designed to evaluate the performance of various **Machine-Learned Interatomic Potentials (MLIPs)**.
It offers both static and dynamic test recipes, helping you identify the most suitable MLIP for your specific problem.

The ``mlipx`` package is modular and highly extensible, achieved by leveraging the capabilities of :term:`ZnTrack` and community support to provide a wide range of different test cases and :term:`MLIP` interfaces.

Static Tests
------------

Static tests focus on predefined datasets that serve as benchmarks for evaluating the performance of different :term:`MLIP` models.
You provide a dataset file, and ``mlipx`` evaluates a specified list of :term:`MLIP` models to generate performance metrics.
These tests are ideal for comparing general performance across multiple MLIPs on tasks with well-defined input data.

Dynamic Tests
-------------

Dynamic tests are designed to address specific user-defined problems where the dataset is not predetermined. These tests provide flexibility and adaptability to evaluate :term:`MLIP` models based on your unique requirements. For example, if you provide only the composition of a system, ``mlipx`` can assess the suitability of various :term:`MLIP` models for the problem.

- ``mlipx`` offers several methods to generate new data using recipes such as :ref:`relax`, :ref:`md`, :ref:`homonuclear_diatomics`, or :ref:`ev`.
- If no starting structures are available, ``mlipx`` can search public datasets like ``mptraj`` or the Materials Project for similar data. Alternatively, new structures can be generated directly from ``smiles`` strings, as detailed in the :ref:`data` section.

This dynamic approach enables a more focused evaluation of :term:`MLIP` models, tailoring the process to the specific challenges and requirements of the user's system.

Comparison
----------

A comprehensive comparison of different :term:`MLIP` models is crucial to identifying the best model for a specific problem.
To facilitate this, ``mlipx`` integrates with :ref:`ZnDraw <zndraw>` for visualizing trajectories and creating interactive plots of the generated data.

Additionally, ``mlipx`` interfaces with :term:`DVC` for data versioning and can log metrics to :term:`mlflow`,
providing a quick overview of all past evaluations.


.. toctree::
   :hidden:

   concept/data
   concept/models
   concept/recipes
   concept/zntrack
   concept/zndraw
   concept/metrics
   concept/distributed
