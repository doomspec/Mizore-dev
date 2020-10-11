BASE_DIR=$(pwd)

# install mizore
cd $BASE_DIR
echo $PWD
# workaround for infomap
pip3 install pyscf
pip3 install -r requirements.txt
python3 setup.py install
