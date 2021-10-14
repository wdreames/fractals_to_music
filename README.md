# fractals_to_music

This is a Python script used to convert fractal patterns into music through the use of L-systems. This was made as part of a project in Christopher Newport University's HONR 379: Fractals and Infinity course taught by Dr. Morena. See [Making Melodious Music From Fractals](Making\ Melodious\ Music\ From\ Fractals.pdf) for more details.

The following repositories were used during the creation of this program:
- https://github.com/Mizzlr/L-Systems-Compiler-And-Renderer was used to create the L-systems and iterate over a given pattern (lsystem.py).
- https://github.com/weeping-angel/Mathematics-of-Music was used to generate music/sound (mathematics_of_music.py).

## Usage
1. Create a virtual environment

`# virtualenv env`

2. Activate the environment

`# source ./env/bin/activate`

3. Install all the requirements

`# pip install -r requirements.txt`

4. Run the program 

` # python3 fractals_to_music.py`

## Changes made to other repository code:
Changes made to L-Systems-Compiler-And-Renderer:
- Updated certain aspects to work in Python3. This mainly included adding parenthesis to print statements.
- Altered code so that the program is not always required to create the turtle drawing window.
- Removed some print statements regarding turtle movements to clean up the output.
- Remove the option to save images as that was giving me issues and I could not get it to work.

Changes made to Mathematics-of-Music:
- Added an option to control note duration
