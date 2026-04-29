from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    1,
    '',
    'product.proto'
)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\x12\x08products\"\x07\n\x05\x45mpty\"3\n\x14\x43reateProductRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x02\"#\n\x15GetProductByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"?\n\x14UpdateProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x02\"\"\n\x14\x44\x65leteProductRequest\x12\n\n\x02id\x18\x01 \x01(\t\"b\n\x0fProductResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x02\x12\x12\n\ncreated_at\x18\x04 \x01(\t\x12\x12\n\nupdated_at\x18\x05 \x01(\t\"C\n\x14ListProductsResponse\x12+\n\x08products\x18\x01 \x03(\x0b\x32\x19.products.ProductResponse\"9\n\x15\x44\x65leteProductResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x89\x03\n\x0eProductService\x12J\n\rCreateProduct\x12\x1e.products.CreateProductRequest\x1a\x19.products.ProductResponse\x12L\n\x0eGetProductById\x12\x1f.products.GetProductByIdRequest\x1a\x19.products.ProductResponse\x12?\n\x0cListProducts\x12\x0f.products.Empty\x1a\x1e.products.ListProductsResponse\x12J\n\rUpdateProduct\x12\x1e.products.UpdateProductRequest\x1a\x19.products.ProductResponse\x12P\n\rDeleteProduct\x12\x1e.products.DeleteProductRequest\x1a\x1f.products.DeleteProductResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=27
  _globals['_EMPTY']._serialized_end=34
  _globals['_CREATEPRODUCTREQUEST']._serialized_start=36
  _globals['_CREATEPRODUCTREQUEST']._serialized_end=87
  _globals['_GETPRODUCTBYIDREQUEST']._serialized_start=89
  _globals['_GETPRODUCTBYIDREQUEST']._serialized_end=124
  _globals['_UPDATEPRODUCTREQUEST']._serialized_start=126
  _globals['_UPDATEPRODUCTREQUEST']._serialized_end=189
  _globals['_DELETEPRODUCTREQUEST']._serialized_start=191
  _globals['_DELETEPRODUCTREQUEST']._serialized_end=225
  _globals['_PRODUCTRESPONSE']._serialized_start=227
  _globals['_PRODUCTRESPONSE']._serialized_end=325
  _globals['_LISTPRODUCTSRESPONSE']._serialized_start=327
  _globals['_LISTPRODUCTSRESPONSE']._serialized_end=394
  _globals['_DELETEPRODUCTRESPONSE']._serialized_start=396
  _globals['_DELETEPRODUCTRESPONSE']._serialized_end=453
  _globals['_PRODUCTSERVICE']._serialized_start=456
  _globals['_PRODUCTSERVICE']._serialized_end=849
# @@protoc_insertion_point(module_scope)
