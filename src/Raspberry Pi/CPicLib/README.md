# CPicLib

## Benötigte Software
  * [CMake](https://cmake.org/)
  * [MinGW](http://mingw.org/) (Windows) oder GCC (*nix)
  * Make (in MinGW enthalten)
  * Python 3

## Library compilieren
  * `mkdir build` - das `build`-Verzeichnis wird von der Versionsverwaltung ignoriert
  * `cd build` - der CMake-Output soll im `build`-Verzeichnis landen
  * `cmake .. -G <generator-name>` - eine vollständige Liste der verfügbaren Generatoren kann unter `cmake -h` nachgelesen werden  
  Empfehlung:
    * `cmake .. -G "MinGW Makefiles"` unter Windows
    * `cmake .. -G "Unix Makefiles"` unter *nix
  * `cmake --build .` um die Library zu compilieren

## Run Python Test
  * `python __init__.py`  
