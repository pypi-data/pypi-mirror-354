Getting started
================

1. Install dependencies 📦️
---------------------------

a. Install KiCad 7 or later 👉️ https://www.kicad.org/download/
b. When using EDeA as a command line tool, please use `pipx <https://pipx.pypa.io/stable/installation/>`_ to manage the virtualenv easier.


2. EDeA vet 🔍️
----------------

This command checks if the KiCad version is compatible with EDeA:

.. code-block:: bash

    edea vet

If everything is OK, install `edea` command completion:

.. code-block:: bash

    edea --install-completion

.. asciinema:: 670309

3. Time to use EDeA 💫
-----------------------

.. tab:: One time use
    
    |
    
    .. code-block:: bash

        pipx run --system-site-packages edea version

    .. asciinema:: 669841

.. tab:: Install
    
    |

    .. code-block:: bash

        pipx install --system-site-packages edea
        edea version

    .. asciinema:: 669842

For more information about the commands, check the :ref:`cli` page.
