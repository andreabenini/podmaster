# SpacePod - Container and Pod creator from outer space



## Templates
Templates are simple text files with `.tpl` extension, they don't really have any rules apart
from being just plain text files. You can use Jinja template specs if you want to add some macro
functions. See "_**Functions**_" section below for details.  
"`templates`" directory supplied with this software contains some sample template files, feel free to
edit them or add your own.  
Template search path follow these basic rules:
- There's no need to specify the full path with "`--template`" option, "`--template python.tpl`"
is enough, search path will be used to reach that particular file
- A template will be searched in the current directory (`./`), if file is not found it will be searched
in program's `templates` directory (`./templates` where program is located).
- If a template full path is provided program will try to use it too (`/my/full/path/to/filename.tpl`)
- Add `--verbose` option to the program to see template search order
- To list all available templates you can use: "`spacepod templatelist`" command.
Description for a template file is just the first line of it when it's a comment, `python.tpl` is
a good example.
- Newer files and definitions will be added to the **templates** directory, fill free to contribute
and suggest yours; please contact me or create merge requests for new material.


## Functions
Program defined maro functions, they can be used inside a template file.
- Templates are following **jinja** specs, please refer to
    [jinja official specifications](https://jinja.palletsprojects.com/en/3.1.x/) for details.
- Function resolution is based on file order definition inside the template: first come, first served.
    If you want to solve a function before something else just put it before others or write it in a
    comment in the first lines of the file.


### `basename(varName)`
Return file `basename()` from `varName` variable without its extension (if any), examples:
```python
basename('helloWorld')                  # 'helloWorld'
basename('helloWorld.py')               # 'helloWorld'
basename('/tmp/path/helloWorld.py')     # 'helloWorld'
```

### `input(varName, prompt, defaultValue)`
Get some user input from stdin with `prompt` and stores in `varName` variable, if nothing is provided
`defaultValue` will be used instead. All parameters are mandatory.
- if `varName` already has a value (from `--variables` option or from previous `input()`) this prompt
will be ignored and nothing will be presented as user input
- `prompt` is a string, it might be empty too
- `defaultValue` can be: a string, a number, None

Example:
```sh
input("filename", "Enter python filename", "defaultValue.py")
#input> Enter python filename [defaultValue.py]:
#store> filename=<stdin|defaultValue.py>
```

### `var(varName, [defaultValue=''])`
Return `varName` value (if any)
- If `varName` is not set it will be created at runtime with `defaultValue` value
- `defaultValue` will be used when `varName` is not set, default is `''`



## Usage examples
```sh
# Generate container output using 'python.tpl' template file, output redirected on stdout
spacepod create --template python.tpl

# Generate container output on stdout using 'python.tpl' template file. Verbose output
# container stdout on 1>
# verbose messages on 2>
spacepod create --template python.tpl --verbose

# Same as above. Adding verbose output information. Output on 'Containerfile' file (not on stdout)
spacepod create --template python.tpl --verbose --output Containerfile

# Passing variables to the template, input() function will be ignored on these defined variables
spacepod create --template python.tpl --verbose --variables='filename=/tmp/hellohttp.py,port=9090'
```

