import os
import platform
from ctypes import *
from javonet.core.callback.callbackFunc import callbackFunc

CMPFUNC = CFUNCTYPE(py_object, POINTER(c_ubyte), c_int)
callbackFunction = CMPFUNC(callbackFunc)


class TransmitterWrapper:
    _python_lib = None

    @staticmethod
    def get_native_lib():
        if TransmitterWrapper._python_lib is None:
            file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            machine = platform.machine().lower()
            if '64' in machine:
                arch = 'X64'
            elif 'arm' in machine:
                arch = 'ARM64' if '64' in machine else 'ARM'
            else:
                arch = 'X86'

            if platform.system() == 'Windows':
                python_lib_path = file_path + f'/Binaries/Native/Windows/{arch}/JavonetPythonRuntimeNative.dll'
            elif platform.system() == 'Linux':
                python_lib_path = file_path + f'/Binaries/Native/Linux/{arch}/libJavonetPythonRuntimeNative.so'
            elif platform.system() == 'Darwin':
                python_lib_path = file_path + f'/Binaries/Native/MacOs/{arch}/libJavonetPythonRuntimeNative.dylib'
            else:
                raise RuntimeError("Unsupported OS: " + platform.system())
            lib = cdll.LoadLibrary(python_lib_path)
            lib.SetCallback(callbackFunction)
            TransmitterWrapper._python_lib = lib
        return TransmitterWrapper._python_lib

    @staticmethod
    def send_command(message):
        lib = TransmitterWrapper.get_native_lib()
        message_array = bytearray(message)
        message_ubyte_array = c_ubyte * len(message_array)
        response_array_len = lib.SendCommand(message_ubyte_array.from_buffer(message_array), len(message_array))
        if response_array_len > 0:
            response = bytearray(response_array_len)
            response_ubyte_array = c_ubyte * response_array_len
            lib.ReadResponse(response_ubyte_array.from_buffer(response), response_array_len)
            return response
        elif response_array_len == 0:
            error_message = "Response is empty"
            raise RuntimeError(error_message)
        else:
            get_native_error = lib.GetNativeError
            get_native_error.restype = c_char_p
            get_native_error.argtypes = []
            error_message = get_native_error()
            raise RuntimeError("Javonet native error code: " + str(response_array_len) + ". " + str(error_message))

    @staticmethod
    def activate(license_key):
        lib = TransmitterWrapper.get_native_lib()
        activate = lib.Activate
        activate.restype = c_int
        activate.argtypes = [c_char_p]
        activation_result = activate(license_key.encode('ascii'))
        if activation_result < 0:
            get_native_error = lib.GetNativeError
            get_native_error.restype = c_char_p
            get_native_error.argtypes = []
            error_message = get_native_error()
            raise RuntimeError(
                "Javonet activation result: " + str(activation_result) + ". Native error message: " + str(
                    error_message))
        else:
            return activation_result

    @staticmethod
    def set_config_source(source_path):
        lib = TransmitterWrapper.get_native_lib()
        set_config_source = lib.SetConfigSource
        set_config_source.restype = c_int
        set_config_source.argtypes = [c_char_p]
        set_config_result = set_config_source(source_path.encode('utf-8'))
        if set_config_result < 0:
            get_native_error = lib.GetNativeError
            get_native_error.restype = c_char_p
            get_native_error.argtypes = []
            error_message = get_native_error()
            raise RuntimeError(
                "Javonet set config source result: " + str(set_config_result) + ". Native error message: " + str(
                    error_message))
        else:
            return set_config_result

    @staticmethod
    def set_javonet_working_directory(path):
        lib = TransmitterWrapper.get_native_lib()
        set_working_directory = lib.SetWorkingDirectory
        set_working_directory.restype = c_int
        set_working_directory.argtypes = [c_char_p]
        set_working_directory_result = set_working_directory(path.encode('utf-8'))
        if set_working_directory_result < 0:
            get_native_error = lib.GetNativeError
            get_native_error.restype = c_char_p
            get_native_error.argtypes = []
            error_message = get_native_error()
            raise RuntimeError("Javonet set working directory result: " + str(
                set_working_directory_result) + ". Native error message: " + str(error_message))
        else:
            return set_working_directory_result