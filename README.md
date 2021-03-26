# BeeHou 🐝

Package of tools and scripts for Sidefx Houdini.

I intended to keep this package open and free and welcome feedback and suggestions! 🥂

[twitter @simonreeves3d](https://twitter.com/simonreeves3d)

[simonreeves.com](http://www.simonreeves.com)

## Setup
This repository is a [Houdini Package](https://www.sidefx.com/docs/houdini/ref/plugins.html) just like [qLib](https://github.com/qLab/qLib) or [SideFXLabs](https://github.com/sideeffects/SideFXLabs) and the installation is the same.


1. Clone this repository into the folder of your choosing eg. `C:/HoudiniPackages`

2. Copy the `BeeHou.json` file from the package to $HOME/Houdini[version]/packages (eg. windows default for 18.5 is `C:\Users\[youruser]\houdini18.5\packages`)

3. Create the environment variable `$HOUDINI_PACKAGE_PATH` referenced in the json to where your packages are stored eg. `C:/HoudiniPackages` 



# HDAs

### Place Highlight
![bee](docs/media/placehighlight.gif)
Object level viewer state tool to interactivly position a light by placing its highlight on geo.
My first attempt with python viewer state to replicate the #1 feature in 3dsmax 3.1


### Align
![bee](docs/media/bee_align2.0.0.gif)
Align one object by target object

I built this as to control an object's position by percentage target bounding box, to specficially allow you to place inside or outside of object


### Barndoors
Not sure I have ever used this but I thought it would be fun.
Parented to a light, creates a [barn door](https://en.wikipedia.org/wiki/Stage_lighting_accessories#Barn_doors) object for a bit more control over light casting

### Camshake
wip

### Coloriser
![bee](docs/media/coloriser.png)
SOP to quickly set color using connectivity and a gradient

### Railings
![bee](docs/media/railings.png)
Built for creating background railings easily from generated curves - SOP to create simple railings from a curve, has various options for number if horizontals/verticals, sweep shape etc.!

## Variant
![bee](docs/media/variant.png)
Very simple SOP for the common task of creating `variant` attributes on template points for `copy to points`
