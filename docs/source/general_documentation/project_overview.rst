Project Hierarchy
=================

.. contents:: Table of Contents
   :depth: 3

Overview
--------

In order to utilize Valkyrie effectively and correctly, it is adhering to a fairly
strict file and folder naming convention. Below you can find the basic structure of
how I currently have assets laid out.

.. NOTE::
   I recommend using Perforce as the means of Version Control of the CG assets. I also
   use it with the deployment of the Pipeline, though I'm still figuring out a way to
   include some Python packages as standalone packages for Maya user's to call from with
   some of the tools.

Project Folder Hierarchy
------------------------

Let's start with the root folders::

    ProjectName/
    ├── DCC/
    │   ├── AE
    │   ├── CG
    │   ├── Deliverables
    │   ├── Diagrams
    │   ├── Editorial
    │   ├── IO
    │   ├── Jira
    │   ├── ProjectConfig
    │   ├── Reference
    │   ├── Story
    │   └── Valkyrie <-- Repository Location
    └── UE/
        ├── Binaries
        ├── Config
        ├── Content
        ├── DerivedDataCache
        ├── Intermediate
        ├── Platforms
        ├── Saved
        └── Source

Let's go over what each folder is and what kind of files they should contain.

DCC Folder
``````````

The DCC folder contains any assets created outside of the Unreal Engine. Assets from
After Effects, Maya, 3DS, Premiere Pro, etc. Currently the main programs in use for
this pipeline are (but not limited to):

- Maya
- After Effects
- Unreal Engine
- Photoshop
- Zbrush
- Substance Painter
- Substance Designer

.. csv-table:: DCC Directory Explanations
   :header: "Directory", "Purpose"
   :widths: 15, 85

   "AE", "Contains general project After Effects files."
   "CG", "The CG folder is where all the CG assets are created and their dependent
   source files e.g. **Maya files, texture files, Substance and Zbrush projects, etc.**"
   "Deliverables", "Files that are to for final delivery to client."
   "Diagrams", "Internal diagrams for project workflow explanations."
   "Editorial", "All video/marketing editing files and projects."
   "IO", "Work in progress incoming and outgoing to/from client files."
   "Jira", "Jira related CSV and Bulk ticket creation templates."
   "ProjectConfig", "Contains the **ProjectConfig.json** file that is used to
   query important project information like naming conventions, version padding, etc."
   "Reference", "All shareable images or documents that pertain to broader project
   objectives."
   "Story", "All written documents pertaining to the story."
   "Valkyrie", "Pipeline Repository location."

This covers the root level project directory structure. Next I would read how to set up
the Pipeline to work with this folder structure over at :doc:`project_setup`.