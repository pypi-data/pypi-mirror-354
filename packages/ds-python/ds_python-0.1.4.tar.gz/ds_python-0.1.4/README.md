# 📊 `ds-python` - Estatísticas de containers em tempo real


### 📺 __Demo:__
![](assets/clip.gif)

### 📝 __Objetivo:__
Esse projeto é uma altenativa ao comando `docker stats` para o monitoramento de containers em execução, esse projeto foi inspirado na ferramenta [ds](https://github.com/rafaelrcamargo/ds)


### 💻 __Stack:__
- Python (3.12) - __runtime__
- dashing - __charts__
- rich - __loading__
- briefcase - __package builder__

### 🪛 __Instalação:__
Existem duas maneiras de instalação, nativa ou virtual

usando o __pipx__
```bash
pipx install ds-python
```

usando o __uv__
```bash
uv tool install ds-python
```

usando o __uvx__
```bash
uvx tool install ds-python
```


todos os exemplos acima envolvem a virtualização do projeto,
caso queira se aventurar em uma instalação nativa siga os passos abaixo:
#### 1. Clonando o projeto
```bash
git clone https://github.com/gpocas/ds-python
```

#### 2. Instalando as dependencias:
```bash
cd ds-python
uv sync
```

#### 3. Gerando o pacote:
```bash
uv run briefcase build
uv run briefcase package
```

#### 4. Instalando o pacote (Ubuntu):
```bash
sudo apt install pacote.deb
```

