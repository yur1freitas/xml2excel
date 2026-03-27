## [0.3.0] - 2026-03-27

### 🚀 Features

- Use uma estrutura hierárquica na visualização de colunas
- Readicione a funcionalidade de adicionar coluna de índice
- Readicione a funcionalidade de prefixo de colunas
- [**breaking**] Substitua o conversor atual pelo o novo baseado em `flatdict`
- Crie um conversor de `flatdict` para excel
- Crie um converso de xml para `flatdict`
- Implemente a classe `flatdict`
- Crie um botão para alternar entre o modo escuro e modo claro
- Adicione ícones nos botões de importação e exportação
- Crie um novo tema para a aplicação

### 🐛 Bug Fixes

- Corrija o nome do parâmetro ao instanciar `ExportFilesInput`
- Use a propriedade correta ao usar o método `trace` em `prefix_mode`
- Verifique se `column_index` não é `None` em vez de convertê-lo para booleano
- Corrija a importação de `Path` em `ImportFilesButton.py`

### 🚜 Refactor

- Renomeie o termo `index` para `index_column`
- Atualize a mensagem da opção de adicionar coluna de índice
- Renomeie o termo `prefix_mode` para `column_prefix_style`
- Use `any()` para verificar se alguma condição é atendida em `_can_ignore_column()`
- Use `Iterable[str]` no parâmetro `ignore_columns` em `FlatDict2Excel`
- Inicialize `_ignore_columns` como um `set` vazio em `Config`
- Inicialize `_filepaths` como uma tupla vazia em `Store`
- Substitua `tuple[XMLData]` por `tuple[XMLData, ...]`
- Inicialize `_data` como uma tupla vazia em `Store`
- Remova o antigo conversor de xml e utilitários do pandas
- Remova o arquivo inútil `icons.py`

### ⚙️ Miscellaneous Tasks

- Faça o commit do `CHANGELOG.md` na branch `main` na action `Release`
- Use `github.ref_name` ao gerar o título da release
- Compile executáveis com nomes diferentes para cada sistema operacional
- Adicione o parâmetro `name` no script `build` no `justfile`
- Use o argumento `--latest` ao usar o gif-cliff para gerar o `CHANGELOG.md`
- Use o `just` para executar o script de building na action `Release`
- Permita lançar releases quando tags de versão com sufixos são detectadas
- Adicione o `pillow` para converter ícones durante o building
- Atualize as dependências do projeto
- Remova o `pandas` do projeto
- Remova a dependência `pillow` do projeto
- Remova `qt-material` das dependências do projeto
- Inclua o arquivo de estilo e os ícones durante o building
- Reconfigure o devcontainer do zero

### ◀️ Revert

- "ci: permita lançar releases quando tags de versão com sufixos são detectadas"
