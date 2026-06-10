# Projeto 3 - Ilha do Mestre Kame (Versão Low Cost :D)

#### Felipe Azambuja - 14675437
#### Luiz Fellipe Catuzzi Araujo Hotoshi - 11871198

## Descrição

Nós tentamos fazer uma ilha e uma casa que remetessem a sensação de tranquilidade com que o Mestre Kame (DB) vivia.

Claro, dadas as limitações do projeto e a baixa diversidade de modelos gratuitos com textura disponíveis para essa construção, fizemos mudanças cabíveis, mas mantivemos a essência. No lugar das revistas que o Kame costumava ler, adicionamos outra forma de entretenimento, um notebook com segundo monitor e uma cadeira ergonomica para garantir a gameplay. Porém, assim como no anime, o maior lazer é ficar em uma cadeira de praia do lado de fora, aproveitando a vista para o mar sob a sombra de um guarda sol (e uma garrafinha de água, para ficar hidratado).

Adicionamos também muitos outros objetos. O objetivo não era fazer o mínimo entregavel, mas sim construir um ambiente coerente e que fosse interessante de explorar.

O Projeto 3 adiciona iluminação Phong completa: 3 fontes de luz com separação indoor/outdoor, normais por face, parâmetros de material por objeto e controles interativos de iluminação.


## DEMO


https://github.com/user-attachments/assets/f83ce9dd-c1e8-41dd-8cf0-2c775e32d436



## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Também é possível executar o projeto pelo notebook:

```text
main.ipynb
```

## Controles

### Câmera e cena
- `WASD` e mouse: mover a câmera.
- `Shift + WASD`: mover a câmera mais rápido.
- `Shift + qualquer comando de alteração nos objetos`: acelerar o movimento.
- `Setas`: mover a cadeira de praia (a luz externa segue junto).
- `Q` e `E`: girar a cadeira interna.
- `Z` e `X`: mudar o tamanho do guarda-sol.
- `Scroll`: mudar o zoom.
- `P`: alternar malha (wireframe).
- `ESC`: sair.

### Iluminação (Projeto 3)
- `1`: ligar/desligar luz ambiente global.
- `2`: ligar/desligar luz externa (segue a cadeira de praia).
- `3`: ligar/desligar abajur (luz interna quente).
- `4`: ligar/desligar luz de teto (luz interna fria).
- `J` / `K`: diminuir / aumentar intensidade da luz ambiente.
- `N` / `M`: diminuir / aumentar multiplicador difuso.
- `U` / `I`: diminuir / aumentar multiplicador especular.
- `Shift + J/K/N/M/U/I`: ajuste 3× mais rápido.

## Arquivos

```text
main.py                  código principal
main.ipynb               versão em notebook
vertex_shader.vs         shader de vértices (Phong — posição + normal)
fragment_shader.fs       shader de fragmentos (Phong — 3 luzes, zonas, emissivo)
requirements.txt         dependências
assets/                  modelos e texturas usados
```

## Iluminação

| Luz | Zona    | Cor               | Posição                              |
|-----|---------|-------------------|--------------------------------------|
| 2   | Externa | amarelo-laranja   | acima da cadeira de praia (segue ela) |
| 3   | Interna | laranja-quente    | acima do abajur                      |
| 4   | Interna | branco-azulado    | centro do teto                       |

A separação indoor/outdoor garante que luzes internas não afetam objetos externos e vice-versa.

## Modelos da cena

Modelos internos: cama, tapete, escrivaninha, abajur, laptop, travesseiros, PC, cadeira ergonomica, cabide e chapeu.

Modelos externos: guarda-sol, mesa redonda, cadeira de praia, garrafa, poco e barco.

O quarto separa o ambiente interno do ambiente externo.

As telhas ficam no teto como detalhe externo, mas não entram na contagem mínima porque esse modelo não veio com textura de imagem.
