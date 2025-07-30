Photo Condenser
===============

A modern Python application for finding and managing similar or duplicate images in your photo collection.
The tool uses Machine Learning to compare images and provides an intuitive interface for reviewing and organizing your photos.

**Select the photo you want to keep with arrow keys**

Features
--------

- 🖼️ Supports multiple image formats (JPG, PNG, WebP, etc.)
- 🔍 Advanced image comparison using Machine Learning
- 🎯 Smart caching for improved performance
- 📊 Image metadata display
- 🖱️ Intuitive navigation with address bar

Screenshot
----------

.. image:: screemshot.png
   :alt: Photo Condenser Screenshot
   :align: center
   :width: 80%
   :target: screemshot.png

Installation
------------

Using pipx
~~~~~~~~~~

.. code-block:: bash

    pipx install photo_condenser

Usage
-----

Command Line
~~~~~~~~~~~~

.. code-block:: bash

    # Launch the application
    photo_condenser

    # Or run directly
    python -m photo_condenser

Basic Workflow
~~~~~~~~~~~~~~

1. Launch the application
2. Use the address bar to navigate to your photo directory
3. The application will present you with pairs of similar images
4. Use the arrow keys to select the image you want to keep or Spac
