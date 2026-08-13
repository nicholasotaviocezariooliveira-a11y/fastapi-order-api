from  fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session 
from models import Usuario
from jose import jwt, JWTError 
def pegar_sessao():
    try:
        session = sessionmaker(bind=db)
        session = session()
        yield session
        
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY,  ALGORITHM)
        id_usuario = int(dict_info.get("sub"))
    except JWTError :
        raise HTTPException(status_code=401, detail="asseso negado, verifique a validade do token ")
        #verificar token e valido 
        # estrair o ID do usuario do token 
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise   HTTPException(status_code=402, detail="Acesso Negado")
    return usuario
