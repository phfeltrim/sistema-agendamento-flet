# Sistema de Agendamento Profissional

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-Desktop_App-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)

## 📖 Descrição

Este projeto é uma aplicação de desktop moderna para o gerenciamento de agendamentos em consultórios. Desenvolvido em Python com o framework **Flet**, o sistema oferece uma interface de usuário limpa e reativa, conectada a um banco de dados **MySQL** para persistência de dados.

O objetivo é fornecer uma solução completa e segura para profissionais que precisam organizar sessões com pacientes, gerenciar informações de clientes e acompanhar o desempenho do consultório através de um dashboard analítico.

## ✨ Funcionalidades Principais

- **Autenticação Segura:** Sistema de login com senhas criptografadas (bcrypt) e gerenciamento de sessão de usuário.
- **Gerenciamento de Pacientes:** Funcionalidades completas de CRUD (Criar, Ler, Atualizar, Excluir) para o cadastro de pacientes.
- **Gestão de Agendamentos:** Interface para criar, visualizar e gerenciar sessões e agendamentos.
- **Dashboard Analítico:** Uma tela de dashboard que apresenta KPIs (Indicadores Chave de Performance) importantes, como:
    - Faturamento Bruto e Lucro Líquido.
    - Número de sessões realizadas.
    - Aquisição de novos pacientes.
    - Gráfico de faturamento mensal.
- **Exportação de Dados:** Funcionalidade no dashboard para exportar relatórios em formatos **CSV** (dados brutos) e **PDF** (visualização do relatório).
- **Acessibilidade:**
    - Modo de **Alto Contraste** para melhor visualização.
    - Ferramenta de **Zoom de Texto** para ajustar o tamanho da fonte em toda a aplicação.
    - **Textos Alternativos** (`tooltip`) em ícones e imagens para auxiliar leitores de tela.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface Gráfica (GUI):** Flet
- **Banco de Dados:** MySQL (gerenciado localmente via XAMPP)
- **Bibliotecas Principais:**
    - `mysql-connector-python` para a conexão com o banco de dados.
    - `bcrypt` para hashing e segurança de senhas.
    - `pandas` para manipulação e exportação de dados para CSV.
    - `reportlab` para a geração programática de relatórios em PDF.
    - `pygetwindow` e `mss` para a funcionalidade de captura de tela.

## 🚀 Como Começar

Siga os passos abaixo para configurar e executar o projeto em seu ambiente de desenvolvimento.

### Pré-requisitos

- Python 3.10 ou superior.
- Git instalado na sua máquina.
- Um servidor de banco de dados MySQL. Recomendamos o uso do **[XAMPP](https://www.apachefriends.org/pt_br/index.html)** para um ambiente de desenvolvimento local rápido.

### Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/phfeltrim/sistema-agendamento-flet.git](https://github.com/phfeltrim/sistema-agendamento-flet.git)
    cd sistema-agendamento-flet
    ```

2.  **Configure o Banco de Dados:**
    - Inicie o serviço **MySQL** no seu painel XAMPP.
    - Usando uma ferramenta como MySQL Workbench ou phpMyAdmin, crie um banco de dados chamado `agendamento`.
    - Execute os scripts SQL localizados na pasta `database/commands/` para criar as tabelas (`create-table-*.sql`) e inserir os dados iniciais (`insert-data-tables.sql`).

3.  **Crie e configure o arquivo de ambiente:**
    - Na pasta raiz do projeto, crie um arquivo chamado `config.ini`.
    - Copie e cole o conteúdo abaixo, substituindo com suas credenciais do MySQL (para XAMPP, o usuário é `root` e a senha é vazia).
        ```ini
        [database]
        host = localhost
        user = root
        password = 
        database = agendamento
        ```

4.  **Instale as dependências:**
    - Recomenda-se o uso de um ambiente virtual (`venv`).
        ```bash
        python -m venv .venv
        # No Windows
        .\.venv\Scripts\activate
        # No macOS/Linux
        # source .venv/bin/activate
        ```
    - Instale todas as bibliotecas necessárias com o `requirements.txt`.
        ```bash
        pip install -r requirements.txt
        ```

5.  **Atualize as senhas:**
    - Execute o script de utilidade para definir senhas seguras (em formato bcrypt) para os usuários iniciais.
        ```bash
        python utility_scripts/update_passwords.py
        ```
    - Siga as instruções no terminal para definir uma nova senha para o usuário administrador.

### Executando a Aplicação

Com o ambiente configurado, execute o seguinte comando a partir da pasta **raiz** do projeto:
```bash
python -m app.main
```
A janela do aplicativo de agendamento deve abrir, exibindo a tela de login.

---
### Estrutura do Projeto

```
/sistema-web-gerenciamento-de-agendamento/
|-- app/                  # Contém todo o código-fonte da aplicação
|   |-- controllers/      # Lógica de negócio (autenticação, dashboard)
|   |-- models/           # Conexão com o banco de dados
|   |-- settings/         # Módulos de configuração (temas, etc.)
|   |-- utils/            # Funções auxiliares (gerador de PDF)
|   |-- views/            # Componentes da interface do usuário (telas)
|   |-- main.py           # Ponto de entrada da aplicação Flet
|
|-- database/             # Scripts e documentação do banco de dados
|-- utility_scripts/      # Scripts de manutenção (ex: atualizar senhas)
|-- config.ini            # Arquivo de configuração (credenciais do BD)
|-- requirements.txt      # Lista de dependências Python
|-- README.md             # Este arquivo
```
