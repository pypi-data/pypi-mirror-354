{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :show-inheritance:
   :inherited-members: ModelHooks

   {% block methods %}
   .. automethod:: __init__

   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

.. 
      We get error when building doc because lightning uses the :paramref: directive, coming
      from the paramlinks sphinx extension https://pypi.org/project/sphinx-paramlinks/

      Sphinx is not able to not generate errors because an external project is using some extensions...
      see https://github.com/sphinx-doc/sphinx/issues/1530

      We won't add an extension because an external project uses it, so we have to exclude the class
      of lightning that use this directive from the inherited-members: ModelHooks