#!/bin/sh
echo "Hello mother fu3ker"
CWD=$(pwd)
controllerPath=$CWD"/controllers/"
modelPath=$CWD"/models/"
buildPath=$CWD"/build/"
cp -r $controllerPath ~/.local/lib/python3.10/site-packages/polyvisor/
cp -r $modelPath ~/.local/lib/python3.10/site-packages/polyvisor/
cp -r $buildPath ~/.local/lib/python3.10/site-packages/polyvisor/
echo "My lord, update has completed :)))"