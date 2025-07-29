from ctypes import *
from enum import Enum
from enum import Flag
from enum import IntEnum
try:
    # When using as package
    from .streams import *
    from .utils import *
except ImportError:
    # When using locally
    from streams import *
    from utils import *

# Load library
_lib = load_library()

# ErrorCode type definition
class ErrorCode(IntEnum):
    SUCCESS = 0
    GENERIC = 10
    LICENSE = 12
    UNKNOWN_FORMAT = 15
    CORRUPT = 16
    PASSWORD = 17
    CONFORMANCE = 18
    UNSUPPORTED_FEATURE = 19
    PROCESSING = 21
    EXISTS = 22
    PERMISSION = 23
    HTTP = 24
    RETRY = 25
    UNSUPPORTED_OPERATION = 1
    ILLEGAL_STATE = 2
    ILLEGAL_ARGUMENT = 3
    NOT_FOUND = 5
    I_O = 4


# Enumerations type definitions

class PdfPermission(Flag):
    NONE = 0
    PRINT = 4
    MODIFY = 8
    COPY = 16
    ANNOTATE = 32
    FILL_FORMS = 256
    SUPPORT_DISABILITIES = 512
    ASSEMBLE = 1024
    DIGITAL_PRINT = 2048

    ALL = 3900

class PdfXfaType(IntEnum):
    NO_XFA = 0
    XFA_NEEDS_RENDERING = 1
    XFA_RENDERED = 2


class PdfMdpPermissions(IntEnum):
    NO_CHANGES = 1
    FORM_FILLING = 2
    ANNOTATE = 3


class PdfConformance(IntEnum):
    PDF10 = 0x1000
    PDF11 = 0x1100
    PDF12 = 0x1200
    PDF13 = 0x1300
    PDF14 = 0x1400
    PDF15 = 0x1500
    PDF16 = 0x1600
    PDF17 = 0x1700
    PDF20 = 0x2000
    PDF_A1_B = 0x1401
    PDF_A1_A = 0x1402
    PDF_A2_B = 0x1701
    PDF_A2_U = 0x1702
    PDF_A2_A = 0x1703
    PDF_A3_B = 0x1711
    PDF_A3_U = 0x1712
    PDF_A3_A = 0x1713


class DocumentAssemblyCopyStrategy(IntEnum):
    COPY = 1
    FLATTEN = 2
    REMOVE = 3


class DocumentAssemblyRemovalStrategy(IntEnum):
    FLATTEN = 1
    REMOVE = 2


class DocumentAssemblyNamedDestinationCopyStrategy(IntEnum):
    COPY = 1
    RESOLVE = 2


class DocumentAssemblyNameConflictResolution(IntEnum):
    MERGE = 1
    RENAME = 2


class DocumentAssemblyPageRotation(IntEnum):
    NO_ROTATION = 0
    CLOCKWISE90 = 1
    CLOCKWISE180 = 2
    CLOCKWISE270 = 3


class OptimizationConversionStrategy(IntEnum):
    COPY = 1
    FLATTEN = 2


class OptimizationRemovalStrategy(IntEnum):
    FLATTEN = 2
    REMOVE = 3


class OptimizationCompressionAlgorithmSelection(IntEnum):
    PRESERVE_QUALITY = 1
    BALANCED = 2
    SPEED = 3


class Pdf2ImageFaxVerticalResolution(IntEnum):
    STANDARD = 1
    HIGH = 2


class Pdf2ImageTiffBitonalCompressionType(IntEnum):
    G3 = 1
    G4 = 2


class Pdf2ImageBackgroundType(IntEnum):
    WHITE = 1
    TRANSPARENT = 2


class Pdf2ImagePngColorSpace(IntEnum):
    RGB = 1
    GRAY = 2


class Pdf2ImageJpegColorSpace(IntEnum):
    RGB = 1
    GRAY = 2
    CMYK = 3


class Pdf2ImageColorSpace(IntEnum):
    RGB = 1
    GRAY = 2
    CMYK = 3


class Pdf2ImageAnnotationOptions(IntEnum):
    SHOW_ANNOTATIONS = 1
    SHOW_ANNOTATIONS_AND_POPUPS = 2


class PdfAValidationErrorCategory(IntEnum):
    FORMAT = 0x00000001
    PDF = 0x00000002
    ENCRYPTION = 0x00000004
    COLOR = 0x00000008
    RENDERING = 0x00000010
    ALTERNATE = 0x00000020
    POST_SCRIPT = 0x00000040
    EXTERNAL = 0x00000080
    FONT = 0x00000100
    UNICODE = 0x00000200
    TRANSPARENCY = 0x00000400
    UNSUPPORTED_ANNOTATION = 0x00000800
    MULTIMEDIA = 0x00001000
    PRINT = 0x00002000
    APPEARANCE = 0x00004000
    ACTION = 0x00008000
    METADATA = 0x00010000
    STRUCTURE = 0x00020000
    OPTIONAL_CONTENT = 0x00040000
    EMBEDDED_FILE = 0x00080000
    SIGNATURE = 0x00100000
    CUSTOM = 0x40000000


class PdfAConversionEventSeverity(IntEnum):
    INFORMATION = 1
    WARNING = 2
    ERROR = 3


class PdfAConversionEventCategory(IntEnum):
    VISUAL_DIFFERENCES = 0x00000001
    REPAIRED_CORRUPTION = 0x00000002
    MANAGED_COLORS = 0x00000004
    CHANGED_COLORANT = 0x00000008
    REMOVED_EXTERNAL_CONTENT = 0x00000010
    CONVERTED_FONT = 0x00000020
    SUBSTITUTED_FONT = 0x00000040
    REMOVED_TRANSPARENCY = 0x00000080
    REMOVED_ANNOTATION = 0x00000100
    REMOVED_MULTIMEDIA = 0x00000200
    REMOVED_ACTION = 0x00000400
    REMOVED_METADATA = 0x00000800
    REMOVED_STRUCTURE = 0x00001000
    REMOVED_OPTIONAL_CONTENT = 0x00002000
    CONVERTED_EMBEDDED_FILE = 0x00004000
    REMOVED_EMBEDDED_FILE = 0x00008000
    REMOVED_SIGNATURE = 0x00010000


class PdfAConversionEventCode(IntEnum):
    GENERIC = 0x00000001
    REMOVED_XFA = 0x01000000
    FONT_NON_EMBEDDED_ORDERING_IDENTITY = 0x01000001
    FONT_NO_ROTATE = 0x01000002
    FONT_NO_ITALIC_SIMULATION = 0x01000003
    CLIPPED_NUMBER_VALUE = 0x01000004
    RECOVERED_IMAGE_SIZE = 0x02000000
    REPAIRED_FONT = 0x02000001
    COPIED_OUTPUT_INTENT = 0x03000000
    SET_OUTPUT_INTENT = 0x03000001
    GENERATED_OUTPUT_INTENT = 0x03000002
    SET_COLOR_PROFILE = 0x03000003
    GENERATED_COLOR_PROFILE = 0x03000004
    CREATED_CALIBRATED = 0x03000005
    RENAMED_COLORANT = 0x04000000
    RESOLVED_COLORANT_COLLISION = 0x04000001
    EMBEDED_FONT = 0x06000000
    SUBSTITUTED_FONT = 0x07000000
    SUBSTITUTED_MULTIPLE_MASTER = 0x07000001
    CONVERTED_TO_STAMP = 0x09000000
    REMOVED_DOCUMENT_METADATA = 0x0C000000
    COPIED_EMBEDDED_FILE = 0x0F000000
    CONVERTING_EMBEDDED_FILE_START = 0x0F000001
    CONVERTING_EMBEDDED_FILE_SUCCESS = 0x0F000002
    CHANGED_TO_INITIAL_DOCUMENT = 0x10000000
    CONVERTING_EMBEDDED_FILE_ERROR = 0x10000001
    REMOVED_EMBEDDED_FILE = 0x10000002
    REMOVED_FILE_ATTACHMENT_ANNOTATION = 0x10000003


class PdfAConversionInvoiceType(IntEnum):
    ZUGFERD = 1
    FACTUR_X = 2


class PdfAConversionAFRelationship(IntEnum):
    SOURCE = 1
    DATA = 2
    ALTERNATIVE = 3
    SUPPLEMENT = 4
    UNSPECIFIED = 5


class SignWarningCategory(IntEnum):
    PDF_A_REMOVED = 1
    SIGNED_DOC_ENCRYPTION_UNCHANGED = 2
    ADD_VALIDATION_INFORMATION_FAILED = 3


class SignSignatureRemoval(IntEnum):
    NONE = 1
    SIGNED = 2
    ALL = 3


class SignAddValidationInformation(IntEnum):
    NONE = 1
    LATEST = 2
    ALL = 3


class CryptoHashAlgorithm(IntEnum):
    MD5 = 1
    RIPE_MD160 = 2
    SHA1 = 3
    SHA256 = 4
    SHA384 = 5
    SHA512 = 6
    SHA3_256 = 7
    SHA3_384 = 8
    SHA3_512 = 9


class CryptoSignatureAlgorithm(IntEnum):
    RSA_RSA = 1
    RSA_SSA_PSS = 2
    ECDSA = 3


class CryptoSignaturePaddingType(IntEnum):
    DEFAULT = 0
    RSA_RSA = 1
    RSA_SSA_PSS = 2


class CryptoSignatureFormat(IntEnum):
    ADBE_PKCS7_DETACHED = 1
    ETSI_CADES_DETACHED = 2


class CryptoValidationInformation(IntEnum):
    NONE = 0
    EMBED_IN_SIGNATURE = 1
    EMBED_IN_DOCUMENT = 2


class SignatureValidationIndication(IntEnum):
    VALID = 1
    INVALID = 2
    INDETERMINATE = 3


class SignatureValidationSubIndication(IntEnum):
    REVOKED = 1
    HASH_FAILURE = 2
    SIG_CRYPTO_FAILURE = 3
    SIG_CONSTRAINTS_FAILURE = 4
    CHAIN_CONSTRAINTS_FAILURE = 5
    CRYPTO_CONSTRAINTS_FAILURE = 6
    EXPIRED = 7
    NOT_YET_VALID = 8
    FORMAT_FAILURE = 9
    POLICY_PROCESSING_ERROR = 10
    UNKNOWN_COMMITMENT_TYPE = 11
    TIMESTAMP_ORDER_FAILURE = 12
    NO_SIGNER_CERTIFICATE_FOUND = 13
    NO_CERTIFICATE_CHAIN_FOUND = 14
    REVOKED_NO_POE = 15
    REVOKED_CA_NO_POE = 16
    OUT_OF_BOUNDS_NO_POE = 17
    CRYPTO_CONSTRAINTS_FAILURE_NO_POE = 18
    NO_POE = 19
    TRY_LATER = 20
    NO_POLICY = 21
    SIGNED_DATA_NOT_FOUND = 22
    INCOMPLETE_CERTIFICATE_CHAIN = 512
    CERTIFICATE_NO_REVOCATION_INFORMATION = 513
    MISSING_REVOCATION_INFORMATION = 514
    EXPIRED_NO_REVOCATION_INFORMATION = 515
    UNTRUSTED = 516
    GENERIC = 1024


class SignatureValidationSignatureSelector(IntEnum):
    LATEST = 1
    ALL = 2


class SignatureValidationTimeSource(Flag):
    PROOF_OF_EXISTENCE = 0x0001
    EXPIRED_TIME_STAMP = 0x0002
    SIGNATURE_TIME = 0x0004


class SignatureValidationDataSource(Flag):
    EMBED_IN_SIGNATURE = 0x0001
    EMBED_IN_DOCUMENT = 0x0002
    DOWNLOAD = 0x0004
    SYSTEM = 0x0008
    AATL = 0x0100
    EUTL = 0x0200
    CUSTOM_TRUST_LIST = 0x0400


class SignatureValidationProfilesRevocationCheckPolicy(IntEnum):
    REQUIRED = 1
    SUPPORTED = 2
    OPTIONAL = 3
    NO_CHECK = 4



# Derived types enumerations
class PdfOutputOptionsType(IntEnum):
    PDF_OUTPUT_OPTIONS = 1
    SIGN_OUTPUT_OPTIONS = 2

class PdfDocumentType(IntEnum):
    PDF_DOCUMENT = 1
    SIGN_PREPARED_DOCUMENT = 2

class PdfSignatureFieldType(IntEnum):
    PDF_SIGNATURE_FIELD = 1
    PDF_UNSIGNED_SIGNATURE_FIELD = 2
    PDF_SIGNED_SIGNATURE_FIELD = 3
    PDF_SIGNATURE = 4
    PDF_DOCUMENT_SIGNATURE = 5
    PDF_CERTIFICATION_SIGNATURE = 6
    PDF_DOCUMENT_TIMESTAMP = 7

class PdfSignedSignatureFieldType(IntEnum):
    PDF_SIGNED_SIGNATURE_FIELD = 1
    PDF_SIGNATURE = 2
    PDF_DOCUMENT_SIGNATURE = 3
    PDF_CERTIFICATION_SIGNATURE = 4
    PDF_DOCUMENT_TIMESTAMP = 5

class PdfSignatureType(IntEnum):
    PDF_SIGNATURE = 1
    PDF_DOCUMENT_SIGNATURE = 2
    PDF_CERTIFICATION_SIGNATURE = 3

class ImageDocumentType(IntEnum):
    IMAGE_DOCUMENT = 1
    IMAGE_SINGLE_PAGE_DOCUMENT = 2
    IMAGE_MULTI_PAGE_DOCUMENT = 3

class OptimizationProfilesProfileType(IntEnum):
    OPTIMIZATION_PROFILES_PROFILE = 1
    OPTIMIZATION_PROFILES_WEB = 2
    OPTIMIZATION_PROFILES_PRINT = 3
    OPTIMIZATION_PROFILES_ARCHIVE = 4
    OPTIMIZATION_PROFILES_MINIMAL_FILE_SIZE = 5
    OPTIMIZATION_PROFILES_MRC = 6

class Pdf2ImageImageOptionsType(IntEnum):
    PDF2_IMAGE_IMAGE_OPTIONS = 1
    PDF2_IMAGE_FAX_IMAGE_OPTIONS = 2
    PDF2_IMAGE_TIFF_JPEG_IMAGE_OPTIONS = 3
    PDF2_IMAGE_TIFF_LZW_IMAGE_OPTIONS = 4
    PDF2_IMAGE_TIFF_FLATE_IMAGE_OPTIONS = 5
    PDF2_IMAGE_PNG_IMAGE_OPTIONS = 6
    PDF2_IMAGE_JPEG_IMAGE_OPTIONS = 7

class Pdf2ImageImageSectionMappingType(IntEnum):
    PDF2_IMAGE_IMAGE_SECTION_MAPPING = 1
    PDF2_IMAGE_RENDER_PAGE_AS_FAX = 2
    PDF2_IMAGE_RENDER_PAGE_AT_RESOLUTION = 3
    PDF2_IMAGE_RENDER_PAGE_TO_MAX_IMAGE_SIZE = 4

class Pdf2ImageProfilesProfileType(IntEnum):
    PDF2_IMAGE_PROFILES_PROFILE = 1
    PDF2_IMAGE_PROFILES_FAX = 2
    PDF2_IMAGE_PROFILES_ARCHIVE = 3
    PDF2_IMAGE_PROFILES_VIEWING = 4

class Image2PdfImageMappingType(IntEnum):
    IMAGE2_PDF_IMAGE_MAPPING = 1
    IMAGE2_PDF_AUTO = 2
    IMAGE2_PDF_SHRINK_TO_PAGE = 3
    IMAGE2_PDF_SHRINK_TO_FIT = 4
    IMAGE2_PDF_SHRINK_TO_PORTRAIT = 5

class Image2PdfProfilesProfileType(IntEnum):
    IMAGE2_PDF_PROFILES_PROFILE = 1
    IMAGE2_PDF_PROFILES_DEFAULT = 2
    IMAGE2_PDF_PROFILES_ARCHIVE = 3

class SignSignatureConfigurationType(IntEnum):
    SIGN_SIGNATURE_CONFIGURATION = 1
    CRYPTO_PROVIDERS_GLOBAL_SIGN_DSS_SIGNATURE_CONFIGURATION = 2
    CRYPTO_PROVIDERS_SWISSCOM_SIG_SRV_SIGNATURE_CONFIGURATION = 3
    CRYPTO_PROVIDERS_PKCS11_SIGNATURE_CONFIGURATION = 4
    CRYPTO_PROVIDERS_BUILT_IN_SIGNATURE_CONFIGURATION = 5

class SignTimestampConfigurationType(IntEnum):
    SIGN_TIMESTAMP_CONFIGURATION = 1
    CRYPTO_PROVIDERS_GLOBAL_SIGN_DSS_TIMESTAMP_CONFIGURATION = 2
    CRYPTO_PROVIDERS_SWISSCOM_SIG_SRV_TIMESTAMP_CONFIGURATION = 3
    CRYPTO_PROVIDERS_PKCS11_TIMESTAMP_CONFIGURATION = 4
    CRYPTO_PROVIDERS_BUILT_IN_TIMESTAMP_CONFIGURATION = 5

class CryptoProvidersProviderType(IntEnum):
    CRYPTO_PROVIDERS_PROVIDER = 1
    CRYPTO_PROVIDERS_GLOBAL_SIGN_DSS_SESSION = 2
    CRYPTO_PROVIDERS_SWISSCOM_SIG_SRV_SESSION = 3
    CRYPTO_PROVIDERS_PKCS11_SESSION = 4
    CRYPTO_PROVIDERS_BUILT_IN_PROVIDER = 5

class SignatureValidationSignatureContentType(IntEnum):
    SIGNATURE_VALIDATION_SIGNATURE_CONTENT = 1
    SIGNATURE_VALIDATION_UNSUPPORTED_SIGNATURE_CONTENT = 2
    SIGNATURE_VALIDATION_CMS_SIGNATURE_CONTENT = 3
    SIGNATURE_VALIDATION_TIME_STAMP_CONTENT = 4

class SignatureValidationProfilesProfileType(IntEnum):
    SIGNATURE_VALIDATION_PROFILES_PROFILE = 1
    SIGNATURE_VALIDATION_PROFILES_DEFAULT = 2




# Structs type definitions

class GeomIntSize(Structure):
    _fields_ = [
        ("width", c_int),
        ("height", c_int),
    ]
class GeomUnitsResolution(Structure):
    _fields_ = [
        ("x_dpi", c_double),
        ("y_dpi", c_double),
    ]
class GeomUnitsSize(Structure):
    _fields_ = [
        ("width", c_double),
        ("height", c_double),
    ]
class GeomUnitsMargin(Structure):
    _fields_ = [
        ("left", c_double),
        ("bottom", c_double),
        ("right", c_double),
        ("top", c_double),
    ]
class GeomUnitsPoint(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
    ]
class GeomUnitsRectangle(Structure):
    _fields_ = [
        ("x", c_double),
        ("y", c_double),
        ("width", c_double),
        ("height", c_double),
    ]

class SysDate(Structure):
    _fields_ = [
        ("year", c_short),
        ("month", c_short),
        ("day", c_short),
        ("hour", c_short),
        ("minute", c_short),
        ("second", c_short),
        ("tz_sign", c_short),
        ("tz_hour", c_short),
        ("tz_minute", c_short),
    ]

PdfAValidation_Validator_ErrorFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_int, c_int)

PdfAConversion_Converter_ConversionEventFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_wchar_p, c_int, c_int, c_int, c_wchar_p, c_int)

Sign_Signer_WarningFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_int, c_wchar_p)

CryptoProvidersSwisscomSigSrv_StepUp_ConsentRequiredFunc = CFUNCTYPE(None, c_void_p, c_wchar_p)

SignatureValidation_Validator_ConstraintFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_int, c_int, c_void_p, c_wchar_p)



# General library functions

_lib.PdfTools_Initialize.restype = None
_lib.PdfTools_Initialize.argtypes = []

def initialize():
    return _lib.PdfTools_Initialize()

_lib.PdfTools_Uninitialize.restype = None
_lib.PdfTools_Uninitialize.argtypes = []

def uninitialize():
    return _lib.PdfTools_Uninitialize()

_lib.PdfTools_GetLastError.argtypes = None
_lib.PdfTools_GetLastError.restype = c_int

def getlasterror():
    return _lib.PdfTools_GetLastError()

_lib.PdfTools_GetLastErrorMessageW.restype = c_size_t
_lib.PdfTools_GetLastErrorMessageW.argtypes = [POINTER(c_wchar), c_size_t]

def getlasterrormessage():
    buffer_size = _lib.PdfTools_GetLastErrorMessageW(None, 0)
    buffer = create_unicode_buffer(buffer_size)
    _lib.PdfTools_GetLastErrorMessageW(buffer, buffer_size)
    return utf16_to_string(buffer, buffer_size)

_lib.PdfTools_SetLastErrorW.argtypes = [c_int, c_wchar_p]
_lib.PdfTools_SetLastErrorW.restype = None

def setlasterror(error_code, error_message):
    return _lib.PdfTools_SetLastErrorW(error_code, string_to_utf16(error_message))

# General object functions

_lib.PdfTools_Release.restype = None
_lib.PdfTools_Release.argtypes = [c_void_p]

def release(object):
    _lib.PdfTools_Release(object)

_lib.PdfTools_AddRef.restype = None
_lib.PdfTools_AddRef.argtypes = [c_void_p]

def addref(object):
    _lib.PdfTools_AddRef(object)

_lib.PdfTools_Equals.restype = c_bool
_lib.PdfTools_Equals.argtypes = [c_void_p, c_void_p]

def equals(object, other):
    _lib.PdfTools_Equals(object, other)

_lib.PdfTools_GetHashCode.restype = c_int
_lib.PdfTools_GetHashCode.argtypes = [c_void_p]

def gethashcode(object):
    _lib.PdfTools_GetHashCode(object)

# Class functions
_lib.PdfTools_ConsumptionData_GetRemainingPages.argtypes = [c_void_p]
_lib.PdfTools_ConsumptionData_GetRemainingPages.restype = c_int

def consumptiondata_getremainingpages(consumption_data):
    return _lib.PdfTools_ConsumptionData_GetRemainingPages(consumption_data)
_lib.PdfTools_ConsumptionData_GetOverconsumption.argtypes = [c_void_p]
_lib.PdfTools_ConsumptionData_GetOverconsumption.restype = c_int

def consumptiondata_getoverconsumption(consumption_data):
    return _lib.PdfTools_ConsumptionData_GetOverconsumption(consumption_data)


_lib.PdfTools_LicenseInfo_IsValid.argtypes = [c_void_p]
_lib.PdfTools_LicenseInfo_IsValid.restype = c_bool

def licenseinfo_isvalid(license_info):
    return _lib.PdfTools_LicenseInfo_IsValid(license_info)
_lib.PdfTools_LicenseInfo_GetExpirationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfTools_LicenseInfo_GetExpirationDate.restype = c_bool

def licenseinfo_getexpirationdate(license_info, ret_val):
    return _lib.PdfTools_LicenseInfo_GetExpirationDate(license_info, byref(ret_val))
_lib.PdfTools_LicenseInfo_GetConsumptionData.argtypes = [c_void_p]
_lib.PdfTools_LicenseInfo_GetConsumptionData.restype = c_void_p

def licenseinfo_getconsumptiondata(license_info):
    return _lib.PdfTools_LicenseInfo_GetConsumptionData(license_info)


_lib.PdfTools_Sdk_InitializeW.argtypes = [c_wchar_p, c_wchar_p]
_lib.PdfTools_Sdk_InitializeW.restype = c_bool

def sdk_initialize(license, producer_suffix):
    return _lib.PdfTools_Sdk_InitializeW(string_to_utf16(license), string_to_utf16(producer_suffix))

_lib.PdfTools_Sdk_AddFontDirectoryW.argtypes = [c_wchar_p]
_lib.PdfTools_Sdk_AddFontDirectoryW.restype = c_bool

def sdk_addfontdirectory(directory):
    return _lib.PdfTools_Sdk_AddFontDirectoryW(string_to_utf16(directory))


_lib.PdfTools_Sdk_GetVersionW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Sdk_GetVersionW.restype = c_size_t

def sdk_getversion():
    ret_buffer_size = _lib.PdfTools_Sdk_GetVersionW(None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Sdk_GetVersionW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Sdk_SetProducerSuffixW.argtypes = [c_wchar_p]
_lib.PdfTools_Sdk_SetProducerSuffixW.restype = c_bool

def sdk_setproducersuffix(val):
    return _lib.PdfTools_Sdk_SetProducerSuffixW(string_to_utf16(val))
_lib.PdfTools_Sdk_GetProducerFullNameW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Sdk_GetProducerFullNameW.restype = c_size_t

def sdk_getproducerfullname():
    ret_buffer_size = _lib.PdfTools_Sdk_GetProducerFullNameW(None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Sdk_GetProducerFullNameW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Sdk_GetProxyW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Sdk_GetProxyW.restype = c_size_t

def sdk_getproxy():
    ret_buffer_size = _lib.PdfTools_Sdk_GetProxyW(None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Sdk_GetProxyW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Sdk_SetProxyW.argtypes = [c_wchar_p]
_lib.PdfTools_Sdk_SetProxyW.restype = c_bool

def sdk_setproxy(val):
    return _lib.PdfTools_Sdk_SetProxyW(string_to_utf16(val))
_lib.PdfTools_Sdk_GetHttpClientHandler.argtypes = []
_lib.PdfTools_Sdk_GetHttpClientHandler.restype = c_void_p

def sdk_gethttpclienthandler():
    return _lib.PdfTools_Sdk_GetHttpClientHandler()
_lib.PdfTools_Sdk_GetUsageTracking.argtypes = []
_lib.PdfTools_Sdk_GetUsageTracking.restype = c_bool

def sdk_getusagetracking():
    return _lib.PdfTools_Sdk_GetUsageTracking()
_lib.PdfTools_Sdk_SetUsageTracking.argtypes = [c_bool]
_lib.PdfTools_Sdk_SetUsageTracking.restype = c_bool

def sdk_setusagetracking(val):
    return _lib.PdfTools_Sdk_SetUsageTracking(val)
_lib.PdfTools_Sdk_GetLicensingServiceW.argtypes = [POINTER(c_wchar), c_size_t]
_lib.PdfTools_Sdk_GetLicensingServiceW.restype = c_size_t

def sdk_getlicensingservice():
    ret_buffer_size = _lib.PdfTools_Sdk_GetLicensingServiceW(None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_Sdk_GetLicensingServiceW(ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_Sdk_SetLicensingServiceW.argtypes = [c_wchar_p]
_lib.PdfTools_Sdk_SetLicensingServiceW.restype = c_bool

def sdk_setlicensingservice(val):
    return _lib.PdfTools_Sdk_SetLicensingServiceW(string_to_utf16(val))
_lib.PdfTools_Sdk_GetLicenseInfoSnapshot.argtypes = []
_lib.PdfTools_Sdk_GetLicenseInfoSnapshot.restype = c_void_p

def sdk_getlicenseinfosnapshot():
    return _lib.PdfTools_Sdk_GetLicenseInfoSnapshot()


_lib.PdfTools_StringList_GetCount.argtypes = [c_void_p]
_lib.PdfTools_StringList_GetCount.restype = c_int

def stringlist_getcount(string_list):
    return _lib.PdfTools_StringList_GetCount(string_list)
_lib.PdfTools_StringList_GetW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_StringList_GetW.restype = c_size_t

def stringlist_get(string_list, i_index):
    ret_buffer_size = _lib.PdfTools_StringList_GetW(string_list, i_index, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_StringList_GetW(string_list, i_index, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_StringList_AddW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_StringList_AddW.restype = c_bool

def stringlist_add(string_list, string):
    return _lib.PdfTools_StringList_AddW(string_list, string_to_utf16(string))

_lib.PdfTools_StringList_New.argtypes = []
_lib.PdfTools_StringList_New.restype = c_void_p

def stringlist_new():
    return _lib.PdfTools_StringList_New()


_lib.PdfTools_MetadataDictionary_GetCount.argtypes = [c_void_p]
_lib.PdfTools_MetadataDictionary_GetCount.restype = c_int

def metadatadictionary_getcount(metadata_dictionary):
    return _lib.PdfTools_MetadataDictionary_GetCount(metadata_dictionary)
_lib.PdfTools_MetadataDictionary_GetSize.argtypes = [c_void_p]
_lib.PdfTools_MetadataDictionary_GetSize.restype = c_int

def metadatadictionary_getsize(metadata_dictionary):
    return _lib.PdfTools_MetadataDictionary_GetSize(metadata_dictionary)
_lib.PdfTools_MetadataDictionary_GetBegin.argtypes = [c_void_p]
_lib.PdfTools_MetadataDictionary_GetBegin.restype = c_int

def metadatadictionary_getbegin(metadata_dictionary):
    return _lib.PdfTools_MetadataDictionary_GetBegin(metadata_dictionary)
_lib.PdfTools_MetadataDictionary_GetEnd.argtypes = [c_void_p]
_lib.PdfTools_MetadataDictionary_GetEnd.restype = c_int

def metadatadictionary_getend(metadata_dictionary):
    return _lib.PdfTools_MetadataDictionary_GetEnd(metadata_dictionary)
_lib.PdfTools_MetadataDictionary_GetNext.argtypes = [c_void_p, c_int]
_lib.PdfTools_MetadataDictionary_GetNext.restype = c_int

def metadatadictionary_getnext(metadata_dictionary, it):
    return _lib.PdfTools_MetadataDictionary_GetNext(metadata_dictionary, it)
_lib.PdfTools_MetadataDictionary_GetW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfTools_MetadataDictionary_GetW.restype = c_int

def metadatadictionary_get(metadata_dictionary, key):
    return _lib.PdfTools_MetadataDictionary_GetW(metadata_dictionary, string_to_utf16(key))
_lib.PdfTools_MetadataDictionary_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_MetadataDictionary_GetKeyW.restype = c_size_t

def metadatadictionary_getkey(metadata_dictionary, it):
    ret_buffer_size = _lib.PdfTools_MetadataDictionary_GetKeyW(metadata_dictionary, it, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_MetadataDictionary_GetKeyW(metadata_dictionary, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_MetadataDictionary_GetValueW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfTools_MetadataDictionary_GetValueW.restype = c_size_t

def metadatadictionary_getvalue(metadata_dictionary, it):
    ret_buffer_size = _lib.PdfTools_MetadataDictionary_GetValueW(metadata_dictionary, it, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfTools_MetadataDictionary_GetValueW(metadata_dictionary, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfTools_MetadataDictionary_SetW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
_lib.PdfTools_MetadataDictionary_SetW.restype = c_bool

def metadatadictionary_set(metadata_dictionary, key, value):
    return _lib.PdfTools_MetadataDictionary_SetW(metadata_dictionary, string_to_utf16(key), string_to_utf16(value))

_lib.PdfTools_MetadataDictionary_SetValueW.argtypes = [c_void_p, c_int, c_wchar_p]
_lib.PdfTools_MetadataDictionary_SetValueW.restype = c_bool

def metadatadictionary_setvalue(metadata_dictionary, it, value):
    return _lib.PdfTools_MetadataDictionary_SetValueW(metadata_dictionary, it, string_to_utf16(value))

_lib.PdfTools_MetadataDictionary_Clear.argtypes = [c_void_p]
_lib.PdfTools_MetadataDictionary_Clear.restype = c_bool

def metadatadictionary_clear(metadata_dictionary):
    return _lib.PdfTools_MetadataDictionary_Clear(metadata_dictionary)

_lib.PdfTools_MetadataDictionary_Remove.argtypes = [c_void_p, c_int]
_lib.PdfTools_MetadataDictionary_Remove.restype = c_bool

def metadatadictionary_remove(metadata_dictionary, it):
    return _lib.PdfTools_MetadataDictionary_Remove(metadata_dictionary, it)


_lib.PdfTools_MetadataDictionary_New.argtypes = []
_lib.PdfTools_MetadataDictionary_New.restype = c_void_p

def metadatadictionary_new():
    return _lib.PdfTools_MetadataDictionary_New()


_lib.PdfTools_HttpClientHandler_SetClientCertificateW.argtypes = [c_void_p, POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfTools_HttpClientHandler_SetClientCertificateW.restype = c_bool

def httpclienthandler_setclientcertificate(http_client_handler, archive, password):
    return _lib.PdfTools_HttpClientHandler_SetClientCertificateW(http_client_handler, archive, string_to_utf16(password))

_lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW.argtypes = [c_void_p, POINTER(StreamDescriptor), POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW.restype = c_bool

def httpclienthandler_setclientcertificateandkey(http_client_handler, cert, key, password):
    return _lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW(http_client_handler, cert, key, string_to_utf16(password))

_lib.PdfTools_HttpClientHandler_AddTrustedCertificate.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfTools_HttpClientHandler_AddTrustedCertificate.restype = c_bool

def httpclienthandler_addtrustedcertificate(http_client_handler, cert):
    return _lib.PdfTools_HttpClientHandler_AddTrustedCertificate(http_client_handler, cert)


_lib.PdfTools_HttpClientHandler_New.argtypes = []
_lib.PdfTools_HttpClientHandler_New.restype = c_void_p

def httpclienthandler_new():
    return _lib.PdfTools_HttpClientHandler_New()

_lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate.argtypes = [c_void_p]
_lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate.restype = c_bool

def httpclienthandler_getsslverifyservercertificate(http_client_handler):
    return _lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate(http_client_handler)
_lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate.argtypes = [c_void_p, c_bool]
_lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate.restype = c_bool

def httpclienthandler_setsslverifyservercertificate(http_client_handler, val):
    return _lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate(http_client_handler, val)


_lib.PdfToolsPdf_MetadataSettings_New.argtypes = []
_lib.PdfToolsPdf_MetadataSettings_New.restype = c_void_p

def pdf_metadatasettings_new():
    return _lib.PdfToolsPdf_MetadataSettings_New()

_lib.PdfToolsPdf_MetadataSettings_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetTitleW.restype = c_size_t

def pdf_metadatasettings_gettitle(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetTitleW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetTitleW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetTitleW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetTitleW.restype = c_bool

def pdf_metadatasettings_settitle(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetTitleW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetAuthorW.restype = c_size_t

def pdf_metadatasettings_getauthor(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetAuthorW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetAuthorW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetAuthorW.restype = c_bool

def pdf_metadatasettings_setauthor(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetAuthorW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetSubjectW.restype = c_size_t

def pdf_metadatasettings_getsubject(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetSubjectW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetSubjectW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetSubjectW.restype = c_bool

def pdf_metadatasettings_setsubject(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetSubjectW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetKeywordsW.restype = c_size_t

def pdf_metadatasettings_getkeywords(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetKeywordsW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetKeywordsW.restype = c_bool

def pdf_metadatasettings_setkeywords(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetKeywordsW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetCreatorW.restype = c_size_t

def pdf_metadatasettings_getcreator(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetCreatorW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetCreatorW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetCreatorW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetCreatorW.restype = c_bool

def pdf_metadatasettings_setcreator(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetCreatorW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_MetadataSettings_GetProducerW.restype = c_size_t

def pdf_metadatasettings_getproducer(metadata_settings):
    ret_buffer_size = _lib.PdfToolsPdf_MetadataSettings_GetProducerW(metadata_settings, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_MetadataSettings_GetProducerW(metadata_settings, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_MetadataSettings_SetProducerW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_MetadataSettings_SetProducerW.restype = c_bool

def pdf_metadatasettings_setproducer(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetProducerW(metadata_settings, string_to_utf16(val))
_lib.PdfToolsPdf_MetadataSettings_GetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_MetadataSettings_GetCreationDate.restype = c_bool

def pdf_metadatasettings_getcreationdate(metadata_settings, ret_val):
    return _lib.PdfToolsPdf_MetadataSettings_GetCreationDate(metadata_settings, byref(ret_val))
_lib.PdfToolsPdf_MetadataSettings_SetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_MetadataSettings_SetCreationDate.restype = c_bool

def pdf_metadatasettings_setcreationdate(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetCreationDate(metadata_settings, val)
_lib.PdfToolsPdf_MetadataSettings_GetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_MetadataSettings_GetModificationDate.restype = c_bool

def pdf_metadatasettings_getmodificationdate(metadata_settings, ret_val):
    return _lib.PdfToolsPdf_MetadataSettings_GetModificationDate(metadata_settings, byref(ret_val))
_lib.PdfToolsPdf_MetadataSettings_SetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_MetadataSettings_SetModificationDate.restype = c_bool

def pdf_metadatasettings_setmodificationdate(metadata_settings, val):
    return _lib.PdfToolsPdf_MetadataSettings_SetModificationDate(metadata_settings, val)


_lib.PdfToolsPdf_Encryption_SetPermissionsW.argtypes = [c_void_p, c_wchar_p, c_int]
_lib.PdfToolsPdf_Encryption_SetPermissionsW.restype = c_bool

def pdf_encryption_setpermissions(encryption, owner_password, permissions):
    return _lib.PdfToolsPdf_Encryption_SetPermissionsW(encryption, string_to_utf16(owner_password), permissions)


_lib.PdfToolsPdf_Encryption_NewW.argtypes = [c_wchar_p, c_wchar_p, c_int]
_lib.PdfToolsPdf_Encryption_NewW.restype = c_void_p

def pdf_encryption_new(user_password, owner_password, permissions):
    return _lib.PdfToolsPdf_Encryption_NewW(string_to_utf16(user_password), string_to_utf16(owner_password), permissions)

_lib.PdfToolsPdf_Encryption_GetUserPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Encryption_GetUserPasswordW.restype = c_size_t

def pdf_encryption_getuserpassword(encryption):
    ret_buffer_size = _lib.PdfToolsPdf_Encryption_GetUserPasswordW(encryption, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Encryption_GetUserPasswordW(encryption, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Encryption_SetUserPasswordW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsPdf_Encryption_SetUserPasswordW.restype = c_bool

def pdf_encryption_setuserpassword(encryption, val):
    return _lib.PdfToolsPdf_Encryption_SetUserPasswordW(encryption, string_to_utf16(val))
_lib.PdfToolsPdf_Encryption_GetOwnerPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Encryption_GetOwnerPasswordW.restype = c_size_t

def pdf_encryption_getownerpassword(encryption):
    ret_buffer_size = _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW(encryption, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW(encryption, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Encryption_GetPermissions.argtypes = [c_void_p]
_lib.PdfToolsPdf_Encryption_GetPermissions.restype = c_int

def pdf_encryption_getpermissions(encryption):
    return _lib.PdfToolsPdf_Encryption_GetPermissions(encryption)


_lib.PdfToolsPdf_OutputOptions_New.argtypes = []
_lib.PdfToolsPdf_OutputOptions_New.restype = c_void_p

def pdf_outputoptions_new():
    return _lib.PdfToolsPdf_OutputOptions_New()

_lib.PdfToolsPdf_OutputOptions_GetEncryption.argtypes = [c_void_p]
_lib.PdfToolsPdf_OutputOptions_GetEncryption.restype = c_void_p

def pdf_outputoptions_getencryption(output_options):
    return _lib.PdfToolsPdf_OutputOptions_GetEncryption(output_options)
_lib.PdfToolsPdf_OutputOptions_SetEncryption.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsPdf_OutputOptions_SetEncryption.restype = c_bool

def pdf_outputoptions_setencryption(output_options, val):
    return _lib.PdfToolsPdf_OutputOptions_SetEncryption(output_options, val)
_lib.PdfToolsPdf_OutputOptions_GetMetadataSettings.argtypes = [c_void_p]
_lib.PdfToolsPdf_OutputOptions_GetMetadataSettings.restype = c_void_p

def pdf_outputoptions_getmetadatasettings(output_options):
    return _lib.PdfToolsPdf_OutputOptions_GetMetadataSettings(output_options)
_lib.PdfToolsPdf_OutputOptions_SetMetadataSettings.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsPdf_OutputOptions_SetMetadataSettings.restype = c_bool

def pdf_outputoptions_setmetadatasettings(output_options, val):
    return _lib.PdfToolsPdf_OutputOptions_SetMetadataSettings(output_options, val)

_lib.PdfToolsPdf_OutputOptions_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf_OutputOptions_GetType.restype = c_int

def pdf_outputoptions_gettype(object):
    return _lib.PdfToolsPdf_OutputOptions_GetType(object)

_lib.PdfToolsPdf_Document_OpenW.argtypes = [POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfToolsPdf_Document_OpenW.restype = c_void_p

def pdf_document_open(stream, password):
    return _lib.PdfToolsPdf_Document_OpenW(stream, string_to_utf16(password))

_lib.PdfToolsPdf_Document_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf_Document_GetConformance.restype = c_bool

def pdf_document_getconformance(document, ret_val):
    return _lib.PdfToolsPdf_Document_GetConformance(document, byref(ret_val))
_lib.PdfToolsPdf_Document_GetPageCount.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_GetPageCount.restype = c_int

def pdf_document_getpagecount(document):
    return _lib.PdfToolsPdf_Document_GetPageCount(document)
_lib.PdfToolsPdf_Document_GetPermissions.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf_Document_GetPermissions.restype = c_bool

def pdf_document_getpermissions(document, ret_val):
    return _lib.PdfToolsPdf_Document_GetPermissions(document, byref(ret_val))
_lib.PdfToolsPdf_Document_IsLinearized.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_IsLinearized.restype = c_bool

def pdf_document_islinearized(document):
    return _lib.PdfToolsPdf_Document_IsLinearized(document)
_lib.PdfToolsPdf_Document_IsSigned.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_IsSigned.restype = c_bool

def pdf_document_issigned(document):
    return _lib.PdfToolsPdf_Document_IsSigned(document)
_lib.PdfToolsPdf_Document_GetSignatureFields.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_GetSignatureFields.restype = c_void_p

def pdf_document_getsignaturefields(document):
    return _lib.PdfToolsPdf_Document_GetSignatureFields(document)
_lib.PdfToolsPdf_Document_GetXfa.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_GetXfa.restype = c_int

def pdf_document_getxfa(document):
    return _lib.PdfToolsPdf_Document_GetXfa(document)
_lib.PdfToolsPdf_Document_GetMetadata.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_GetMetadata.restype = c_void_p

def pdf_document_getmetadata(document):
    return _lib.PdfToolsPdf_Document_GetMetadata(document)

_lib.PdfToolsPdf_Document_Close.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_Close.restype = c_bool

def pdf_document_close(object):
    return _lib.PdfToolsPdf_Document_Close(object)

_lib.PdfToolsPdf_Document_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf_Document_GetType.restype = c_int

def pdf_document_gettype(object):
    return _lib.PdfToolsPdf_Document_GetType(object)

_lib.PdfToolsPdf_Metadata_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetTitleW.restype = c_size_t

def pdf_metadata_gettitle(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetTitleW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetTitleW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetAuthorW.restype = c_size_t

def pdf_metadata_getauthor(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetAuthorW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetAuthorW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetSubjectW.restype = c_size_t

def pdf_metadata_getsubject(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetSubjectW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetSubjectW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetKeywordsW.restype = c_size_t

def pdf_metadata_getkeywords(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetKeywordsW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetKeywordsW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetCreatorW.restype = c_size_t

def pdf_metadata_getcreator(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetCreatorW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetCreatorW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Metadata_GetProducerW.restype = c_size_t

def pdf_metadata_getproducer(metadata):
    ret_buffer_size = _lib.PdfToolsPdf_Metadata_GetProducerW(metadata, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Metadata_GetProducerW(metadata, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Metadata_GetCreationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_Metadata_GetCreationDate.restype = c_bool

def pdf_metadata_getcreationdate(metadata, ret_val):
    return _lib.PdfToolsPdf_Metadata_GetCreationDate(metadata, byref(ret_val))
_lib.PdfToolsPdf_Metadata_GetModificationDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_Metadata_GetModificationDate.restype = c_bool

def pdf_metadata_getmodificationdate(metadata, ret_val):
    return _lib.PdfToolsPdf_Metadata_GetModificationDate(metadata, byref(ret_val))


_lib.PdfToolsPdf_SignatureField_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_SignatureField_GetFieldNameW.restype = c_size_t

def pdf_signaturefield_getfieldname(signature_field):
    ret_buffer_size = _lib.PdfToolsPdf_SignatureField_GetFieldNameW(signature_field, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_SignatureField_GetFieldNameW(signature_field, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_SignatureField_GetPageNumber.argtypes = [c_void_p]
_lib.PdfToolsPdf_SignatureField_GetPageNumber.restype = c_int

def pdf_signaturefield_getpagenumber(signature_field):
    return _lib.PdfToolsPdf_SignatureField_GetPageNumber(signature_field)
_lib.PdfToolsPdf_SignatureField_GetBoundingBox.argtypes = [c_void_p, POINTER(GeomUnitsRectangle)]
_lib.PdfToolsPdf_SignatureField_GetBoundingBox.restype = c_bool

def pdf_signaturefield_getboundingbox(signature_field, ret_val):
    return _lib.PdfToolsPdf_SignatureField_GetBoundingBox(signature_field, byref(ret_val))

_lib.PdfToolsPdf_SignatureField_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf_SignatureField_GetType.restype = c_int

def pdf_signaturefield_gettype(object):
    return _lib.PdfToolsPdf_SignatureField_GetType(object)

_lib.PdfToolsPdf_SignedSignatureField_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_SignedSignatureField_GetNameW.restype = c_size_t

def pdf_signedsignaturefield_getname(signed_signature_field):
    ret_buffer_size = _lib.PdfToolsPdf_SignedSignatureField_GetNameW(signed_signature_field, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_SignedSignatureField_GetNameW(signed_signature_field, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_SignedSignatureField_GetDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsPdf_SignedSignatureField_GetDate.restype = c_bool

def pdf_signedsignaturefield_getdate(signed_signature_field, ret_val):
    return _lib.PdfToolsPdf_SignedSignatureField_GetDate(signed_signature_field, byref(ret_val))
_lib.PdfToolsPdf_SignedSignatureField_GetRevision.argtypes = [c_void_p]
_lib.PdfToolsPdf_SignedSignatureField_GetRevision.restype = c_void_p

def pdf_signedsignaturefield_getrevision(signed_signature_field):
    return _lib.PdfToolsPdf_SignedSignatureField_GetRevision(signed_signature_field)

_lib.PdfToolsPdf_SignedSignatureField_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf_SignedSignatureField_GetType.restype = c_int

def pdf_signedsignaturefield_gettype(object):
    return _lib.PdfToolsPdf_SignedSignatureField_GetType(object)

_lib.PdfToolsPdf_Signature_GetLocationW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Signature_GetLocationW.restype = c_size_t

def pdf_signature_getlocation(signature):
    ret_buffer_size = _lib.PdfToolsPdf_Signature_GetLocationW(signature, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Signature_GetLocationW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Signature_GetReasonW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Signature_GetReasonW.restype = c_size_t

def pdf_signature_getreason(signature):
    ret_buffer_size = _lib.PdfToolsPdf_Signature_GetReasonW(signature, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Signature_GetReasonW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsPdf_Signature_GetContactInfoW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsPdf_Signature_GetContactInfoW.restype = c_size_t

def pdf_signature_getcontactinfo(signature):
    ret_buffer_size = _lib.PdfToolsPdf_Signature_GetContactInfoW(signature, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsPdf_Signature_GetContactInfoW(signature, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)

_lib.PdfToolsPdf_Signature_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf_Signature_GetType.restype = c_int

def pdf_signature_gettype(object):
    return _lib.PdfToolsPdf_Signature_GetType(object)

_lib.PdfToolsPdf_CertificationSignature_GetPermissions.argtypes = [c_void_p]
_lib.PdfToolsPdf_CertificationSignature_GetPermissions.restype = c_int

def pdf_certificationsignature_getpermissions(certification_signature):
    return _lib.PdfToolsPdf_CertificationSignature_GetPermissions(certification_signature)


_lib.PdfToolsPdf_SignatureFieldList_GetCount.argtypes = [c_void_p]
_lib.PdfToolsPdf_SignatureFieldList_GetCount.restype = c_int

def pdf_signaturefieldlist_getcount(signature_field_list):
    return _lib.PdfToolsPdf_SignatureFieldList_GetCount(signature_field_list)
_lib.PdfToolsPdf_SignatureFieldList_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf_SignatureFieldList_Get.restype = c_void_p

def pdf_signaturefieldlist_get(signature_field_list, i_index):
    return _lib.PdfToolsPdf_SignatureFieldList_Get(signature_field_list, i_index)


_lib.PdfToolsPdf_Revision_Write.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfToolsPdf_Revision_Write.restype = c_bool

def pdf_revision_write(revision, stream):
    return _lib.PdfToolsPdf_Revision_Write(revision, stream)


_lib.PdfToolsPdf_Revision_IsLatest.argtypes = [c_void_p]
_lib.PdfToolsPdf_Revision_IsLatest.restype = c_bool

def pdf_revision_islatest(revision):
    return _lib.PdfToolsPdf_Revision_IsLatest(revision)
_lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates.argtypes = [c_void_p]
_lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates.restype = c_bool

def pdf_revision_gethasnonsigningupdates(revision):
    return _lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates(revision)


_lib.PdfToolsImage_Page_GetSize.argtypes = [c_void_p, POINTER(GeomIntSize)]
_lib.PdfToolsImage_Page_GetSize.restype = c_bool

def image_page_getsize(page, ret_val):
    return _lib.PdfToolsImage_Page_GetSize(page, byref(ret_val))
_lib.PdfToolsImage_Page_GetResolution.argtypes = [c_void_p, POINTER(GeomUnitsResolution)]
_lib.PdfToolsImage_Page_GetResolution.restype = c_bool

def image_page_getresolution(page, ret_val):
    return _lib.PdfToolsImage_Page_GetResolution(page, byref(ret_val))


_lib.PdfToolsImage_PageList_GetCount.argtypes = [c_void_p]
_lib.PdfToolsImage_PageList_GetCount.restype = c_int

def image_pagelist_getcount(page_list):
    return _lib.PdfToolsImage_PageList_GetCount(page_list)
_lib.PdfToolsImage_PageList_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsImage_PageList_Get.restype = c_void_p

def image_pagelist_get(page_list, i_index):
    return _lib.PdfToolsImage_PageList_Get(page_list, i_index)


_lib.PdfToolsImage_Document_Open.argtypes = [POINTER(StreamDescriptor)]
_lib.PdfToolsImage_Document_Open.restype = c_void_p

def image_document_open(stream):
    return _lib.PdfToolsImage_Document_Open(stream)

_lib.PdfToolsImage_Document_Close.argtypes = [c_void_p]
_lib.PdfToolsImage_Document_Close.restype = c_bool

def image_document_close(object):
    return _lib.PdfToolsImage_Document_Close(object)

_lib.PdfToolsImage_Document_GetType.argtypes = [c_void_p]
_lib.PdfToolsImage_Document_GetType.restype = c_int

def image_document_gettype(object):
    return _lib.PdfToolsImage_Document_GetType(object)

_lib.PdfToolsImage_SinglePageDocument_GetPage.argtypes = [c_void_p]
_lib.PdfToolsImage_SinglePageDocument_GetPage.restype = c_void_p

def image_singlepagedocument_getpage(single_page_document):
    return _lib.PdfToolsImage_SinglePageDocument_GetPage(single_page_document)


_lib.PdfToolsImage_MultiPageDocument_GetPages.argtypes = [c_void_p]
_lib.PdfToolsImage_MultiPageDocument_GetPages.restype = c_void_p

def image_multipagedocument_getpages(multi_page_document):
    return _lib.PdfToolsImage_MultiPageDocument_GetPages(multi_page_document)


_lib.PdfToolsImage_DocumentList_GetCount.argtypes = [c_void_p]
_lib.PdfToolsImage_DocumentList_GetCount.restype = c_int

def image_documentlist_getcount(document_list):
    return _lib.PdfToolsImage_DocumentList_GetCount(document_list)
_lib.PdfToolsImage_DocumentList_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsImage_DocumentList_Get.restype = c_void_p

def image_documentlist_get(document_list, i_index):
    return _lib.PdfToolsImage_DocumentList_Get(document_list, i_index)
_lib.PdfToolsImage_DocumentList_Add.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsImage_DocumentList_Add.restype = c_bool

def image_documentlist_add(document_list, document):
    return _lib.PdfToolsImage_DocumentList_Add(document_list, document)

_lib.PdfToolsImage_DocumentList_New.argtypes = []
_lib.PdfToolsImage_DocumentList_New.restype = c_void_p

def image_documentlist_new():
    return _lib.PdfToolsImage_DocumentList_New()


_lib.PdfToolsDocumentAssembly_PageCopyOptions_New.argtypes = []
_lib.PdfToolsDocumentAssembly_PageCopyOptions_New.restype = c_void_p

def documentassembly_pagecopyoptions_new():
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_New()

_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks.restype = c_int

def documentassembly_pagecopyoptions_getlinks(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks.restype = c_bool

def documentassembly_pagecopyoptions_setlinks(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields.restype = c_int

def documentassembly_pagecopyoptions_getformfields(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields.restype = c_bool

def documentassembly_pagecopyoptions_setformfields(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures.restype = c_int

def documentassembly_pagecopyoptions_getsignedsignatures(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures.restype = c_bool

def documentassembly_pagecopyoptions_setsignedsignatures(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures.restype = c_int

def documentassembly_pagecopyoptions_getunsignedsignatures(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures.restype = c_bool

def documentassembly_pagecopyoptions_setunsignedsignatures(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations.restype = c_int

def documentassembly_pagecopyoptions_getannotations(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations.restype = c_bool

def documentassembly_pagecopyoptions_setannotations(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems.restype = c_bool

def documentassembly_pagecopyoptions_getcopyoutlineitems(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems.restype = c_bool

def documentassembly_pagecopyoptions_setcopyoutlineitems(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles.restype = c_bool

def documentassembly_pagecopyoptions_getcopyassociatedfiles(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles.restype = c_bool

def documentassembly_pagecopyoptions_setcopyassociatedfiles(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure.restype = c_bool

def documentassembly_pagecopyoptions_getcopylogicalstructure(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure.restype = c_bool

def documentassembly_pagecopyoptions_setcopylogicalstructure(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution.restype = c_int

def documentassembly_pagecopyoptions_getformfieldconflictresolution(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution.restype = c_bool

def documentassembly_pagecopyoptions_setformfieldconflictresolution(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations.restype = c_int

def documentassembly_pagecopyoptions_getnameddestinations(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations.restype = c_bool

def documentassembly_pagecopyoptions_setnameddestinations(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources.restype = c_bool

def documentassembly_pagecopyoptions_getoptimizeresources(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources.restype = c_bool

def documentassembly_pagecopyoptions_setoptimizeresources(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources(page_copy_options, val)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation.restype = c_int

def documentassembly_pagecopyoptions_getpagerotation(page_copy_options):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation(page_copy_options)
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation.argtypes = [c_void_p, c_int]
_lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation.restype = c_bool

def documentassembly_pagecopyoptions_setpagerotation(page_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation(page_copy_options, val)


_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New.argtypes = []
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New.restype = c_void_p

def documentassembly_documentcopyoptions_new():
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New()

_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata.restype = c_bool

def documentassembly_documentcopyoptions_getcopymetadata(document_copy_options):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata(document_copy_options)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata.restype = c_bool

def documentassembly_documentcopyoptions_setcopymetadata(document_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata(document_copy_options, val)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent.restype = c_bool

def documentassembly_documentcopyoptions_getcopyoutputintent(document_copy_options):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent(document_copy_options)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent.restype = c_bool

def documentassembly_documentcopyoptions_setcopyoutputintent(document_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent(document_copy_options, val)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings.restype = c_bool

def documentassembly_documentcopyoptions_getcopyviewersettings(document_copy_options):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings(document_copy_options)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings.restype = c_bool

def documentassembly_documentcopyoptions_setcopyviewersettings(document_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings(document_copy_options, val)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles.restype = c_bool

def documentassembly_documentcopyoptions_getcopyembeddedfiles(document_copy_options):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles(document_copy_options)
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles.argtypes = [c_void_p, c_bool]
_lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles.restype = c_bool

def documentassembly_documentcopyoptions_setcopyembeddedfiles(document_copy_options, val):
    return _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles(document_copy_options, val)


_lib.PdfToolsDocumentAssembly_DocumentAssembler_Append.argtypes = [c_void_p, c_void_p, POINTER(c_int), POINTER(c_int), c_void_p, c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentAssembler_Append.restype = c_bool

def documentassembly_documentassembler_append(document_assembler, in_doc, first_page, last_page, document_copy_options, page_copy_options):
    return _lib.PdfToolsDocumentAssembly_DocumentAssembler_Append(document_assembler, in_doc, byref(c_int(first_page)) if first_page is not None else None, byref(c_int(last_page)) if last_page is not None else None, document_copy_options, page_copy_options)

_lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble.restype = c_void_p

def documentassembly_documentassembler_assemble(document_assembler):
    return _lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble(document_assembler)

_lib.PdfToolsDocumentAssembly_DocumentAssembler_New.argtypes = [POINTER(StreamDescriptor), c_void_p, POINTER(c_int)]
_lib.PdfToolsDocumentAssembly_DocumentAssembler_New.restype = c_void_p

def documentassembly_documentassembler_new(out_stream, out_options, conformance):
    return _lib.PdfToolsDocumentAssembly_DocumentAssembler_New(out_stream, out_options, byref(c_int(conformance)) if conformance is not None else None)

_lib.PdfToolsDocumentAssembly_DocumentAssembler_Close.argtypes = [c_void_p]
_lib.PdfToolsDocumentAssembly_DocumentAssembler_Close.restype = c_bool

def documentassembly_documentassembler_close(object):
    return _lib.PdfToolsDocumentAssembly_DocumentAssembler_Close(object)


_lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection.argtypes = [c_void_p]
_lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection.restype = c_int

def optimization_imagerecompressionoptions_getalgorithmselection(image_recompression_options):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection(image_recompression_options)
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection.argtypes = [c_void_p, c_int]
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection.restype = c_bool

def optimization_imagerecompressionoptions_setalgorithmselection(image_recompression_options, val):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection(image_recompression_options, val)
_lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality.argtypes = [c_void_p]
_lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality.restype = c_double

def optimization_imagerecompressionoptions_getcompressionquality(image_recompression_options):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality(image_recompression_options)
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality.argtypes = [c_void_p, c_double]
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality.restype = c_bool

def optimization_imagerecompressionoptions_setcompressionquality(image_recompression_options, val):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality(image_recompression_options, val)
_lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity.argtypes = [c_void_p]
_lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity.restype = c_bool

def optimization_imagerecompressionoptions_getreducecolorcomplexity(image_recompression_options):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity(image_recompression_options)
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity.restype = c_bool

def optimization_imagerecompressionoptions_setreducecolorcomplexity(image_recompression_options, val):
    return _lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity(image_recompression_options, val)


_lib.PdfToolsOptimization_FontOptions_GetMerge.argtypes = [c_void_p]
_lib.PdfToolsOptimization_FontOptions_GetMerge.restype = c_bool

def optimization_fontoptions_getmerge(font_options):
    return _lib.PdfToolsOptimization_FontOptions_GetMerge(font_options)
_lib.PdfToolsOptimization_FontOptions_SetMerge.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_FontOptions_SetMerge.restype = c_bool

def optimization_fontoptions_setmerge(font_options, val):
    return _lib.PdfToolsOptimization_FontOptions_SetMerge(font_options, val)
_lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts.argtypes = [c_void_p]
_lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts.restype = c_bool

def optimization_fontoptions_getremovestandardfonts(font_options):
    return _lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts(font_options)
_lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts.restype = c_bool

def optimization_fontoptions_setremovestandardfonts(font_options, val):
    return _lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts(font_options, val)


_lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages.restype = c_bool

def optimization_removaloptions_getremovealternateimages(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages.restype = c_bool

def optimization_removaloptions_setremovealternateimages(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads.restype = c_bool

def optimization_removaloptions_getremovearticlethreads(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads.restype = c_bool

def optimization_removaloptions_setremovearticlethreads(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata.restype = c_bool

def optimization_removaloptions_getremovemetadata(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata.restype = c_bool

def optimization_removaloptions_setremovemetadata(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents.restype = c_bool

def optimization_removaloptions_getremoveoutputintents(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents.restype = c_bool

def optimization_removaloptions_setremoveoutputintents(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo.restype = c_bool

def optimization_removaloptions_getremovepieceinfo(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo.restype = c_bool

def optimization_removaloptions_setremovepieceinfo(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree.restype = c_bool

def optimization_removaloptions_getremovestructuretree(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree.restype = c_bool

def optimization_removaloptions_setremovestructuretree(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails.restype = c_bool

def optimization_removaloptions_getremovethumbnails(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails.restype = c_bool

def optimization_removaloptions_setremovethumbnails(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances.restype = c_int

def optimization_removaloptions_getremovesignatureappearances(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances.argtypes = [c_void_p, c_int]
_lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances.restype = c_bool

def optimization_removaloptions_setremovesignatureappearances(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetAnnotations.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetAnnotations.restype = c_int

def optimization_removaloptions_getannotations(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetAnnotations(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetAnnotations.argtypes = [c_void_p, c_int]
_lib.PdfToolsOptimization_RemovalOptions_SetAnnotations.restype = c_bool

def optimization_removaloptions_setannotations(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetAnnotations(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetFormFields.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetFormFields.restype = c_int

def optimization_removaloptions_getformfields(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetFormFields(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetFormFields.argtypes = [c_void_p, c_int]
_lib.PdfToolsOptimization_RemovalOptions_SetFormFields.restype = c_bool

def optimization_removaloptions_setformfields(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetFormFields(removal_options, val)
_lib.PdfToolsOptimization_RemovalOptions_GetLinks.argtypes = [c_void_p]
_lib.PdfToolsOptimization_RemovalOptions_GetLinks.restype = c_int

def optimization_removaloptions_getlinks(removal_options):
    return _lib.PdfToolsOptimization_RemovalOptions_GetLinks(removal_options)
_lib.PdfToolsOptimization_RemovalOptions_SetLinks.argtypes = [c_void_p, c_int]
_lib.PdfToolsOptimization_RemovalOptions_SetLinks.restype = c_bool

def optimization_removaloptions_setlinks(removal_options, val):
    return _lib.PdfToolsOptimization_RemovalOptions_SetLinks(removal_options, val)


_lib.PdfToolsOptimization_Optimizer_OptimizeDocument.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsOptimization_Optimizer_OptimizeDocument.restype = c_void_p

def optimization_optimizer_optimizedocument(optimizer, in_doc, out_stream, profile, out_options):
    return _lib.PdfToolsOptimization_Optimizer_OptimizeDocument(optimizer, in_doc, out_stream, profile, out_options)

_lib.PdfToolsOptimization_Optimizer_New.argtypes = []
_lib.PdfToolsOptimization_Optimizer_New.restype = c_void_p

def optimization_optimizer_new():
    return _lib.PdfToolsOptimization_Optimizer_New()


_lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions.restype = c_void_p

def optimizationprofiles_profile_getimagerecompressionoptions(profile):
    return _lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions(profile)
_lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions.restype = c_void_p

def optimizationprofiles_profile_getfontoptions(profile):
    return _lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions(profile)
_lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions.restype = c_void_p

def optimizationprofiles_profile_getremovaloptions(profile):
    return _lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions(profile)
_lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata.restype = c_bool

def optimizationprofiles_profile_getcopymetadata(profile):
    return _lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata(profile)
_lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata.restype = c_bool

def optimizationprofiles_profile_setcopymetadata(profile, val):
    return _lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata(profile, val)

_lib.PdfToolsOptimizationProfiles_Profile_GetType.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Profile_GetType.restype = c_int

def optimizationprofiles_profile_gettype(object):
    return _lib.PdfToolsOptimizationProfiles_Profile_GetType(object)

_lib.PdfToolsOptimizationProfiles_Web_New.argtypes = []
_lib.PdfToolsOptimizationProfiles_Web_New.restype = c_void_p

def optimizationprofiles_web_new():
    return _lib.PdfToolsOptimizationProfiles_Web_New()

_lib.PdfToolsOptimizationProfiles_Web_GetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_Web_GetResolutionDPI.restype = c_bool

def optimizationprofiles_web_getresolutiondpi(web, ret_val):
    return _lib.PdfToolsOptimizationProfiles_Web_GetResolutionDPI(web, byref(ret_val))
_lib.PdfToolsOptimizationProfiles_Web_SetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_Web_SetResolutionDPI.restype = c_bool

def optimizationprofiles_web_setresolutiondpi(web, val):
    return _lib.PdfToolsOptimizationProfiles_Web_SetResolutionDPI(web, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsOptimizationProfiles_Web_GetThresholdDPI.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Web_GetThresholdDPI.restype = c_double

def optimizationprofiles_web_getthresholddpi(web):
    return _lib.PdfToolsOptimizationProfiles_Web_GetThresholdDPI(web)
_lib.PdfToolsOptimizationProfiles_Web_SetThresholdDPI.argtypes = [c_void_p, c_double]
_lib.PdfToolsOptimizationProfiles_Web_SetThresholdDPI.restype = c_bool

def optimizationprofiles_web_setthresholddpi(web, val):
    return _lib.PdfToolsOptimizationProfiles_Web_SetThresholdDPI(web, val)


_lib.PdfToolsOptimizationProfiles_Print_New.argtypes = []
_lib.PdfToolsOptimizationProfiles_Print_New.restype = c_void_p

def optimizationprofiles_print_new():
    return _lib.PdfToolsOptimizationProfiles_Print_New()


_lib.PdfToolsOptimizationProfiles_Archive_New.argtypes = []
_lib.PdfToolsOptimizationProfiles_Archive_New.restype = c_void_p

def optimizationprofiles_archive_new():
    return _lib.PdfToolsOptimizationProfiles_Archive_New()


_lib.PdfToolsOptimizationProfiles_MinimalFileSize_New.argtypes = []
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_New.restype = c_void_p

def optimizationprofiles_minimalfilesize_new():
    return _lib.PdfToolsOptimizationProfiles_MinimalFileSize_New()

_lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI.restype = c_bool

def optimizationprofiles_minimalfilesize_getresolutiondpi(minimal_file_size, ret_val):
    return _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI(minimal_file_size, byref(ret_val))
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI.restype = c_bool

def optimizationprofiles_minimalfilesize_setresolutiondpi(minimal_file_size, val):
    return _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI(minimal_file_size, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI.restype = c_double

def optimizationprofiles_minimalfilesize_getthresholddpi(minimal_file_size):
    return _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI(minimal_file_size)
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI.argtypes = [c_void_p, c_double]
_lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI.restype = c_bool

def optimizationprofiles_minimalfilesize_setthresholddpi(minimal_file_size, val):
    return _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI(minimal_file_size, val)


_lib.PdfToolsOptimizationProfiles_Mrc_New.argtypes = []
_lib.PdfToolsOptimizationProfiles_Mrc_New.restype = c_void_p

def optimizationprofiles_mrc_new():
    return _lib.PdfToolsOptimizationProfiles_Mrc_New()

_lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality.restype = c_double

def optimizationprofiles_mrc_getlayercompressionquality(mrc):
    return _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality(mrc)
_lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality.argtypes = [c_void_p, c_double]
_lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality.restype = c_bool

def optimizationprofiles_mrc_setlayercompressionquality(mrc, val):
    return _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality(mrc, val)
_lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI.restype = c_bool

def optimizationprofiles_mrc_getlayerresolutiondpi(mrc, ret_val):
    return _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI(mrc, byref(ret_val))
_lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI.restype = c_bool

def optimizationprofiles_mrc_setlayerresolutiondpi(mrc, val):
    return _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI(mrc, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures.argtypes = [c_void_p]
_lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures.restype = c_bool

def optimizationprofiles_mrc_getrecognizepictures(mrc):
    return _lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures(mrc)
_lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures.argtypes = [c_void_p, c_bool]
_lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures.restype = c_bool

def optimizationprofiles_mrc_setrecognizepictures(mrc, val):
    return _lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures(mrc, val)


_lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations.restype = c_int

def pdf2image_contentoptions_getannotations(content_options):
    return _lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations(content_options)
_lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations.restype = c_bool

def pdf2image_contentoptions_setannotations(content_options, val):
    return _lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations(content_options, val)


_lib.PdfToolsPdf2Image_ImageOptions_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_ImageOptions_GetType.restype = c_int

def pdf2image_imageoptions_gettype(object):
    return _lib.PdfToolsPdf2Image_ImageOptions_GetType(object)

_lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution.restype = c_int

def pdf2image_faximageoptions_getverticalresolution(fax_image_options):
    return _lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution(fax_image_options)
_lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution.restype = c_bool

def pdf2image_faximageoptions_setverticalresolution(fax_image_options, val):
    return _lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution(fax_image_options, val)
_lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression.restype = c_int

def pdf2image_faximageoptions_getcompression(fax_image_options):
    return _lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression(fax_image_options)
_lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression.restype = c_bool

def pdf2image_faximageoptions_setcompression(fax_image_options, val):
    return _lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression(fax_image_options, val)


_lib.PdfToolsPdf2Image_TiffJpegImageOptions_New.argtypes = []
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_New.restype = c_void_p

def pdf2image_tiffjpegimageoptions_new():
    return _lib.PdfToolsPdf2Image_TiffJpegImageOptions_New()

_lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetJpegQuality.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetJpegQuality.restype = c_int

def pdf2image_tiffjpegimageoptions_getjpegquality(tiff_jpeg_image_options):
    return _lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetJpegQuality(tiff_jpeg_image_options)
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetJpegQuality.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetJpegQuality.restype = c_bool

def pdf2image_tiffjpegimageoptions_setjpegquality(tiff_jpeg_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetJpegQuality(tiff_jpeg_image_options, val)
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetColorSpace.restype = c_bool

def pdf2image_tiffjpegimageoptions_getcolorspace(tiff_jpeg_image_options, ret_val):
    return _lib.PdfToolsPdf2Image_TiffJpegImageOptions_GetColorSpace(tiff_jpeg_image_options, byref(ret_val))
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetColorSpace.restype = c_bool

def pdf2image_tiffjpegimageoptions_setcolorspace(tiff_jpeg_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffJpegImageOptions_SetColorSpace(tiff_jpeg_image_options, byref(c_int(val)) if val is not None else None)


_lib.PdfToolsPdf2Image_TiffLzwImageOptions_New.argtypes = []
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_New.restype = c_void_p

def pdf2image_tifflzwimageoptions_new():
    return _lib.PdfToolsPdf2Image_TiffLzwImageOptions_New()

_lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground.restype = c_int

def pdf2image_tifflzwimageoptions_getbackground(tiff_lzw_image_options):
    return _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground(tiff_lzw_image_options)
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground.restype = c_bool

def pdf2image_tifflzwimageoptions_setbackground(tiff_lzw_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground(tiff_lzw_image_options, val)
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace.restype = c_bool

def pdf2image_tifflzwimageoptions_getcolorspace(tiff_lzw_image_options, ret_val):
    return _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace(tiff_lzw_image_options, byref(ret_val))
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace.restype = c_bool

def pdf2image_tifflzwimageoptions_setcolorspace(tiff_lzw_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace(tiff_lzw_image_options, byref(c_int(val)) if val is not None else None)


_lib.PdfToolsPdf2Image_TiffFlateImageOptions_New.argtypes = []
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_New.restype = c_void_p

def pdf2image_tiffflateimageoptions_new():
    return _lib.PdfToolsPdf2Image_TiffFlateImageOptions_New()

_lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetBackground.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetBackground.restype = c_int

def pdf2image_tiffflateimageoptions_getbackground(tiff_flate_image_options):
    return _lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetBackground(tiff_flate_image_options)
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetBackground.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetBackground.restype = c_bool

def pdf2image_tiffflateimageoptions_setbackground(tiff_flate_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetBackground(tiff_flate_image_options, val)
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetColorSpace.restype = c_bool

def pdf2image_tiffflateimageoptions_getcolorspace(tiff_flate_image_options, ret_val):
    return _lib.PdfToolsPdf2Image_TiffFlateImageOptions_GetColorSpace(tiff_flate_image_options, byref(ret_val))
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetColorSpace.restype = c_bool

def pdf2image_tiffflateimageoptions_setcolorspace(tiff_flate_image_options, val):
    return _lib.PdfToolsPdf2Image_TiffFlateImageOptions_SetColorSpace(tiff_flate_image_options, byref(c_int(val)) if val is not None else None)


_lib.PdfToolsPdf2Image_PngImageOptions_New.argtypes = []
_lib.PdfToolsPdf2Image_PngImageOptions_New.restype = c_void_p

def pdf2image_pngimageoptions_new():
    return _lib.PdfToolsPdf2Image_PngImageOptions_New()

_lib.PdfToolsPdf2Image_PngImageOptions_GetBackground.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_PngImageOptions_GetBackground.restype = c_int

def pdf2image_pngimageoptions_getbackground(png_image_options):
    return _lib.PdfToolsPdf2Image_PngImageOptions_GetBackground(png_image_options)
_lib.PdfToolsPdf2Image_PngImageOptions_SetBackground.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_PngImageOptions_SetBackground.restype = c_bool

def pdf2image_pngimageoptions_setbackground(png_image_options, val):
    return _lib.PdfToolsPdf2Image_PngImageOptions_SetBackground(png_image_options, val)
_lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace.restype = c_int

def pdf2image_pngimageoptions_getcolorspace(png_image_options):
    return _lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace(png_image_options)
_lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace.restype = c_bool

def pdf2image_pngimageoptions_setcolorspace(png_image_options, val):
    return _lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace(png_image_options, val)


_lib.PdfToolsPdf2Image_JpegImageOptions_New.argtypes = []
_lib.PdfToolsPdf2Image_JpegImageOptions_New.restype = c_void_p

def pdf2image_jpegimageoptions_new():
    return _lib.PdfToolsPdf2Image_JpegImageOptions_New()

_lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace.restype = c_bool

def pdf2image_jpegimageoptions_getcolorspace(jpeg_image_options, ret_val):
    return _lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace(jpeg_image_options, byref(ret_val))
_lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace.restype = c_bool

def pdf2image_jpegimageoptions_setcolorspace(jpeg_image_options, val):
    return _lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace(jpeg_image_options, byref(c_int(val)) if val is not None else None)
_lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality.restype = c_int

def pdf2image_jpegimageoptions_getjpegquality(jpeg_image_options):
    return _lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality(jpeg_image_options)
_lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality.restype = c_bool

def pdf2image_jpegimageoptions_setjpegquality(jpeg_image_options, val):
    return _lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality(jpeg_image_options, val)


_lib.PdfToolsPdf2Image_ImageSectionMapping_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf2Image_ImageSectionMapping_GetType.restype = c_int

def pdf2image_imagesectionmapping_gettype(object):
    return _lib.PdfToolsPdf2Image_ImageSectionMapping_GetType(object)

_lib.PdfToolsPdf2Image_RenderPageAtResolution_New.argtypes = [POINTER(GeomUnitsResolution)]
_lib.PdfToolsPdf2Image_RenderPageAtResolution_New.restype = c_void_p

def pdf2image_renderpageatresolution_new(resolution):
    return _lib.PdfToolsPdf2Image_RenderPageAtResolution_New(resolution)

_lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution.argtypes = [c_void_p, POINTER(GeomUnitsResolution)]
_lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution.restype = c_bool

def pdf2image_renderpageatresolution_getresolution(render_page_at_resolution, ret_val):
    return _lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution(render_page_at_resolution, byref(ret_val))
_lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution.argtypes = [c_void_p, POINTER(GeomUnitsResolution)]
_lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution.restype = c_bool

def pdf2image_renderpageatresolution_setresolution(render_page_at_resolution, val):
    return _lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution(render_page_at_resolution, val)


_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New.argtypes = [POINTER(GeomIntSize)]
_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New.restype = c_void_p

def pdf2image_renderpagetomaximagesize_new(size):
    return _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New(size)

_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize.argtypes = [c_void_p, POINTER(GeomIntSize)]
_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize.restype = c_bool

def pdf2image_renderpagetomaximagesize_getsize(render_page_to_max_image_size, ret_val):
    return _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize(render_page_to_max_image_size, byref(ret_val))
_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize.argtypes = [c_void_p, POINTER(GeomIntSize)]
_lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize.restype = c_bool

def pdf2image_renderpagetomaximagesize_setsize(render_page_to_max_image_size, val):
    return _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize(render_page_to_max_image_size, val)


_lib.PdfToolsPdf2Image_Converter_ConvertDocument.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p]
_lib.PdfToolsPdf2Image_Converter_ConvertDocument.restype = c_void_p

def pdf2image_converter_convertdocument(converter, in_doc, out_stream, profile):
    return _lib.PdfToolsPdf2Image_Converter_ConvertDocument(converter, in_doc, out_stream, profile)
_lib.PdfToolsPdf2Image_Converter_ConvertPage.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_int]
_lib.PdfToolsPdf2Image_Converter_ConvertPage.restype = c_void_p

def pdf2image_converter_convertpage(converter, in_doc, out_stream, profile, page_number):
    return _lib.PdfToolsPdf2Image_Converter_ConvertPage(converter, in_doc, out_stream, profile, page_number)

_lib.PdfToolsPdf2Image_Converter_New.argtypes = []
_lib.PdfToolsPdf2Image_Converter_New.restype = c_void_p

def pdf2image_converter_new():
    return _lib.PdfToolsPdf2Image_Converter_New()


_lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions.restype = c_void_p

def pdf2imageprofiles_profile_getcontentoptions(profile):
    return _lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions(profile)

_lib.PdfToolsPdf2ImageProfiles_Profile_GetType.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Profile_GetType.restype = c_int

def pdf2imageprofiles_profile_gettype(object):
    return _lib.PdfToolsPdf2ImageProfiles_Profile_GetType(object)

_lib.PdfToolsPdf2ImageProfiles_Fax_New.argtypes = []
_lib.PdfToolsPdf2ImageProfiles_Fax_New.restype = c_void_p

def pdf2imageprofiles_fax_new():
    return _lib.PdfToolsPdf2ImageProfiles_Fax_New()

_lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions.restype = c_void_p

def pdf2imageprofiles_fax_getimageoptions(fax):
    return _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions(fax)
_lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping.restype = c_void_p

def pdf2imageprofiles_fax_getimagesectionmapping(fax):
    return _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping(fax)


_lib.PdfToolsPdf2ImageProfiles_Archive_New.argtypes = []
_lib.PdfToolsPdf2ImageProfiles_Archive_New.restype = c_void_p

def pdf2imageprofiles_archive_new():
    return _lib.PdfToolsPdf2ImageProfiles_Archive_New()

_lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions.restype = c_void_p

def pdf2imageprofiles_archive_getimageoptions(archive):
    return _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions(archive)
_lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions.restype = c_bool

def pdf2imageprofiles_archive_setimageoptions(archive, val):
    return _lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions(archive, val)
_lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping.restype = c_void_p

def pdf2imageprofiles_archive_getimagesectionmapping(archive):
    return _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping(archive)


_lib.PdfToolsPdf2ImageProfiles_Viewing_New.argtypes = []
_lib.PdfToolsPdf2ImageProfiles_Viewing_New.restype = c_void_p

def pdf2imageprofiles_viewing_new():
    return _lib.PdfToolsPdf2ImageProfiles_Viewing_New()

_lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions.restype = c_void_p

def pdf2imageprofiles_viewing_getimageoptions(viewing):
    return _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions(viewing)
_lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions.restype = c_bool

def pdf2imageprofiles_viewing_setimageoptions(viewing, val):
    return _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions(viewing, val)
_lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping.argtypes = [c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping.restype = c_void_p

def pdf2imageprofiles_viewing_getimagesectionmapping(viewing):
    return _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping(viewing)
_lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping.restype = c_bool

def pdf2imageprofiles_viewing_setimagesectionmapping(viewing, val):
    return _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping(viewing, val)


_lib.PdfToolsImage2Pdf_ImageMapping_GetType.argtypes = [c_void_p]
_lib.PdfToolsImage2Pdf_ImageMapping_GetType.restype = c_int

def image2pdf_imagemapping_gettype(object):
    return _lib.PdfToolsImage2Pdf_ImageMapping_GetType(object)

_lib.PdfToolsImage2Pdf_Auto_New.argtypes = []
_lib.PdfToolsImage2Pdf_Auto_New.restype = c_void_p

def image2pdf_auto_new():
    return _lib.PdfToolsImage2Pdf_Auto_New()

_lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize.restype = c_bool

def image2pdf_auto_getmaxpagesize(auto, ret_val):
    return _lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize(auto, byref(ret_val))
_lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize.restype = c_bool

def image2pdf_auto_setmaxpagesize(auto, val):
    return _lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize(auto, val)
_lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin.restype = c_bool

def image2pdf_auto_getdefaultpagemargin(auto, ret_val):
    return _lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin(auto, byref(ret_val))
_lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin.restype = c_bool

def image2pdf_auto_setdefaultpagemargin(auto, val):
    return _lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin(auto, val)


_lib.PdfToolsImage2Pdf_ShrinkToPage_New.argtypes = []
_lib.PdfToolsImage2Pdf_ShrinkToPage_New.restype = c_void_p

def image2pdf_shrinktopage_new():
    return _lib.PdfToolsImage2Pdf_ShrinkToPage_New()

_lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageSize.restype = c_bool

def image2pdf_shrinktopage_getpagesize(shrink_to_page, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageSize(shrink_to_page, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageSize.restype = c_bool

def image2pdf_shrinktopage_setpagesize(shrink_to_page, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageSize(shrink_to_page, val)
_lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageMargin.restype = c_bool

def image2pdf_shrinktopage_getpagemargin(shrink_to_page, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPage_GetPageMargin(shrink_to_page, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageMargin.restype = c_bool

def image2pdf_shrinktopage_setpagemargin(shrink_to_page, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPage_SetPageMargin(shrink_to_page, val)


_lib.PdfToolsImage2Pdf_ShrinkToFit_New.argtypes = []
_lib.PdfToolsImage2Pdf_ShrinkToFit_New.restype = c_void_p

def image2pdf_shrinktofit_new():
    return _lib.PdfToolsImage2Pdf_ShrinkToFit_New()

_lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageSize.restype = c_bool

def image2pdf_shrinktofit_getpagesize(shrink_to_fit, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageSize(shrink_to_fit, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageSize.restype = c_bool

def image2pdf_shrinktofit_setpagesize(shrink_to_fit, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageSize(shrink_to_fit, val)
_lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageMargin.restype = c_bool

def image2pdf_shrinktofit_getpagemargin(shrink_to_fit, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToFit_GetPageMargin(shrink_to_fit, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageMargin.restype = c_bool

def image2pdf_shrinktofit_setpagemargin(shrink_to_fit, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToFit_SetPageMargin(shrink_to_fit, val)


_lib.PdfToolsImage2Pdf_ShrinkToPortrait_New.argtypes = []
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_New.restype = c_void_p

def image2pdf_shrinktoportrait_new():
    return _lib.PdfToolsImage2Pdf_ShrinkToPortrait_New()

_lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageSize.restype = c_bool

def image2pdf_shrinktoportrait_getpagesize(shrink_to_portrait, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageSize(shrink_to_portrait, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageSize.argtypes = [c_void_p, POINTER(GeomUnitsSize)]
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageSize.restype = c_bool

def image2pdf_shrinktoportrait_setpagesize(shrink_to_portrait, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageSize(shrink_to_portrait, val)
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageMargin.restype = c_bool

def image2pdf_shrinktoportrait_getpagemargin(shrink_to_portrait, ret_val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPortrait_GetPageMargin(shrink_to_portrait, byref(ret_val))
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageMargin.argtypes = [c_void_p, POINTER(GeomUnitsMargin)]
_lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageMargin.restype = c_bool

def image2pdf_shrinktoportrait_setpagemargin(shrink_to_portrait, val):
    return _lib.PdfToolsImage2Pdf_ShrinkToPortrait_SetPageMargin(shrink_to_portrait, val)


_lib.PdfToolsImage2Pdf_ImageOptions_GetMapping.argtypes = [c_void_p]
_lib.PdfToolsImage2Pdf_ImageOptions_GetMapping.restype = c_void_p

def image2pdf_imageoptions_getmapping(image_options):
    return _lib.PdfToolsImage2Pdf_ImageOptions_GetMapping(image_options)
_lib.PdfToolsImage2Pdf_ImageOptions_SetMapping.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsImage2Pdf_ImageOptions_SetMapping.restype = c_bool

def image2pdf_imageoptions_setmapping(image_options, val):
    return _lib.PdfToolsImage2Pdf_ImageOptions_SetMapping(image_options, val)


_lib.PdfToolsImage2Pdf_Converter_Convert.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsImage2Pdf_Converter_Convert.restype = c_void_p

def image2pdf_converter_convert(converter, image, out_stream, profile, out_options):
    return _lib.PdfToolsImage2Pdf_Converter_Convert(converter, image, out_stream, profile, out_options)
_lib.PdfToolsImage2Pdf_Converter_ConvertMultiple.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsImage2Pdf_Converter_ConvertMultiple.restype = c_void_p

def image2pdf_converter_convertmultiple(converter, images, out_stream, profile, out_options):
    return _lib.PdfToolsImage2Pdf_Converter_ConvertMultiple(converter, images, out_stream, profile, out_options)

_lib.PdfToolsImage2Pdf_Converter_New.argtypes = []
_lib.PdfToolsImage2Pdf_Converter_New.restype = c_void_p

def image2pdf_converter_new():
    return _lib.PdfToolsImage2Pdf_Converter_New()


_lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions.argtypes = [c_void_p]
_lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions.restype = c_void_p

def image2pdfprofiles_profile_getimageoptions(profile):
    return _lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions(profile)

_lib.PdfToolsImage2PdfProfiles_Profile_GetType.argtypes = [c_void_p]
_lib.PdfToolsImage2PdfProfiles_Profile_GetType.restype = c_int

def image2pdfprofiles_profile_gettype(object):
    return _lib.PdfToolsImage2PdfProfiles_Profile_GetType(object)

_lib.PdfToolsImage2PdfProfiles_Default_New.argtypes = []
_lib.PdfToolsImage2PdfProfiles_Default_New.restype = c_void_p

def image2pdfprofiles_default_new():
    return _lib.PdfToolsImage2PdfProfiles_Default_New()

_lib.PdfToolsImage2PdfProfiles_Default_GetConformance.argtypes = [c_void_p]
_lib.PdfToolsImage2PdfProfiles_Default_GetConformance.restype = c_int

def image2pdfprofiles_default_getconformance(default):
    return _lib.PdfToolsImage2PdfProfiles_Default_GetConformance(default)
_lib.PdfToolsImage2PdfProfiles_Default_SetConformance.argtypes = [c_void_p, c_int]
_lib.PdfToolsImage2PdfProfiles_Default_SetConformance.restype = c_bool

def image2pdfprofiles_default_setconformance(default, val):
    return _lib.PdfToolsImage2PdfProfiles_Default_SetConformance(default, val)


_lib.PdfToolsImage2PdfProfiles_Archive_New.argtypes = []
_lib.PdfToolsImage2PdfProfiles_Archive_New.restype = c_void_p

def image2pdfprofiles_archive_new():
    return _lib.PdfToolsImage2PdfProfiles_Archive_New()

_lib.PdfToolsImage2PdfProfiles_Archive_GetConformance.argtypes = [c_void_p]
_lib.PdfToolsImage2PdfProfiles_Archive_GetConformance.restype = c_int

def image2pdfprofiles_archive_getconformance(archive):
    return _lib.PdfToolsImage2PdfProfiles_Archive_GetConformance(archive)
_lib.PdfToolsImage2PdfProfiles_Archive_SetConformance.argtypes = [c_void_p, c_int]
_lib.PdfToolsImage2PdfProfiles_Archive_SetConformance.restype = c_bool

def image2pdfprofiles_archive_setconformance(archive, val):
    return _lib.PdfToolsImage2PdfProfiles_Archive_SetConformance(archive, val)
_lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText.argtypes = [c_void_p]
_lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText.restype = c_void_p

def image2pdfprofiles_archive_getalternatetext(archive):
    return _lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText(archive)
_lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText.restype = c_bool

def image2pdfprofiles_archive_setalternatetext(archive, val):
    return _lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText(archive, val)
_lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW.restype = c_size_t

def image2pdfprofiles_archive_getlanguage(archive):
    ret_buffer_size = _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW(archive, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW(archive, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW.restype = c_bool

def image2pdfprofiles_archive_setlanguage(archive, val):
    return _lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW(archive, string_to_utf16(val))


_lib.PdfToolsPdfAValidation_Validator_Validate.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfToolsPdfAValidation_Validator_Validate.restype = c_void_p

def pdfavalidation_validator_validate(validator, document, options):
    return _lib.PdfToolsPdfAValidation_Validator_Validate(validator, document, options)
_lib.PdfToolsPdfAValidation_Validator_Analyze.argtypes = [c_void_p, c_void_p, c_void_p]
_lib.PdfToolsPdfAValidation_Validator_Analyze.restype = c_void_p

def pdfavalidation_validator_analyze(validator, document, options):
    return _lib.PdfToolsPdfAValidation_Validator_Analyze(validator, document, options)

_lib.PdfToolsPdfAValidation_Validator_New.argtypes = []
_lib.PdfToolsPdfAValidation_Validator_New.restype = c_void_p

def pdfavalidation_validator_new():
    return _lib.PdfToolsPdfAValidation_Validator_New()

_lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW.argtypes = [c_void_p, c_void_p, PdfAValidation_Validator_ErrorFunc]
_lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW.restype = c_bool

def pdfavalidation_validator_adderrorhandler(obj, context, function):
    return _lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW(obj, context, function)

_lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW.argtypes = [c_void_p, c_void_p, PdfAValidation_Validator_ErrorFunc]
_lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW.restype = c_bool

def pdfavalidation_validator_removeerrorhandler(obj, context, function):
    return _lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW(obj, context, function)



_lib.PdfToolsPdfAValidation_ValidationOptions_New.argtypes = []
_lib.PdfToolsPdfAValidation_ValidationOptions_New.restype = c_void_p

def pdfavalidation_validationoptions_new():
    return _lib.PdfToolsPdfAValidation_ValidationOptions_New()

_lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance.restype = c_bool

def pdfavalidation_validationoptions_getconformance(validation_options, ret_val):
    return _lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance(validation_options, byref(ret_val))
_lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance.restype = c_bool

def pdfavalidation_validationoptions_setconformance(validation_options, val):
    return _lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance(validation_options, byref(c_int(val)) if val is not None else None)


_lib.PdfToolsPdfAValidation_ValidationResult_GetConformance.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_ValidationResult_GetConformance.restype = c_int

def pdfavalidation_validationresult_getconformance(validation_result):
    return _lib.PdfToolsPdfAValidation_ValidationResult_GetConformance(validation_result)
_lib.PdfToolsPdfAValidation_ValidationResult_IsConforming.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_ValidationResult_IsConforming.restype = c_bool

def pdfavalidation_validationresult_isconforming(validation_result):
    return _lib.PdfToolsPdfAValidation_ValidationResult_IsConforming(validation_result)


_lib.PdfToolsPdfAValidation_AnalysisOptions_New.argtypes = []
_lib.PdfToolsPdfAValidation_AnalysisOptions_New.restype = c_void_p

def pdfavalidation_analysisoptions_new():
    return _lib.PdfToolsPdfAValidation_AnalysisOptions_New()

_lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance.restype = c_int

def pdfavalidation_analysisoptions_getconformance(analysis_options):
    return _lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance(analysis_options)
_lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance.argtypes = [c_void_p, c_int]
_lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance.restype = c_bool

def pdfavalidation_analysisoptions_setconformance(analysis_options, val):
    return _lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance(analysis_options, val)
_lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode.restype = c_bool

def pdfavalidation_analysisoptions_getstrictmode(analysis_options):
    return _lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode(analysis_options)
_lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode.argtypes = [c_void_p, c_bool]
_lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode.restype = c_bool

def pdfavalidation_analysisoptions_setstrictmode(analysis_options, val):
    return _lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode(analysis_options, val)


_lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance.restype = c_int

def pdfavalidation_analysisresult_getconformance(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance.restype = c_int

def pdfavalidation_analysisresult_getrecommendedconformance(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended.restype = c_bool

def pdfavalidation_analysisresult_isconversionrecommended(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming.restype = c_bool

def pdfavalidation_analysisresult_isconforming(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned.restype = c_bool

def pdfavalidation_analysisresult_issigned(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles.restype = c_bool

def pdfavalidation_analysisresult_gethasembeddedfiles(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles(analysis_result)
_lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount.argtypes = [c_void_p]
_lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount.restype = c_int

def pdfavalidation_analysisresult_getfontcount(analysis_result):
    return _lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount(analysis_result)


_lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml.argtypes = [c_void_p, c_int, POINTER(StreamDescriptor), POINTER(c_int)]
_lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml.restype = c_bool

def pdfaconversion_converter_addinvoicexml(converter, invoice_type, invoice, af_relationship):
    return _lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml(converter, invoice_type, invoice, byref(c_int(af_relationship)) if af_relationship is not None else None)

_lib.PdfToolsPdfAConversion_Converter_Convert.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsPdfAConversion_Converter_Convert.restype = c_void_p

def pdfaconversion_converter_convert(converter, analysis, document, out_stream, options, out_options):
    return _lib.PdfToolsPdfAConversion_Converter_Convert(converter, analysis, document, out_stream, options, out_options)

_lib.PdfToolsPdfAConversion_Converter_New.argtypes = []
_lib.PdfToolsPdfAConversion_Converter_New.restype = c_void_p

def pdfaconversion_converter_new():
    return _lib.PdfToolsPdfAConversion_Converter_New()

_lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW.argtypes = [c_void_p, c_void_p, PdfAConversion_Converter_ConversionEventFunc]
_lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW.restype = c_bool

def pdfaconversion_converter_addconversioneventhandler(obj, context, function):
    return _lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW(obj, context, function)

_lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW.argtypes = [c_void_p, c_void_p, PdfAConversion_Converter_ConversionEventFunc]
_lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW.restype = c_bool

def pdfaconversion_converter_removeconversioneventhandler(obj, context, function):
    return _lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW(obj, context, function)



_lib.PdfToolsPdfAConversion_ConversionOptions_New.argtypes = []
_lib.PdfToolsPdfAConversion_ConversionOptions_New.restype = c_void_p

def pdfaconversion_conversionoptions_new():
    return _lib.PdfToolsPdfAConversion_ConversionOptions_New()

_lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance.restype = c_bool

def pdfaconversion_conversionoptions_getconformance(conversion_options, ret_val):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance(conversion_options, byref(ret_val))
_lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance.restype = c_bool

def pdfaconversion_conversionoptions_setconformance(conversion_options, val):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance(conversion_options, byref(c_int(val)) if val is not None else None)
_lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata.argtypes = [c_void_p]
_lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata.restype = c_bool

def pdfaconversion_conversionoptions_getcopymetadata(conversion_options):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata(conversion_options)
_lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata.argtypes = [c_void_p, c_bool]
_lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata.restype = c_bool

def pdfaconversion_conversionoptions_setcopymetadata(conversion_options, val):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata(conversion_options, val)
_lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality.argtypes = [c_void_p]
_lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality.restype = c_double

def pdfaconversion_conversionoptions_getimagequality(conversion_options):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality(conversion_options)
_lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality.argtypes = [c_void_p, c_double]
_lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality.restype = c_bool

def pdfaconversion_conversionoptions_setimagequality(conversion_options, val):
    return _lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality(conversion_options, val)


_lib.PdfToolsSign_CustomTextVariableMap_GetCount.argtypes = [c_void_p]
_lib.PdfToolsSign_CustomTextVariableMap_GetCount.restype = c_int

def sign_customtextvariablemap_getcount(custom_text_variable_map):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetCount(custom_text_variable_map)
_lib.PdfToolsSign_CustomTextVariableMap_GetSize.argtypes = [c_void_p]
_lib.PdfToolsSign_CustomTextVariableMap_GetSize.restype = c_int

def sign_customtextvariablemap_getsize(custom_text_variable_map):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetSize(custom_text_variable_map)
_lib.PdfToolsSign_CustomTextVariableMap_GetBegin.argtypes = [c_void_p]
_lib.PdfToolsSign_CustomTextVariableMap_GetBegin.restype = c_int

def sign_customtextvariablemap_getbegin(custom_text_variable_map):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetBegin(custom_text_variable_map)
_lib.PdfToolsSign_CustomTextVariableMap_GetEnd.argtypes = [c_void_p]
_lib.PdfToolsSign_CustomTextVariableMap_GetEnd.restype = c_int

def sign_customtextvariablemap_getend(custom_text_variable_map):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetEnd(custom_text_variable_map)
_lib.PdfToolsSign_CustomTextVariableMap_GetNext.argtypes = [c_void_p, c_int]
_lib.PdfToolsSign_CustomTextVariableMap_GetNext.restype = c_int

def sign_customtextvariablemap_getnext(custom_text_variable_map, it):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetNext(custom_text_variable_map, it)
_lib.PdfToolsSign_CustomTextVariableMap_GetW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_CustomTextVariableMap_GetW.restype = c_int

def sign_customtextvariablemap_get(custom_text_variable_map, key):
    return _lib.PdfToolsSign_CustomTextVariableMap_GetW(custom_text_variable_map, string_to_utf16(key))
_lib.PdfToolsSign_CustomTextVariableMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_CustomTextVariableMap_GetKeyW.restype = c_size_t

def sign_customtextvariablemap_getkey(custom_text_variable_map, it):
    ret_buffer_size = _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW(custom_text_variable_map, it, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW(custom_text_variable_map, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_CustomTextVariableMap_GetValueW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_CustomTextVariableMap_GetValueW.restype = c_size_t

def sign_customtextvariablemap_getvalue(custom_text_variable_map, it):
    ret_buffer_size = _lib.PdfToolsSign_CustomTextVariableMap_GetValueW(custom_text_variable_map, it, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_CustomTextVariableMap_GetValueW(custom_text_variable_map, it, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_CustomTextVariableMap_SetW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
_lib.PdfToolsSign_CustomTextVariableMap_SetW.restype = c_bool

def sign_customtextvariablemap_set(custom_text_variable_map, key, value):
    return _lib.PdfToolsSign_CustomTextVariableMap_SetW(custom_text_variable_map, string_to_utf16(key), string_to_utf16(value))

_lib.PdfToolsSign_CustomTextVariableMap_SetValueW.argtypes = [c_void_p, c_int, c_wchar_p]
_lib.PdfToolsSign_CustomTextVariableMap_SetValueW.restype = c_bool

def sign_customtextvariablemap_setvalue(custom_text_variable_map, it, value):
    return _lib.PdfToolsSign_CustomTextVariableMap_SetValueW(custom_text_variable_map, it, string_to_utf16(value))

_lib.PdfToolsSign_CustomTextVariableMap_Clear.argtypes = [c_void_p]
_lib.PdfToolsSign_CustomTextVariableMap_Clear.restype = c_bool

def sign_customtextvariablemap_clear(custom_text_variable_map):
    return _lib.PdfToolsSign_CustomTextVariableMap_Clear(custom_text_variable_map)

_lib.PdfToolsSign_CustomTextVariableMap_Remove.argtypes = [c_void_p, c_int]
_lib.PdfToolsSign_CustomTextVariableMap_Remove.restype = c_bool

def sign_customtextvariablemap_remove(custom_text_variable_map, it):
    return _lib.PdfToolsSign_CustomTextVariableMap_Remove(custom_text_variable_map, it)



_lib.PdfToolsSign_Appearance_CreateFromJson.argtypes = [POINTER(StreamDescriptor)]
_lib.PdfToolsSign_Appearance_CreateFromJson.restype = c_void_p

def sign_appearance_createfromjson(stream):
    return _lib.PdfToolsSign_Appearance_CreateFromJson(stream)
_lib.PdfToolsSign_Appearance_CreateFromXml.argtypes = [POINTER(StreamDescriptor)]
_lib.PdfToolsSign_Appearance_CreateFromXml.restype = c_void_p

def sign_appearance_createfromxml(stream):
    return _lib.PdfToolsSign_Appearance_CreateFromXml(stream)
_lib.PdfToolsSign_Appearance_CreateFieldBoundingBox.argtypes = [POINTER(GeomUnitsSize)]
_lib.PdfToolsSign_Appearance_CreateFieldBoundingBox.restype = c_void_p

def sign_appearance_createfieldboundingbox(size):
    return _lib.PdfToolsSign_Appearance_CreateFieldBoundingBox(size)

_lib.PdfToolsSign_Appearance_GetPageNumber.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsSign_Appearance_GetPageNumber.restype = c_bool

def sign_appearance_getpagenumber(appearance, ret_val):
    return _lib.PdfToolsSign_Appearance_GetPageNumber(appearance, byref(ret_val))
_lib.PdfToolsSign_Appearance_SetPageNumber.argtypes = [c_void_p, POINTER(c_int)]
_lib.PdfToolsSign_Appearance_SetPageNumber.restype = c_bool

def sign_appearance_setpagenumber(appearance, val):
    return _lib.PdfToolsSign_Appearance_SetPageNumber(appearance, byref(c_int(val)) if val is not None else None)
_lib.PdfToolsSign_Appearance_GetTop.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_GetTop.restype = c_bool

def sign_appearance_gettop(appearance, ret_val):
    return _lib.PdfToolsSign_Appearance_GetTop(appearance, byref(ret_val))
_lib.PdfToolsSign_Appearance_SetTop.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_SetTop.restype = c_bool

def sign_appearance_settop(appearance, val):
    return _lib.PdfToolsSign_Appearance_SetTop(appearance, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsSign_Appearance_GetRight.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_GetRight.restype = c_bool

def sign_appearance_getright(appearance, ret_val):
    return _lib.PdfToolsSign_Appearance_GetRight(appearance, byref(ret_val))
_lib.PdfToolsSign_Appearance_SetRight.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_SetRight.restype = c_bool

def sign_appearance_setright(appearance, val):
    return _lib.PdfToolsSign_Appearance_SetRight(appearance, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsSign_Appearance_GetBottom.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_GetBottom.restype = c_bool

def sign_appearance_getbottom(appearance, ret_val):
    return _lib.PdfToolsSign_Appearance_GetBottom(appearance, byref(ret_val))
_lib.PdfToolsSign_Appearance_SetBottom.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_SetBottom.restype = c_bool

def sign_appearance_setbottom(appearance, val):
    return _lib.PdfToolsSign_Appearance_SetBottom(appearance, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsSign_Appearance_GetLeft.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_GetLeft.restype = c_bool

def sign_appearance_getleft(appearance, ret_val):
    return _lib.PdfToolsSign_Appearance_GetLeft(appearance, byref(ret_val))
_lib.PdfToolsSign_Appearance_SetLeft.argtypes = [c_void_p, POINTER(c_double)]
_lib.PdfToolsSign_Appearance_SetLeft.restype = c_bool

def sign_appearance_setleft(appearance, val):
    return _lib.PdfToolsSign_Appearance_SetLeft(appearance, byref(c_double(val)) if val is not None else None)
_lib.PdfToolsSign_Appearance_GetCustomTextVariables.argtypes = [c_void_p]
_lib.PdfToolsSign_Appearance_GetCustomTextVariables.restype = c_void_p

def sign_appearance_getcustomtextvariables(appearance):
    return _lib.PdfToolsSign_Appearance_GetCustomTextVariables(appearance)


_lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW.restype = c_size_t

def sign_signatureconfiguration_getfieldname(signature_configuration):
    ret_buffer_size = _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW(signature_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW(signature_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW.restype = c_bool

def sign_signatureconfiguration_setfieldname(signature_configuration, val):
    return _lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW(signature_configuration, string_to_utf16(val))
_lib.PdfToolsSign_SignatureConfiguration_GetAppearance.argtypes = [c_void_p]
_lib.PdfToolsSign_SignatureConfiguration_GetAppearance.restype = c_void_p

def sign_signatureconfiguration_getappearance(signature_configuration):
    return _lib.PdfToolsSign_SignatureConfiguration_GetAppearance(signature_configuration)
_lib.PdfToolsSign_SignatureConfiguration_SetAppearance.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsSign_SignatureConfiguration_SetAppearance.restype = c_bool

def sign_signatureconfiguration_setappearance(signature_configuration, val):
    return _lib.PdfToolsSign_SignatureConfiguration_SetAppearance(signature_configuration, val)
_lib.PdfToolsSign_SignatureConfiguration_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureConfiguration_GetNameW.restype = c_size_t

def sign_signatureconfiguration_getname(signature_configuration):
    ret_buffer_size = _lib.PdfToolsSign_SignatureConfiguration_GetNameW(signature_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureConfiguration_GetNameW(signature_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureConfiguration_GetLocationW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureConfiguration_GetLocationW.restype = c_size_t

def sign_signatureconfiguration_getlocation(signature_configuration):
    ret_buffer_size = _lib.PdfToolsSign_SignatureConfiguration_GetLocationW(signature_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureConfiguration_GetLocationW(signature_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureConfiguration_SetLocationW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_SignatureConfiguration_SetLocationW.restype = c_bool

def sign_signatureconfiguration_setlocation(signature_configuration, val):
    return _lib.PdfToolsSign_SignatureConfiguration_SetLocationW(signature_configuration, string_to_utf16(val))
_lib.PdfToolsSign_SignatureConfiguration_GetReasonW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureConfiguration_GetReasonW.restype = c_size_t

def sign_signatureconfiguration_getreason(signature_configuration):
    ret_buffer_size = _lib.PdfToolsSign_SignatureConfiguration_GetReasonW(signature_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureConfiguration_GetReasonW(signature_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureConfiguration_SetReasonW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_SignatureConfiguration_SetReasonW.restype = c_bool

def sign_signatureconfiguration_setreason(signature_configuration, val):
    return _lib.PdfToolsSign_SignatureConfiguration_SetReasonW(signature_configuration, string_to_utf16(val))
_lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW.restype = c_size_t

def sign_signatureconfiguration_getcontactinfo(signature_configuration):
    ret_buffer_size = _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW(signature_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW(signature_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW.restype = c_bool

def sign_signatureconfiguration_setcontactinfo(signature_configuration, val):
    return _lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW(signature_configuration, string_to_utf16(val))

_lib.PdfToolsSign_SignatureConfiguration_GetType.argtypes = [c_void_p]
_lib.PdfToolsSign_SignatureConfiguration_GetType.restype = c_int

def sign_signatureconfiguration_gettype(object):
    return _lib.PdfToolsSign_SignatureConfiguration_GetType(object)

_lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW.restype = c_size_t

def sign_timestampconfiguration_getfieldname(timestamp_configuration):
    ret_buffer_size = _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW(timestamp_configuration, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW(timestamp_configuration, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW.restype = c_bool

def sign_timestampconfiguration_setfieldname(timestamp_configuration, val):
    return _lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW(timestamp_configuration, string_to_utf16(val))
_lib.PdfToolsSign_TimestampConfiguration_GetAppearance.argtypes = [c_void_p]
_lib.PdfToolsSign_TimestampConfiguration_GetAppearance.restype = c_void_p

def sign_timestampconfiguration_getappearance(timestamp_configuration):
    return _lib.PdfToolsSign_TimestampConfiguration_GetAppearance(timestamp_configuration)
_lib.PdfToolsSign_TimestampConfiguration_SetAppearance.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsSign_TimestampConfiguration_SetAppearance.restype = c_bool

def sign_timestampconfiguration_setappearance(timestamp_configuration, val):
    return _lib.PdfToolsSign_TimestampConfiguration_SetAppearance(timestamp_configuration, val)

_lib.PdfToolsSign_TimestampConfiguration_GetType.argtypes = [c_void_p]
_lib.PdfToolsSign_TimestampConfiguration_GetType.restype = c_int

def sign_timestampconfiguration_gettype(object):
    return _lib.PdfToolsSign_TimestampConfiguration_GetType(object)

_lib.PdfToolsSign_OutputOptions_New.argtypes = []
_lib.PdfToolsSign_OutputOptions_New.restype = c_void_p

def sign_outputoptions_new():
    return _lib.PdfToolsSign_OutputOptions_New()

_lib.PdfToolsSign_OutputOptions_GetRemoveSignatures.argtypes = [c_void_p]
_lib.PdfToolsSign_OutputOptions_GetRemoveSignatures.restype = c_int

def sign_outputoptions_getremovesignatures(output_options):
    return _lib.PdfToolsSign_OutputOptions_GetRemoveSignatures(output_options)
_lib.PdfToolsSign_OutputOptions_SetRemoveSignatures.argtypes = [c_void_p, c_int]
_lib.PdfToolsSign_OutputOptions_SetRemoveSignatures.restype = c_bool

def sign_outputoptions_setremovesignatures(output_options, val):
    return _lib.PdfToolsSign_OutputOptions_SetRemoveSignatures(output_options, val)
_lib.PdfToolsSign_OutputOptions_GetAddValidationInformation.argtypes = [c_void_p]
_lib.PdfToolsSign_OutputOptions_GetAddValidationInformation.restype = c_int

def sign_outputoptions_getaddvalidationinformation(output_options):
    return _lib.PdfToolsSign_OutputOptions_GetAddValidationInformation(output_options)
_lib.PdfToolsSign_OutputOptions_SetAddValidationInformation.argtypes = [c_void_p, c_int]
_lib.PdfToolsSign_OutputOptions_SetAddValidationInformation.restype = c_bool

def sign_outputoptions_setaddvalidationinformation(output_options, val):
    return _lib.PdfToolsSign_OutputOptions_SetAddValidationInformation(output_options, val)


_lib.PdfToolsSign_MdpPermissionOptions_New.argtypes = [c_int]
_lib.PdfToolsSign_MdpPermissionOptions_New.restype = c_void_p

def sign_mdppermissionoptions_new(permissions):
    return _lib.PdfToolsSign_MdpPermissionOptions_New(permissions)

_lib.PdfToolsSign_MdpPermissionOptions_GetPermissions.argtypes = [c_void_p]
_lib.PdfToolsSign_MdpPermissionOptions_GetPermissions.restype = c_int

def sign_mdppermissionoptions_getpermissions(mdp_permission_options):
    return _lib.PdfToolsSign_MdpPermissionOptions_GetPermissions(mdp_permission_options)
_lib.PdfToolsSign_MdpPermissionOptions_SetPermissions.argtypes = [c_void_p, c_int]
_lib.PdfToolsSign_MdpPermissionOptions_SetPermissions.restype = c_bool

def sign_mdppermissionoptions_setpermissions(mdp_permission_options, val):
    return _lib.PdfToolsSign_MdpPermissionOptions_SetPermissions(mdp_permission_options, val)


_lib.PdfToolsSign_SignatureFieldOptions_New.argtypes = [c_void_p]
_lib.PdfToolsSign_SignatureFieldOptions_New.restype = c_void_p

def sign_signaturefieldoptions_new(bounding_box):
    return _lib.PdfToolsSign_SignatureFieldOptions_New(bounding_box)

_lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox.argtypes = [c_void_p]
_lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox.restype = c_void_p

def sign_signaturefieldoptions_getboundingbox(signature_field_options):
    return _lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox(signature_field_options)
_lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW.restype = c_size_t

def sign_signaturefieldoptions_getfieldname(signature_field_options):
    ret_buffer_size = _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW(signature_field_options, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW(signature_field_options, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW.restype = c_bool

def sign_signaturefieldoptions_setfieldname(signature_field_options, val):
    return _lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW(signature_field_options, string_to_utf16(val))


_lib.PdfToolsSign_PreparedDocument_GetHash.argtypes = [c_void_p, c_int, POINTER(c_ubyte), c_size_t]
_lib.PdfToolsSign_PreparedDocument_GetHash.restype = c_size_t

def sign_prepareddocument_gethash(prepared_document, algorithm, ret_val, ret_val_buffer):
    return _lib.PdfToolsSign_PreparedDocument_GetHash(prepared_document, algorithm, ret_val, ret_val_buffer)


_lib.PdfToolsSign_Signer_Sign.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p]
_lib.PdfToolsSign_Signer_Sign.restype = c_void_p

def sign_signer_sign(signer, document, configuration, stream, output_options):
    return _lib.PdfToolsSign_Signer_Sign(signer, document, configuration, stream, output_options)
_lib.PdfToolsSign_Signer_Certify.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsSign_Signer_Certify.restype = c_void_p

def sign_signer_certify(signer, document, configuration, stream, permissions, output_options):
    return _lib.PdfToolsSign_Signer_Certify(signer, document, configuration, stream, permissions, output_options)
_lib.PdfToolsSign_Signer_AddTimestamp.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p]
_lib.PdfToolsSign_Signer_AddTimestamp.restype = c_void_p

def sign_signer_addtimestamp(signer, document, configuration, stream, output_options):
    return _lib.PdfToolsSign_Signer_AddTimestamp(signer, document, configuration, stream, output_options)
_lib.PdfToolsSign_Signer_AddSignatureField.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p]
_lib.PdfToolsSign_Signer_AddSignatureField.restype = c_void_p

def sign_signer_addsignaturefield(signer, document, options, stream, output_options):
    return _lib.PdfToolsSign_Signer_AddSignatureField(signer, document, options, stream, output_options)
_lib.PdfToolsSign_Signer_AddPreparedSignature.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p]
_lib.PdfToolsSign_Signer_AddPreparedSignature.restype = c_void_p

def sign_signer_addpreparedsignature(signer, document, configuration, stream, output_options):
    return _lib.PdfToolsSign_Signer_AddPreparedSignature(signer, document, configuration, stream, output_options)
_lib.PdfToolsSign_Signer_SignPreparedSignature.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(StreamDescriptor)]
_lib.PdfToolsSign_Signer_SignPreparedSignature.restype = c_void_p

def sign_signer_signpreparedsignature(signer, document, configuration, stream):
    return _lib.PdfToolsSign_Signer_SignPreparedSignature(signer, document, configuration, stream)
_lib.PdfToolsSign_Signer_Process.argtypes = [c_void_p, c_void_p, POINTER(StreamDescriptor), c_void_p, c_void_p]
_lib.PdfToolsSign_Signer_Process.restype = c_void_p

def sign_signer_process(signer, document, stream, output_options, provider):
    return _lib.PdfToolsSign_Signer_Process(signer, document, stream, output_options, provider)

_lib.PdfToolsSign_Signer_New.argtypes = []
_lib.PdfToolsSign_Signer_New.restype = c_void_p

def sign_signer_new():
    return _lib.PdfToolsSign_Signer_New()

_lib.PdfToolsSign_Signer_AddWarningHandlerW.argtypes = [c_void_p, c_void_p, Sign_Signer_WarningFunc]
_lib.PdfToolsSign_Signer_AddWarningHandlerW.restype = c_bool

def sign_signer_addwarninghandler(obj, context, function):
    return _lib.PdfToolsSign_Signer_AddWarningHandlerW(obj, context, function)

_lib.PdfToolsSign_Signer_RemoveWarningHandlerW.argtypes = [c_void_p, c_void_p, Sign_Signer_WarningFunc]
_lib.PdfToolsSign_Signer_RemoveWarningHandlerW.restype = c_bool

def sign_signer_removewarninghandler(obj, context, function):
    return _lib.PdfToolsSign_Signer_RemoveWarningHandlerW(obj, context, function)



_lib.PdfToolsCryptoProviders_Provider_Close.argtypes = [c_void_p]
_lib.PdfToolsCryptoProviders_Provider_Close.restype = c_bool

def cryptoproviders_provider_close(object):
    return _lib.PdfToolsCryptoProviders_Provider_Close(object)

_lib.PdfToolsCryptoProviders_Provider_GetType.argtypes = [c_void_p]
_lib.PdfToolsCryptoProviders_Provider_GetType.restype = c_int

def cryptoproviders_provider_gettype(object):
    return _lib.PdfToolsCryptoProviders_Provider_GetType(object)

_lib.PdfToolsCryptoProviders_Certificate_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProviders_Certificate_GetNameW.restype = c_size_t

def cryptoproviders_certificate_getname(certificate):
    ret_buffer_size = _lib.PdfToolsCryptoProviders_Certificate_GetNameW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProviders_Certificate_GetNameW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProviders_Certificate_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProviders_Certificate_GetSubjectW.restype = c_size_t

def cryptoproviders_certificate_getsubject(certificate):
    ret_buffer_size = _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProviders_Certificate_GetIssuerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProviders_Certificate_GetIssuerW.restype = c_size_t

def cryptoproviders_certificate_getissuer(certificate):
    ret_buffer_size = _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW.restype = c_size_t

def cryptoproviders_certificate_getfingerprint(certificate):
    ret_buffer_size = _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey.argtypes = [c_void_p]
_lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey.restype = c_bool

def cryptoproviders_certificate_gethasprivatekey(certificate):
    return _lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey(certificate)


_lib.PdfToolsCryptoProviders_CertificateList_GetCount.argtypes = [c_void_p]
_lib.PdfToolsCryptoProviders_CertificateList_GetCount.restype = c_int

def cryptoproviders_certificatelist_getcount(certificate_list):
    return _lib.PdfToolsCryptoProviders_CertificateList_GetCount(certificate_list)
_lib.PdfToolsCryptoProviders_CertificateList_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProviders_CertificateList_Get.restype = c_void_p

def cryptoproviders_certificatelist_get(certificate_list, i_index):
    return _lib.PdfToolsCryptoProviders_CertificateList_Get(certificate_list, i_index)


_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersglobalsigndss_signatureconfiguration_gethashalgorithm(signature_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetHashAlgorithm(signature_configuration)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignaturePaddingType.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignaturePaddingType.restype = c_int

def cryptoprovidersglobalsigndss_signatureconfiguration_getsignaturepaddingtype(signature_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignaturePaddingType(signature_configuration)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignatureFormat.restype = c_int

def cryptoprovidersglobalsigndss_signatureconfiguration_getsignatureformat(signature_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetSignatureFormat(signature_configuration)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetSignatureFormat.restype = c_bool

def cryptoprovidersglobalsigndss_signatureconfiguration_setsignatureformat(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetSignatureFormat(signature_configuration, val)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetAddTimestamp.restype = c_bool

def cryptoprovidersglobalsigndss_signatureconfiguration_getaddtimestamp(signature_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetAddTimestamp(signature_configuration)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetAddTimestamp.restype = c_bool

def cryptoprovidersglobalsigndss_signatureconfiguration_setaddtimestamp(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetAddTimestamp(signature_configuration, val)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetValidationInformation.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetValidationInformation.restype = c_int

def cryptoprovidersglobalsigndss_signatureconfiguration_getvalidationinformation(signature_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_GetValidationInformation(signature_configuration)
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetValidationInformation.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetValidationInformation.restype = c_bool

def cryptoprovidersglobalsigndss_signatureconfiguration_setvalidationinformation(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_SignatureConfiguration_SetValidationInformation(signature_configuration, val)


_lib.PdfToolsCryptoProvidersGlobalSignDss_TimestampConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_TimestampConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersglobalsigndss_timestampconfiguration_gethashalgorithm(timestamp_configuration):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_TimestampConfiguration_GetHashAlgorithm(timestamp_configuration)


_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity.restype = c_void_p

def cryptoprovidersglobalsigndss_session_createsignatureforstaticidentity(session):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity(session)
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW.restype = c_void_p

def cryptoprovidersglobalsigndss_session_createsignaturefordynamicidentity(session, identity):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW(session, string_to_utf16(identity))
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp.restype = c_void_p

def cryptoprovidersglobalsigndss_session_createtimestamp(session):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp(session)

_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW.argtypes = [c_wchar_p, c_wchar_p, c_wchar_p, c_void_p]
_lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW.restype = c_void_p

def cryptoprovidersglobalsigndss_session_new(url, api_key, api_secret, http_client_handler):
    return _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW(string_to_utf16(url), string_to_utf16(api_key), string_to_utf16(api_secret), http_client_handler)


_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersswisscomsigsrv_signatureconfiguration_gethashalgorithm(signature_configuration):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm(signature_configuration)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_sethashalgorithm(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm(signature_configuration, val)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat.restype = c_int

def cryptoprovidersswisscomsigsrv_signatureconfiguration_getsignatureformat(signature_configuration):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat(signature_configuration)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_setsignatureformat(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat(signature_configuration, val)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_getaddtimestamp(signature_configuration):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp(signature_configuration)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_setaddtimestamp(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp(signature_configuration, val)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_getembedvalidationinformation(signature_configuration):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation(signature_configuration)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation.restype = c_bool

def cryptoprovidersswisscomsigsrv_signatureconfiguration_setembedvalidationinformation(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation(signature_configuration, val)


_lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersswisscomsigsrv_timestampconfiguration_gethashalgorithm(timestamp_configuration):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm(timestamp_configuration)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoprovidersswisscomsigsrv_timestampconfiguration_sethashalgorithm(timestamp_configuration, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm(timestamp_configuration, val)


_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW.argtypes = [c_wchar_p, c_wchar_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW.restype = c_void_p

def cryptoprovidersswisscomsigsrv_stepup_new(msisdn, message, language):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW(string_to_utf16(msisdn), string_to_utf16(message), string_to_utf16(language))

_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW.restype = c_size_t

def cryptoprovidersswisscomsigsrv_stepup_getmsisdn(step_up):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW(step_up, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW(step_up, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW.restype = c_bool

def cryptoprovidersswisscomsigsrv_stepup_setmsisdn(step_up, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW(step_up, string_to_utf16(val))
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW.restype = c_size_t

def cryptoprovidersswisscomsigsrv_stepup_getmessage(step_up):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW(step_up, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW(step_up, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW.restype = c_bool

def cryptoprovidersswisscomsigsrv_stepup_setmessage(step_up, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW(step_up, string_to_utf16(val))
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW.restype = c_size_t

def cryptoprovidersswisscomsigsrv_stepup_getlanguage(step_up):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW(step_up, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW(step_up, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW.restype = c_bool

def cryptoprovidersswisscomsigsrv_stepup_setlanguage(step_up, val):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW(step_up, string_to_utf16(val))

_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW.argtypes = [c_void_p, c_void_p, CryptoProvidersSwisscomSigSrv_StepUp_ConsentRequiredFunc]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW.restype = c_bool

def cryptoprovidersswisscomsigsrv_stepup_addconsentrequiredhandler(obj, context, function):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW(obj, context, function)

_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW.argtypes = [c_void_p, c_void_p, CryptoProvidersSwisscomSigSrv_StepUp_ConsentRequiredFunc]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW.restype = c_bool

def cryptoprovidersswisscomsigsrv_stepup_removeconsentrequiredhandler(obj, context, function):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW(obj, context, function)



_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW.restype = c_void_p

def cryptoprovidersswisscomsigsrv_session_createsignatureforstaticidentity(session, identity, name):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW(session, string_to_utf16(identity), string_to_utf16(name))
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW.restype = c_void_p

def cryptoprovidersswisscomsigsrv_session_createsignatureforondemandidentity(session, identity, distinguished_name, step_up):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW(session, string_to_utf16(identity), string_to_utf16(distinguished_name), step_up)
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW.restype = c_void_p

def cryptoprovidersswisscomsigsrv_session_createtimestamp(session, identity):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW(session, string_to_utf16(identity))

_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW.argtypes = [c_wchar_p, c_void_p]
_lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW.restype = c_void_p

def cryptoprovidersswisscomsigsrv_session_new(url, http_client_handler):
    return _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW(string_to_utf16(url), http_client_handler)


_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_addcertificate(signature_configuration, certificate):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate(signature_configuration, certificate)


_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm.restype = c_int

def cryptoproviderspkcs11_signatureconfiguration_gethashalgorithm(signature_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm(signature_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_sethashalgorithm(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm(signature_configuration, val)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType.restype = c_int

def cryptoproviderspkcs11_signatureconfiguration_getsignaturepaddingtype(signature_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType(signature_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_setsignaturepaddingtype(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType(signature_configuration, val)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat.restype = c_int

def cryptoproviderspkcs11_signatureconfiguration_getsignatureformat(signature_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat(signature_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_setsignatureformat(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat(signature_configuration, val)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_getaddtimestamp(signature_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp(signature_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_setaddtimestamp(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp(signature_configuration, val)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation.restype = c_int

def cryptoproviderspkcs11_signatureconfiguration_getvalidationinformation(signature_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation(signature_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation.restype = c_bool

def cryptoproviderspkcs11_signatureconfiguration_setvalidationinformation(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation(signature_configuration, val)


_lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_GetHashAlgorithm.restype = c_int

def cryptoproviderspkcs11_timestampconfiguration_gethashalgorithm(timestamp_configuration):
    return _lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_GetHashAlgorithm(timestamp_configuration)
_lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoproviderspkcs11_timestampconfiguration_sethashalgorithm(timestamp_configuration, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_TimestampConfiguration_SetHashAlgorithm(timestamp_configuration, val)


_lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW.argtypes = [c_wchar_p]
_lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW.restype = c_void_p

def cryptoproviderspkcs11_module_load(library):
    return _lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW(string_to_utf16(library))

_lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization.restype = c_bool

def cryptoproviderspkcs11_module_getenablefullparallelization(module):
    return _lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization(module)
_lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization.restype = c_bool

def cryptoproviderspkcs11_module_setenablefullparallelization(module, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization(module, val)
_lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices.restype = c_void_p

def cryptoproviderspkcs11_module_getdevices(module):
    return _lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices(module)

_lib.PdfToolsCryptoProvidersPkcs11_Module_Close.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Module_Close.restype = c_bool

def cryptoproviderspkcs11_module_close(object):
    return _lib.PdfToolsCryptoProvidersPkcs11_Module_Close(object)


_lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW.restype = c_void_p

def cryptoproviderspkcs11_device_createsession(device, password):
    return _lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW(device, string_to_utf16(password))

_lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW.restype = c_size_t

def cryptoproviderspkcs11_device_getdescription(device):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW(device, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW(device, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW.restype = c_size_t

def cryptoproviderspkcs11_device_getmanufacturerid(device):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW(device, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW(device, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)


_lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW.restype = c_bool

def cryptoproviderspkcs11_session_login(session, password):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW(session, string_to_utf16(password))

_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature.restype = c_void_p

def cryptoproviderspkcs11_session_createsignature(session, certificate):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature(session, certificate)
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW.restype = c_void_p

def cryptoproviderspkcs11_session_createsignaturefromname(session, name):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW(session, string_to_utf16(name))
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t, POINTER(StreamDescriptor)]
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId.restype = c_void_p

def cryptoproviderspkcs11_session_createsignaturefromkeyid(session, id, id_buffer, certificate):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId(session, id, id_buffer, certificate)
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW.argtypes = [c_void_p, c_wchar_p, POINTER(StreamDescriptor)]
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW.restype = c_void_p

def cryptoproviderspkcs11_session_createsignaturefromkeylabel(session, label, certificate):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW(session, string_to_utf16(label), certificate)
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp.restype = c_void_p

def cryptoproviderspkcs11_session_createtimestamp(session):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp(session)

_lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW.restype = c_size_t

def cryptoproviderspkcs11_session_gettimestampurl(session):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW(session, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW(session, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW.restype = c_bool

def cryptoproviderspkcs11_session_settimestampurl(session, val):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW(session, string_to_utf16(val))
_lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates.restype = c_void_p

def cryptoproviderspkcs11_session_getcertificates(session):
    return _lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates(session)


_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle.restype = c_void_p

def cryptoproviderspkcs11_devicelist_getsingle(device_list):
    return _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle(device_list)
_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount.restype = c_int

def cryptoproviderspkcs11_devicelist_getcount(device_list):
    return _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount(device_list)
_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get.restype = c_void_p

def cryptoproviderspkcs11_devicelist_get(device_list, i_index):
    return _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get(device_list, i_index)


_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersbuiltin_signatureconfiguration_gethashalgorithm(signature_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetHashAlgorithm(signature_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_sethashalgorithm(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetHashAlgorithm(signature_configuration, val)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignaturePaddingType.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignaturePaddingType.restype = c_int

def cryptoprovidersbuiltin_signatureconfiguration_getsignaturepaddingtype(signature_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignaturePaddingType(signature_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignaturePaddingType.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignaturePaddingType.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_setsignaturepaddingtype(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignaturePaddingType(signature_configuration, val)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignatureFormat.restype = c_int

def cryptoprovidersbuiltin_signatureconfiguration_getsignatureformat(signature_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetSignatureFormat(signature_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignatureFormat.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_setsignatureformat(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetSignatureFormat(signature_configuration, val)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetAddTimestamp.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_getaddtimestamp(signature_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetAddTimestamp(signature_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetAddTimestamp.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_setaddtimestamp(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetAddTimestamp(signature_configuration, val)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetValidationInformation.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetValidationInformation.restype = c_int

def cryptoprovidersbuiltin_signatureconfiguration_getvalidationinformation(signature_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_GetValidationInformation(signature_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetValidationInformation.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetValidationInformation.restype = c_bool

def cryptoprovidersbuiltin_signatureconfiguration_setvalidationinformation(signature_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_SignatureConfiguration_SetValidationInformation(signature_configuration, val)


_lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_GetHashAlgorithm.restype = c_int

def cryptoprovidersbuiltin_timestampconfiguration_gethashalgorithm(timestamp_configuration):
    return _lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_GetHashAlgorithm(timestamp_configuration)
_lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
_lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_SetHashAlgorithm.restype = c_bool

def cryptoprovidersbuiltin_timestampconfiguration_sethashalgorithm(timestamp_configuration, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_TimestampConfiguration_SetHashAlgorithm(timestamp_configuration, val)


_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW.argtypes = [c_void_p, POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW.restype = c_void_p

def cryptoprovidersbuiltin_provider_createsignaturefromcertificate(provider, stream, password):
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW(provider, stream, string_to_utf16(password))
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp.argtypes = [c_void_p]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp.restype = c_void_p

def cryptoprovidersbuiltin_provider_createtimestamp(provider):
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp(provider)
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW.argtypes = [c_void_p, c_int, c_wchar_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW.restype = c_void_p

def cryptoprovidersbuiltin_provider_createpreparedsignature(provider, size, format, name):
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW(provider, size, string_to_utf16(format), string_to_utf16(name))
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature.restype = c_void_p

def cryptoprovidersbuiltin_provider_readexternalsignature(provider, signature, signature_buffer):
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature(provider, signature, signature_buffer)

_lib.PdfToolsCryptoProvidersBuiltIn_Provider_New.argtypes = []
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_New.restype = c_void_p

def cryptoprovidersbuiltin_provider_new():
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_New()

_lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW.restype = c_size_t

def cryptoprovidersbuiltin_provider_gettimestampurl(provider):
    ret_buffer_size = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW(provider, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW(provider, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW.argtypes = [c_void_p, c_wchar_p]
_lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW.restype = c_bool

def cryptoprovidersbuiltin_provider_settimestampurl(provider, val):
    return _lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW(provider, string_to_utf16(val))


_lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW.restype = c_size_t

def signaturevalidation_constraintresult_getmessage(constraint_result):
    ret_buffer_size = _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW(constraint_result, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW(constraint_result, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication.restype = c_int

def signaturevalidation_constraintresult_getindication(constraint_result):
    return _lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication(constraint_result)
_lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication.restype = c_int

def signaturevalidation_constraintresult_getsubindication(constraint_result):
    return _lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication(constraint_result)


_lib.PdfToolsSignatureValidation_Validator_Validate.argtypes = [c_void_p, c_void_p, c_void_p, c_int]
_lib.PdfToolsSignatureValidation_Validator_Validate.restype = c_void_p

def signaturevalidation_validator_validate(validator, document, profile, selector):
    return _lib.PdfToolsSignatureValidation_Validator_Validate(validator, document, profile, selector)

_lib.PdfToolsSignatureValidation_Validator_New.argtypes = []
_lib.PdfToolsSignatureValidation_Validator_New.restype = c_void_p

def signaturevalidation_validator_new():
    return _lib.PdfToolsSignatureValidation_Validator_New()

_lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW.argtypes = [c_void_p, c_void_p, SignatureValidation_Validator_ConstraintFunc]
_lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW.restype = c_bool

def signaturevalidation_validator_addconstrainthandler(obj, context, function):
    return _lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW(obj, context, function)

_lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW.argtypes = [c_void_p, c_void_p, SignatureValidation_Validator_ConstraintFunc]
_lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW.restype = c_bool

def signaturevalidation_validator_removeconstrainthandler(obj, context, function):
    return _lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW(obj, context, function)



_lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW.restype = c_size_t

def signaturevalidation_certificate_getsubjectname(certificate):
    ret_buffer_size = _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSignatureValidation_Certificate_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSignatureValidation_Certificate_GetSubjectW.restype = c_size_t

def signaturevalidation_certificate_getsubject(certificate):
    ret_buffer_size = _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW.restype = c_size_t

def signaturevalidation_certificate_getissuername(certificate):
    ret_buffer_size = _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSignatureValidation_Certificate_GetNotAfter.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsSignatureValidation_Certificate_GetNotAfter.restype = c_bool

def signaturevalidation_certificate_getnotafter(certificate, ret_val):
    return _lib.PdfToolsSignatureValidation_Certificate_GetNotAfter(certificate, byref(ret_val))
_lib.PdfToolsSignatureValidation_Certificate_GetNotBefore.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsSignatureValidation_Certificate_GetNotBefore.restype = c_bool

def signaturevalidation_certificate_getnotbefore(certificate, ret_val):
    return _lib.PdfToolsSignatureValidation_Certificate_GetNotBefore(certificate, byref(ret_val))
_lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
_lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW.restype = c_size_t

def signaturevalidation_certificate_getfingerprint(certificate):
    ret_buffer_size = _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW(certificate, None, 0)
    if ret_buffer_size == 0 and getlasterror() != 0:
        raise Exception(f"{getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")
    elif ret_buffer_size == 0:
        return None
    ret_buffer = create_unicode_buffer(ret_buffer_size)
    _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW(certificate, ret_buffer, ret_buffer_size)
    return utf16_to_string(ret_buffer, ret_buffer_size)
_lib.PdfToolsSignatureValidation_Certificate_GetRawData.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
_lib.PdfToolsSignatureValidation_Certificate_GetRawData.restype = c_size_t

def signaturevalidation_certificate_getrawdata(certificate, ret_val, ret_val_buffer):
    return _lib.PdfToolsSignatureValidation_Certificate_GetRawData(certificate, ret_val, ret_val_buffer)
_lib.PdfToolsSignatureValidation_Certificate_GetSource.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_Certificate_GetSource.restype = c_int

def signaturevalidation_certificate_getsource(certificate):
    return _lib.PdfToolsSignatureValidation_Certificate_GetSource(certificate)
_lib.PdfToolsSignatureValidation_Certificate_GetValidity.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_Certificate_GetValidity.restype = c_void_p

def signaturevalidation_certificate_getvalidity(certificate):
    return _lib.PdfToolsSignatureValidation_Certificate_GetValidity(certificate)


_lib.PdfToolsSignatureValidation_CertificateChain_GetCount.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CertificateChain_GetCount.restype = c_int

def signaturevalidation_certificatechain_getcount(certificate_chain):
    return _lib.PdfToolsSignatureValidation_CertificateChain_GetCount(certificate_chain)
_lib.PdfToolsSignatureValidation_CertificateChain_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidation_CertificateChain_Get.restype = c_void_p

def signaturevalidation_certificatechain_get(certificate_chain, i_index):
    return _lib.PdfToolsSignatureValidation_CertificateChain_Get(certificate_chain, i_index)

_lib.PdfToolsSignatureValidation_CertificateChain_IsComplete.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CertificateChain_IsComplete.restype = c_bool

def signaturevalidation_certificatechain_iscomplete(certificate_chain):
    return _lib.PdfToolsSignatureValidation_CertificateChain_IsComplete(certificate_chain)


_lib.PdfToolsSignatureValidation_ValidationResults_GetCount.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_ValidationResults_GetCount.restype = c_int

def signaturevalidation_validationresults_getcount(validation_results):
    return _lib.PdfToolsSignatureValidation_ValidationResults_GetCount(validation_results)
_lib.PdfToolsSignatureValidation_ValidationResults_Get.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidation_ValidationResults_Get.restype = c_void_p

def signaturevalidation_validationresults_get(validation_results, i_index):
    return _lib.PdfToolsSignatureValidation_ValidationResults_Get(validation_results, i_index)


_lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField.restype = c_void_p

def signaturevalidation_validationresult_getsignaturefield(validation_result):
    return _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField(validation_result)
_lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent.restype = c_void_p

def signaturevalidation_validationresult_getsignaturecontent(validation_result):
    return _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent(validation_result)


_lib.PdfToolsSignatureValidation_SignatureContent_GetValidity.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_SignatureContent_GetValidity.restype = c_void_p

def signaturevalidation_signaturecontent_getvalidity(signature_content):
    return _lib.PdfToolsSignatureValidation_SignatureContent_GetValidity(signature_content)

_lib.PdfToolsSignatureValidation_SignatureContent_GetType.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_SignatureContent_GetType.restype = c_int

def signaturevalidation_signaturecontent_gettype(object):
    return _lib.PdfToolsSignatureValidation_SignatureContent_GetType(object)

_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime.restype = c_bool

def signaturevalidation_cmssignaturecontent_getvalidationtime(cms_signature_content, ret_val):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime(cms_signature_content, byref(ret_val))
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource.restype = c_int

def signaturevalidation_cmssignaturecontent_getvalidationtimesource(cms_signature_content):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource(cms_signature_content)
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm.restype = c_int

def signaturevalidation_cmssignaturecontent_gethashalgorithm(cms_signature_content):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm(cms_signature_content)
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp.restype = c_void_p

def signaturevalidation_cmssignaturecontent_gettimestamp(cms_signature_content):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp(cms_signature_content)
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate.restype = c_void_p

def signaturevalidation_cmssignaturecontent_getsigningcertificate(cms_signature_content):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate(cms_signature_content)
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain.restype = c_void_p

def signaturevalidation_cmssignaturecontent_getcertificatechain(cms_signature_content):
    return _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain(cms_signature_content)


_lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTime.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTime.restype = c_bool

def signaturevalidation_timestampcontent_getvalidationtime(time_stamp_content, ret_val):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTime(time_stamp_content, byref(ret_val))
_lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTimeSource.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTimeSource.restype = c_int

def signaturevalidation_timestampcontent_getvalidationtimesource(time_stamp_content):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetValidationTimeSource(time_stamp_content)
_lib.PdfToolsSignatureValidation_TimeStampContent_GetHashAlgorithm.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetHashAlgorithm.restype = c_int

def signaturevalidation_timestampcontent_gethashalgorithm(time_stamp_content):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetHashAlgorithm(time_stamp_content)
_lib.PdfToolsSignatureValidation_TimeStampContent_GetDate.argtypes = [c_void_p, POINTER(SysDate)]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetDate.restype = c_bool

def signaturevalidation_timestampcontent_getdate(time_stamp_content, ret_val):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetDate(time_stamp_content, byref(ret_val))
_lib.PdfToolsSignatureValidation_TimeStampContent_GetSigningCertificate.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetSigningCertificate.restype = c_void_p

def signaturevalidation_timestampcontent_getsigningcertificate(time_stamp_content):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetSigningCertificate(time_stamp_content)
_lib.PdfToolsSignatureValidation_TimeStampContent_GetCertificateChain.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidation_TimeStampContent_GetCertificateChain.restype = c_void_p

def signaturevalidation_timestampcontent_getcertificatechain(time_stamp_content):
    return _lib.PdfToolsSignatureValidation_TimeStampContent_GetCertificateChain(time_stamp_content)


_lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates.argtypes = [c_void_p, POINTER(StreamDescriptor)]
_lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates.restype = c_bool

def signaturevalidation_customtrustlist_addcertificates(custom_trust_list, certificate):
    return _lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates(custom_trust_list, certificate)

_lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW.argtypes = [c_void_p, POINTER(StreamDescriptor), c_wchar_p]
_lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW.restype = c_bool

def signaturevalidation_customtrustlist_addarchive(custom_trust_list, stream, password):
    return _lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW(custom_trust_list, stream, string_to_utf16(password))


_lib.PdfToolsSignatureValidation_CustomTrustList_New.argtypes = []
_lib.PdfToolsSignatureValidation_CustomTrustList_New.restype = c_void_p

def signaturevalidation_customtrustlist_new():
    return _lib.PdfToolsSignatureValidation_CustomTrustList_New()


_lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions.restype = c_void_p

def signaturevalidationprofiles_profile_getvalidationoptions(profile):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions(profile)
_lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints.restype = c_void_p

def signaturevalidationprofiles_profile_getsigningcerttrustconstraints(profile):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints(profile)
_lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints.restype = c_void_p

def signaturevalidationprofiles_profile_gettimestamptrustconstraints(profile):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints(profile)
_lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList.restype = c_void_p

def signaturevalidationprofiles_profile_getcustomtrustlist(profile):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList(profile)
_lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList.argtypes = [c_void_p, c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList.restype = c_bool

def signaturevalidationprofiles_profile_setcustomtrustlist(profile, val):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList(profile, val)

_lib.PdfToolsSignatureValidationProfiles_Profile_GetType.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_Profile_GetType.restype = c_int

def signaturevalidationprofiles_profile_gettype(object):
    return _lib.PdfToolsSignatureValidationProfiles_Profile_GetType(object)

_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource.restype = c_int

def signaturevalidationprofiles_validationoptions_gettimesource(validation_options):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource(validation_options)
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource.restype = c_bool

def signaturevalidationprofiles_validationoptions_settimesource(validation_options, val):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource(validation_options, val)
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources.restype = c_int

def signaturevalidationprofiles_validationoptions_getcertificatesources(validation_options):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources(validation_options)
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources.restype = c_bool

def signaturevalidationprofiles_validationoptions_setcertificatesources(validation_options, val):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources(validation_options, val)
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources.restype = c_int

def signaturevalidationprofiles_validationoptions_getrevocationinformationsources(validation_options):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources(validation_options)
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources.restype = c_bool

def signaturevalidationprofiles_validationoptions_setrevocationinformationsources(validation_options, val):
    return _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources(validation_options, val)


_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources.restype = c_int

def signaturevalidationprofiles_trustconstraints_gettrustsources(trust_constraints):
    return _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources(trust_constraints)
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources.restype = c_bool

def signaturevalidationprofiles_trustconstraints_settrustsources(trust_constraints, val):
    return _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources(trust_constraints, val)
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy.argtypes = [c_void_p]
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy.restype = c_int

def signaturevalidationprofiles_trustconstraints_getrevocationcheckpolicy(trust_constraints):
    return _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy(trust_constraints)
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy.argtypes = [c_void_p, c_int]
_lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy.restype = c_bool

def signaturevalidationprofiles_trustconstraints_setrevocationcheckpolicy(trust_constraints, val):
    return _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy(trust_constraints, val)


_lib.PdfToolsSignatureValidationProfiles_Default_New.argtypes = []
_lib.PdfToolsSignatureValidationProfiles_Default_New.restype = c_void_p

def signaturevalidationprofiles_default_new():
    return _lib.PdfToolsSignatureValidationProfiles_Default_New()




# Struct functions

# Utility functions

def print_error_message(message):
    print(f"{message} {getlasterrormessage()}. Error type: {ErrorCode(getlasterror()).name}.")