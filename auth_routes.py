from fastapi import APIRouter, Depends, HTTPException  
from models import Usuario
from dependencie import pegar_sessao, verificar_token 
from main import brcypt_context, ALGORITHM, ACCESS_TOCKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/auth", tags=["autenticação"])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOCKEN_EXPIRE_MINUTES)):
    data_expiraçao = datetime.now(timezone.utc) + duracao_token
    dict_info = {"sub": str(id_usuario), "exp": data_expiraçao}
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM )
    token = f"fnsyubf7s8fs9{id_usuario}"
    return jwt_codificado



def autenticar_usuario(email, senha, session):
    usuario =session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not brcypt_context.verify(senha, usuario.senha):
        return False
    return usuario



@auth_router.get("/")
async def autenticar():
    """
    Essa e arrota padrão de autenticação do sistema
    """
    return {"mensagem": "voce acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        
        raise HTTPException(status_cod=400 , datail="email do usuario já cadastrado!")
    else:
        senha_criptografada = brcypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.adimin, usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuaeio cadastrado com sucesso {usuario_schema.email}"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais não encontrada ")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais não encontrada ")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)): 
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
            }



#headers ={"Access - Token":"Barer token"}
