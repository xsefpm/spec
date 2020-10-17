.. _v1-package-specification:

XSEF Specification [WIP]
======================

.. include:: _include.rst

This document defines the specification for an XsefPM package manifest.
A package manifest provides metadata about a |Package|, and in most cases
should provide sufficient information about the packaged transactions and its
dependencies to do schema verification of its transactions.

.. only:: asciidoc

  .. note:: A `hosted version <http://xsefpm.github.io/xsefpm-spec>`_ of this
      specification is available via GitHub Pages.
----

Design Principles
------------------

This specification makes the following assumptions about the
document lifecycle.

1. Package manifests are intended to be generated programatically by package
   management software as part of the release process.
2. Package manifests will be consumed by package managers during tasks like
   installing package dependencies or building and deploying new
   releases.


----

Conventions
-----------

RFC2119
~~~~~~~

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in RFC 2119.

-  https://www.ietf.org/rfc/rfc2119.txt

Prefixed vs Unprefixed
~~~~~~~~~~~~~~~~~~~~~~

A |prefixed| hexadecimal value begins with ``0x``. |Unprefixed| values
have no prefix. Unless otherwise specified, all hexadecimal values
**should** be represented with the ``0x`` prefix.

  :Prefixed: ``0xdeadbeef``
  :Unprefixed: ``deadbeef``

----

Document Format
---------------

The canonical format is a single JSON object. Packages **must** conform to the
following serialization rules.

-  The document **must** be tightly packed, meaning no linebreaks or
   extra whitespace.
-  The keys in all objects must be sorted alphabetically.
-  Duplicate keys in the same object are invalid.
-  The document **must** use `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`_ encoding.
-  The document **must** not have a trailing newline.
-  To ensure backwards compatibility, `manifest_version` is a forbidden
   top-level key.

----

Document Specification
----------------------

The following fields are defined for the package. Custom fields **may** be
included. Custom fields **should** be prefixed with ``x-`` to prevent
name collisions with future versions of the specification.

  :See Also: Formalized (`JSON-Schema <http://json-schema.org>`_) version of
    this specification: `package.spec.json <https://github.com/xsefpm/xsefpm-spec/blob/master/spec/v1.spec.json>`_
  :Jump To: `Definitions`_

.. _manifest-version:

----

XsefPM Manifest Version: ``manifest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``manifest`` field defines the specification version that
this document conforms to.

  - Packages **must** include this field.

  :Required: Yes
  :Key: ``manifest``
  :Type: String
  :Allowed Values: ``xsefpm/1``

.. _package-names:

----

Package Name: ``name``
~~~~~~~~~~~~~~~~~~~~~~

The ``name`` field defines a human readable name for this package.

  - Packages **should** include this field to be released on an XsefPM registry.
  - Package names **must** begin with a lowercase letter and be comprised of only lowercase
    letters, numeric characters, and the dash character ``-``.
  - Package names **must** not exceed 255 characters in length.

  :Required: If ``version`` is included.
  :Key: ``name``
  :Type: String
  :Format: **must** match the regular expression
    ``^[a-z][-a-z0-9]{0,255}$``

----

Package Version: ``version``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``version`` field declares the version number of this release.
  
  - Packages **should** include this field to be released on an XsefPM registry.
  - This value **should** conform to the `semver <http://semver.org/>`__ version numbering specification.

  :Required: If ``name`` is included.
  :Key: ``version``
  :Type: String

----

Package Metadata: ``meta``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``meta`` field defines a location for metadata about the package
which is not integral in nature for package installation, but may be
important or convenient to have on-hand for other reasons.

  -  This field **should** be included in all Packages.

  :Required: No
  :Key: ``meta``
  :Type: `Package Meta Object`_

----

Sources: ``sources``
~~~~~~~~~~~~~~~~~~~~

The ``sources`` field defines a source tree that **should** comprise the
full source tree necessary to recompile the transactions contained in this
release.

  :Required: No
  :Key: ``sources``
  :Type: Object (String: `Sources Object`_)

----

Transaction Types: ``transactionTypes``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``transactionTypes`` field hosts the |TransactionTypes| which have been
included in this release.

  - Packages **should** only include transaction types that can be found in the source files for this package.
  - Packages **should not** include transaction types from dependencies.
  - Packages **should not** include abstract transactions in the transaction types section of a release.

  :Required: No
  :Key: ``transactionTypes``
  :Type: Object (String: `Transaction Type Object`_)
  :Format:
    - Keys **must** be valid |TransactionAliases|.
    - Values **must** conform to the `Transaction Type Object`_ definition.

----

Transaction Groups: ``transaction groups``
~~~~~~~~~~~~~~~~~~~~~~~~

The ``transaction groups`` field holds the information about the transaction groups and their
issuing agency (e.g. ASC or U.N). These determine the settings that can be used to generate 
the various ``transactionTypes`` included in this release.

  :Required: Yes 
  :Key: ``transaction groups``
  :Type: Array (`the Transaction Group Information object`_)

----

Deployments: ``deployments``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``deployments`` field holds the information for the |Trading Channel| insance on which
this release has |TransactionInstances| as well as the |TransactionTypes|
and other deployment details for those deployed transaction instances.
The set of insance defined by the :ref:`BIP122 URI<bip122-bip122-1>` keys for this
object **must** be unique. There cannot be two different URI keys in a deployments
field representing the same blockchain.

  :Required: No
  :Key: ``deployments``
  :Type: Object (String: Object(String: `Transaction Instance Object`_))
  :Format:
    - Keys **must** be a valid URI/BIP122 URI URL and/or chain definition.
    - Values **must** be objects which conform to the following format.
        -  Keys **must** be valid |TransactionInstanceNames|.
        -  Values **must** be a valid `Transaction Instance Object`_.

----

Build Dependencies: ``buildDependencies``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``buildDependencies`` field defines a key/value mapping of XSEF
|Packages| that this project depends on.

  :Required: No
  :Key: ``buildDependencies``
  :Type: Object (String: String)
  :Format:
    - Keys **must** be valid `package-names`_.
    - Values **must** be a |ContentAddressableURI| which resolves to a valid package that conforms the same XsefPM manifest version as its parent.

----

Definitions
-----------

Definitions for different objects used within the Package. All objects
allow custom fields to be included. Custom fields **should** be prefixed
with ``x-`` to prevent name collisions with future versions of the
specification.

----

.. _link-reference-object:

The *Link Reference* Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A |LinkReference| object has the following key/value pairs. All
link references are assumed to be associated with some corresponding
|Schema|.

Offsets: ``offsets``
^^^^^^^^^^^^^^^^^^^^

The ``offsets`` field is an array of integers, corresponding to each of the
start positions where the link reference appears in the schema.
Locations are 0-indexed from the beginning of the bytes representation of
the corresponding schema.  This field is invalid if it references a position
that is beyond the end of the schema.

  :Required: Yes
  :Type: Array

Length: ``length``
^^^^^^^^^^^^^^^^^^

The ``length`` field is an integer which defines the length in bytes
of the link reference. This field is invalid if the end of the defined
link reference exceeds the end of the schema.

  :Required: Yes
  :Type: Integer

Name: ``name``
^^^^^^^^^^^^^^

The ``name`` field is a string which **must** be a valid |Identifier|.
Any link references which **should** be linked with the same
link value **should** be given the same name.

  :Required: No
  :Type: String
  :Format: **must** conform to the |Identifier| format.

----

.. _Link-value-object:

The *Link Value* Object
~~~~~~~~~~~~~~~~~~~~~~~

Describes a single |LinkValue|.

A **Link Value object** is defined to have the following key/value pairs.

.. _offset-offset-1:

Offsets: ``offsets``
^^^^^^^^^^^^^^^^^^^^

The ``offsets`` field defines the locations within the corresponding schema
where the ``value`` for this link value was written.  These locations are
0-indexed from the beginning of the bytes representation of the
corresponding schema.

  :Required: Yes
  :Type: Integer
  :Format: See Below.

**Format**

Array of integers, where each integer **must** conform to all of the following.

   -  greater than or equal to zero
   -  strictly less than the length of the unprefixed hexadecimal
      representation of the corresponding schema.

Type: ``type``
^^^^^^^^^^^^^^

The ``type`` field defines the ``value`` type for determining what is encoded
when |linking| the corresponding schema.

  :Required: Yes
  :Type: String
  :Allowed Values:
      ``"literal"`` for schema literals

      ``"reference"`` for named references to a particular |TransactionInstance|

Value: ``value``
^^^^^^^^^^^^^^^^

The ``value`` field defines the value which should be written when
|linking| the corresponding schema.

  :Required: Yes
  :Type: String
  :Format: Determined based on ``type``, see below.

**Format**

For static value *literals* (e.g. address), value **must** be a
*byte string*

To reference the address of a |TransactionInstance| from the current
package the value should be the name of that transaction instance.

    -  This value **must** be a valid |TransactionInstanceName|.
    -  The chain definition under which the transaction instance that this
       link value belongs to must contain this value within its keys.
    -  This value **may not** reference the same transaction instance that
       this link value belongs to.

To reference a transaction instance from a |Package| from somewhere
within the dependency tree the value is constructed as follows.

    -  Let ``[p1, p2, .. pn]`` define a path down the dependency tree.
    -  Each of ``p1, p2, pn`` **must** be valid package names.
    -  ``p1`` **must** be present in keys of the ``build_dependencies`` for
       the current package.
    -  For every ``pn`` where ``n > 1``, ``pn`` **must** be present in the
       keys of the ``build_dependencies`` of the package for ``pn-1``.
    -  The value is represented by the string
       ``<p1>:<p2>:<...>:<pn>:<transaction-instance>`` where all of ``<p1>``,
       ``<p2>``, ``<pn>`` are valid package names and
       ``<transaction-instance>`` is a valid |TransactionName|.
    -  The ``<transaction-instance>`` value **must** be a valid
       |TransactionInstanceName|.
    -  Within the package of the dependency defined by ``<pn>``, all of the
       following must be satisfiable:

       -  There **must** be *exactly* one chain defined under the
          ``deployments`` key which matches the chain definition that this
          link value is nested under.

       -  The ``<transaction-instance>`` value **must** be present in the keys
          of the matching chain.

----

The *Schema* Object
~~~~~~~~~~~~~~~~~~~~~

A schema object has the following key/value pairs.

Schema: ``schema``
^^^^^^^^^^^^^^^^^^^^^^

The ``schema`` field is a string containing the ``0x`` prefixed
hexadecimal representation of the schema.

  :Required: Yes
  :Type: String
  :Format: ``0x`` prefixed hexadecimal.


Link References: ``linkReferences``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``linkReferences`` field defines the locations in the corresponding
schema which require |linking|.

  :Required: No
  :Type: Array
  :Format: All values **must** be valid :ref:`Link Reference objects <link-reference-object>`.
    See also below.

**Format**

This field is considered invalid if *any* of the |LinkReferences| are
invalid when applied to the corresponding ``schema`` field, *or* if
any of the link references intersect.

Intersection is defined as two link references which overlap.

Link Dependencies: ``linkDependencies``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``linkDependencies`` defines the |LinkValues| that have been used
to link the corresponding schema.

  :Required: No
  :Type: Array
  :Format: All values **must** be valid :ref:`Link Value objects <link-value-object>`.
    See also below.

**Format**

Validation of this field includes the following:

-  Two link value objects **must not** contain any of the same values for
   ``offsets``.

-  Each :ref:`link value object <link-value-object>` **must** have a
   corresponding :ref:`link reference object <link-reference-object>` under
   the ``linkReferences`` field.

-  The length of the resolved ``value`` **must** be equal to the
   ``length`` of the corresponding |LinkReference|.

----

.. _Package Meta Object:

The *Package Meta* Object
~~~~~~~~~~~~~~~~~~~~~~~~~

The *Package Meta* object is defined to have the following key/value pairs.

Authors: ``authors``
^^^^^^^^^^^^^^^^^^^^

The ``authors`` field defines a list of human readable names for the
authors of this package. Packages **may** include this field.

  :Required: No
  :Key: ``authors``
  :Type: Array (String)

.. _Meta License:

License: ``license``
^^^^^^^^^^^^^^^^^^^^

The ``license`` field declares the license associated with this
package. This value **should** conform to the
`SPDX <https://en.wikipedia.org/wiki/Software_Package_Data_Exchange>`__
format. Packages **should** include this field. If a file `Source Object`_
defines its own license, that license takes precedence for that particular
file over this package-scoped ``meta`` license.

  :Required: No
  :Key: ``license``
  :Type: String

Description: ``description``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``description`` field provides additional detail that may be
relevant for the package. Packages **may** include this field.

  :Required: No
  :Key: ``description``
  :Type: String

Keywords: ``keywords``
^^^^^^^^^^^^^^^^^^^^^^

The ``keywords`` field provides relevant keywords related to this
package.

  :Required: No
  :Key: ``keywords``
  :Type: Array(String)

Links: ``links``
^^^^^^^^^^^^^^^^

The ``links`` field provides URIs to relevant resources associated with
this package. When possible, authors **should** use the following keys
for the following common resources.

  - ``website``: Primary website for the package.
  - ``documentation``: Package Documentation
  - ``repository``: Location of the project source code.

  :Key: ``links``

  :Type: Object (String: String)

----

.. _Sources Object:

The *Sources* Object
~~~~~~~~~~~~~~~~~~~~

A *Sources* object is defined to have the following fields.

  :Key: A unique identifier for the source file. (string)
  :Value: `SourceObject`_

.. _SourceObject:

Source Object
^^^^^^^^^^^^^

Checksum: ``checksum``
^^^^^^^^^^^^^^^^^^^^^^

Hash of the source file.

  :Required: **If** there are no URLs present that contain a content hash.
  :Key: ``checksum``
  :Value: `ChecksumObject`_

URLs: ``urls``
^^^^^^^^^^^^^^
Array of urls that resolve to the same source file.
  - Urls **should** be stored on a content-addressable filesystem. **If** they are not, then either ``content``
    or ``checksum`` **must** be included.
  - Urls **must** be prefixed with a scheme.
  - If the resulting document is a directory the key **should** be interpreted as a directory path.
  - If the resulting document is a file the key **should** be interpreted as a file path.

  :Required: If ``content`` is not included.
  :Key: ``urls``
  :Value: Array(string)

Content: ``content``
^^^^^^^^^^^^^^^^^^^^
Inlined transaction source.

  :Required: If ``urls`` is not included.
  :Key: ``content``
  :Value: string

Install Path: ``installPath``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Filesystem path of source file.
  - **Must** be a relative filesystem path that begins with a ``./``.
  - **Must** resolve to a path that is within the current virtual working directory.
  - **Must** be unique across all included sources.

  :Required: This field **must** be included for the package to be writable to disk.
  :Key: ``installPath``
  :Value: string

Type: ``type``
^^^^^^^^^^^^^^

The ``type`` field declares the type of the source file. The field **should** be one
of the following values: ``solidity``, ``vyper``, ``abi-json``, ``solidity-ast-json``. 

  :Required: No
  :Key: ``type``
  :Type: String

License: ``license``
^^^^^^^^^^^^^^^^^^^^

The ``license`` field declares the type of license associated with
this source file. When defined, this license overrides the
package-scoped `Meta License`_.

  :Required: No
  :Key: ``license``
  :Type: String

----

.. _ChecksumObject:

The *Checksum* Object
~~~~~~~~~~~~~~~~~~~~~~~~~~

A *Checksum* object is defined to have the following key/value pairs.

Algorithm: ``algorithm``
^^^^^^^^^^^^^^^^^^^^^^^^

The ``algorithm`` used to generate the corresponding hash.

  :Required: Yes
  :Type: String

Hash: ``hash``
^^^^^^^^^^^^^^

The ``hash`` of a source files contents generated with the corresponding algorithm.

  :Required: Yes
  :Type: String

----

.. _Transaction Type Object:

The *Transaction Type* Object
~~~~~~~~~~~~~~~~~~~~~~~~~~

A *Transaction Type* object is defined to have the following key/value pairs.

Transaction Name: ``transactionName``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``transactionName`` field defines the |TransactionName| for this
|TransactionType|.

  :Required: If the |TransactionName| and |TransactionAlias| are not the
   same.
  :Type: String
  :Format: **Must** be a valid |TransactionName|.

Source ID: ``sourceId``
^^^^^^^^^^^^^^^^^^^^^^^
The global source identifier for the source file from which this transaction type was generated.

  :Required: No
  :Type: String
  :Value: **Must** match a unique source ID included in the `Sources Object`_ for this package.

Deployment Schema: ``deploymentSchema``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``deploymentSchema`` field defines the schema for this |TransactionType|.

  :Required: No
  :Type: Object
  :Format: **Must** conform to `the Schema Object`_ format.

Grammar Schema: ``grammarSchema``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``grammarSchema`` field defines the unlinked ``0x``-prefixed
grammar portion of |Schema| for this |TransactionType|.

  :Required: Yes
  :Type: Object
  :Format: **Must** conform to `the Schema Object`_ format.

ABI: ``abi``
^^^^^^^^^^^^

  :Required: No
  :Type: Array
  :Format: **Must** conform to the `Ethereum Transaction ABI JSON format <https://github.com/ethereum/wiki/wiki/Ethereum-Transaction-ABI#json>`_.

UserDoc: ``userdoc``
^^^^^^^^^^^^^^^^^^^^

  :Required: No
  :Type: Object
  :Format: **Must** conform to the `UserDoc <https://github.com/ethereum/wiki/wiki/Ethereum-Natural-Specification-Format#user-documentation>`_ format.

DevDoc: ``devdoc``
^^^^^^^^^^^^^^^^^^^^

  :Required: No
  :Type: Object
  :Format: **Must** conform to the `DevDoc <https://github.com/ethereum/wiki/wiki/Ethereum-Natural-Specification-Format#developer-documentation>`_ format.

----

.. _Transaction Instance Object:

The *Transaction Instance* Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **Transaction Instance Object** represents a single deployed |TransactionInstance|
and is defined to have the following key/value pairs.

Transaction Type: ``transactionType``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``transactionType`` field defines the |TransactionType| for this
|TransactionInstance|. This can reference any of the transaction types
included in this |Package| *or* any of the transaction types found in any
of the package dependencies from the ``buildDependencies`` section of
the |PackageManifest|.

  :Required: Yes
  :Type: String
  :Format: See Below.

**Format**

Values for this field **must** conform to *one of* the two formats herein.

To reference a transaction type from this Package, use the format
``<transaction-alias>``.

-  The ``<transaction-alias>`` value **must** be a valid |TransactionAlias|.
-  The value **must** be present in the keys of the ``transactionTypes``
   section of this Package.

To reference a transaction type from a dependency, use the format
``<package-name>:<transaction-alias>``.

-  The ``<package-name>`` value **must** be present in the keys of the
   ``buildDependencies`` of this Package.
-  The ``<transaction-alias>`` value **must** be be a valid |TransactionAlias|.
-  The resolved package for ``<package-name>`` must contain the
   ``<transaction-alias>`` value in the keys of the ``transactionTypes``
   section.

.. _address:

Contract Address: ``contract_address``
^^^^^^^^^^^^^^^^^^^^

The ``contract_address`` field defines the |Contract Address| of the |TransactionInstance|.

  :Required: Yes
  :Type: String
  :Format: Hex encoded ``0x`` prefixed Ethereum address matching the
   regular expression ``^0x[0-9a-fA-F]{40}$``.

Transaction: ``transaction``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``transaction`` field defines the transaction hash in which this
|TransactionInstance| was created.

  :Required: No
  :Type: String
  :Format: ``0x`` prefixed hex encoded transaction hash.

Block: ``block``
^^^^^^^^^^^^^^^^

The ``block`` field defines the block hash in which this the transaction
which created this *transaction instance* was mined.

  :Required: No
  :Type: String
  :Format: ``0x`` prefixed hex encoded block hash.

.. _grammar-schema-grammar_schema-1:

grammar Schema: ``grammarSchema``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``grammarSchema`` field defines the grammar portion of schema for this
|TransactionInstance|.  When present, the value from this field supersedes
the ``grammarSchema`` from the |TransactionType| for this |TransactionInstance|.

  :Required: No
  :Type: Object
  :Format: **must** conform to `the Schema Object`_ format.

Every entry in the ``linkReferences`` for this schema **must** have a
corresponding entry in the ``linkDependencies`` section.

----

.. _transaction group information object:

The *Transaction Group Information* Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``transaction groups`` field defines the various transaction groups and settings used
during compilation of any |TransactionTypes| or |TransactionInstance| included in this pacakge.

A *Transaction Group Information* object is defined to have the following
key/value pairs.

Name ``name``
^^^^^^^^^^^^^

The ``name`` field defines which transaction group was used in compilation.

  :Required: Yes
  :Key: ``name``
  :Type: String

.. _version-version-1:

Version: ``version``
^^^^^^^^^^^^^^^^^^^^

The ``version`` field defines the version of the transaction group. The field
**should** be OS agnostic (OS not included in the string) and take the
form of either the stable version in `semver <http://semver.org/>`__ format or if built on a
nightly should be denoted in the form of ``<semver>-<commit-hash>`` ex:
``0.4.8-commit.60cc1668``.

  :Required: Yes
  :Key: ``version``
  :Type: String

Settings: ``settings``
^^^^^^^^^^^^^^^^^^^^^^

The ``settings`` field defines any settings or configuration that was
used.

  :Required: No
  :Key: ``settings``
  :Type: Object

Transaction Types: ``transactionTypes``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A list of the |TransactionAlias| in this package that used this transaction group to generate its outputs. 

  - All ``transactionTypes`` that locally declare ``grammarSchema`` **should** be attributed for by a transaction group object.
  - A single ``transactionTypes`` **must** not be attributed to more than one transaction group.

  :Required: No
  :Key: ``transactionTypes``
  :Type: Array(|TransactionAlias|)

----

.. _bip122-bip122-1:

BIP122 URIs
~~~~~~~~~~~

BIP122 URIs are used to define a blockchain via a subset of the
`BIP-122 <https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki>`__
spec.

::

   blockchain://<genesis_hash>/block/<latest confirmed block hash>

The ``<genesis hash>`` represents the blockhash of the first block on
the chain, and ``<latest confirmed block hash>`` represents the hash of
the latest block that's been reliably confirmed (package managers should
be free to choose their desired level of confirmations).
