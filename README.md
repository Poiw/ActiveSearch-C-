# Bundle

## Environment
- `sudo apt-get install gfortran`
- comment `BundlerApp.h` line 620
- May need to add `<root>/Bundler/bin` to `LD_LIBRARY` 

## Installation 
- `cd Bundler` 
- `make -j7`

## Generate .jpg files
- `mogrify -format jpg *.png` 

## Generate key files
- `mkdir ./Bundler/info`
- `cd ./Bundler/info`
- `../RunBundler.sh <file_dir>`

## Generate bundle.out
- `python3 getBundle.py <list_file>`
Then generated file is in `Bundler/info`

# ACG_Localizer
