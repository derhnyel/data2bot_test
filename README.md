# JSON SCHEMA GENERATOR

### REQUIRES

- Python 3.10

### INSTALLATION

- Clone and Navigate into project directory

```shell
git clone https://github.com/derhnyel/data2bot_test
cd data2bot_test
```

- Install project requirements using `pip` by running

```shell
pip install -r requirments.txt
```

### USAGE

```shell
usage: main.py [-h] [--depth DEPTH] [--verbose] [--select SELECT] source target

Parse JSON files and generate a schema

positional arguments:
  source                source path
  target                target path

options:
  -h, --help            show this help message and exit
  --depth DEPTH         depth of search
  --verbose             increase output verbosity
  --select SELECT       select a particular parent attribute from json file
```

The simplest usage is running

```shell
python3 main.py data schema --depth 2 --select message
```

This will get all .json files in the `data` source directory and write all the schemas to the `schema` target directory. It will `select` just the `message` attribute and a search `depth` of `2`

### TEST

Test can be ran using the command

```shell
python3 test.py
```

### EDGE CASES HANDLED

- Handles target is a directory or file | source is a directory or file
- Handles all Callable and Coroutine Map functions.
- Breaks out of the recursive loop when depth is 0.
- Handles cases where the parent value is a dictionary or a list and iterates through the items or elements respectively.

### LIMITATIONS

- `json.dump()` does iteratively write JSON data to the given file-like object, you must first produce the entire document to be written as standard python types (dict, list, etc). For a very large document, this could be more memory than you have available to your system.
- Reading and writing multiple json file uses the `open()` built in method which is synchronous and a blocking function.
- Cannot select more than one attribute at different depths for different json files.
- Cannot select attributes from a json list object.

### IMPROVEMENTS

- Reading and Writing to files asynchronously using aiofiles !!
- Using an AsyncGenerator object for in memory schema map.
- Convert AsyncGeneartor to a streamable dictionary and dump to file in streams
- Parse selecting attributes dynamically with a yaml/json file.
