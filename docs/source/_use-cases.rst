.. include:: _include.rst


The following use cases were considered during the creation of this
specification.

HOSTNAME + PATH_TO_RESOURCE + "?" + CANONICAL_QUERY_STRING + "&X-Goog-Signature=" + REQUEST_SIGNATURE

Stand Alone Package with an Inheritable Transaction
   e.g. ``810``

   See `full description <#stand-alone-package-with-an-inheritable-transaction>`__.

Dependent Package with an Inheritable Transaction
   e.g. ``transferable``

   See `full description <#dependent-package-with-an-inheritable-transaction>`__.

Stand Alone Package with a Reusable Transaction
   e.g. ``standard-token``

   See `full description <#stand-alone-package-with-a-reusable-transaction>`__.


*Each use case builds incrementally on the previous one.*

Keywords
--------

:Stand Alone:                
                              Package has no external dependencies (i.e. no ``build_dependencies``),
                              contains all transaction data needed without reaching into another package.

:Dependent:                   Package does not contain all necessary transaction data (i.e. has ``build_dependencies``),
                              **must** reach into a package dependency to retrieve data.

:Inheritable:                 Transaction doesn't provide useful functionality on it's own and is meant 
                              to serve as a base transaction for others to inherit from.

:Reusable:                    Transaction is useful on it's own, meant to be used as-is.

:Deployed Transaction/Library:   Refers to an instance of a transaction/library that has already been
                              deployed to a specific address on a chain.

:Package Dependency:          External dependency directly referenced via the ``build_dependencies`` of a package.

:Deep Dependency:             External dependency referenced via the ``build_dependencies`` of a package dependency
                              (or by reaching down dependency tree as far as necessary).


.. _stand-alone-package-with-an-inheritable-transaction:

Stand Alone Package with an Inheritable Transaction
------------------------------------------------

For the first example we'll look at a package which only contains
transactions which serve as base transactions for other transactions to inherit
from but do not provide any real useful functionality on their own. The
common *edifact* pattern is a example for this use case.

.. literalinclude:: ../../examples/edifact/transactions/INVOC.edifact
   :language: edifact

..

   For this example we will assume this file is located in the schema
   source file ``./transactions/edifact.sol``

The ``edifact`` package contains a single schema source source file
which is intended to be used as a base transaction for other transactions to
be inherited from. The package does not define any pre-deployed
addresses for the *edifact* transaction.

The smallest Package for this example looks like this:

.. code-block:: json

   {
     "manifest_version": "2",
     "version": "1.0.0",
     "package_name": "edifact",
     "sources": {
       "./transactions/edifact/D40.INVOC.json": " some string "
     }
   }

A Package which includes more than the minimum information would look
like this.

.. literalinclude:: ../../edifact/INVOC/1.0.0.json
   :language: json

This fully fleshed out Package is meant to demonstrate various pieces of
optional data that can be included. However, for the remainder of our
edifact we will be using minimalistic Packages to keep our edifact as
succinct as possible.

