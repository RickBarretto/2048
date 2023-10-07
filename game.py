"""
==============
The 2048 Game!
==============

----------------------
(C) RickBarretto, 2023
----------------------

License:
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.


1. Instruções de uso
=================

Para rodar o jogo basta usar o seguinte comando 
com o Python 3 instalado no sistema:

.. code::

    $ py game.py

Então será necessário configurar o jogo como desejar.
Logo de cara será possível selecionar o idioma e o suporte a UTF-8.

Certifique-se que seu terminal suporta UTF-8, do contrário configure o
jogo para modo ASCII. Mas não se preocupe, é possível mudar essas configurações 
durante o jogo também.


2. Algoritmo Push 
==============

2.1 Explicando o Algoritmo Push do jogo 2048 
----------------------------------------

O nome dado ao algoritmo foi Push. Ele é dividido em duas partes,
a primeira é o algoritmo de soma, e a segunda é o algoritmo de movimentação.
Ambos retornam verdadeiro em caso de movimentação.

A ideia é que se use as funções públicas pre-identificadas por ``push``.

2.2 Explicação do algoritmo de soma
-------------------------------

A soma funciona com dois ponteiros, o primeiro chamado de :idx:
e o segundo de :cursor:.

Basicamente, :idx: é o nosso pivô, este é usado como nossa referência principal.
Nosso :idx: ignore 0s. Então, se o bloco atual for 0, ele irá para o próximo.
Obviamente, a direção poderá mudar, mas o princípio se mantêm.

Se o número atual for diferente de 0, então ele lançará um cursor na próxima
posição, e então checar.

.. note:: 
    A direção de iteração é oposta à escolhida pelo usuário,
    logo, se o usuário escolheu empurrar para a esquerda, 
    o algoritmo percorrerá da esquerda para a direita.

Caso o bloco apontado pelo :cursor: for 0, ele irá para o próximo, do contrário,
se for igual ao bloco apontado por :idx:, então ele irá somar, 
caso nenhum dos dois requisitos seja escolhido, 
ele irá avançar até o último bloco da linha ou coluna.

:idx: é capaz de andar do primeiro ao penúltimo índice da linha ou coluna,
enquanto o :cursor: é capaz de percorrer todos eles.

A soma em si funciona da seguinte forma: um bloco é dobrado 
e o outro é atribuído a 0.


.. code::
                 Tabela                              Explicação

    [   4       0       4       4   ]   <- O algoritmo começa no primeiro 
        ~                                  elemento.
       idx
    ---------------------------------

    [   4       0       4       4   ]   <- Então o :cursor: começa a caminhar,
        ~       ^                          se ele aponta para 0, então, saltará
       idx                                 para a próxima posição.
              cursor
    ---------------------------------

    [   4       0       4       4   ]   <- Se :idx: e o :cursor: apontarem para
        ~               ^                  o mesmo número, então ele dobra o
       idx                                 apontado de :idx: e zera o do :cursor:.
                      cursor
    ---------------------------------

    [   8       0       0       4   ]   <- Se o apontado por :idx: for 0, ele o
                ~                          ignora e pula para o próximo.
               idx
    ---------------------------------

    [   8       0       0       4   ]   <- O :idx: sempre para na penúltima
                        ~                  posição. Como o bloco apontado é 0,
                       idx                 o algoritmo finaliza.


2.3 Explicação do algotimo de movimentação
--------------------------------------

A movimentação também trabalha com dois ponteiros, o primeiro chamado de :idx:
e o segundo, de :cursor:.

Basicamente, :idx: é usado como nossa referência principal. Porém,
diferentemente do anterior, :idx: não irá ignorar blocos 0, mas quaisquer 
diferentes números.

Se um bloco 0 for encontrado, ele lançará o :cursor: na próxima posição,
que vai avançando até que encontre um número diferente de 0, 
e troque a posições de seus blocos apontados. 

Em suma, ele troca 0 por outro número, indo bloco por bloco.
Assim como no algoritmo anterior, ele também funciona na direção oposta
à escolhida pelo usuário.

.. code::
                  Tabela                               Explicação

    [   4       0       0       4   ]   <-  O algoritmo inicia :idx: pelo
        ~                                   primeiro elemento.
       idx                                  Se o apontado for diferente de 0,
                                            :idx: avançará.
    ---------------------------------

    [   4       0       0       4   ]   <-  Se :idx: aponta para 0, teremos nosso
                ~       ^                   :cursor: apontado para o próximo.
               idx                          Como o apontado pelo :cursor: é 0,
                      cursor                ele continuará avançando.
    ---------------------------------
    [   4       0       0       4   ]   <-  Aqui, como o apontado pelo :cursor:
                ~               ^           diferente de 0, trocamos os blocos
               idx                          do :idx: pelo do :cursor:.
                              cursor
    ---------------------------------
    [   4       4       0       0   ]   <-  Trocados!
                ~               ^
               idx
                              cursor
    ---------------------------------
    [   4       4       0       0   ]   <-  Indo para o próximo, temos a seguinte
                        ~       ^           representação ao lado.
                       idx                  Assim, finalizando o algoritmo.
                              cursor

3. Limitações
=============

Esse código é parte do meu Problem Based Learning (PBL) da universidade,
logo muita ferramenta me fora restrita para o desenvolvimento dessa aplicação.

São elas:
  - Uso de pacotes externos
  - Uso de pacotes da aplicação e mais de dois módulos
  - Uso de determinados módulos internos do Python
  - Interface gráfica
  - Banco de dados
  - Filtros e Ranking para o histórico de partidas
  - Uso de funções muitas internas do Python
  - Uso de classes, dataclasses e orientação à objetos
  - Uso de logging
  - Uso de decorators, generators, iterators, list comprehensions...
"""

import helpers


def choice_menu(
    message: str, options: list[str], banner_config: bool | None = None
) -> str:
    """Esse menu é usado para escolha do usuário de forma segura.

    O menu será impresso no centro da tela, podendo ter banner ou não.
    O usuário deverá escolher uma das opções. Caso entrada esteja errada,
    o usuário permanecerá no menu até que digite a opção correta.

    .. note::
        O menu irá resistir à saída forçada da aplicação com ``Ctrl+Z``.

    Parameters
    ----------
    message: str
        A mensagem que será impressa.

    options: list[str]
        A lista de opções da escolha.

    banner_config: bool | None
        A configuração do banner.
        Se for ``None``, então o banner não deve ser impresso.
        Case seja uma ``bool``, indicará se ele deverá ser impresso em ASCII.

    Returns
    -------
    Retorna a escolha do usuário em forma de ``str``.

    Example
    -------
    .. code::
        *----------------------------------------------*
        |                                              |
        |                                              |
        |              [      BANNER      ]            |
        |              Mensagem                        |
        |              1. Op 1                         |
        |              2. Op 2                         |
        |              >>> |                           |
        |                                              |
        |                                              |
        *----------------------------------------------*
    """

    def print_options(options: list[str]) -> None:
        for i in range(len(options)):
            print(helpers.align_start(f"[{i+1}] - {options[i]}"))

    possibilities: list[str] = []  # Possibilidades disponíveis
    banner = banner_config != None  # Se há banner

    # Adiciona todas as possibilidades disponíveis em ``possibilities``
    for i in range(len(options)):
        possibilities.append(str(i + 1))

    while True:
        # Define se irá imprimir o banner ou não
        if banner:
            # Altura total = Altura do banner + Mensagem + Opções + Input
            helpers.refresh_screen(helpers.banner()[2] + len(options) + 2)
            for line in helpers.banner(banner_config)[0]:
                print(helpers.align_start(line))
        else:
            # Altura total = Mensagem + Opções + Input
            helpers.refresh_screen(1 + len(options) + 1)

        print(helpers.align_start(message))
        print_options(options)

        # Segurança contra Ctrl+Z
        try:
            choice: str = input(helpers.align_start(">>> "))
        except EOFError:
            choice = ""

        if choice in possibilities:
            return choice


def welcome_menu() -> tuple[int, bool]:
    """Abre o menu de abertura do jogo.

    O usuário deverá selecionar a linguagem do jogo
    e se seu sistema suporta UTF-8 ou ASCII.

    Returns
    -------
    tuple[int, bool]
        0: a linguagem escolhida (1 para Inglês e 2 para Português).
        1: ``True`` caso o sistema só suporte ASCII.
    """
    helpers.refresh_screen(1)
    print(helpers.align_middle("Welcome to 2048 game!"))

    lang: str = choice_menu("Please, choose your language.", ["English", "Portugues"])

    ascii: str = choice_menu(
        "Does your system support UTF-8?", ["Yes", "No, just ASCII"]
    )

    return int(lang), ascii in "2"


def main_menu(lang: int, ascii: bool) -> tuple[list[tuple[str, int, int]], int, bool]:
    """Menu principal do jogo.

    Opções disponíveis ao usuário:
        1. Iniciar novo jogo
        2. Mostrar histórico de partidas
        3. Trocar entre modo ASCII e UTF-8
        4. Trocar entre Inglês e Português
        5. Sair do jogo e mostrar o histórico.

    .. note::
        A Interface é usada com base no :choice_menu:.

    Parameters
    ----------
    lang: int
        A linguagem do jogo. 1 para Inglês e 2 para Português.
    ascii: bool
        Se o jogo está em modo ASCII.

    Returns
    -------
    tuple[list[tuple[str, int, int]], bool, int]
        0: O histórico do jogo:
            0: nickname do jogador
            1: score da partida
            2: movimentos da partida
        1: Se está em modo ASCII
        2: A linguagem atual.
    """

    def get_options(config: tuple[int, bool]) -> list[str]:
        """Retorna as opções de acordo com a :config: atual."""
        match config:
            case (2, False):
                return [
                    "Novo Jogo",
                    "Historico",
                    "ASCII/UTF-8",
                    "Ingles/Portugues",
                    "Sair",
                ]
            case (2, True):
                return [
                    "Novo Jogo",
                    "Histórico",
                    "ASCII/UTF-8",
                    "Inglês/Português",
                    "Sair",
                ]
            case _:
                return [
                    "New Game",
                    "History",
                    "ASCII/UTF-8",
                    "English/Portuguese",
                    "Exit",
                ]

    def get_nickname(lang: int) -> str:
        """Um menu para capturar o nickname do jogador."""
        if 1 == lang:
            msg = "Type your nickname."
        else:
            msg = "Digite seu nickname."

        while True:
            # Altura total = Mensagem + Input
            helpers.refresh_screen(2)
            print(helpers.align_start(msg))

            # Segurança contra Ctrl+Z
            try:
                nick: str = input(helpers.align_start(">>> "))
                # O nickname não pode ser vazio.
                if nick:
                    return nick
            except EOFError:
                pass

    records: list[tuple[str, int, int]] = []  # Histórico de partidas

    while True:
        match choice_menu("", get_options((lang, ascii)), banner_config=ascii):
            # Nova partida
            case "1":
                repeat: bool = True
                while repeat:
                    results = game_match(lang, ascii, get_nickname(lang))
                    records.append((results[0], results[1], results[2]))
                    repeat = results[3]

            # Menu de histórico
            case "2":
                records_menu((lang, ascii), records)

            # Toggle ASCII/UTF-8
            case "3":
                ascii = not ascii

            # Toggle Inglês/Português
            case "4":
                if 1 == lang:
                    lang = 2
                else:
                    lang = 1

            # Sair
            case "5":
                return records, lang, ascii


def records_menu(config: tuple[int, bool], records: list[tuple[str, int, int]]) -> None:
    """Menu de histórico do jogo.

    .. note::
        A interface gráfica está de acordo com :helpers.print_records:.
    """
    while True:
        helpers.print_records(records, config=config)

        match config:
            case (2, True):
                msg = "Aperte qualquer botao para sair."
            case (2, False):
                msg = "Aperte qualquer botão para sair."
            case _:
                msg = "Press anything to exit."

        # Segurança contra Ctrl+Z
        try:
            input(helpers.align_start(msg))
            return
        except EOFError:
            pass


def game_match(lang, ascii, player) -> tuple[str, int, int, bool]:
    """O menu de partida do jogo.

    1. O jogo inicia com uma tabela 4x4, preenchida por um par de números,
    podendo estes serem 2 ou 4.
    2. O jogo entra em um Loop, onde o usuário poderá empurrar os blocos,
        sair ou reiniciar.

    .. note::
        A interface gráfica está de acordo com :helpers.print_table:.
    """
    CONFIG: tuple[int, bool] = (lang, ascii)

    table: list[list[int]] = helpers.new_table()  # Tabuleiro da partida
    score: int = 0  # Pontuação da partida
    moves: int = 0  # Movimentos da partida

    # Insere dois blocos iniciais no :table:
    for _ in range(2):
        helpers.insert_block(table)

    while True:
        status: tuple[str, int, int] = (player, score, moves)

        helpers.print_table(table, status, CONFIG)

        match direction := safe_input_choice():
            # Reiniciar
            case "R":
                return player, score, moves, True
            # Sair
            case "Q":
                return player, score, moves, False
            # Movimentação
            case "W" | "A" | "S" | "D":
                # Realiza a movimentação
                turn_score, turn_moves = helpers.push_blocks(table, direction)

                # Atualiza o status da partida.
                score += turn_score
                moves += turn_moves
                status = (player, score, moves)

                if helpers.has_won(table):
                    return end_of_match(table, status, CONFIG, has_won=True)
                elif not helpers.can_move(table):
                    return end_of_match(table, status, CONFIG)

                if turn_moves or turn_score:
                    helpers.insert_block(table)


def end_of_match(
    table: list[list[int]],
    status: tuple[str, int, int],
    config: tuple[int, bool],
    has_won: bool = False,
) -> tuple[str, int, int, bool]:
    """Finaliza a partida de acordo com o :has_won:

    Será mostrado uma mensagem e
    opções para sair ou reiniciar a partida.
    """
    player, score, moves = status
    while True:
        if has_won:
            helpers.print_win(table, status, config)
        else:
            helpers.print_lose(table, status, config)
        match safe_input_choice():
            case "R":
                return player, score, moves, True
            case "Q":
                return player, score, moves, False
            case _:
                pass


def safe_input_choice() -> str:
    """Retorna o input do usuário em maiúsculo e de forma segura.

    .. note:: Possui mecanismos de defesa contra encerramento forçado.
    """
    # Segurança contra ``Ctrl+Z``
    try:
        inp: str = input(helpers.align_start(">>> ")).upper()
        return inp
    except EOFError:
        return ""


if __name__ == "__main__":
    lang, ascii = welcome_menu()
    records, lang, ascii = main_menu(lang, ascii)
    records_menu((lang, ascii), records)