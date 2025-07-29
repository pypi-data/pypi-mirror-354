|Build Status| |Coverage| |Pypi package| |Pypi status| |Python versions| |License|


==============================================================
DjangoCMS OIDC (OpenID Connect) plugins for Aldryn form fields
==============================================================

Plugins for post a data hangovered from OpenID provider, based on plugins `DjangoCMS OIDC <https://github.com/CZ-NIC/djangocms-oidc/>`_
and `Aldryn Forms <https://github.com/CZ-NIC/djangocms-aldryn-forms>`_.


Installation
============

.. code-block:: shell

    $ pip install djangocms-oidc-form-fields



Add settings to settings.py
---------------------------

Start by making the following changes to your ``settings.py`` file.

.. code-block:: python

   # Add 'aldryn_forms' and 'djangocms_oidc_form_fields' to INSTALLED_APPS
   INSTALLED_APPS = [
       # ...
       'multiselectfield',
       'django_countries',
       'mozilla_django_oidc',  # place after auth (django.contrib.auth)
       'djangocms_oidc',
       'aldryn_forms',
       'djangocms_oidc_form_fields',
   ]

   AUTHENTICATION_BACKENDS = [
       # ...
       'djangocms_oidc.auth.DjangocmsOIDCAuthenticationBackend',
   ]

   MIDDLEWARE = [
       # ...
       'djangocms_oidc.middleware.OIDCSessionRefresh',
   ]

   # Define OIDC classes
   OIDC_AUTHENTICATE_CLASS = "djangocms_oidc.views.DjangocmsOIDCAuthenticationRequestView"
   OIDC_CALLBACK_CLASS = "djangocms_oidc.views.DjangocmsOIDCAuthenticationCallbackView"
   OIDC_OP_AUTHORIZATION_ENDPOINT = "https://example.com/authorization-endpoint"
   OIDC_RP_CLIENT_ID = "myClientId"


Add OIDC urls to urls.py
---------------------------

Modify your project ``urls.py`` file.

.. code-block:: python

    urlpatterns = [
        # ....
        path('oidc/', include('mozilla_django_oidc.urls')),
        path('djangocms-oidc/', include('djangocms_oidc.urls')),
    ]


Usage in administration
=======================

These plugins are available to the editor in the administration:

  * OIDC Fields
  * OIDC Text
  * OIDC Textarea
  * OIDC Hidden
  * OIDC Email
  * OIDC EmailIntoFromField
  * OIDC Phone
  * OIDC Number
  * OIDC Boolean
  * OIDC Span element

How to use provider MojeID
==========================

Home › Djangocms_Oidc › Oidc register consumers › oidc register consumer: Add

 | Name: MojeID Test
 | Register consumer: https://mojeid.regtest.nic.cz/oidc/registration/


Home › Djangocms_Oidc › Oidc providers › oidc provider: add

 | Name: MojeID Test
 | Code: mojeid
 | Register consumer: MojeID Test
 | Authorization endpoint: https://mojeid.regtest.nic.cz/oidc/authorization/
 | Token endpoint: https://mojeid.regtest.nic.cz/oidc/token/
 | User endpoint: https://mojeid.regtest.nic.cz/oidc/userinfo/
 | Account URL: https://mojeid.regtest.nic.cz/editor/
 | Logout URL: https://mojeid.regtest.nic.cz/logout/

Page structure: Add

 | OpenID Connect: OIDC Handover data
 | Provider: MojeID Test
 | Claims: {...} (copy from the example below) For mojeid see list "claims_supported" in .well-known `openid-configuration <https://mojeid.cz/.well-known/openid-configuration>`_.
 | Verified by names: ... (copy from the example below)


How to run an example
=====================

Run the example in Docker. Install as follows:

.. code-block:: shell

    $ git clone https://github.com/CZ-NIC/djangocms-oidc-form-fields.git
    $ cd djangocms-oidc-form-fields/example
    $ docker-compose build web
    $ docker-compose run --user $(id -u):$(id -g) web python manage.py migrate
    $ docker-compose run --user $(id -u):$(id -g) web python manage.py loaddata site.json

You start the webserver:

.. code-block:: shell

    $ docker-compose up -d

Open in your browser: https://localhost:8000/. To log in to the administrations use ``admin:password`` at http://localhost:8000/admin.

You sto Webserver:

.. code-block:: shell

    $ docker-compose down


License
-------

This software is licensed under the GNU GPL license. For more info check the LICENSE file.



.. |Build Status| image:: https://travis-ci.org/CZ-NIC/djangocms-oidc-form-fields.svg?branch=master
    :target: https://travis-ci.org/CZ-NIC/djangocms-oidc-form-fields
    :alt: Build Status
.. |Coverage| image:: https://codecov.io/gh/CZ-NIC/djangocms-oidc-form-fields/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/CZ-NIC/djangocms-oidc-form-fields
    :alt: Coverage
.. |Pypi package| image:: https://img.shields.io/pypi/v/djangocms-oidc-form-fields.svg
    :target: https://pypi.python.org/pypi/djangocms-oidc-form-fields/
    :alt: Pypi package
.. |Pypi status| image:: https://img.shields.io/pypi/status/djangocms-oidc-form-fields.svg
   :target: https://pypi.python.org/pypi/djangocms-oidc-form-fields
   :alt: status
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/djangocms-oidc-form-fields.svg
   :target: https://pypi.python.org/pypi/djangocms-oidc-form-fields
   :alt: Python versions
.. |License| image:: https://img.shields.io/pypi/l/djangocms-oidc-form-fields.svg
    :target: https://pypi.python.org/pypi/djangocms-oidc-form-fields/
    :alt: license
