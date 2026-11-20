Resolve a fixed-energy tunneling path
=====================================


The eOn client selects this calculation with the ``lineb`` job in the
``[Main]`` section. The ``[Lineb]`` section holds the seed path and the controls.

* ``initial_path`` names the multi-frame seed band.
* ``energy`` sets the turning energy in eV. The resolver retains whether the caller supplied it.
* ``opt_tol`` and ``perp_tol`` are mass-weighted force tolerances in √eV. Each defaults to 0.001.
* ``beads`` selects the number of harmonic quantum TST replicas. Use zero for the path alone, or at least two for the rate.
* ``molecular`` enables rigid alignment of a free molecule.

The resolver reports the canonical fields and the origin of each value. Run
the example from the repository root.


.. code-block:: bash

   rgconf resolve --profile eonLegacyIni --ini examples/lineb.ini


The output includes ``lineb.energyEv`` with value 0.25 and ``lineb.beads``
with value zero. Both come from the example file.
