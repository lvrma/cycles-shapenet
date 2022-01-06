# Cycles ShapeNet
This script adjusts the objects in ShapeNet, enabling their texture to be visualized using the Cycles path tracer in Blender. 


![Example](https://github.com/lvrma/cycles-shapenet/blob/main/example.jpg)
**Note 1:** this is an initial version of the code with a temporary solution. The objects are much improved, but artifacts are still present (as can be seen in the white portions of the propeller, in the "After" image above). I'll continue to improve this repository as I finish coding the proper solution to replace this quick fix.

**Note 2:** the script is still being worked on, so it is not fully documented. Do send me questions if you have any.

**Note 3:** the outputs of this script might not look right at all with Eevee, please make sure you're using Cycles.

## Dependencies
The script requires the library [obj2gltf](https://github.com/CesiumGS/obj2gltf), which requires Node.js.
Thus, first [install Node.js](https://nodejs.org/en/), then run `npm install -g obj2gltf`.

The script has been tested with Blender 3.0.0, other versions might need adjustments.

**Note:** the script converts OBJ models to GLTF in order to better operate with the meshes. The end result is converted back to OBJ and the GLTF models are deleted.

## Usage
To run the script, simply open the `cycles-shapenet.py` file on Blender (or run it through the command line). Before, do make sure to open the script and alter the `DB` variable with the path of your ShapeNet folder and `OUT` with the path of your desired output folder.

Example for Windows \
`DB = 'C:\\Users\\john\\shapenet'`\
`OUT = 'C:\\Users\\john\\output'` 

Example for Linux/Mac \
`DB = '/home/john/shapenet'`\
`OUT = '/home/john/output'`

Then simply run the script and wait, it can take a long time given the dataset is over 100GB. Please make sure you have enough disk space. The output folder will contain the same folder structure as the original ShapeNet, but the OBJ models inside will be adjusted.

**Note:** this usage method is very rudimentary, as is the current solution. As the algorithm gets more refined, I'll make this a command-line-only tool with an easier in/out usage.
