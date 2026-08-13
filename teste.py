import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzg1MjgyNzIwfQ.N_YQ59u9rpXCt-W_V6fUgo_k-7zAndu_fQhJ2q6w-VM"

}


requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers )
print(requisicao)
print(requisicao.json())