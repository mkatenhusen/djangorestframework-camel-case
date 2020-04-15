=============================================
Django REST Framework JSON CamelCase Advanced
=============================================

Camel case JSON support for Django REST framework.

Added the class CamelCaseOrderingFilter in order to allow camelCase on Ordering Filters.

============
Installation
============

In the requirements.txt (or via pip install)::

    $ git+https://github.com/mkatenhusen/djangorestframework-camel-case.git@master

Add the render and parser to your django settings file.

.. code-block:: python

    # ...
    REST_FRAMEWORK = {

        'DEFAULT_RENDERER_CLASSES': (
            'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
            'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
            # Any other renders
        ),

        'DEFAULT_PARSER_CLASSES': (
            # If you use MultiPartFormParser or FormParser, we also have a camel case version
            'djangorestframework_camel_case.parser.CamelCaseFormParser',
            'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
            # Any other parsers
        ),
        'DEFAULT_FILTER_BACKENDS': (
           'djangorestframework_camel_case.ordering.CamelCaseOrderingFilter',
           # Any other filter backends
        ),
    }
    # ...

=================
Swapping Renderer
=================

By default the package uses `rest_framework.renderers.JSONRenderer`. If you want
to use another renderer (the only possible alternative is
`rest_framework.renderers.UnicodeJSONRenderer`, only available in DRF < 3.0), you must specify it in your django
settings file.

.. code-block:: python

    # ...
    JSON_CAMEL_CASE = {
        'RENDERER_CLASS': 'rest_framework.renderers.UnicodeJSONRenderer'
    }
    # ...

=====================
Underscoreize Options
=====================

As raised in https://github.com/krasa/StringManipulation/issues/8#issuecomment-121203018
there are two conventions of snake case.

.. code-block:: text

    # Case 1 (Package default)
    v2Counter -> v_2_counter
    fooBar2 -> foo_bar_2

    # Case 2
    v2Counter -> v2_counter
    fooBar2 -> foo_bar2


By default, the package uses the first case. To use the second case, specify it in your django settings file.

.. code-block:: python

    REST_FRAMEWORK = {
        # ...
        'JSON_UNDERSCOREIZE': {
            'no_underscore_before_number': True,
        },
        # ...
    }

Alternatively, you can change this behavior on a class level by setting `json_underscoreize`:

.. code-block:: python

    from djangorestframework_camel_case.parser import CamelCaseJSONParser
    from rest_framework.generics import CreateAPIView

    class NoUnderscoreBeforeNumberCamelCaseJSONParser(CamelCaseJSONParser):
        json_underscoreize = {'no_underscore_before_number': True}

    class MyView(CreateAPIView):
        queryset = MyModel.objects.all()
        serializer_class = MySerializer
        parser_classes = (NoUnderscoreBeforeNumberCamelCaseJSONParser,)

=============
Running Tests
=============

To run the current test suite, execute the following from the root of he project::

    $ python -m unittest discover


=======
License
=======

* Free software: BSD license
