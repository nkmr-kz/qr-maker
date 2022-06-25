from pydantic import BaseModel


class QrCodeParams(BaseModel):
    product_id:str
    l_type:str
    s_type:str
    free_format:str
    length:str
    diameter:str
    upper_fittings_type:str
    lower_fittings_type:str
    delimiter_str: str
    
