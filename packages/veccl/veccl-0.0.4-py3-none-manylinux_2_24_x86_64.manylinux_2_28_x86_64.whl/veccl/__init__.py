# Copyright 2025 Beijing Volcano Engine Technology Ltd. All rights reserved.
import os
import ctypes
import sys

def lib_paths():
    libraries = ["/libnccl-net-soft-bonding.so", "/libnccl.so"]
    dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    return ":".join([dir + lib for lib in libraries])

def ld_library_path():
    return os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

def enable():
    veccl_so_files = lib_paths()
    os.environ["LD_PRELOAD"] = veccl_so_files + ("" if not os.environ.get("LD_PRELOAD")else ":"+os.environ['LD_PRELOAD'])
    sys.stderr.write(f"[veCCL] set LD_PRELOAD={os.environ['LD_PRELOAD']}\n")
    os.environ["NCCL_NET_PLUGIN"] = "soft-bonding"
    sys.stderr.write(f"[veCCL] set NCCL_NET_PLUGIN=soft-bonding\n")
    os.environ["LD_LIBRARY_PATH"] = ld_library_path() + ("" if not os.environ.get("LD_LIBRARY_PATH") else ":"+os.environ['LD_LIBRARY_PATH'])
    sys.stderr.write(f"[veCCL] set LD_LIBRARY_PATH={os.environ['LD_LIBRARY_PATH']}\n")

class Dl_info(ctypes.Structure):
    _fields_ = [("dli_fname", ctypes.c_char_p),
                ("dli_fbase", ctypes.c_void_p),
                ("dli_sname", ctypes.c_char_p),
                ("dli_saddr", ctypes.c_void_p)]

def check_cuda_version(required_major=12, required_minor=None):
    print_path = True
    try:
        libdl = ctypes.CDLL("libdl.so.2")
        dladdr = libdl.dladdr
        dladdr.argtypes = [ctypes.c_void_p, ctypes.POINTER(Dl_info)]
        dladdr.restype = ctypes.c_int
        info = Dl_info()
    except:
        print_path = False
    try:
        # CUDA driver library
        cuda = ctypes.CDLL("libcuda.so")
        if print_path:
            symbol_address = ctypes.cast(cuda.cuInit, ctypes.c_void_p)
            result = dladdr(symbol_address, ctypes.byref(info))
            if result != 0:
                sys.stderr.write(f"[veCCL] Checking CUDA driver library at {info.dli_fname.decode()}\n")
        result = cuda.cuInit(0)
        if result != 0:
            raise RuntimeError(f"Failed to initialize CUDA driver, error code: {result}")
        version = ctypes.c_int()
        result = cuda.cuDriverGetVersion(ctypes.byref(version))
        if result != 0:
            raise RuntimeError(f"Failed to get CUDA driver version, error code: {result}")

        major_version = version.value // 1000
        minor_version = (version.value % 1000) // 10

        if major_version < required_major:
            raise RuntimeError(f"CUDA driver {required_major} or higher is required, but version {major_version} is installed.")
        elif major_version == required_major and required_minor is not None:
            if minor_version < required_minor:
                raise RuntimeError(f"CUDA driver {required_major}.{required_minor} or higher is required, but version {major_version}.{minor_version} is installed.")
        sys.stderr.write(f"[veCCL] Compatible CUDA driver {major_version}.{minor_version} detected.\n")

    except Exception as e:
        sys.stderr.write(f"[veCCL] Failed to detect proper CUDA driver in your system: {e}\nPlease ensure CUDA driver {required_major} is configured properly or veCCL may not work.\n")

    # don't really need these since we bundle libcudart...
    #try:
    #    # CUDA runtime library
    #    cudart = ctypes.CDLL(f"libcudart.so.{required_major}{'' if not required_minor else f'.{required_minor}'}")
    #    if print_path:
    #        symbol_address = ctypes.cast(cudart.cudaRuntimeGetVersion, ctypes.c_void_p)
    #        result = dladdr(symbol_address, ctypes.byref(info))
    #        if result != 0:
    #            sys.stderr.write(f"[veCCL] Checking CUDA runtime library at {info.dli_fname.decode()}\n")
    #    cudart_version = ctypes.c_int()
    #    result = cudart.cudaRuntimeGetVersion(ctypes.byref(cudart_version))
    #    if result != 0:
    #        raise RuntimeError(f"Failed to get CUDA runtime version, error code: {result}")

    #    runtime_major_version = cudart_version.value // 1000
    #    runtime_minor_version = (cudart_version.value % 1000) // 10

    #    if runtime_major_version < required_major:
    #        raise RuntimeError(f"CUDA {required_major} or higher is required, but runtime version {runtime_major_version} is installed.")
    #    elif runtime_major_version == required_major and required_minor is not None:
    #        if runtime_minor_version < required_minor:
    #            raise RuntimeError(f"CUDA {required_major}.{required_minor} or higher is required, but runtime version {runtime_major_version}.{runtime_minor_version} is installed.")
    #    sys.stderr.write(f"[veCCL] Compatible CUDA runtime {runtime_major_version}.{runtime_minor_version} detected.\n")

    #except Exception as e:
    #    sys.stderr.write(f"[veCCL] Failed to detect proper CUDA runtime library in your system: {e}\nPlease ensure CUDA runtime {required_major} is configured properly or veCCL may not work.\n")
