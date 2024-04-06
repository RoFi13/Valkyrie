# VALKYRIE PIPELINE

## IMPORTANT DISCLAIMER 4/6/24

This README will be phased out for Sphinx documentation that is currently in progress.

Important note is that this repository is still a wip including documentation
for setting this pipeline up if you wish to use for your own personal projects. There
is a small bit of a setup involved.

## SUMMARY

Valkyrie is a personal Maya/Unreal Pipeline I started to develop. The purpose for this
set of tools is to optimize work inside Maya in a simple and easy to understand way.

A primary goal of the pipeline is to standardize naming conventions, folder hierarchies,
and some basic I/O of CG assets between Maya and Unreal Engine.

## PROJECT HIERARCHY

In order to utilize Valkyrie effectively, it is adhering to a fairly strict file and
folder naming convention. Below you can find the basic structure of how I currently
have assets laid out.

I recommend using **Perforce** as the means of **Version Control of the CG assets**. I
also use it with the deployment of the Pipeline, though I'm still figuring out a way to
include some Python packages as standalone packages for Maya user's to call from
with some of the tools.

Let's start with the root folders:

```
DCC/
├── AE
├── CG
├── Deliverables
├── Diagrams
├── Editorial
├── IO
├── Jira
├── ProjectConfig
├── Reference
├── Story
└── Valkyrie

UE/
├── Binaries
├── Config
├── Content
├── DerivedDataCache
├── Intermediate
├── Platforms
├── Saved
└── Source
```

### DCC FOLDER

The DCC folder contains **any assets created outside of the Unreal Engine**. Assets from
After Effects, Maya, 3DS, Premiere Pro, etc. Currently the main programs in use for this
pipeline are (but not limited to):

- Maya
- After Effects
- Unreal Engine
- Photoshop
- Zbrush
- Substance Painter
- Substance Designer

As you can see in the hierarchy, there is a folder named **Valkyrie**. This folder is
where this repository should exist. The [**Maya Launcher**](Maya2025_Launcher.bat) Batch
files work with the relative paths from that location.

#### CG FOLDER

The CG folder is where all the **CG assets** are created and their dependent source files
e.g. Maya files, texture files, Substance and Zbrush projects, etc.

#### PROJECT CONFIG FOLDER

The **ProjectConfig** folder includes a very important files for the project. A lot of the
tools utilize a **ProjectConfig.json file** to query important project information like
naming conventions, version padding, etc.

### MAYA ASSET HIERARCHY

Let's cover the basic Maya Asset folder hierachy. This hierarchy is automatically
created and managed by the [**Asset Manager**](src/python/Asset/AssetManager/README.md)
tool.

### UE FOLDER

This folder contains all the Unreal Engine assets. Pretty self-explanatory.