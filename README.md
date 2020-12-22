# BeeHou 🐝

Package for Sidefx Houdini, very early!


## Setup
This repository is a [Houdini Package](https://www.sidefx.com/docs/houdini/ref/plugins.html) just like [qLib](https://github.com/qLab/qLib) or [SideFXLabs](https://github.com/sideeffects/SideFXLabs) and the installation is the same.


1. Clone this repository into the folder of your choosing eg. `C:/HoudiniPackages`

2. Copy the `BeeHou.json` file from the package to $HOME/Houdini[version]/packages (eg. windows default for 18.5 is `C:\Users\[youruser]\houdini18.5\packages`)

3. Create the environment variable `$HOUDINI_PACKAGE_PATH` referenced in the json to where your packages are stored eg. `C:/HoudiniPackages`


# HDAs
### Barndoors
Parented to a light, creates a [barn door](https://en.wikipedia.org/wiki/Stage_lighting_accessories#Barn_doors) object for a bit more control over light casting
