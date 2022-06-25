from curses.panel import update_panels
from typing import Union
from urllib.parse import quote_from_bytes

import pyqrcode
from qr_settings.qr_size_map import QR_SIZE
from schemas.QrCode import QrCodeParams


class QrCode:
    qr_str:bytes
    file_name:str
    qr_version: int
    
    def __init__(self,params:Union[QrCodeParams,str],file_name:str):
        self.file_name = file_name
        if type(params) == QrCodeParams:
            self.qr_str = params.delimiter_str.join([
                params.product_id,
                "", # not required
                "", # not required
                params.l_type,
                params.s_type,
                params.free_format,
                params.length,
                params.diameter,
                params.upper_fittings_type,
                params.lower_fittings_type
                ]).encode()
        elif type(params) == str:
            self.qr_str = params.encode()
        else:
            self.qr_str = "".encode()
            
        print(len(self.qr_str))
        version = 0        
        for v in QR_SIZE:
            if v["upper_str_count"] >= len(self.qr_str):
                version = v["version"]
                break
        self.qr_version = version

    def create_qr_code(self) -> None:
        pyqrcode.create(
            self.qr_str,error="H", version=self.qr_version ,mode="binary"
        ).png(
            self.file_name, scale=5, module_color=[0,0,0,128], background=[255,255,255]
        )
    
