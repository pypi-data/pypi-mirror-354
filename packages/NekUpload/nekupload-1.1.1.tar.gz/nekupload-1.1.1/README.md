# NekUpload

**NekUpload** is a Python package designed to streamline the upload and data management process of Nektar++ datasets to AE Datastore. It automates the validation of simulation datasets to ensure consistency and completeness. Furthermore, it extracts relevant parameters embedded within the files, enriching database records with valuable metadata. This aligns with the FAIR principles (Findable, Accessible, Interoperable, Reusable), making your data accessible, understandable and compatible with other NekRDM tools.

# Installation

There are two installation methods. With pip:

```bash
python3 -m pip install NekUpload
```

Or build from source:

```bash
git clone https://gitlab.nektar.info/nektar/NekUpload.git

#if just need the package as a user
python3 -m pip install .
#if you want development tools too
python3 -m pip install .[dev]
```

The GUI can then be opened using the command ```nekupload```.

# User Guide

User guide can be found at https://nekupload.readthedocs.io/en/latest/.

# Documentation

The following steps can be used to generate documentation locally. Assming development tools are installed:

```bash
cd docs
make html
```

Open ``build/index.html`` to view the documentation locally.

# Other Info

Note that the root repository contains a schema_update.json file. This is for reference purposes and is the one currently used by the Imperial Aeronautics Data Store for storing CFD-specific metadata. This may evolve in the future.

There is also a launch.sh file, which given the correct venv path, it can be used to invoke the GUI. 