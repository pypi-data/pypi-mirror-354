"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from . import widget_data_pb2 as widget__data__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16widget-data-msgs.proto\x1a\x11widget-data.proto"\x1e\n\x10WidgetDataGetReq\x12\n\n\x02id\x18\x01 \x01(\t"4\n\x11WidgetDataGetResp\x12\x1f\n\nwidgetData\x18\x01 \x01(\x0b2\x0b.WidgetData"5\n\x12WidgetDataWriteReq\x12\x1f\n\nwidgetData\x18\x01 \x01(\x0b2\x0b.WidgetData"6\n\x13WidgetDataWriteResp\x12\x1f\n\nwidgetData\x18\x01 \x01(\x0b2\x0b.WidgetData""\n\x14WidgetMetadataGetReq\x12\n\n\x02id\x18\x01 \x01(\t"R\n\x15WidgetMetadataGetResp\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nwidgetName\x18\x02 \x01(\t\x12\x19\n\x11widgetDescription\x18\x03 \x01(\t"S\n\x16WidgetMetadataWriteReq\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nwidgetName\x18\x02 \x01(\t\x12\x19\n\x11widgetDescription\x18\x03 \x01(\t"T\n\x17WidgetMetadataWriteResp\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nwidgetName\x18\x02 \x01(\t\x12\x19\n\x11widgetDescription\x18\x03 \x01(\tB\nZ\x08.;protosb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'widget_data_msgs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z\x08.;protos'
    _globals['_WIDGETDATAGETREQ']._serialized_start = 45
    _globals['_WIDGETDATAGETREQ']._serialized_end = 75
    _globals['_WIDGETDATAGETRESP']._serialized_start = 77
    _globals['_WIDGETDATAGETRESP']._serialized_end = 129
    _globals['_WIDGETDATAWRITEREQ']._serialized_start = 131
    _globals['_WIDGETDATAWRITEREQ']._serialized_end = 184
    _globals['_WIDGETDATAWRITERESP']._serialized_start = 186
    _globals['_WIDGETDATAWRITERESP']._serialized_end = 240
    _globals['_WIDGETMETADATAGETREQ']._serialized_start = 242
    _globals['_WIDGETMETADATAGETREQ']._serialized_end = 276
    _globals['_WIDGETMETADATAGETRESP']._serialized_start = 278
    _globals['_WIDGETMETADATAGETRESP']._serialized_end = 360
    _globals['_WIDGETMETADATAWRITEREQ']._serialized_start = 362
    _globals['_WIDGETMETADATAWRITEREQ']._serialized_end = 445
    _globals['_WIDGETMETADATAWRITERESP']._serialized_start = 447
    _globals['_WIDGETMETADATAWRITERESP']._serialized_end = 531