GPU_SIM_PATH="src/GPUSimulator/"
BASE_DIR=$(pwd)

echo "PWD :"$(pwd)

# Initial submodules
git submodule init
git submodule update

# install GPU Simulator
cd $GPU_SIM_PATH
echo "GPU Simulator Path: "$(pwd)

# Build GPU Simulator
mkdir build
cd build
cmake ../
make

# install mizore
cd $BASE_DIR
echo $PWD
# workaround for infomap
pip3 install pyscf
pip3 install -r requirements.txt
python3 setup.py install