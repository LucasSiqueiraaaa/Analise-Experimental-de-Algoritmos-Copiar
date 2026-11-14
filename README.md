## 1. O que instalar

- Python 3.10 ou mais recente.
- Visual Studio Code.
- Extensão **Python**, publicada pela Microsoft, instalada no VS Code.

## 2. Abrir o projeto

1. Extraia o arquivo ZIP.
2. Abra o VS Code.
3. Clique em **Arquivo > Abrir Pasta**.
4. Selecione a pasta `versao_python`, que contém o arquivo `main.py`.
5. Se solicitado, escolha o interpretador Python instalado.

## 3. Instalar a biblioteca de gráficos

No VS Code, abra **Terminal > Novo Terminal** e execute:

```bash
python -m pip install -r requirements.txt
```

Se estiver no Windows e `python` não funcionar, tente:

```bash
py -m pip install -r requirements.txt
```

Faça isso uma única vez no ambiente Python escolhido.

## 4. Executar pelo VS Code

1. Abra o arquivo `main.py`.
2. Na lateral, abra **Executar e Depurar**.
3. Selecione **Executar projeto de algoritmos**.
4. Pressione `F5` para executar ou `Ctrl + F5` para executar sem depuração.

Também é possível abrir `main.py` e clicar em **Run Python File** no canto superior direito.

O menu aparecerá no terminal integrado do VS Code. Digite o número da opção e pressione Enter.

## 5. Opções do programa

- `1`: realiza os testes rápidos e cria os gráficos.
- `2`: realiza os testes com mais repetições e cria os gráficos.
- `3`: prepara as bases de dados.
- `4`: cria os gráficos a partir dos resultados existentes.
- `5`: mostra o resumo dos resultados.
- `0`: encerra o programa.

## 6. Arquivos gerados

- `dados/`: bases utilizadas nos experimentos.
- `resultados/`: tabelas CSV, resumo e informações do computador.
- `graficos/`: imagens PNG criadas pelo programa.

