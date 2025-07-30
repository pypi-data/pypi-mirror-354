# 📊 `ds-python` - Estatísticas de containers em tempo real


### 📺 __Demo:__
![](assets/clip.gif)

### 📝 __Objetivo:__
Esse projeto é uma altenativa ao comando `docker stats` para o monitoramento de containers em execução, esse projeto foi inspirado na ferramenta [ds](https://github.com/rafaelrcamargo/ds)


### 💻 __Stack:__
- Python (3.10) - __runtime__
- dashing - __charts__
- rich - __loading__
- briefcase - __package builder__

### 🪛 __Instalação:__

#### Instalando o projeto:
```bash
git clone https://github.com/gpocas/ds-python
```

#### Instalando as dependencias:
```bash
cd ds-python
uv sync
```
#### Gerando o pacote:
```bash
uv run briefcase build
uv run briefcase package
```
#### Instalando o pacote (Ubuntu):
```bash
sudo apt install pacote.deb
```

