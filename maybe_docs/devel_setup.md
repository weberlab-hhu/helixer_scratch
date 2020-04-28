# Development install

useful e.g. for people working on this project / who will be frequently updating the code

## setup virtual environmnet 

(the directory name and location of 'venv' below may be changed).

```
# create (run once)
virtualenv venv -p python3
# activate (this should be run once per terminal that one's executing Helixer code from)
source venv/bin/activate
```

## clone and dev install repositories

First `cd` into the directory where you wan't the repositories, then

```
# GeenuFF (for data management)
git clone https://github.com/weberlab-hhu/GeenuFF
cd GeenuFF/
git checkout dev
pip install -r requirements.txt
python setup.py develop
cd ..

# HelixerPrep (all things DL)
git clone https://github.com/weberlab-hhu/HelixerPrep.git
cd HelixerPrep/
git checkout dev
pip install -r requirements.txt
python setup.py develop
```

That should do it, just don't forget the `source venv/bin/activate` when you 
need to use the code (you could also add this to your .bashrc, if you're not using multiple
virtual environments).
