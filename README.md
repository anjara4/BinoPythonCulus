# Binoculus
This code is a Python and PyQt 5 implementation of Binoculus or Orthoptica, 
which was originally developed using C# and Unity.

More information about Orthoptica is available here: 
https://cdn.cahiers-ophtalmologie.fr/media/91ab08a042d2f06c2b05bf3201d02612.pdf

## Installation
Clone the project in the repertory on your choice <br />
Create a virtual environment with python = 3.6  <br />
Install the uvc-0.14 package by downloading the affiliated wheel (pip install .\uvc-0.14-cp36-cp36m-win_amd64.whl) disponible here : https://github.com/pupil-labs/pyuvc/releases/tag/v0.14 <br />
Install the required packages with 'pip install -r requirements.txt' <br />
Finally, check that you have the correct drivers for your cameras, folling the instruction available here :  https://github.com/pupil-labs/pyuvc/blob/master/WINDOWS_USER.md <br />

## Run project
Launch your  virtual environnment and run !
```sh
python binoculus.py
```