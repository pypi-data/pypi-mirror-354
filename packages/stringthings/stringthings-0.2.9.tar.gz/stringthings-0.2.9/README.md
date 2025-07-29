# `stringthings`
a set of functions to work with strings:  

- ## splits
  - **`multisplit`** similar to the `.split()` method from the standard `str` class, but able to separate the string using multiple separators at once.
  - **`split_dmmmy`** splits a date string in format 'dmmmy' (like '5jan23') into a list ['d', 'mmm', 'y'].
- ## numbers
  - **`is_numeric`** returns *True* if the string represents a number, not limited to integers as the `.isdigit()` string method.
  - **`get_number`** extract the number represented by the string.
- ## filenames
  - **`extension`** splits a fullpath represented by the string into:
    - the extension of the file
    - the name of the file
    - the directory containing the file
    - the input fullpath  
  - Handy functions to get the folder, the file name, or the extension from a full path:
    - `get_folder` returns the folder containing the file,
    - `get_file` returns the file name,
    - `get_name` returns the name of the file without the extension,
    - `get_extension` returns the extension of the file.
- ## dates
  - **`is_date`** returns *True* if the input string represents a date.
  - **`format_date`** change the format of the date represented by the string, as requested by the user.
- ## compression
  - **`compress`** compress the repeated items in a string sequence, i.e.: compress('1 2 2 2') returns '1 3*2'.
  - **`expand`** expand the compressed string repetitions, i.e.: expand('1 3*2') returns '1 2 2 2'.

## To install this package:  
Install it from the <a href="https://pypi.org/project/stringthings/">pypi.org</a> repository:  
`pip install stringthings`  
or upgrade to the latest version:  
`pip install --upgrade stringthings`  
  
## Optional requisites:  
The main functionalities are purely Python powered and does not require any other package to work but, if present, some functions requires NumPy and Pandas:  
- `NumPy`
- `Pandas`
