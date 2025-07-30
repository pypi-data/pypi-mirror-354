#############
Binning Utils
#############
|TestStatus| |PyPiStatus| |BlackStyle| |BlackPackStyle| |MITLicenseBadge|

A collection of tools to help with binning.

*******
Binning
*******

The ``Binning`` is powerful dict which contains many bin related quantities and
is soley constructed from the edges of a binning.

.. code:: python

    import numpy as np
    import binning_utils
    binning_utils.Binning(bin_edges=np.linspace(0, 1, 9))

    {'num': 4,
     'edges': array([0.  , 0.25, 0.5 , 0.75, 1.  ]),
     'centers': array([0.125, 0.375, 0.625, 0.875]),
     'widths': array([0.25, 0.25, 0.25, 0.25]),
     'start': 0.0,
     'stop': 1.0,
     'limits': array([0., 1.])}


**************
random drawing
**************

Draw the bin to which a sample is randomly assigned to. This assumes that the
distribution of samples is uniform over the entire range of the binning.
You can provide the aperture of the bins though. (This is the widths of the
bins if the binning is one dimensional).

.. code:: python

    import numpy as np
    import binning_utils
    prng = np.random.Generator(np.random.PCG64(19))

    assignment = binning_utils.draw_random_bin(
        prng=prng,
        bin_apertures=[1000, 4000, 2000, 3000],
        size=10000,
    )

    print(np.unique(assignment, return_counts=True))

    (array([0, 1, 2, 3]), array([ 974, 3950, 2060, 3016]))


*******
power10
*******

Create binning in geomspace which is aligned to decades.

.. code:: python

    import binning_utils
    binning_utils.power10.space(
        start_decade=0,
        start_bin=0,
        stop_decade=2,
        stop_bin=1,
        num_bins_per_decade=3,
    )
    array([ 1., 2.15, 4.64, 10., 21.54, 46.41, 100.])


**********
powerspace
**********

To make bin edges for distributions occuring in power laws.
For example to histogram the energies of cosmic rays which occur in a
power law with slope ``-2.7``

.. code:: python

    import binning_utils
    binning_utils.powerspace(
        start=1,
        stop=10,
        power_slope=-2.7,
        size=10,
    )
    array([ 1.        ,  1.07017144,  1.15544801,  1.26196439,  1.39995703,
        1.58808152,  1.86493297,  2.32807878,  3.33799855, 10.        ])


******
sphere
******

Make tiles of roughly same areas on the surface of a sphere using a
Fibonacci spacing.

.. code:: python

    import binning_utils
    vertices_on_sphere = binning_utils.sphere.fibonacci_space(
        size=100,
        max_zenith_distance_rad=0.5,
    )


.. |BlackStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |BlackPackStyle| image:: https://img.shields.io/badge/pack%20style-black-000000.svg
    :target: https://github.com/cherenkov-plenoscope/black_pack

.. |TestStatus| image:: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/test.yml/badge.svg?branch=main
    :target: https://github.com/cherenkov-plenoscope/binning_utils/actions/workflows/test.yml

.. |MITLicenseBadge| image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. |PyPiStatus| image:: https://img.shields.io/pypi/v/binning_utils_sebastian-achim-mueller
    :target: https://pypi.org/project/binning_utils_sebastian-achim-mueller
