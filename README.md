# Jornal Voz Ativa — Ásia em Transformação

Jornal digital interativo desenvolvido para a CIARTEC, com foco no Afeganistão, nas desigualdades sociais e no Objetivo de Desenvolvimento Sustentável 10 (ODS 10), da Organização das Nações Unidas.

O projeto apresenta informações em formato de jornal, combinando reportagens, recursos visuais e uma avaliação interativa para tornar a experiência de leitura mais envolvente.

## Funcionalidades

- **Capa jornalística:** manchete, fotografia principal e colunas informativas.
- **Reportagens:** conteúdos sobre desigualdade de gênero, desigualdade educacional, desigualdade social e o Talibã.
- **Quiz interativo:** perguntas com alternativas, explicações e feedback após as respostas.
- **Navegação entre páginas:** avanço sequencial, retorno à página anterior e indicadores de progresso.
- **Design responsivo:** adaptação para computadores e dispositivos móveis.
- **Modo noturno:** opção de leitura com tema escuro.
- **Barra de leitura:** indicador visual do progresso na página.
- **Persistência local:** o melhor resultado do quiz e a preferência de tema podem ser armazenados no navegador.

## Tecnologias utilizadas

- Python — organização dos conteúdos e geração do site.
- Jinja2 — renderização dos templates HTML.
- HTML5 — estrutura das páginas.
- CSS3 — identidade visual e responsividade.
- JavaScript — navegação, interações e lógica do quiz.

## Como executar localmente

**Requisitos:** Python 3.10 ou superior.

1. Clone o repositório:

   ```bash
   git clone https://github.com/gomes333/projeto-ciartec.git
   cd projeto-ciartec
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Gere o site e inicie o servidor local de teste:

   ```bash
   python build.py --serve
   ```

4. Acesse `http://localhost:8000` no navegador.

Para gerar somente os arquivos do site, execute:

```bash
python build.py
```

Os arquivos gerados estarão na pasta `dist/`. Depois da geração, o site pode ser aberto localmente ou publicado em um serviço de hospedagem estática.

Execute novamente o gerador sempre que modificar os conteúdos, os templates ou os recursos utilizados pelo site.

## Estrutura do projeto

```text
projeto-ciartec/
├── build.py                 # Geração do site estático
├── dados.py                 # Textos e conteúdos das reportagens
├── quiz.py                  # Perguntas e lógica dos resultados
├── componentes.py           # Funções auxiliares
├── requirements.txt         # Dependências Python
├── templates/               # Templates HTML com Jinja2
├── static/
│   ├── estilo.css            # Estilos e identidade visual
│   ├── jornal.js             # Navegação e recursos interativos
│   └── quiz.js               # Lógica e animações do quiz
├── imagens/                  # Fotografias e recursos visuais
├── .github/
│   └── workflows/
│       └── pages.yml         # Publicação automatizada no GitHub Pages
├── netlify.toml              # Configuração do Netlify
├── vercel.json               # Configuração do Vercel
├── LICENSE                   # Licença MIT
└── dist/                     # Site gerado para publicação
```

A pasta `dist/` é gerada pelo processo de build. Sua inclusão no controle de versão depende da configuração de publicação adotada.

## Como editar o projeto

### Textos e reportagens

Edite os conteúdos em `dados.py`. Cada item da lista `jornais` representa uma página e pode conter seu próprio identificador (`slug`), título de seção, textos e imagens.

### Imagens

Adicione ou substitua as fotografias na pasta `imagens/`, respeitando os nomes de arquivo utilizados pelos conteúdos. Consulte `imagens/LEIAME.txt` para verificar as imagens esperadas.

### Quiz

Edite a lista `perguntas` em `quiz.py`. Cada pergunta deve ter alternativas válidas, uma resposta correspondente a uma das opções e, quando aplicável, uma explicação para o feedback após a resposta.

O processo de build verifica a consistência das respostas antes de gerar o site.

### Aparência

Edite `static/estilo.css`. As variáveis definidas em `:root` concentram as principais cores e configurações visuais.

### Interatividade

Os arquivos JavaScript da pasta `static/` controlam os recursos interativos do jornal e do quiz. Após as alterações, gere novamente o site para atualizar os arquivos em `dist/`.

## Publicação

O site pode ser publicado em serviços de hospedagem estática, como:

- **GitHub Pages:** publicação automatizada por GitHub Actions, conforme a configuração do repositório.
- **Netlify:** publicação por integração com o GitHub ou envio dos arquivos gerados.
- **Vercel:** publicação por integração com o repositório.

A configuração de cada plataforma deve apontar para o comando de build e o diretório de saída corretos.

## Créditos

Projeto desenvolvido originalmente por **Isadora Gomes - ([@gomes333](https://github.com/gomes333))** para a CIARTEC, com contribuições posteriores de **Miguel Henrique — ([@GalvaoLabs](https://github.com/GalvaoLabs))** no desenvolvimento e aprimoramento do site.

A autoria das contribuições deve ser reconhecida de acordo com a participação efetiva de cada colaborador.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
