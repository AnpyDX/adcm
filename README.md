# ADCM
**adcm** is a python library that allow you to work on CMake project in Visual Studio Code easily with following features:

- real-time `CMakeLists.txt` update.
- custom workflow *tasks* and *triggers*.

This project was originally created to help me generate `compile_commands.json` automatically, which is needed by `clangd` extension in Visual Studio Code. Now I improve it furter and public for everyone to use.

## Use ADCM in your project

**Project Structure**
```
Project-Dir/
|
|-- main.cpp
|-- CMakeList.txt
|-- workflow.py
```

****

**Necessary Extensions**
- **C/C++ (by Microsoft)**
- **Python (by Microsoft)**
- **clangd (by LLVM)**
- **CMake Language Support (by Jose Torres)**

*NOTICE* don't install extension **CMake** and **CMake Tools**.

****

**workflow.py**
```python
import os
import adcm

adcm.new_project("your-project's-name")

adcm.add_task(
    "generate",
    [
        "mkdir build" if not os.path.exists("build") else "",
        "cd build && cmake .. -G Ninja -D CMAKE_C_COMPILER=clang -D CMAKE_CXX_COMPILER=clang++ -D CMAKE_EXPORT_COMPILE_COMMANDS=ON"
    ]
)

adcm.add_trigger(
    "cmake-detector",
    ["CMakeLists.txt"],
    ["generate"]
)

adcm.launch()
```

Then run `workflow.py`, and done.

## License
Licensed under the MIT license, read [LICENSE](LICENSE) for details.