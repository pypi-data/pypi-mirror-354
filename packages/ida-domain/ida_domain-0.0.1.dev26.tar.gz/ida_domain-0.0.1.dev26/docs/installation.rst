Installation Guide
==================

This guide provides detailed instructions for installing and setting up the IDA Domain API.

Prerequisites
-------------

System Requirements
~~~~~~~~~~~~~~~~~~~

- **Python**: 3.7 or higher
- **IDA Pro**: Version 7.0 or higher
- **Operating System**: Windows, macOS, or Linux

IDA Pro Setup
~~~~~~~~~~~~~

The IDA Domain API requires access to the IDA SDK. You have two options:

Option 1: Set IDADIR Environment Variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the ``IDADIR`` environment variable to point to your IDA installation directory:

**Windows:**

.. code-block:: batch

   set IDADIR="C:\Program Files\IDA Professional 9.1"

**macOS:**

.. code-block:: bash

   export IDADIR="/Applications/IDA Professional 9.1.app/Contents/MacOS/"

**Linux:**

.. code-block:: bash

   export IDADIR="/opt/ida-9.1"

To make this permanent, add the export command to your shell profile (``~/.bashrc``, ``~/.zshrc``, etc.).

Option 2: Use idapro Python Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have already installed and configured the ``idapro`` Python package, setting ``IDADIR`` is not required.

Installation Methods
--------------------

Install from PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install the IDA Domain API is from PyPI:

.. code-block:: bash

   pip install ida-domain

This will automatically install the latest stable version with all dependencies.

Visit the `PyPI package page <https://pypi.org/project/ida-domain/>`_ to see available versions, release notes, and download statistics.

Install from Source
~~~~~~~~~~~~~~~~~~~

For the latest development version or to contribute to the project:

1. **Clone the repository:**

   .. code-block:: bash

      git clone git@github.com:HexRaysSA/ida-api-domain.git
      cd ida-api-domain

2. **Install the package:**

   .. code-block:: bash

      pip install .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development work, install in editable mode:

.. code-block:: bash

   git clone git@github.com:HexRaysSA/ida-api-domain.git
   cd ida-api-domain
   pip install -e .

This allows you to modify the source code and see changes immediately without reinstalling.

Virtual Environment (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

.. code-block:: bash

   # Create virtual environment
   python -m venv ida-domain-env

   # Activate virtual environment
   # On Windows:
   ida-domain-env\Scripts\activate
   # On macOS/Linux:
   source ida-domain-env/bin/activate

   # Install the package
   pip install .

Verification
------------

Test Your Installation
~~~~~~~~~~~~~~~~~~~~~~~

Create a simple test script to verify the installation:

.. code-block:: python

   # test_installation.py
   try:
       from ida_domain import Database
       print("✓ IDA Domain API imported successfully")

       # Test basic functionality
       db = Database()
       print("✓ Database object created successfully")

       print("Installation verification complete!")

   except ImportError as e:
       print(f"✗ Import error: {e}")
   except Exception as e:
       print(f"✗ Error: {e}")

Run the test:

.. code-block:: bash

   python test_installation.py

Expected output:

.. code-block:: text

   ✓ IDA Domain API imported successfully
   ✓ Database object created successfully
   Installation verification complete!

Test with a Sample Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have an IDA database file, you can test the full functionality:

.. code-block:: python

   # test_with_database.py
   from ida_domain import Database

   def test_database(db_path):
       db = Database()

       if db.open(db_path):
           print(f"✓ Successfully opened: {db_path}")
           print(f"  Entry point: {hex(db.entry_point())}")
           print(f"  Address range: {hex(db.minimum_ea())} - {hex(db.maximum_ea())}")

           # Count functions
           func_count = 0
           for _ in db.functions.get_all():
               func_count += 1
           print(f"  Functions: {func_count}")

           db.close(save=False)
           print("✓ Database closed successfully")
       else:
           print(f"✗ Failed to open: {db_path}")

   # Replace with your database path
   test_database("/path/to/your/database.idb")

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'ida_domain'**

- Ensure you've installed the package: ``pip install .``
- Check if you're in the correct virtual environment
- Verify Python can find the package: ``pip list | grep ida-domain``

**IDA SDK not found errors**

- Verify ``IDADIR`` is set correctly: ``echo $IDADIR`` (Linux/macOS) or ``echo %IDADIR%`` (Windows)
- Ensure the path points to the actual IDA installation directory
- Check that IDA Pro is properly installed

**Permission errors during installation**

- Use ``pip install --user .`` to install for the current user only
- Or use a virtual environment (recommended)

**Database opening failures**

- Ensure the database file exists and is accessible
- Verify the database was created with a compatible IDA version
- Check file permissions

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. **Check the documentation**: Review this guide and the API documentation
2. **Search existing issues**: Check the `GitHub Issues <https://github.com/HexRaysSA/ida-api-domain/issues>`_
3. **Create a new issue**: If your problem isn't covered, create a detailed issue report

When reporting issues, please include:

- Operating system and version
- Python version (``python --version``)
- IDA Pro version
- Complete error messages
- Steps to reproduce the issue

Development Setup
-----------------

Additional Dependencies for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you plan to contribute to the project, install additional development dependencies:

.. code-block:: bash

   # Install development dependencies
   pip install pytest pytest-cov black flake8

   # Run tests
   pytest tests/

   # Format code
   black ida_domain/

   # Check code style
   flake8 ida_domain/

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

The documentation will be generated in ``docs/_build/html/``.

Next Steps
----------

Once installation is complete:

1. **Read the API documentation**: Explore the :doc:`index` and other API modules
2. **Try the examples**: Check out :doc:`examples` for practical usage patterns
3. **Start your project**: Begin integrating the IDA Domain API into your reverse engineering workflow

.. note::
   The IDA Domain API is designed to work with IDA databases (.idb, .i64 files). You'll need to create these databases using IDA Pro before you can analyze them with this API.
