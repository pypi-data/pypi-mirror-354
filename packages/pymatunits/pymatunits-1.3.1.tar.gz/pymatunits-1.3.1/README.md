# pyMatUnits - Python Materials and Units handling package

Package for handling units systems and conversion, leveraging the 
[pint package](https://pint.readthedocs.io/en/stable/), as well as material property definition for use
with in physics-based modeling.

## Installation
Once the appropriate conda or virtual environment is activated, navigate to the main directory and run:

`pip install --editable .`

This should install the dependencies if not already installed

## Documentation
The formatted documentation for this package can be found at https://github.gatech.edu/pages/acox37/pymatunits/

If the documentation has been modified in your current branch, you can do the following to view the detailed documentation as a website:

- Verify that mkdocs is installed
-  Navigate to main folder (same folder as mkdocs.yml)
-  Either:
      - Run  `mkdocs serve` and open  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
      - **OR** run `mkdocs build` which will compile it into a `site` folder, then just open `site/index.html`

## Changelog

### v1.3.1: Dynamic versioning, streamline unit corrections
- Add dynamic versioning to pyproject.toml
- Save unit corrections after running check_consistency once to not have to call every time `convert` is used
### v1.3: Installation and documentation update
- Move from setup.py to pyproject.toml
- Add mkdocs setup and files for initial version of documentation website
### v1.2: Encoding improvements, material unit system conversion
#### to/read_json: allow for saving unit string in JSON files
#### Material.unit_system can be set, which will convert all quantities

## Built-In/Saved Materials and Unit Systems
`mat_prop` and `units` modules have `builtin_dir` and `builtin_paths` to lead to saved `JSON` files

## Unit Systems

### Module name : **units**
Works on top of the [pint package](https://pint.readthedocs.io/en/stable/). `UnitSystem` class allows for
storage of system of units (length, mass, time, etc.), as well as the ability to check for internal
consistency of said system using `check_consistency` method. Logs consistency issues as well as returning
conversion factors to be used when converting inconsistent units.

Unit systems can be stored or read from JSON file format using `.to_json`/`.read_json`, similar to Pandas.

- Main class : `UnitSystem`
- Unit conversion function : `convert`

## Materials

### Module name : **mat_prop**
Allows for material definitions, based on those defined in Abaqus. Can create materials in Abaqus CAE or
Nastran input file (bdf) if the appropriate dependencies are in place (Abaqus API or Nastran Utils package). 

Materials can be stored or read from JSON file format using `.to_json`/`.read_json`, similar to Pandas.

## Apps
Dash apps (`units_app.py` and `mat_app.py`) for creating, reading, or writing unit systems or material
objects.
