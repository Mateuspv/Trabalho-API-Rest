from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class RegistroVeiculo(BaseModel):
    marca_veiculo: str
    placa: str
    cliente_nome: str
    mecanico_nome: str
    horario_chegada: str = None
    horario_saida: str = None

registros = []
@app.get("/")
def root():
    return {"message": "Status: OK"}

@app.post("/registrar_veiculo/")
def registrar_veiculo(registro: RegistroVeiculo):
    horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if registro.horario_chegada == None:
        registro.horario_chegada = horario_atual
    registros.append(registro)
    return {"message": "Registro salvo com sucesso!"}

@app.get("/registros/")
def listar_registros():
    return registros