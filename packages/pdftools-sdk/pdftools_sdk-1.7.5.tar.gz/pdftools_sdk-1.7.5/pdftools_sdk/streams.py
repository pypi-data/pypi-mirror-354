import ctypes
import os

class StreamAdapter:
    def __init__(self, py_stream):
        self.stream = py_stream  # Stream initialization

    def get_length(self, handle):
        # Get length of stream in bytes
        try:
            iPos = self.stream.tell()
            self.stream.seek(0, os.SEEK_END)
            nLen = self.stream.tell()
            self.stream.seek(iPos, os.SEEK_SET)
            return nLen
        except OSError:
            return -1

    def seek(self, handle, iPos):
        # Set position
        try:
            if iPos == -1:
                self.stream.seek(0, os.SEEK_END)
            else :
                self.stream.seek(iPos, os.SEEK_SET)
            return 1
        except (OSError, ValueError):
            return 0

    def tell(self, handle):
        # Get current byte position
        try:
            return self.stream.tell()
        except OSError:
            return -1

    def read(self, handle, pData, nSize):
        # Read nSize bytes from stream
        try:
            data = self.stream.read(nSize)
            length = len(data)
            ctypes.memmove(pData, data, length)
            return length  # Return number of bytes read
        except (OSError, ValueError) as e:
            return -1

    def write(self, handle, pData, nSize):
        # Write nSize bytes to stream
        try:
            data = (ctypes.c_char * nSize).from_address(pData)
            written = self.stream.write(data)
            if written != nSize:
                return -1
            return written  # Return number of bytes written
        except (OSError, ValueError):
            return -1

    def release(self, handle):
        return # i.e. close stream explicitly using the "with statement"

# Define the StreamDescriptor struct
class StreamDescriptor(ctypes.Structure):
    _fields_ = [("pfGetLength", ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)),
                ("pfSeek", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_longlong)),
                ("pfTell", ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)),
                ("pfRead", ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)),
                ("pfWrite", ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)),
                ("pfRelease", ctypes.CFUNCTYPE(None, ctypes.c_void_p)),
                ("m_handle", ctypes.c_void_p)]

    def __init__(self, py_stream):
        adapter = StreamAdapter(py_stream)
        super().__init__(
            pfGetLength=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(adapter.get_length),
            pfSeek=ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_longlong)(adapter.seek),
            pfTell=ctypes.CFUNCTYPE(ctypes.c_longlong, ctypes.c_void_p)(adapter.tell),
            pfRead=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(adapter.read),
            pfWrite=ctypes.CFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)(adapter.write),
            pfRelease=ctypes.CFUNCTYPE(None, ctypes.c_void_p)(adapter.release),
            m_handle=ctypes.cast(ctypes.pointer(ctypes.py_object(adapter)), ctypes.c_void_p)
        )