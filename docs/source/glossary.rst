Glossary
========

Terms utilized throughout the specification 

.. include:: _include.rst

.. glossary::

   API
      The JSON representation of the application programming interface. `see Open EDI`

   Address
      A public identifier for an account on a particular chain or URI

      **Example**: `` HOSTNAME + PATH_TO_RESOURCE + "?" + CANONICAL_QUERY_STRING + "&X-Goog-Signature=" + REQUEST_SIGNATURE ``

   Schema
      The XSD or JSON-Schema defining the Trading Channel 

      Schema can either be linked or unlinked. (see |Linking|)

      :Unlinked Schema: 
         The sections of code which are unlinked **must** be filled in with zero bytes.

         **Example**: `` <FIXME> ``

      :Linked Schema: A representation of a non-standard schema.
         The Schema utilizes a |LinkReferences| to an Unlinked Schema, and can be replaced with the
         desired |LinkValues|.

         **Example**: `` <FIXME>  ``

   Chain Definition
      This definition originates from `BIP122 URI <https://github.com/bitcoin/bips/blob/master/bip-0122.mediawiki>`__.

      A URI in the format ``blockchain://<chain_id>/block/<block_hash>``

      -  ``chain_id`` is the unprefixed hexadecimal representation of the
         genesis hash for the chain.
      -  ``block_hash`` is the unprefixed hexadecimal representation of the
         hash of a block on the chain.

      A chain is considered to match a chain definition if the the genesis
      block hash matches the ``chain_id`` and the block defined by
      ``block_hash`` can be found on that chain. It is possible for multiple
      chains to match a single URI, in which case all chains are considered
      valid matches

   Content Addressable URI
      Any URI which contains a cryptographic hash which can be used to verify
      the integrity of the content found at the URI.

      The URI format is defined in RFC3986

      **Example**: `` HOSTNAME + PATH_TO_RESOURCE + "?" + CANONICAL_QUERY_STRING + "&X-Goog-Signature=" + REQUEST_SIGNATURE ``

   Transaction Alias
      This is a name used to reference a specific |TransactionType|. Transaction
      aliases **must** be unique within a single |Package|.

      The transaction alias **must** use *one of* the following naming schemes:

      -  ``<transaction-name>``
      -  ``<transaction-name><identifier>``

      The ``<transaction-name>`` portion **must** be the same as the
      |TransactionName| for this transaction type.

      The ``<identifier>`` portion **must** match the regular expression
      ``^[-a-zA-Z0-9]{1,256}$``.

   Transaction Instance
      A transaction instance a specific deployed version of a |TransactionType|.

      All transaction instances have an |Address| on some specific chain.

   Transaction Instance Name
      A name which refers to a specific |TransactionInstance| on a specific
      chain from the deployments of a single |Package|. This name **must** be
      unique across all other transaction instances for the given chain. The
      name must conform to the regular expression
      ``^[a-zA-Z_$][a-zA-Z0-9_$]{0,255}$``

      In cases where there is a single deployed instance of a given
      |TransactionType|, package managers **should** use the |TransactionAlias| for
      that transaction type for this name.

      In cases where there are multiple deployed instances of a given
      transaction type, package managers **should** use a name which provides
      some added semantic information as to help differentiate the two
      deployed instances in a meaningful way.

   Transaction Name
      The name found in the source code that defines a specific |TransactionType|.
      These names **must** conform to the regular expression
      ``^[a-zA-Z_$][a-zA-Z0-9_$]{0,255}$``.

      There can be multiple transactions with the same transaction name in a
      projects source files.

   Transaction Type
      Refers to a specific transaction in the package source.
      This term can be used to refer to an abstract transaction, a normal
      transaction, or a library. Two transactions are of the same transaction type if
      they have the same bytecode.

      Example:

      ::

         transaction edifact.INVOC {
             ...
         }

      A deployed instance of the ``INVOC`` transaction would be of of type
      ``INVOC``.

   Identifier
      Refers generally to a named entity in the |Package|.

      A string matching the regular expression ``^[a-zA-Z][-_a-zA-Z0-9]{0,255}$``

   Link Reference
      A location within a transaction's bytecode which needs to be linked.  A link
      reference has the following properties.

        :``offset``: Defines the location within the bytecode where the
          link reference begins.
        :``length``: Defines the length of the reference.
        :``name``: (optional.) A string to identify the reference

   Link Value
      A link value is the value which can be inserted in place of a
      |LinkReference|

   Linking
      The act of replacing |LinkReferences| with |LinkValues| within some
      |Schema|.

   Package
      Distribution of an application's source or compiled bytecode along with
      metadata related to authorship, license, versioning, et al.

      For brevity, the term **Package** is often used metonymously to mean
      |PackageManifest|.

   Package Manifest
      A machine-readable description of a package (See
      :ref:`v2-package-specification` for information about the format for package
      manifests.)

   Prefixed
      |Schema| string with leading ``0x``.

        :Example: ``0xdeadb33f``

   Unprefixed
      Not |Prefixed|.

        :Example: ``deadb33f``
