from typeguard import typechecked
from enum import Enum


@typechecked
def encode_varint(value:int) -> bytes:
    if value == 0:
        return b'\x00'
    
    result = bytearray()
    while value: # sayı 0 olana kadar devam
        part = value & 0b01111111 #asıl sayının maskelenmesi
        value >>= 7
        if value: #7 bit kaydırmadan sonra hala 0 dan farklı ise devamı var demektir başa 1 ekliyoruz
            part |= 0b10000000 
        result.append(part)
    return bytes(result)

@typechecked
def decode_varint(value:bytes, offset:int = 0) -> tuple[int, int]:
    result:int = 0
    index:int = 0
    temp = []
    while True:
        part = value[offset + index] #başlamamız gereken nokta + kaçıncı byte da olduğumuz verisi ile byte çekiyoruz
        temp.append(part)
        index += 1
        if not (part & 0b10000000):
            break
    
    for i, byte in enumerate(temp):
        result |= (byte & 0b01111111) << (7 * i)

    return result, index
