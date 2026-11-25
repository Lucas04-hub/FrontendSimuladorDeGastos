# Simulador de Gastos — Frontend

Aplicação web para gerenciamento de finanças pessoais, desenvolvida com Python, Flask, HTML, CSS e JavaScript.

## Sobre o projeto

O Simulador de Gastos é uma aplicação desenvolvida para ajudar no controle financeiro pessoal, permitindo registrar e acompanhar entradas e saídas de dinheiro de maneira simples e organizada.

O projeto utiliza uma aplicação Flask como backend e uma interface web interativa para facilitar o gerenciamento das movimentações financeiras.

## Funcionalidades

- Cadastro de entradas e saídas financeiras.
- Listagem de movimentações.
- Edição de movimentações existentes.
- Exclusão de movimentações.
- Cálculo automático de entradas, saídas e saldo.
- Organização por categorias.
- Filtros e pesquisa de movimentações.
- Validação dos dados informados.
- Interface responsiva.
- Armazenamento dos dados em arquivo JSON.

## Tecnologias utilizadas

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- JSON
- Pytest
- Git e GitHub

## Estrutura do projeto

```text
Projeto-SimuladorDeGastos-Frontend/
├── app.py
├── src/
│   └── financeiro/
├── frontend/
│   ├── templates/
│   └── static/
│       ├── css/
│       └── js/
├── data/
├── tests/
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Lucas04-hub/FrontendSimuladorDeGastos.git
```

### 2. Entrar na pasta do projeto

```bash
cd FrontendSimuladorDeGastos
```

### 3. Criar um ambiente virtual

```bash
python3 -m venv .venv
```

### 4. Ativar o ambiente virtual

No macOS ou Linux:

```bash
source .venv/bin/activate
```

### 5. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Executar a aplicação

```bash
python app.py
```

Depois, acesse no navegador:

http://127.0.0.1:5000

## Executar os testes

Para executar os testes automatizados:

```bash
python -m pytest -v
```

Os testes verificam as validações das movimentações, o gerenciamento financeiro, o funcionamento da aplicação Flask e as rotas da API.

## Armazenamento de dados

As movimentações financeiras são armazenadas localmente em um arquivo JSON dentro da pasta `data/`.

## Status do projeto

Projeto desenvolvido para fins de aprendizado, prática de desenvolvimento Frontend e Backend e construção de portfólio profissional.