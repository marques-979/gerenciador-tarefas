import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "teste.db")})
    return app.test_client()


def adicionar(client, titulo="Estudar Flask", prioridade="media"):
    return client.post(
        "/adicionar",
        data={"titulo": titulo, "prioridade": prioridade},
        follow_redirects=True,
    )


def test_pagina_inicial_vazia(client):
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert "Nenhuma tarefa" in resposta.get_data(as_text=True)


def test_adicionar_tarefa(client):
    resposta = adicionar(client, "Montar portfólio")
    html = resposta.get_data(as_text=True)
    assert "Montar portfólio" in html
    assert "Tarefa adicionada!" in html


def test_titulo_vazio_nao_cria_tarefa(client):
    resposta = adicionar(client, "   ")
    assert "Digite um título" in resposta.get_data(as_text=True)
    assert client.get("/api/tarefas").get_json() == []


def test_prioridade_invalida_e_rejeitada(client):
    resposta = adicionar(client, "Tarefa", prioridade="urgentissima")
    assert "Prioridade inválida" in resposta.get_data(as_text=True)
    assert client.get("/api/tarefas").get_json() == []


def test_alternar_conclusao(client):
    adicionar(client)
    client.post("/1/alternar")
    assert client.get("/api/tarefas").get_json()[0]["concluida"] is True
    client.post("/1/alternar")
    assert client.get("/api/tarefas").get_json()[0]["concluida"] is False


def test_editar_tarefa(client):
    adicionar(client, "Titulo antigo")
    resposta = client.post(
        "/1/editar",
        data={"titulo": "Titulo novo", "prioridade": "alta"},
        follow_redirects=True,
    )
    assert "Tarefa atualizada!" in resposta.get_data(as_text=True)
    tarefa = client.get("/api/tarefas").get_json()[0]
    assert tarefa["titulo"] == "Titulo novo"
    assert tarefa["prioridade"] == "alta"


def test_excluir_tarefa(client):
    adicionar(client)
    client.post("/1/excluir")
    assert client.get("/api/tarefas").get_json() == []


def test_tarefa_inexistente_retorna_404(client):
    assert client.get("/99/editar").status_code == 404
    assert client.post("/99/excluir").status_code == 404


def test_filtros(client):
    adicionar(client, "Lavar louça")
    adicionar(client, "Pagar conta")
    client.post("/2/alternar")  # conclui "Pagar conta"

    pendentes = client.get("/?filtro=pendentes").get_data(as_text=True)
    assert "Lavar louça" in pendentes
    assert "Pagar conta" not in pendentes

    concluidas = client.get("/?filtro=concluidas").get_data(as_text=True)
    assert "Pagar conta" in concluidas
    assert "Lavar louça" not in concluidas


def test_html_e_escapado(client):
    adicionar(client, "<script>alert(1)</script>")
    html = client.get("/").get_data(as_text=True)
    assert "<script>alert(1)</script>" not in html
