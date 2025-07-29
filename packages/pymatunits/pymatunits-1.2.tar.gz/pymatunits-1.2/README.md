# pyMatUnits - Python Materials and Units handling package

Package for handling units systems and conversion, leveraging the 
[pint package](https://pint.readthedocs.io/en/stable/), as well as material property definition for use
with in physics-based modeling.

## Changelog
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
