====================================================================================================
bisos.myLinkedIn: takes contents of Basic\ :sub:`LinkedInDataExport`.zip and converts them to Vcards
====================================================================================================

.. contents::
   :depth: 3
..

Overview
========

*bisos.myLinkedIn* takes contents of
Basic\ :sub:`LinkedInDataExport`.zip and converts them to vCards for
your connections and then augments them with the *Contact info* of your
first-level connections. The purpose of *bisos.myLinkedIn* is to
facilitate convenient communication with your first-level connections
**outside of LinkedIn**. *bisos.myLinkedIn* is structured as two layers.

-  *Layer 1* – **myLinkedIn.cs** – Operates purely on the content of
   Basic\ :sub:`LinkedInDataExport`.zip. Connections.csv is used to
   create VCards for each of your connections. Invitations.csv is then
   used to augment the VCards. Messages.csv is converted to maildir
   format for reading using your own MUA (Mail User Agent). The email
   address (and other contact info) of only about one-fourth of your
   first-level connections is in Connections.csv. Uses of Layer 1 do not
   violate LinkedIn policies in any way.

-  *Layer 2* – **myLinkedinWeb.cs** – Uses *layer 1* and enriches it
   with the *Contact info* for each of the vCards. The email address
   (and other contact info) of most of your first-level connections is
   not available in *layer 1*. **myLinkedinWeb.cs** goes to your
   first-level connections' home page, clicks on the *Contact info*,
   obtains email and other contact info from the web, and adds it to the
   vCards. Some may say that uses of Layer 2 do violate LinkedIn
   policies. I don't think so. In my view, what **myLinkedinWeb.cs**
   does falls in the category of fair and reasonable use. I have been on
   LinkedIn for more than 20 years and I expect to have convenient
   access to the *Contact info* of my connections. If LinkedIn considers
   this use not acceptable, then it should include the *Contact info* of
   **ALL** of my connections in Basic\ :sub:`LinkedInDataExport`.zip.
   Does LinkedIn really expect me to keep my vCards current manually?

*bisos.myLinkedIn* is a python package that uses the
`PyCS-Framework <https://github.com/bisos-pip/pycs>`__. It is a
BISOS-Capability and a Standalone-BISOS-Package.

The *bisos.linkedin* package automates the process of transforming
LinkedIn export data (.csv) into enriched vCards (.vcf), specifically
focusing on the first-level connections present in your LinkedIn data.
LinkedIn’s export includes valuable information about your
connections—such as names, job titles, company details, and
invitations—that naturally fits into a contact management system like
vCards. However, contact info (email, phone, etc.) of most connections
is not included in the Basic\ :sub:`LinkedInDataExport`.zip file. By
leveraging this package, you can convert, enrich, and augment these
details into vCards that are readily importable into your preferred
usage environment (e.g., Emacs ebdb, MS Outlook, or any other
vCard-compatible system). This process is repeatable and scalable,
making it easier to maintain an up-to-date contact database, effectively
integrating LinkedIn connection data into your daily workflow.

Other than adding the *Contact info* information of your first-level
connections to the vCards, the *bisos.myLinkedIn* package does not
support any form of Web Scraping.

Package Documentation At Github
===============================

The information below is a subset of the full of documentation for this
bisos-pip package. More complete documentation is available at:
https://github.com/bisos-pip/capability-cs

.. _table-of-contents:

Table of Contents TOC
=====================

-  `Overview <#overview>`__
-  `Package Documentation At
   Github <#package-documentation-at-github>`__
-  `A Standalone Command-Services PyCS Facility of
   BISOS <#a-standalone-command-services-pycs-facility-of-bisos>`__
-  `Inputs <#inputs>`__

   -  `Layer-1 –
      Basic\ LinkedInDataExport.zip <#layer-1----basic_linkedindataexportzip>`__
   -  `Layer-2 – Web Connect Info <#layer-2----web-connect-info>`__

-  `Outpts <#outpts>`__

   -  `VCards <#vcards>`__
   -  `Maildirs <#maildirs>`__

-  `Layer-1 – myLinkedIn.cs – Diagram and Software–Diagram
   Mapping <#layer-1----mylinkedincs----diagram-and-softwarediagram-mapping>`__

   -  `Key Features of Layer-1 –
      myLinkedIn.cs <#key-features-of-layer-1----mylinkedincs>`__

-  `Layer-2 – myLinkedInWeb.cs – Diagram and Software–Diagram
   Mapping <#layer-2----mylinkedinwebcs----diagram-and-softwarediagram-mapping>`__

   -  `Key Features of Layer-2 –
      myLinkedInWeb.cs <#key-features-of-layer-2----mylinkedinwebcs>`__

-  `Common Usages – Diagram <#common-usages----diagram>`__
-  `Common Usages <#common-usages>`__
-  `Benefits – Distinct and
   Different <#benefits----distinct-and-different>`__
-  `Installation <#installation>`__

   -  `Installation With pipx <#installation-with-pipx>`__
   -  `Installation With pip <#installation-with-pip>`__

-  `Layer-1 Usage <#layer-1-usage>`__
-  `Layer-2 Usage <#layer-2-usage>`__
-  `Documentation and Blee-Panels <#documentation-and-blee-panels>`__

   -  `bisos.myLinkedIn Blee-Panels <#bisosmylinkedin-blee-panels>`__

-  `Support <#support>`__
-  `Credits <#credits>`__

A Standalone Command-Services PyCS Facility of BISOS
====================================================

Layered on top of Debian, **BISOS** (By\* Internet Services Operating
System) is a unified and universal framework for developing both
internet services and software-service continuums that use internet
services. PyCS (Python Command-Services) of BISOS is a framework that
converges development of CLI and Services. See the `Nature of
Polyexistentials <https://github.com/bxplpc/120033>`__ book for
additional information.

bisos.myLinkedIn is a standalone piece of BISOS. It can be used as a
self-contained Python package separate from BISOS.

Inputs
======

Layer-1 – Basic\ :sub:`LinkedInDataExport`.zip
----------------------------------------------

-  **Connections.csv**: The basic connection data, including LinkedIn
   ID, profile URL, name, etc.
-  **Invitations.csv**: Captures whether you invited the connection or
   were invited, along with the invitation text.
-  **Messages.csv**: Adds LinkedIn message history between you and your
   connections, showing the conversation details and direction.

Layer-2 – Web Connect Info
--------------------------

-  email
-  websites
-  phones

Outpts
======

VCards
------

**Connections.csv** and **Invitations.csv** inputs and Web Connect Info
are transformed into a series of VCards (.vcf) – one for each
connection.

Maildirs
--------

**Messages.csv** is converted into maildir format.

Layer-1 – **myLinkedIn.cs** – Diagram and Software–Diagram Mapping
==================================================================

The figure above, provides an overview of Layer-1.

A brief description of the nodes is provided below.

+-----------------+------------------------+------------------------+
| Diagram Node    | Software               | Description            |
|                 | Component/Class        |                        |
+=================+========================+========================+
| LinkedIn        | Data Source (LinkedIn) | Origin of all LinkedIn |
|                 |                        | user data              |
+-----------------+------------------------+------------------------+
| Export.zip      | Raw Input              | Downloaded export ZIP  |
|                 |                        | file from LinkedIn     |
+-----------------+------------------------+------------------------+
| ExportedData    | Unzipped Data          | Directory containing   |
|                 | Directory              | CSV and JSON files     |
+-----------------+------------------------+------------------------+
| Connections.csv | LinkedInConnections    | Parses first-level     |
|                 |                        | connections            |
+-----------------+------------------------+------------------------+
| Invitations.csv | LinkedInInvitations    | Parses sent and        |
|                 |                        | received invitations   |
+-----------------+------------------------+------------------------+
| VCard           | VCardUtils / Core      | Base vCards from       |
|                 | Output                 | LinkedIn data          |
+-----------------+------------------------+------------------------+
| Messages.csv    | LinkedInMessages       | Parses message         |
|                 |                        | exchanges with         |
|                 |                        | connections            |
+-----------------+------------------------+------------------------+
| Maildir         | messages               | Enriched vCards with   |
|                 |                        | remote and external    |
|                 |                        | information            |
+-----------------+------------------------+------------------------+

Key Features of Layer-1 – myLinkedIn.cs
---------------------------------------

The \`bisos.myLinkedIn\` Layer-1 Python package provides a set of
utilities for creating a set of vCards for your first-level LinkedIn
connections based on the **Basic\ LinkedInDataExport**. It creates rich
representations of your LinkedIn network in vCard (.vcf) format.

-  VCard Creation:

   Based on data from \`Connections.csv\` a VCard is created for each
   contact. This VCard will then be augmented and enriched.

-  VCard Local Augmentation:

   Augments vCards with data from \`Invitations.csv`. For each contact,
   the invitation status is captured (whether you invited the connection
   or vice versa) and the invitation message text is added to the vCard.

-  Maildir Conversion:

   With data from \`Messages.csv`, maildirs are created. Conversation
   details are added from **Messages.csv**, organizing the messages in
   chronological order with sender information.

Layer-2 – **myLinkedInWeb.cs** – Diagram and Software–Diagram Mapping
=====================================================================

The figure above, provides an overview of Layer-2. Layer-2 builds on
Layer-1 by enriching the vCards with the information obtained from the
*Contact Info* for each VCard.

A brief description of the relevant nodes is provided below.

+--------------+--------------------------+--------------------------+
| Diagram Node | Software Component/Class | Description              |
+==============+==========================+==========================+
| ContactInfo  | Remote Augmentation      | Scraped contact details  |
|              | Logic                    | from LinkedIn website    |
+--------------+--------------------------+--------------------------+
| VCard        | VCardUtils / Core Output | Base vCards from         |
|              |                          | LinkedIn data            |
+--------------+--------------------------+--------------------------+

Key Features of Layer-2 – myLinkedInWeb.cs
------------------------------------------

Layer-2 is about Remote enrichment of Layer-1 VCard.

-  Web Contact Info Retrieval:

Extracts additional details from LinkedIn's Contact Info page via
automated scraping, such as email addresses, phone numbers, and other
publicly available contact information.

-  Addition of Contact Info to Local VCard:

Common Usages – Diagram
=======================

The figure above, provides an overview of how MyLinkedIn (Layers-1 and
Layer-2) are commonly used.

A brief description of the relevant nodes is provided below.

+--------------+--------------------------+--------------------------+
| Diagram Node | Software Component/Class | Description              |
+==============+==========================+==========================+
| External     | User-supplied Sources    | Any third-party or       |
|              |                          | user-maintained source   |
|              |                          | of data                  |
+--------------+--------------------------+--------------------------+
| ExternalInfo | External Data Processor  | Prepares and aligns      |
|              |                          | external info for        |
|              |                          | enrichment               |
+--------------+--------------------------+--------------------------+
| VCard        | VCardUtils / Core Output | Base vCards from         |
|              |                          | LinkedIn data            |
+--------------+--------------------------+--------------------------+
| VCardPlus    | VCardAugmentor           | Enriched vCards with     |
|              |                          | remote and external      |
|              |                          | information              |
+--------------+--------------------------+--------------------------+

Common Usages
=============

-  Seamless Repeatable VCard Generation and Re-Generation:

   The tool automatically converts your first-level LinkedIn connections
   into individual vCard files, using the unique LinkedIn ID as the file
   name. Periodically, you re-generate these.

-  External Augmentation: Optionally integrates with external services
   for contact enrichment to further enhance your vCards with data such
   as job titles, company names, and social profiles.

-  Output vCards are ready for import into other systems (e.g., address
   books, contacts app, Outlook, ebdb).

-  With LinkedIn vCards addresses now in your address book, you can now
   use MTDT (Mail Templating and Distribution and Tracking) to engage in
   mass communications with your LinkedIn connections through email
   (outside of LinkedIn).

Benefits – Distinct and Different
=================================

Open-Source, Self-Hosted Solution: This package offers a self-hosted,
open-source solution that gives users complete control over their
LinkedIn data and privacy, without relying on third-party SaaS
platforms.

This holistic, self-contained solution for augmenting LinkedIn data with
multiple sources and outputting it in a standardized vCard format makes
our approach unique in the landscape of LinkedIn data tools.

Installation
============

The sources for the bisos.myLinkedIn pip package are maintained at:
https://github.com/bisos-pip/linkedinVcard.

The bisos.myLinkedIn pip package is available at PYPI as
https://pypi.org/project/bisos.myLinkedIn

You can install bisos.myLinkedIn with pipx or pip.

Installation With pipx
----------------------

If you only need access to bisos.myLinkedIn on the command line, you can
install it with pipx:

.. code:: bash

   pipx install bisos.myLinkedIn

The following commands are made available:

-  myLinkedIn.cs
-  myLinkedInWeb.cs

Installation With pip
---------------------

If you need access to bisos.myLinkedIn as a Python module, you can
install it with pip:

.. code:: bash

   pip install bisos.myLinkedIn

Layer-1 Usage
=============

.. code:: bash

   bin/myLinkedIn.cs

Layer-2 Usage
=============

.. code:: bash

   bin/myLinkedInWeb.cs

Documentation and Blee-Panels
=============================

bisos.myLinkedIn is part of the ByStar Digital Ecosystem
http://www.by-star.net.

This module's primary documentation is in the form of Blee-Panels.
Additional information is also available in:
http://www.by-star.net/PLPC/180047

bisos.myLinkedIn Blee-Panels
----------------------------

bisos.myLinkedIn Blee-Panels are in the ./panels directory. From within
Blee and BISOS, these panels are accessible under the Blee "Panels"
menu.

See
`file:./panels/_nodeBase_/fullUsagePanel-en.org <./panels/_nodeBase_/fullUsagePanel-en.org>`__
for a starting point.

Support
=======

| For support, criticism, comments, and questions, please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact

Credits
=======

ChatGPT initial implementation is at: myLinkedIn/chatgpt
