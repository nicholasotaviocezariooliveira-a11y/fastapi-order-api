from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencie import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema,ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedidos
from typing import List
order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrao para pedidos do nosso sistema. Todas as rotas dos pedidos de autenticação 
    """
    return {"mensagem":"voce acessou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido =  Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return{"mensagem": f"Pedido criado com sussesso . ID do pedido:{novo_pedido.id}"}



@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): 
    pedido = session.query(Pedido).filter(Pedido.id ==id_pedido).first()
    if not pedido :
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação ")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"pedido numero : {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int,
                                item_pedido_schema:ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, datail="Pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401,detail="Você não tem autorisação para fazer essa operação")
        
    item_pedido = ItemPedidos(item_pedido_schema.quantidade, 
                              item_pedido_schema.sabor, 
                              item_pedido_schema.tamanho, 
                              item_pedido_schema.preco_unitario, 
                              id_pedido)
   
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem ": "Item criado com Sucesso", 
        "item_id ": item_pedido.id,  
        "preco_pedido": pedido.preco
    }
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedidos).filter(ItemPedidos.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, datail="Item no pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401,detail="Você não tem autorisação para fazer essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem ": "Item removido com Sucesso",
        "quntidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# finalizar pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): 
    pedido = session.query(Pedido).filter(Pedido.id ==id_pedido).first()
    if not pedido :
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação ")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"pedido numero : {pedido.id} finalizado com sucesso",
        "pedido": pedido
    }


# visualizar um pedido
@order_router.get("/pedido/{id.pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id ==id_pedido).first()
    if not pedido :
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação ")
    return{
         "quantidade_itens_pedido ": len(pedido.itens),
         "pedido": pedido
    } 
    
        
#visualizar todos os pedidosS
@order_router.get("/listar/pedidos.usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
    return pedidos
