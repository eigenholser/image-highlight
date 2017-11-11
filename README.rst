===============
Highlight Image
===============

Add highlighter marks to a newspaper image as described in JSON file.


------------
Installation
------------

Clone the repository. Create a Python virtual environment. This program may
work with Python 2.::

    cd image-highlight
    mkvirtualenv --python=/usr/bin/python3 image-highlight
    setvirtualenvproject
    pip install -r requirements.txt


----------
Invocation
----------

Invoke like this::

    python highlight.py --image /path/to/image.jpg \
        --highlights /path/to/highlights.json

----------------------
Structure of JSON Data
----------------------

Highlights are described as square sections defined by an upper left corner
with associated width, height, and color.::

    [
        {
            "comment": "Highlight date",
            "x": 3700,
            "y": 920,
            "width": 1100,
            "height": 180,
            "color": "f3f321"
        },
        {
            "comment": "Highlight article",
            "x": 335,
            "y": 3100,
            "width": 950,
            "height": 3550,
            "color": "f3f321"
        }
    ]
