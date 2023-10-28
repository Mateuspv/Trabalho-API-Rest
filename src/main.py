from fastapi import FastAPI, HTTPException
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

    for r in registros: # Valida se o veículo já saiu da manutenção
        if r.placa == registro.placa and not r.horario_saida:
            raise HTTPException(status_code=400, detail="Esse veículo ainda está em manutenção.")
        
    for r in registros: # Valida quando já existe um registro idêntico
        if r.dict() == registro.model_dump():
            raise HTTPException(status_code=400, detail="Esse registro já existe.")    
        
    if registro.horario_chegada == None:
        registro.horario_chegada = horario_atual

    registros.append(registro)
    return {"message": "Registro salvo com sucesso!"}

@app.get("/registros/")
def listar_registros(
    marca_veiculo: str = None,
    placa: str = None,
    cliente_nome: str = None,
    mecanico_nome: str = None,
    horario_chegada: str = None,
    horario_saida: str = None
):
    resultado = registros

    # Filtra os registros com base nos parâmetros passados
    if marca_veiculo:
        resultado = [r for r in resultado if r.marca_veiculo == marca_veiculo]
    if placa:
        resultado = [r for r in resultado if r.placa == placa]
    if cliente_nome:
        resultado = [r for r in resultado if r.cliente_nome == cliente_nome]
    if mecanico_nome:
        resultado = [r for r in resultado if r.mecanico_nome == mecanico_nome]
    if horario_chegada:
        resultado = [r for r in resultado if r.horario_chegada == horario_chegada]
    if horario_saida:
        resultado = [r for r in resultado if r.horario_saida == horario_saida]

    return resultado