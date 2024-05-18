# ADCM

## Introduce
**adcm** is a python library that allow you to work on CMake project in Visual Studio Code easily with following features:

- real-time `CMakeLists.txt` update.
- custom workflow *tasks* and *triggers*.

This project was originally created to help me generate `compile_commands.json` automatically, which is needed by `clangd` extension in Visual Studio Code. Now I improve it further and public for everyone to use.

## Example

**project structure**
```
Project-Dir/
|
|-- main.cpp
|-- CMakeList.txt
|-- workflow.py
```


**necessary extensions**
- **C/C++** by Microsoft
- **Python** by Microsoft
- **clangd** by LLVM
- **CMake Language Support** by Jose Torres

*NOTICE* please uninstall extensions **CMake** and **CMake Tools** in advance.


**workflow.py**
```python
import os
import adcm

adcm.new_project("my-project")

def mkdir_build():
    if not os.path.exists("build"):
        os.mkdir("build")

adcm.add_task(
    "generate",
    [
        mkdir_build,
        "cd build && cmake .. -G Ninja -D CMAKE_C_COMPILER=clang -D CMAKE_CXX_COMPILER=clang++ -D CMAKE_EXPORT_COMPILE_COMMANDS=ON"
    ]
)

adcm.add_trigger(
    "auto-cmake-generate",
    ["CMakeLists.txt"],
    ["generate"]
)

adcm.launch()
```

Then run `workflow.py`, and done.

## Documentation
Read [Documentation](documentation.md) for more details.

## License
Licensed under the MIT license, read [LICENSE](LICENSE) for details.