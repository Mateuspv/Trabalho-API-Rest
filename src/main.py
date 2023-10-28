from fastapi import FastAPI, HTTPException, Request, Response
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

class RegistroVeiculo(BaseModel):
    id: int = None
    marca_veiculo: str
    placa: str
    cliente_nome: str
    mecanico_nome: str
    horario_chegada: str = None
    horario_saida: str = None


registros = []
id_counter = 1  # Inicialize o contador de ID

@app.get("/")
def root():
    return {"message": "Status: OK"}

@app.post("/registrar_veiculo/")
def registrar_veiculo(registro: RegistroVeiculo):

    global id_counter  
    registro.id = id_counter  
    id_counter += 1  

    horario_atual = datetime.now().strftime("%H:%M")

    for r in registros: # Valida se o veículo já saiu da manutenção
        if r.placa == registro.placa and not r.horario_saida:
            raise HTTPException(status_code=400, detail="Esse veículo ainda está em manutenção.")
        
    for r in registros: # Valida quando já existe um registro idêntico
        if r.dict(exclude={"id"}) == registro.model_dump(exclude={"id"}):
            raise HTTPException(status_code=400, detail="Esse registro já existe.")    
        
    if registro.horario_chegada == None:
        registro.horario_chegada = horario_atual

    registros.append(registro)
    return {"message": "Registro salvo com sucesso!"}

@app.get("/registros/")
def listar_registros(
    id: int = None,
    marca_veiculo: str = None,
    placa: str = None,
    cliente_nome: str = None,
    mecanico_nome: str = None,
    horario_chegada: str = None,
    horario_saida: str = None
):
    resultado = registros

    # Filtra os registros com base nos parâmetros passados
    if id:
        resultado = [r for r in resultado if r.id == id]
    if marca_veiculo:
        resultado = [r for r in resultado if r.marca_veiculo == marca_veiculo]
    if placa:
        resultado = [r for r in resultado if r.placa == placa]
    if cliente_nome:
        resultado = [r for r in resultado if r.cliente_nome == cliente_nome]
    if mecanico_nome:
        resultado = [r for r in resultado if r.mecanico_nome == mecanico_nome]
    if horario_chegada:
        if "e" in horario_chegada:
            inicio, fim = horario_chegada.split(" e ")
            resultado = [r for r in resultado if inicio <= r.horario_chegada <= fim]
        else:
            resultado = [r for r in resultado if r.horario_chegada == horario_chegada]
            # É possível usar tanto um parametro específico quanto um período de tempo. Ex: (08:00 e 09:00)
    if horario_saida:
        if "e" in horario_saida:
            inicio, fim = horario_saida.split(" e ")
            resultado = [r for r in resultado if inicio <= r.horario_saida <= fim]
        else:
            resultado = [r for r in resultado if r.horario_saida == horario_saida]

    return resultado

@app.patch("/atualizar_registro/{id}")
def atualizar_registro(id: int, horario_saida: str = None):
    registro_existe = None

    # Encontra o registro existente com base no ID
    for registro in registros:
        if registro.id == id:
            registro_existe = registro
            break

    if not registro_existe:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    # Atualiza a 'horario_saida' ou a hora atual
    if horario_saida:
        registro_existe.horario_saida = horario_saida
    else:
        registro_existe.horario_saida = datetime.now().strftime("%H:%M")

    return registro_existe

@app.delete("/excluir_registro/{id}")
def excluir_registro(id: int):
    global registros

    registro_existe = None

    # Encontra o registro existente com base no ID
    for registro in registros:
        if registro.id == id:
            registro_existe= registro
            break

    # Valida se registro existe
    if registro_existe is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    #Verifica se o registro contem horario de saida
    if registro_existe.horario_saida:
        raise HTTPException(status_code=400, detail="Este registro não pode ser excluído pois já está finalizado.")

    registros = [r for r in registros if r.id != id]
    return {"message": "Registro excluído com sucesso"}