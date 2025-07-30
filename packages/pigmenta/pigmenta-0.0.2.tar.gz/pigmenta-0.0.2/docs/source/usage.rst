🧪 Usage
========

First you need to start by importing the package.

.. code-block:: python

    from pigmenta import PALETTES

You can access the color palettes as follows:

.. code-block:: python

    # Get a pastel palette
    colors = PALETTES.pastel
    print(colors)

Example with Matplotlib
-----------------------

.. code-block:: python

    import matplotlib.pyplot as plt
    from pigmenta import PALETTES

    colors = PALETTES.sunset

    plt.bar([1, 2, 3], [3, 5, 2], color=colors[:3])
    plt.title("Bar chart using pigmenta")
    plt.show()

🎨 Available Palettes
---------------------

Here are the palette names you can access via ``PALETTES.<name>``:

::

    pastel, vintage, retro, neon, gold, light, dark, warm, cold,
    summer, fall, winter, spring, happy, nature, earth, night, space,
    rainbow, gradient, sunset, sky, sea, kids, skin, food, cream,
    coffee, wedding, christmas, halloween

Access any of them like:

.. code-block:: python

    PALETTES.sky
    PALETTES.christmas

🛠️ Custom Palettes
===================

You can also register or override palettes by modifying the ``COLORS`` dictionary directly if allowed by your API:

.. code-block:: python

    from pigmenta.core import COLORS

    COLORS['custom'] = ['#111111', '#222222', '#333333']
