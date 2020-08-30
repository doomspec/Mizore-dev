cmake_minimum_required(VERSION 2.8.12)
project(projectq_gpu LANGUAGES CXX CUDA)
find_package( CUDA REQUIRED )

add_subdirectory(pybind11)

set(CUDA_SOURCES
    _cppkernels/cudastart.cu
)

set(BINDINGS
    _cppsim.cpp
)

add_library(gpu STATIC "${CUDA_SOURCES}")
set_target_properties(gpu PROPERTIES CUDA_SEPERABLE_COMPILATION ON
                                     POSITION_INDEPENDENT_CODE TRUE)

add_library(_cppsim MODULE "${BINDINGS}")
target_link_libraries(_cppsim PRIVATE pybind11::module gpu)
set_target_properties(_cppsim PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
                                     SUFFIX "${PYTHON_MODULE_EXTENSION}")
# set(CMAKE_SKIP_BUILD_RPATH TRUE)
# set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
# set(CMAKE_INSTALL_RPATH "@loader_path")
# set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
#
# CUDA_SELECT_NVCC_ARCH_FLAGS(ARCH_FLAGS Auto)
#
# LIST(APPEND CUDA_NVCC_FLAGS ${ARCH_FLAGS})
# LIST(APPEND CUDA_NVCC_FLAGS ${NVCC_GEN_OPT})
# LIST(APPEND CUDA_NVCC_FLAGS -Xcompiler ${XCOMPILER_OPT_})
# LIST(APPEND CUDA_NVCC_FLAGS  -lcuda;  -lcublas; -lcudart; -lcudadevrt; --cudart static;  -rdc=true; )
#
# add_subdirectory(pybind11)
# cuda_add_library(cuda_gpu SHARED  _cppkernels/simulator.hpp _cppkernels/cudastart.cu  _cppkernels/cudastart.h)
#
# pybind11_add_module(_cppsim _cppsim.cpp)
# target_link_libraries(_cppsim PRIVATE cuda_gpu)