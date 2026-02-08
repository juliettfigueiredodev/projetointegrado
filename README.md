# EducaSolidario

EducaSolidario é uma aplicação web voltada para a **doação e o reaproveitamento de materiais escolares** e para o fortalecimento de **projetos educacionais e comunitários**.

Na plataforma, **instituições** (como escolas, ONGs e projetos sociais) podem se cadastrar, divulgar suas **necessidades de materiais** e apresentar **projetos** como hortas comunitárias escolares, minicursos de reaproveitamento de materiais, oficinas e outras iniciativas. Já a **população em geral** pode acessar essas informações, conhecer os projetos e:

- realizar doações de materiais escolares;
- entrar em contato com a instituição de interesse;
- apoiar iniciativas que promovam educação, sustentabilidade e inclusão social.

Além disso, a plataforma também permite que **instituições troquem recursos entre si**, facilitando o reaproveitamento de materiais e a construção de uma rede colaborativa.

## Possíveis usos da nossa solução

Um primeiro uso seria por **famílias em situação de vulnerabilidade socioeconômica** que têm dificuldade para comprar materiais escolares para crianças e adolescentes. Por meio da plataforma, essas famílias podem encontrar instituições próximas que recebem doações de mochilas, cadernos, lápis, livros e outros itens, facilitando o acesso a recursos básicos para a permanência na escola.

Do lado das **instituições de ensino, ONGs e projetos sociais**, a aplicação pode ser usada para organizar e divulgar suas demandas de forma clara. Uma escola, por exemplo, pode cadastrar um projeto de *horta comunitária escolar* ou de *minicurso de reaproveitamento de materiais*, especificando os materiais necessários (ferramentas, sementes, materiais recicláveis, etc.). Assim, pessoas da comunidade e outras instituições conseguem visualizar essas necessidades e direcionar suas doações ou apoio de maneira mais eficiente.

Como se trata de um **projeto universitário**, a solução também pode ser utilizada por **laboratórios, grupos de pesquisa e projetos de extensão** que atuam junto a escolas em situação de vulnerabilidade. Um laboratório universitário que tenha uma linha de atuação com escolas públicas, por exemplo, pode utilizar a aplicação para cadastrar as escolas parceiras, mapear suas necessidades e divulgar projetos em andamento. Nesse cenário, o laboratório funciona como uma ponte entre a universidade, as escolas e potenciais doadores, centralizando informações e facilitando a articulação das ações.

A solução também pode ser útil para **negócios do mundo real**, como papelarias, gráficas e empresas que lidam com estoques de material escolar. Esses estabelecimentos poderiam utilizar a plataforma para doar materiais excedentes, coleções antigas ou itens próximos ao fim de linha, reduzindo desperdícios e fortalecendo sua responsabilidade social. Além disso, a participação da empresa nesses projetos pode gerar visibilidade positiva e aproximação com a comunidade local.

Por fim, a plataforma pode atuar como uma **rede de troca entre instituições**, não apenas de materiais, mas também de projetos e conhecimento. Por exemplo, uma escola que já possua estrutura e know-how para montar uma **rádio estudantil** pode, por meio da aplicação, entrar em contato com outra instituição interessada em implementar um projeto semelhante. A primeira escola pode compartilhar sua experiência, orientações e até recursos excedentes, enquanto a segunda recebe apoio para colocar a iniciativa em prática. Dessa forma, nossa solução contribui para um uso mais sustentável dos recursos, incentiva o reaproveitamento de materiais e fortalece iniciativas educacionais e comunitárias no mundo real.

## Projeto físico de banco de dados e sua importância para quem está aprendendo a programar.

O projeto físico de banco de dados é a última etapa do processo de modelagem de um banco. Nela, o modelo criado anteriormente é implementado em um sistema de gerenciamento de banco de dados (como MySQL, PostgreSQL ou Oracle), definindo como os dados serão armazenados no computador.

Essa fase envolve decisões importantes, como a criação de tabelas, definição de tipos de dados, uso de índices e estratégias para melhorar o desempenho das consultas, além de considerar o uso de memória e espaço em disco.

Para quem está aprendendo a programar, o projeto físico é fundamental porque mostra como a estrutura do banco influencia diretamente o funcionamento da aplicação. Um bom projeto físico pode deixar o sistema mais rápido, estável e eficiente, enquanto um projeto mal feito pode causar lentidão e problemas de desempenho, mesmo com um código bem escrito.



### Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/)** — linguagem utilizada no backend da aplicação.
- **[PostgreSQL](https://www.postgresql.org/)** — banco de dados relacional robusto utilizado para persistência dos dados.
- **[Psycopg2](https://pypi.org/project/psycopg2/)** — adaptador de banco de dados PostgreSQL para Python.
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** — gerenciamento de variáveis de ambiente para segurança das credenciais.
- **[Git](https://git-scm.com/)** — controle de versão do código-fonte.
- **[GitHub](https://github.com/)** — hospedagem do repositório e colaboração entre os membros do time.
- **[VS Code](https://code.visualstudio.com/)** — editor de código utilizado no desenvolvimento.


## Rodando localmente

### 1. Clone o projeto

```bash
  git clone https://github.com/juliettfigueiredodev/projetointegrado.git
```

Entre no diretório do projeto

```bash
  cd projetointegrado
```

### 2. Configuração do Ambiente Virtual (Python)

```bash
  # Criar o ambiente virtual
  python3 -m venv .venv

  # Ativar o ambiente (Linux/Mac)
  source .venv/bin/activate
  
  # Ativar o ambiente (Windows)
  # .\.venv\Scripts\activate
```

Instale as dependências do projeto:

```bash
  pip install -r requirements.txt
```

### 3. Configuração de Variáveis de Ambiente

* Crie um arquivo .env como o 'exemplo' na raiz do projeto (baseado no .env.example) e configure as credenciais do banco:

```Ini
DB_NAME=educasolidario_db
DB_USER=admin
DB_PASS=admin123
DB_HOST=localhost
DB_PORT=5432
```

### Importante: A criação das tabelas e a estrutura do banco deve ser feita manualmente via linha de comando na primeira execução. 

* Execute o script de infraestrutura para criar o schema:
```bash
python src/infrastructure/user_db.py
```
Você deverá ver a mensagem: "Tabelas, Types e Triggers criados com sucesso!"


### 5. Inicie a Aplicação
Com o banco configurado, inicie o sistema:
```bash
  python app.py
```


## Etiquetas

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
## Autores

- [@Juliett Figueirêdo](https://github.com/juliettfigueiredodev)
- [@Juan Carlos](https://github.com/JuanCostaDev)
- [@Linderval Matias](https://github.com/Linderval-Moura)
- [@Leandro Pereira](https://github.com/leandropereira-alt)
- [@Levi Brito](https://github.com/juliettfigueiredodev)

