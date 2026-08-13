from pydantic import BaseModel
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    adimin: Optional[bool]

class config:
    form_attributes = True



class PedidoSchema(BaseModel):
    id_usuario: int 

    class config:
        from_attributes = True 

class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
        quantidade: int
        sabor: str
        tamanho: str
        preco_unitario: float

        class config:
             from_attributes = True


class ResponsePedidoSchema(BaseModel):
        id : int 
        status: str
        preco: float
        itens: List[ItemPedidoSchema]

        class config:
             from_attributes = True