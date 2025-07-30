======
Design
======

We discuss the design of the mammos packages, in particular the use of ontology
labels and units when exchanging data.

TLDR
----

- the use of ontology labels and units (through ``mammos-entities``) is
  supported and encouraged, but not compulsory.

- A more detailed summary is available at the end of this page at
  `Design principles for ontology labels and units`_.


FAIR data requirements
----------------------

In the context of open science, it is essential that numerical values in data
are consistently associated both (i) units and (ii) ontology labels.

We use the term `quantity` to refer to a value (such as a number) and associated units.

We understand `entity` as a data point with units that has a label from an
ontology, such as the EMMO.

Units ensure that measurements are interpretable and comparable across datasets,
avoiding ambiguity about scale or dimension. Entities---through they 
ontology-based labels---provide precise semantic definitions for the quantities
being measured, ensuring clarity about what a number actually represents.

Example: we measure spontaneous magnetization in units of Ampere per metre, and
imagine that :math:`M_\mathrm{s} = 10^5 \mathrm{A/m}`. If we wanted to be
absolutely clear what we talk about, we could refer to our entity as a triplet::

    (SpontaneousMagnetization, 1e5, A/m)

Together, Ontology labels, values and units make data more Findable, Accessible,
Interoperable, and Reusable (FAIR) by enabling machines and researchers alike to
interpret and integrate data correctly across disciplines and domains.

Ontology labels (with mammos-entities)
--------------------------------------

How can we support the use of units and ontology labels in
day-to-day data-focused research?

We have created the `mammos_entity` `package
<https://github.com/mammos-project/mammos-entity>`__ to make this easier.

To define an entity for :math:`M_\mathrm{s}` as in the example above, we could write:

.. code-block:: python

  Ms = mammos_entity.Entity('SpontaneousMagnetisation', 1e5, "A/m")

Here ``SpontaneousMagnetization`` links back to the `SpontaneousMagnetization EMMO ontology label <https://mammos-project.github.io/MagneticMaterialsOntology/doc/magnetic_material_mammos.html#EMMO_032731f8-874d-5efb-9c9d-6dafaa17ef25>`__. As this entity is often needen in magnetic research, there is an abbreviation available:

.. code-block:: python

  Ms = mammos_entity.Ms(1e5, "A/m")

The object ``Ms`` knows its ontology label (``SpontaneousMagnetization``), and
the value (``1e5``) and the units (``A/m``) of the value. When this is passed to
other functions, they can check that the entity is of the right type for the
analysis to make sense, and what the units are so that the value makes sense
(for example: do we measure in Ampere per metre or in kilo Ampere per metre).

The example above uses a single float as the value but entities do similar
support vectors or any array-like data structure.

An entity object behaves very much like a float or a numpy array. If needed, one
can get to the numerical value (here ``1e5``) through the attribute
``Ms.value``.

Use of ontology-labels: support, desired or enforced?
-----------------------------------------------------

The use of entities makes data exchange more robust, self-documenting, and
machine readable. The use of entities (and thus units) reduces the number of
implicit assumptions that can lead to errors or non-re-usable data. In the
spirit of fairer data, using entities is highly desirable.

However, there are at least two practical aspects to consider:

1. if a researcher needs to express all their data in entities, they may have to
   type more than if they were just using a floating point number. For example,
   ``mammos_entity.Ms(1e5, "A/m")`` instead of ``1e5``. 

2. if the researcher works with entities and needs to make use of a third-party
   function that expects a floating point number (perhaps a tool from ``scipy``,
   or---as a illustrative example--- ``math.cos()``), then it is possible that
   the entity cannot be used. Instead of ``math.cos(Ms)`` one would need to
   write ``math.cos(Ms.value)`` where ``Ms.value`` gives access to just the
   value of the entity (``1e5`` in our example).

Aspect 1 requires a bit more verbosity in writing the code (including clarity in
the process), aspect 2 needs translation of the entity to other tools which---at
that very point--increases complexity of the code.

There is thus a trade-off: in principle, the use of entities is desirable.
However, there is a cost for doing so. To convince researchers to embrace
ontologies (for example through using entities), we need to reduce the practical
burden as much as possible.

MaMMoS entity support
---------------------

Example
~~~~~~~

First we describe a use case as a concrete example, followed by three different
options of passing data to this. Based on this, we then summarise our approach
towards encouragement of use of entities.

Imagine a part of the MaMMoS software returns to us a function ``f`` (perhaps
from the Kuz'min equation) that returns the exchange coupling constant as a
function of temperature. We assuming the function is called ``f(T)`` and takes a
temperature ``T``, and we want to evaluate it at a temperature of 100 Kelvin.

Here are three options how we could pass the temperature (entity) to the function:

Option 1: just the value
~~~~~~~~~~~~~~~~~~~~~~~~

    >>> f(100)

The least effort.

Missing information: units (Kelvin or Celsius or something else)?

Option 2: number and units (=quantity)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We should say what we mean with ``100``: if we talk about temperature, it could be
100 Kelvin or 100 degree Celsius for example. Using ``mammos_units``, we can be precise:

    >>> import mammos_units as u
    >>> f(100*u.K)   # u.K represents the Unit Kelvin  

The function ``f`` can now check the units of the argument, and complain if
Kelvin is not what was expected.

Option 3: number, units and ontology label (=entity)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can also provide the ontology label for the temperature: this provides a
more precise semantic definition of the argument, and also avoids
misunderstandings (using kB*T one could express energy in units of temperature
T, but that's not what we mean here).

To be as precise as possible, we need to use the ontology label. Using
``mammos_entity``, we can write

    >>> import mammos_entity as me
    >>> f(me.entity("ThermodynamicTemperature", 100, "K"))

or, as an equivalent abbreviation for this:

    >>> f(me.T(100, "K"))

With the ontology label, the function ``f`` can now check if that is the
expected entity ``ThermodynamicTemperature`` and complain if this is not the case.


Discussion 
~~~~~~~~~~

Option 3 is the best in terms of precision and clarity, and the best for
interoperability and re-usability of data and software. However, it does require
some additional effort to specify the units and the type of, in this example,
the temperature.

Once a scientist has used the function ``f`` a few times, they may feel very
confident that the input argument meant to be the thermodynamic temperature, and
that of course the function expects input in SI units (i.e. Kelvin). Given that
knowledge, the scientist may much prefer option 1.

We argue that a syntax like option 1 is useful to support as for some scientists
it would be a game changer (and stop them from using the MaMMoS software) if
that functionality was not available.

Design principles for ontology labels and units
-----------------------------------------------

To balance the benefits of a complete specification (option 3) with the
convenience of being able to just use a number (option 1), we have developed the
following principles within the ``mammos`` packages:

- Return values of functions (and objects behaving like functions):

  - the principle return values are entities

    - entities provide as much context as possible and are the FAIRest we can offer
    - the effort of the scientist to extract just the value (if needed) is small (``.value``)

  - occasionally, there may be additional convenience objects, such as a pandas
    DataFrame for tabular data in
    `mammos_spindynamics.db.get_spontaneous_magnetization <https://mammos-project.github.io/mammos/examples/mammos-spindynamics/quickstart.html>`__
    The DataFrame is a well established object and of great power for data analysis, but cannot carry units.

    The convention in this case is, that the data is expressed in SI base units
    (such as Ampere/metre, or Kelvin, and not in kAmpere/m or Celsius).

- Arguments for functions (and objects behaving like functions) are accepted in
  the following three options:

  - Option 1: functions accept (floating point) numbers as input arguments. The assumption is that
    these are provided in the appropriate SI base units. (Convenient but error prone.)

  - Option 2: functions accept quantities (i.e. value and unit) as input arguments. There are checked
    for the correctness of units (prefactors are allowed).

  - Option 3: functions accept entities (i.e. ontology label, value and unit) as
    input arguments. These are checked for correctness of the ontology label,
    and correctness of the units (prefactors are allowed).

    This is the best and recommended approach.


Users of the packages can mix the three approaches as they see fit. While
consistent use of option 3 would be desirable and is recommded, we have seen in
the past that a lack of flexibility can hinder uptake of well-intended
improvements.
