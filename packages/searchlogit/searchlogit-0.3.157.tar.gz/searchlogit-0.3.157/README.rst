===================================================================================
searchlogit: A Python package for GPU-accelerated estimation of mixed logit models.
===================================================================================

.. removed travis / etc... # TODO

.. _Mixed Logit: https://xlogit.readthedocs.io/en/latest/api/mixed_logit.html
.. _Multinomial Logit: https://xlogit.readthedocs.io/en/latest/api/multinomial_logit.html

.. `Examples <https://xlogit.readthedocs.io/en/latest/examples.html>`__ | `Docs <https://xlogit.readthedocs.io/en/latest/index.html>`__ | `Installation <https://xlogit.readthedocs.io/en/latest/install.html>`__ | `API Reference <https://xlogit.readthedocs.io/en/latest/api/index.html>`__ | `Contributing <https://xlogit.readthedocs.io/en/latest/contributing.html>`__ | `Contact <https://xlogit.readthedocs.io/en/latest/index.html#contact>`__ 

Quick start
===========
The following example uses the base ``searchlogit`` to estimate a mixed logit model for choices of electricity supplier (`See the data here <https://github.com/arteagac/xlogit/blob/master/examples/data/electricity_long.csv>`__). The parameters are:

* ``X``: 2-D array of input data (in long format) with choice situations as rows, and variables as columns
* ``y``: 1-D array of choices (in long format)
* ``varnames``: List of variable names that matches the number and order of the columns in ``X``
* ``alts``:  1-D array of alternative indexes or an alternatives list
* ``ids``:  1-D array of the ids of the choice situations
* ``panels``: 1-D array of ids for panel formation
* ``randvars``: dictionary of variables and their mixing distributions (``"n"`` normal, ``"ln"`` lognormal, ``"t"`` triangular, ``"u"`` uniform, ``"tn"`` truncated normal)
* ``transvars``: List of variables to apply the specified transformation
* ``transformation``: String specifying the transformation to be applied (default is the Box-Cox transformation)
* ``correlation``: Either a list of variables names that are correlated or a boolean to set all randvars as correlated

The current version of `searchlogit` only supports input data in long format.

.. code-block:: python

    # Read data from CSV file
    import pandas as pd
    df = pd.read_csv("https://raw.githubusercontent.com/arteagac/xlogit/master/examples/data/electricity_long.csv")

    # reverse sign for randvars with a lognormal distribution
    df['tod'] = -df['tod']
    df['seas'] = -df['seas']

    X = df[varnames]
    y = df['choice']

    # Fit the model with xlogit
    from searchlogit import MixedLogit
    model = MixedLogit()
    model.fit(X, y,
              varnames,
              alts=df['alt'],
              ids=df['chid'],
              panels=df['id'],
              randvars={'cl':'n','loc':'n','wk':'u','tod':'ln','seas':'n'},
              correlation=['loc', 'wk', 'tod', 'seas'],
              transvars=['cl'],
              n_draws=600
              )
    model.summary()


::

    Optimization terminated successfully.
            Current function value: 3942.930393
            Iterations: 66
            Function evaluations: 77
            Gradient evaluations: 77
    Estimation time= 51.5 seconds
    Frequencies of alternatives: observed choice
    [0.22576177 0.26246537 0.23684211 0.26939058]
    Frequencies of alternatives: predicted choice
    [0.22930773 0.26222102 0.22989339 0.2730377 ]
    ---------------------------------------------------------------------------
    Coefficient              Estimate      Std.Err.         z-val         P>|z|
    ---------------------------------------------------------------------------
    pf                  -0.8844627763  0.0295175526 -29.9639603432             0 ***
    loc                  2.2458727521  0.1032222566 21.7576405168             0 ***
    wk                   0.2276055259  0.0685607922  3.3197621949      0.000901 ***
    tod                  2.1355682749  0.0376005793 56.7961535512             0 ***
    seas                 8.7966341596  0.2824599096 31.1429475855             0 ***
    chol.loc.loc         1.3698552163  0.1301206261 10.5275793490             0 ***
    chol.wk.loc          0.5137795414  0.0664560103  7.7311222681      1.07e-14 ***
    chol.wk.wk          -0.5269078200  0.0465699165 -11.3143389438             0 ***
    chol.tod.loc        -0.0092950782  0.0277084890 -0.3354595849         0.737
    chol.tod.wk          0.0694307288  0.0316747405  2.1919904546        0.0284 *
    chol.tod.tod         0.3998943075  0.0283441100 14.1085504981             0 ***
    chol.seas.loc        0.2636579056  0.1466998262  1.7972611991        0.0723 .
    chol.seas.wk        -0.0387176619  0.1862974259 -0.2078271435         0.835
    chol.seas.tod        1.0931383738  0.1523794076  7.1737933030      7.29e-13 ***
    chol.seas.seas      -2.9951794692  0.1818545992 -16.4701881742             0 ***
    cl                  -0.1571373624  0.0234064621 -6.7134179193       1.9e-11 ***
    sd.cl                0.2767984154  0.0345402217  8.0137996096      1.11e-15 ***
    lambda.cl            1.1525365710  0.1287181869  1.1850428803         0.236
    ---------------------------------------------------------------------------
    Significance:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

    Log-Likelihood= -3942.930
    AIC= 7921.861
    BIC= 7991.861

.. For more examples of ``searchlogit`` see `this Jupyter Notebook in Google Colab <https://colab.research.google.com/github/arteagac/xlogit/blob/master/examples/mixed_logit_model.ipynb>`__. **Google Colab provides GPU resources for free**, which will significantly speed up your model estimation using ``searchlogit``.

Quick install
=============
Install ``searchlogit`` using ``pip`` as follows:

.. code-block:: bash

    pip install searchlogit


.. hint::

    To enable GPU processing, you must install the `CuPy Python library <https://docs.cupy.dev/en/stable/install.html>`__.  When ``searchlogit`` detects that CuPy is properly installed, it switches to GPU processing without any additional setup. If you use Google Colab, CuPy is usually installed by default.


.. For additional installation details check xlogit installation instructions at: https://xlogit.readthedocs.io/en/latest/install.html


No GPU? No problem
==================
``searchlogit`` can also be used without a GPU. However, if you need to speed up your model estimation, there are several low cost and even free options to access cloud GPU resources. For instance:

- `Google Colab <https://colab.research.google.com>`_ offers free GPU resources for learning purposes with no setup required, as the service can be accessed using a web browser. Using searchlogit in Google Colab is very easy as it runs out of the box without needing to install CUDA or CuPy, which are installed by default.
- For examples of xlogit running in Google Colab `see this link <https://colab.research.google.com/github/arteagac/xlogit/blob/master/examples/mixed_logit_model.ipynb>`_.
- The `Google Cloud platform <https://cloud.google.com/compute/gpus-pricing>`_ offers GPU processing starting at $0.45 USD per hour for a NVIDIA Tesla K80 GPU with 4,992 CUDA cores.
- `Amazon Sagemaker <https://aws.amazon.com/ec2/instance-types/p2/>`_ offers virtual machine instances with the same TESLA K80 GPU at less than $1 USD per hour.

Benchmark
=========
 ``searchlogit`` extends ``xlogit``. As shown in the plots below, ``xlogit`` is significantly faster than existing estimation packages. Also, ``xlogit`` provides convenient scaling when the number of random draws increases. These results were obtained using a modest and low-cost NVIDIA GTX 1060 graphics card. More sophisticated graphics cards are expected to provide even faster estimation times. For additional details about this benchmark and for replication instructions check https://xlogit.readthedocs.io/en/latest/benchmark.html.

.. image:: https://raw.githubusercontent.com/arteagac/xlogit/master/examples/benchmark/results/time_benchmark_artificial.png
  :width: 300

.. image:: https://raw.githubusercontent.com/arteagac/xlogit/master/examples/benchmark/results/time_benchmark_apollo_biogeme.png
  :width: 300

Notes
=====
The current version allows estimation of:

- Mixed Logit with several types of mixing distributions (normal, lognormal, triangular, uniform, and truncated normal)
- Mixed Logit with panel data
- Mixed Logit with unbalanced panel data
- Mixed Logit with Halton draws
- Mixed Logit with correlated random variables
- Mixed Logit with Box-Cox transformed fixed and random variables
- Multinomial Logit models with Box-Cox transformed fixed and random variables
- Conditional logit models
- Latent class logit models
- Latent class mixed logit models
- Weighed regression for all of the logit-based models
- Handling of unbalanced availability of choice alternatives for all of the supported models
- Post-estimation tools for prediction and specification testing
- Inclusion of sample weights for all of the supported models

Contact
=======

If you have any questions, ideas to improve ``searchlogit``, or want to report a bug, just open a `new issue in xlogit's GitHub repository <https://github.com/RyanJafefKelly/searchlogit/issues>`__ .

Citing ``searchlogit``
======================
Please cite ``searchlogit`` as follows:

Beeramoole, P. B., Alexander, P., Kelly, R., Arteaga, C.,. (2022). Searchlogit [Computer software]. https://pypi.org/project/searchlogit/

Or using BibTex as follows::

    @misc{searchlogit,
        author = {Beeramoole, P and Paz, A and Kelly, R and Arteaga, C},
        title = "{Searchlogit [Computer software]},
        url = {https://pypi.org/project/searchlogit/},
        year = {2022}
    }


.. .. |Travis| image:: https://travis-ci.com/arteagac/xlogit.svg?branch=master
..    :target: https://travis-ci.com/arteagac/xlogit

.. .. |Docs| image:: https://readthedocs.org/projects/xlogit/badge/?version=latest
..    :target: https://xlogit.readthedocs.io/en/latest/?badge=latest
..    :alt: Documentation Status

.. .. |Coverage| image:: https://coveralls.io/repos/github/arteagac/xlogit/badge.svg?branch=master
..    :target: https://coveralls.io/github/arteagac/xlogit?branch=master

.. .. |PyPi| image:: https://badge.fury.io/py/xlogit.svg
..    :target: https://badge.fury.io/py/xlogit

.. .. |License| image:: https://img.shields.io/github/license/arteagac/xlogit
..    :target: https://github.com/arteagac/xlogit/blob/master/LICENSE
