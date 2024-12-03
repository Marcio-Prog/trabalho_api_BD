from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import mysql.connector

app = FastAPI()

# Modelos de dados
class Autor(BaseModel):
    id: int
    nome: str
    data_nascimento: Optional[str] = None
    nacionalidade: Optional[str] = None

class Livro(BaseModel):
    id: int
    titulo: str
    autor_id: int
    ano_publicacao: int
    genero: Optional[str] = None


# Funcao de conexao
def conecta():
    conexao = mysql.connector.connect(
    host ='localhost',
    user ='result',
    password ='res2003',
    database = 'biblioteca'
    )
    return conexao  

# Página inicial 

@app.get('/')
def index():
    return 'Minha CRUD da Biblioteca'

# CRUD para Autores

@app.post("/autores", response_model=Autor)
def criar_autor(autor: Autor):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        query = "INSERT INTO autores (nome, data_nascimento, nacionalidade) VALUES (%s, %s, %s)"
        valores = (autor.nome, autor.data_nascimento, autor.nacionalidade)
        cursor.execute(query, valores)
        conexao.commit()
        autor.id = cursor.lastrowid 
        return autor
    finally:
        cursor.close()
        conexao.close()


@app.get("/autores", response_model=List[Autor])
def listar_autores():
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    try:
        query = "SELECT * FROM autores"
        cursor.execute(query)
        resultados = cursor.fetchall()
        return [Autor(**resultado) for resultado in resultados]
    finally:
        cursor.close()
        conexao.close()

@app.get("/autores/{autor_id}", response_model=Autor)
def buscar_autor_por_id(autor_id: int):
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    try:
        query = "SELECT * FROM autores WHERE id = %s"
        cursor.execute(query, (autor_id,))
        resultado = cursor.fetchone()
        if not resultado:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return Autor(**resultado)
    finally:
        cursor.close()
        conexao.close()


@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(autor_id: int, autor_atualizado: Autor):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        query = "UPDATE autores SET nome = %s, data_nascimento = %s, nacionalidade = %s WHERE id = %s"
        valores = (autor_atualizado.nome, autor_atualizado.data_nascimento, autor_atualizado.nacionalidade, autor_id)
        cursor.execute(query, valores)
        conexao.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return autor_atualizado
    finally:
        cursor.close()
        conexao.close()


@app.delete("/autores/{autor_id}")
def deletar_autor_por_id(autor_id: int):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        query = "DELETE FROM autores WHERE id = %s"
        cursor.execute(query, (autor_id,))
        conexao.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return {"message": "Autor deletado com sucesso"}
    finally:
        cursor.close()
        conexao.close()


# CRUD para Livros

@app.post("/livros", response_model=Livro)
def criar_livro(livro: Livro):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        # Verifica se o autor existe
        cursor.execute("SELECT id FROM autores WHERE id = %s", (livro.autor_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        query = "INSERT INTO livros (titulo, autor_id, ano_publicacao, genero) VALUES (%s, %s, %s, %s)"
        valores = (livro.titulo, livro.autor_id, livro.ano_publicacao, livro.genero)
        cursor.execute(query, valores)
        conexao.commit()
        livro.id = cursor.lastrowid 
        return livro
    finally:
        cursor.close()
        conexao.close()


@app.get("/livros", response_model=List[Livro])
def listar_livros():
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    try:
        query = "SELECT * FROM livros"
        cursor.execute(query)
        resultados = cursor.fetchall()
        return [Livro(**resultado) for resultado in resultados]
    finally:
        cursor.close()
        conexao.close()


@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro_por_id(livro_id: int):
    conexao = conecta()
    cursor = conexao.cursor(dictionary=True)
    try:
        query = "SELECT * FROM livros WHERE id = %s"
        cursor.execute(query, (livro_id,))
        resultado = cursor.fetchone()
        if not resultado:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return Livro(**resultado)
    finally:
        cursor.close()
        conexao.close()


@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        query = "UPDATE livros SET titulo = %s, autor_id = %s, ano_publicacao = %s, genero = %s WHERE id = %s"
        valores = (livro_atualizado.titulo, livro_atualizado.autor_id, livro_atualizado.ano_publicacao, livro_atualizado.genero, livro_id)
        cursor.execute(query, valores)
        conexao.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro_atualizado
    finally:
        cursor.close()
        conexao.close()


@app.delete("/livros/{livro_id}")
def deletar_livro_por_id(livro_id: int):
    conexao = conecta()
    cursor = conexao.cursor()
    try:
        query = "DELETE FROM livros WHERE id = %s"
        cursor.execute(query, (livro_id,))
        conexao.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return {"message": "Livro deletado com sucesso"}
    finally:
        cursor.close()
        conexao.close()


