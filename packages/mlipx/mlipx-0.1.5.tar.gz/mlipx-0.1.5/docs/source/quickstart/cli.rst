.. _cli-quickstart:

Command Line Interface
======================

This guide will help you get started with ``mlipx`` by creating a new project in an empty directory and computing metrics for a machine-learned interatomic potential (:term:`MLIP`) against reference DFT data.

First, create a new project directory and initialize it with Git and DVC:

.. code-block:: console

    (.venv) $ mkdir my_project
    (.venv) $ cd my_project
    (.venv) $ git init
    (.venv) $ dvc init

Adding Reference Data
----------------------
Next, add a reference DFT dataset to the project. For this example, we use a slice from the mptraj dataset :footcite:`dengCHGNetPretrainedUniversal2023`.

.. note::

    If you have your own data, replace this file with any dataset that can be read by ``ase.io.read`` and includes reference energies and forces. Run the following command instead:

    .. code-block:: bash

        (.venv) $ cp /path/to/your/data.xyz data.xyz
        (.venv) $ dvc add data.xyz

.. code-block:: console

    (.venv) $ dvc import-url https://github.com/zincware/ips-mace/releases/download/v0.1.0/mptraj_slice.xyz data.xyz

Adding the Recipe
-----------------
With the reference data in place, add a ``mlipx`` recipe to compute metrics:

.. code-block:: console

    (.venv) $ mlipx recipes metrics --datapath data.xyz

This command generates a ``main.py`` file in the current directory, which defines the workflow for the recipe.

Defining Models
---------------
Define the models to evaluate. This example uses the MACE-MP-0 model :footcite:`batatiaFoundationModelAtomistic2023` which is provided by the ``mace-torch`` package..

Create a file named ``models.py`` in the current directory with the following content:


.. note::

    If you already have computed energies and forces you can use two different data files or one file and update the keys.
    For more information, see the section on :ref:`update-frames-calc`.

.. code-block:: python

    import mlipx

    mace_mp = mlipx.GenericASECalculator(
        module="mace.calculators",
        class_name="mace_mp",
        device="auto",
        kwargs={
            "model": "medium",
        },
    )

    MODELS = {"mace-mp": mace_mp}

.. note::

    The ``GenericASECalculator`` class passes any provided ``kwargs`` to the specified ``class_name``.
    A special case is the ``device`` argument.
    When set to ``auto``, the class uses ``torch.cuda.is_available()`` to check if a GPU is available and automatically selects it if possible.
    If you are not using ``torch`` or wish to specify a device explicitly, you can omit the ``device`` argument or define it directly in the ``kwargs``.


Running the Workflow
---------------------
Now, run the workflow using the following commands:

.. code-block:: console

    (.venv) $ python main.py
    (.venv) $ dvc repro

Listing Steps and Visualizing Results
-------------------------------------
To explore the available steps and visualize results, use the commands below:

.. code-block:: console

    (.venv) $ zntrack list
    (.venv) $ mlipx compare mace-mp_CompareCalculatorResults

.. note::

    To use ``mlipx compare``, you must have an active ZnDraw server running. Provide the server URL via the ``--zndraw-url`` argument or the ``ZNDRAW_URL`` environment variable.

    You can start a server locally with the command ``zndraw`` in a separate terminal or use the public server at https://zndraw.icp.uni-stuttgart.de.


More CLI Options
----------------

The ``mlipx`` CLI can create the :term:`models.py` for some models.
To evaluate ``data.xyz`` with multiple models, you can also run

.. code-block:: console

    (.venv) $ mlipx recipes metrics --datapath data.xyz --models mace-mpa-0,sevennet,orb-v2,chgnet --repro

.. note::

    Want to see your model here? Open an issue or submit a pull request to the `mlipx repository <https://github.com/basf/mlipx>`_.


.. footbibliography::
