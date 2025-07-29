from ctypes import *
from enum import IntEnum

class EventSeverity(IntEnum):
    """
    The severity of conversion events

    See `pdftools_sdk.pdf_a.conversion.converter.Converter.ConversionEvent` for more information on conversion events.



    Attributes:
        INFORMATION (int):
             
            An informational event requires no further action.
             
            By default events of the following `pdftools_sdk.pdf_a.conversion.event_category.EventCategory` are classified as `pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION`:
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.MANAGEDCOLORS`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CHANGEDCOLORANT`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEXTERNALCONTENT`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDFONT`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.SUBSTITUTEDFONT`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDANNOTATION`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDMULTIMEDIA`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDACTION`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDMETADATA`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDSTRUCTURE`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.CONVERTEDEMBEDDEDFILE`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDSIGNATURE`

        WARNING (int):
             
            An warning that might require further actions.
             
            By default events of the following `pdftools_sdk.pdf_a.conversion.event_category.EventCategory` are classified as `pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING`:
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.VISUALDIFFERENCES`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REPAIREDCORRUPTION`
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDTRANSPARENCY` (PDF/A-1 only)
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDEMBEDDEDFILE`  (PDF/A-1 and PDF/A-2 only)
                - `pdftools_sdk.pdf_a.conversion.event_category.EventCategory.REMOVEDOPTIONALCONTENT` (PDF/A-1 only)

        ERROR (int):
             
            A critical issue for which the conversion must be considered as failed.
             
            By default no event uses this severity.


    """
    INFORMATION = 1
    WARNING = 2
    ERROR = 3

