.. only:: asciidoc

   Overview
   ==============

   A data format describing a data interchange transaction specification package.

   Abstract
   ========

   XSEF defines a data format for *package manifest* documents,
   representing a package of one or more data interchange transactions, optionally including
   source code and any/all deployed instances across multiple networks and/or chains. Package
   manifests are minified JSON objects, to be distributed via content
   addressable storage networks.

   This document presents a natural language description of a formal
   specification for version **1** of the `` XSEF `` format.

   Motivation
   ==========

   This standard aims to encourage the Enterprise Transaction ecosystem towards
   software best practices around code reuse. By defining an open,
   community-driven package data format standard, this effort seeks to provide
   support for package management tools development by offering a
   general-purpose solution that has been designed with observed common
   practices in mind.

   As version 1 of this specification this version:

      - Generalizes storage URIs to represent any content addressable URI
        scheme.

      - Forces format strictness, requiring that package manifests contain
        no extraneous whitespace, and sort object keys in alphabetical order,
        to prevent hash mismatches.

      - TODO - FIXME ; import from existing docs 

      - TODO - FIXME ; import from existing docs 

.. only:: not asciidoc

   Overview
   ========

   Background
   ----------

   These docs are meant to provide insight into the XSEF Packaging
   Specification and facilitate implementation and adoption of these standards.

