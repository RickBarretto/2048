"""
==========================
Funções auxiliares do jogo
==========================

----------------------
(C) RickBarretto, 2023
----------------------

License:
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at https://mozilla.org/MPL/2.0/.

1. Funções Principais
=====================

1.1 Funções referentes ao algoritmos do jogo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:new_table:
    Cria uma nova table 4x4.

:can_move:
    Retorna se o movimento é possível ou não.

:has_won:
    Retorna se o jogador venceu ou não.

:insert_block:
    Insere um bloco aleatório em uma posição permitida.

:push_blocks:
    O algoritmo de movimentação do tabuleiro.

1.2 Funções referentes à interface do usuário
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:print_records:
    Imprime o histórico de partidas.

:print_table:
    Imprime a tabela da partida e suas instruções de jogadas.

:print_lose:
    Imprime uma mensagem de derrota do jogador.

:print_win:
    Imprime uma mensagem de triunfo do jogador.

1.2.1 Funções referentes ao alinhamento da interface de usuário
---------------------------------------------------------------

:align_start:
    Alinha o conteúdo à esquerda do banner principal.

:align_middle:
    Alinha o conteúdo ao meio do banner principal.

:refresh_screen:
    Atualiza a tela, alinhando os conteúdos verticalmente.

:terminal_size:
    Captura o tamanho atual do terminal.

1.3 Funções Extras
~~~~~~~~~~~~~~~~~~

:banner:
    Referente ao banner principal da aplicação.

"""


import os
import random as rand

# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  Lógica do jogo
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~


def new_table() -> list[list[int]]:
    """Cria e retorna uma tabela 4x4 preenchida por 0s.

    Returns
    -------
    list[list[int]]
        Uma tabela 4x4 preenchida por 0s.

    Examples
    --------
    >>> new_table()
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    """
    return [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


def insert_block(table: list[list[int]]) -> None:
    """Insere blocos 2 ou 4 na :table:.

    Parameters
    ----------
    table: list[list[int]]
        A tabela 4x4 do jogo.

        .. note:: A tabela é passada por referência.

    Examples
    --------
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [0, 2, 2, 0], [2, 0, 2, 0]]
    >>> available_spaces_then = len(_get_empty_indexes(table))
    >>> insert_block(table)
    >>> available_spaces_now  = len(_get_empty_indexes(table))
    >>> available_spaces_then - available_spaces_now
    1
    """
    indexes: list[tuple[int, int]] = _get_empty_indexes(table)
    if indexes:
        row, col = rand.choice(indexes)
        table[row][col] = rand.choice([2, 4])


def can_move(table: list[list[int]]) -> bool:
    """Checa a possibilidade de movimentação.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo.

    Returns
    -------
    bool
        Se ainda existe movimento possível.
    """

    def can_move_horizontally(table: list[list[int]]) -> bool:
        for row in range(4):
            for col in range(3):
                if table[row][col] == table[row][col + 1]:
                    return True
        return False

    def can_move_vertically(table: list[list[int]]) -> bool:
        for col in range(4):
            for row in range(3):
                if table[row][col] == table[row + 1][col]:
                    return True
        return False

    if _get_empty_indexes(table):
        return True

    return can_move_horizontally(table) or can_move_vertically(table)


def has_won(table: list[list[int]]) -> bool:
    """Retorna se o jogador venceu.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo.

    Returns
    -------
    bool
        Se há o bloco ``2048``.
    """
    for row in table:
        for block in row:
            if block == 2048:
                return True
    return False


def push_blocks(table: list[list[int]], direction: str) -> tuple[int, int]:
    """Realiza a soma e movimentação da tabela para a esquerda.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo em si.

        .. note:: A tabela é passada por referência.

    direction: str
        :direction: determina a direção que os blocos serão aglutinados.
        Os parâmetros podem ser "W", "A", "S" ou "D".

    Returns
    -------
    tuple[int, bool]
        Retorna uma dupla de dois inteiros:
        0: score total da movimentação
        1: se o movimento existiu

    Examples
    --------
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [2, 2, 2, 2], [0, 2, 2, 2]]
    >>> push_blocks(table, "A")
    (20, True)
    >>> table
    [[4, 4, 0, 0], [4, 2, 0, 0], [4, 4, 0, 0], [4, 2, 0, 0]]
    >>> push_blocks(table, "D")
    (16, True)
    >>> table
    [[0, 0, 0, 8], [0, 0, 4, 2], [0, 0, 0, 8], [0, 0, 4, 2]]
    >>> push_blocks(table, "W")
    (8, True)
    >>> table
    [[0, 0, 8, 8], [0, 0, 0, 2], [0, 0, 0, 8], [0, 0, 0, 2]]
    >>> table[2][2] = 8
    >>> table
    [[0, 0, 8, 8], [0, 0, 0, 2], [0, 0, 8, 8], [0, 0, 0, 2]]
    >>> push_blocks(table, "S")
    (16, True)
    >>> table
    [[0, 0, 0, 8], [0, 0, 0, 2], [0, 0, 0, 8], [0, 0, 16, 2]]
    """
    assert direction in ("W", "A", "S", "D")

    match direction:
        case "A":
            return (_horizontal_sum(table, "a"), _horizontal_move(table, "a"))
        case "D":
            return (_horizontal_sum(table, "d"), _horizontal_move(table, "d"))
        case "W":
            return (_vertical_sum(table, "w"), _vertical_move(table, "w"))
        case "S":
            return (_vertical_sum(table, "s"), _vertical_move(table, "s"))
        case _:
            return 0, 0


# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  Interface do Usuário
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~


def print_records(
    records: list[tuple[str, int, int]], config: tuple[int, bool]
) -> None:
    """Imprime o histórico do usuário.

    .. note::
        As partidas mais antigas ficam mais ao topo.

    Parameters
    ----------
    records: list[tuple[str, int, int]]
        O histórico de partidas.
    config: tuple[int, bool]
        A configuração do jogo.

    Examples
    --------
    .. code::
        *----------------------------------------------*
        |           [        BANNER        ]           |
        |           [Player | Score | Moves]           |
        |           [Rick   | 42    |  10  ]           |
        |           [RickB  | 2048  |  42  ]           |
        |           [Anon   | 10    |  5   ]           |
        |                                              |
        |           Press something...                 |
        |                                              |
        |                                              |
        *----------------------------------------------*
    """

    def get_columns(config: tuple[int, bool]) -> list[str]:
        """Retorna os cabeçalhos das colunas."""
        match config:
            case (2, True):
                return ["Jogador", "Pontuacao", "Movimentos"]
            case (2, False):
                return ["Jogador", "Pontuação", "Movimentos"]
            case _:
                return ["Player", "Score", "Moves"]

    def get_formatation(config: tuple[int, bool]) -> tuple[str, str, str, str]:
        """Retorna uma série de strings usadas para imprimir a tabela.
        Parameters
        ----------
        Returns
        -------
        tuple[str]
            A lista contém 4 elementos:
            0. delimitador do topo da tabela.
            1. template a ser preenchido.
            2. divisor do meio de tabela.
            3. delimitador do final da tabela.
        """
        _, ascii = config
        if ascii:
            return (
                f"+{'-'*48}+{'-'*10}+{'-'*10}+",
                "|{0:<48}|{1:^10}|{2:^10}|",
                f"+{'-'*48}+{'-'*10}+{'-'*10}+",
                f"+{'-'*48}+{'-'*10}+{'-'*10}+",
            )
        else:
            return (
                f"╭{'─'*48}┬{'─'*10}┬{'─'*10}╮",
                "│{0:<48}│{1:^10}│{2:^10}│",
                f"├{'─'*48}┼{'─'*10}┼{'─'*10}┤",
                f"╰{'─'*48}┴{'─'*10}┴{'─'*10}╯",
            )

    top, template, middle, end = get_formatation(config)
    col1, col2, col3 = get_columns(config)

    __clear_screen()

    # Imprime o banner
    banner_content, _, _ = banner(config[1])
    for line in banner_content:
        print(align_start(line))

    # Imprime a tabela
    print(align_start(top))
    print(align_start(template.format(col1, col2, col3)))
    print(align_start(middle))
    for player, score, moves in records:
        print(align_start(template.format(player, score, moves)))
    print(align_start(end))
    print()


def print_table(
    table: list[list[int]], status: tuple[str, int, int], config: tuple[int, bool]
) -> None:
    """Imprime a partida atual.

    A tabela é centralizada, logo à direita, estão as informaões da partida,
    e logo abaixo as instruções ao usuário.

    Parameters
    ----------
    table: list[list[int]]
        A tabela da partida.
    status: tuple[str, int, int]
        O status do jogo: (player, score, movements)
    config: tuple[int, bool]
        A configuração do jogo: (language, ascii-mode)

    Examples
    --------
    .. code::
        *----------------------------------------------*
        |           [        BANNER        ]           |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  TABELA|  ]  ~INFO~            |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  |  |  |  ]                    |
        |                                              |
        |           Instructions                       |
        |           >>>                                |
        |                                              |
        *----------------------------------------------*
    """

    def table_template(ascii: bool) -> list[str]:
        """Retorna uma série de strings para a impressão da tabela."""
        if ascii:
            row = "|{0: ^4}|{1: ^4}|{2: ^4}|{3: ^4}|"
            div = "+----+----+----+----+"
            return [div, row, div, row, div, row, div, row, div]
        else:
            row = "│{0: ^4}│{1: ^4}│{2: ^4}│{3: ^4}│"
            div = "├────┼────┼────┼────┤"
            return [
                "╭────┬────┬────┬────╮",
                row,
                div,
                row,
                div,
                row,
                div,
                row,
                "╰────┴────┴────┴────╯",
            ]

    _, ascii = config
    player, score, moves = status

    template: list[str] = table_template(ascii)
    banner_content, _, banner_height = banner(ascii)

    # Altura total = Altura do Banner + Altura da Tabela + Instruções + Input
    refresh_screen(menu_height=banner_height + 9 + 3)

    # Imprime o banner
    for line in banner_content:
        print(align_start(line))

    # Imprime a tabela
    print(align_middle(f"{template[0]} \tplayer:"))
    print(align_middle(f"{_format_row(template[1], table[0])} \t {player}"))
    print(align_middle(f"{template[2]}"))
    print(align_middle(f"{_format_row(template[3], table[1])} \tscore:"))
    print(align_middle(f"{template[4]} \t {score}"))
    print(align_middle(f"{_format_row(template[5], table[2])}"))
    print(align_middle(f"{template[6]} \tmoves:"))
    print(align_middle(f"{_format_row(template[7], table[3])} \t {moves}"))
    print(align_middle(f"{template[8]}"))

    # Imprime as instruções
    for inst in _get_instructions(config):
        print(align_start(inst))


def print_win(
    table: list[list[int]], status: tuple[str, int, int], config: tuple[int, bool]
) -> None:
    """Imprime a tabela do triunfo.

    Parameters
    ----------
    table: list[list[int]]
        A tabela da partida.
    status: tuple[str, int, int]
        O status do jogo: (player, score, movements)
    config: tuple[int, bool]
        A configuração do jogo: (language, ascii-mode)

    Examples
    --------
    .. code::
        *----------------------------------------------*
        |           [        BANNER        ]           |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  TRIUNFO! ]  ~INFO~            |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  |  |  |  ]                    |
        |                                              |
        |           Instructions                       |
        |           >>>                                |
        |                                              |
        *----------------------------------------------*
    """
    match config:
        case (2, True):
            msg = "Voce venceu!"
        case (2, False):
            msg = "Você venceu!"
        case _:
            msg = "You won!"

    __print_msg(msg, table, status, config)


def print_lose(
    table: list[list[int]], status: tuple[str, int, int], config: tuple[int, bool]
) -> None:
    """Imprime a tabela da derrota.

    Parameters
    ----------
    table: list[list[int]]
        A tabela da partida.
    status: tuple[str, int, int]
        O status do jogo: (player, score, movements)
    config: tuple[int, bool]
        A configuração do jogo: (language, ascii-mode)

    Examples
    --------
    .. code::
        *----------------------------------------------*
        |           [        BANNER        ]           |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  DERROTA! ]  ~INFO~            |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  |  |  |  ]                    |
        |                                              |
        |           Instructions                       |
        |           >>>                                |
        |                                              |
        *----------------------------------------------*
    """
    match config:
        case (2, True):
            msg = "Voce perdeu!"
        case (2, False):
            msg = "Você perdeu!"
        case _:
            msg = "You lost!"

    __print_msg(msg, table, status, config)


def __print_msg(
    message: str,
    table: list[list[int]],
    status: tuple[str, int, int],
    config: tuple[int, bool],
) -> None:
    """Imprime a tabela com uma mensagem

    Parameters
    ----------
    table: list[list[int]]
        A tabela da partida.
    status: tuple[str, int, int]
        O status do jogo: (player, score, movements)
    config: tuple[int, bool]
        A configuração do jogo: (language, ascii-mode)

    Examples
    --------
    .. code::
        *----------------------------------------------*
        |           [        BANNER        ]           |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  Mensagem ]  ~INFO~            |
        |             [  |  |  |  ]  ~~~~~~            |
        |             [  |  |  |  ]                    |
        |                                              |
        |           Instructions                       |
        |           >>>                                |
        |                                              |
        *----------------------------------------------*
    """

    def table_template(ascii: bool) -> list[str]:
        """Retorna o template da tabela de acordo com :ascii:."""
        if ascii:
            row = "|{0: ^4}|{1: ^4}|{2: ^4}|{3: ^4}|"
            div = "+----+----+----+----+"
            return [
                div,
                row,
                div,
                "| +--+----+----+--+ |",
                "+-+{0:^15}+-+",
                "| +--+----+----+--+ |",
                div,
                row,
                div,
            ]
        else:
            row = "│{0: ^4}│{1: ^4}│{2: ^4}│{3: ^4}│"
            div = "├────┼────┼────┼────┤"

            return [
                "╭────┬────┬────┬────╮",
                row,
                div,
                "│ ╭──┴────┴────┴──╮ │",
                "├─┤{0:^15}├─┤",
                "│ ╰──┬────┬────┬──╯ │",
                div,
                row,
                "╰────┴────┴────┴────╯",
            ]

    player, score, moves = status
    _, ascii = config

    template: list[str] = table_template(ascii)
    banner_content, _, banner_height = banner(ascii)

    # Altura Total = Altura do Banner + Altura da Tabela + Instrução + Input
    refresh_screen(banner_height + 9 + 2)

    # Imprime o banner
    for line in banner_content:
        print(align_start(line))

    # Imprime o tabuleiro
    print(align_middle(f"{template[0]} \tplayer:"))
    print(align_middle(f"{_format_row(template[1], table[0])} \t {player}"))
    print(align_middle(f"{template[2]}"))
    print(align_middle(f"{template[3]} \tscore:"))
    print(align_middle(f"{template[4].format(message)} \t {score}"))
    print(align_middle(f"{template[5]}"))
    print(align_middle(f"{template[6]} \tmoves:"))
    print(align_middle(f"{_format_row(template[7], table[3])} \t {moves}"))
    print(align_middle(f"{template[8]}"))

    # Imprime a instrução do jogo
    print(align_start(_get_instructions(config)[0]))


def terminal_size() -> tuple[int, int]:
    """Retorna o tamanho atual do terminal.

    Results
    -------
    tuple[int, int]
        0: colunas
        1: linhas
    """
    SIZE = os.get_terminal_size()
    return SIZE.columns, SIZE.lines


def align_middle(text: str) -> str:
    """Alinha texto no meio do banner principal.

    Parameters
    ----------
    text: str
        O conteúdo em texto.

    Results
    -------
    str
        O texto centralizado ao meio do banner, de referência.
    """
    WIDTH, _ = terminal_size()
    _, BANNER_WIDTH, _ = banner()
    return f"{' '*((WIDTH - BANNER_WIDTH)//2 + BANNER_WIDTH // 4)}{text}"


def align_start(text: str) -> str:
    """Alinha texto ao início do banner principal.

    Parameters
    ----------
    text: str
        O conteúdo em texto.

    Results
    -------
    str
        O texto alinhado à esquerda do banner.
    """
    WIDTH, _ = terminal_size()
    _, BANNER_WIDTH, _ = banner()
    return f"{' '*((WIDTH - BANNER_WIDTH)//2)}{text}"


def refresh_screen(menu_height: int) -> None:
    """Limpa a tela e configura o alinhamento vertical.

    Parameters
    ----------
    menu_height: int
        A altura atual do menu.
    """
    __clear_screen()
    _vertical_align(menu_height)


def banner(ascii: bool = False) -> tuple[list[str], int, int]:
    """Retorna o banner do jogo.

    O banner está disponível em ASCII e UTF-8.

    .. note::
        O banner UTF-8 deriva da ferramenta `ManyTools`_, podendo ser usado
        em projetos não-comerciais.

    .. _ManyTools: https://manytools.org/hacker-tools/ascii-banner/

    Parameters
    ----------
    ascii: bool = False
        Define se o banner deverá ser em formato ASCII ou UTF-8.

    Results
    -------
    tuple[list[str], int, int]
        0: O conteúdo do banner, linha a linha.
        1: O tamanho horizontal do banner.
        2: O tamanho vertical do banner.
    """
    banner = []
    if ascii:
        banner: list[str] = [
            "######\\  ######\\ ##\\  ##\\ #####\\      ######\\  #####\\ ###\\   ###\\#######\\",
            "\\____##\\##/_####\\##|  ##|##/__##\\    ##/____/ ##/__##\\####\\ ####|##/____/",
            "#####//##|##/##|#######|\\#####//    ##|  ###\\\\#######|##/####/##|#####\\  ",
            "##/___/ ####//##|\\____##|##/__##\\    ##|   ##|##/__##|##|\\##//##|##/__/  ",
            "#######\\\\######//     ##|\\#####//    \\######//##|  ##|##| \\_/ ##|#######\\",
            "\\______/ \\_____/      \\_/ \\____/      \\_____/ \\_/  \\_/\\_/     \\_/\\______/",
        ]
    else:
        banner = [
            "██████╗  ██████╗ ██╗  ██╗ █████╗      ██████╗  █████╗ ███╗   ███╗███████╗",
            "╚════██╗██╔═████╗██║  ██║██╔══██╗    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝",
            " █████╔╝██║██╔██║███████║╚█████╔╝    ██║  ███╗███████║██╔████╔██║█████╗  ",
            "██╔═══╝ ████╔╝██║╚════██║██╔══██╗    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ",
            "███████╗╚██████╔╝     ██║╚█████╔╝    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗",
            "╚══════╝ ╚═════╝      ╚═╝ ╚════╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝",
        ]
    return banner, len(banner[0]), len(banner)


# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  Funções Auxiliares
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~

# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  Lógica do jogo
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~


def _get_empty_indexes(table: list[list[int]]) -> list[tuple[int, int]]:
    """Retorna os índices de blocos contendo 0.

    Parameters
    ----------
    table: list[list[int]]
        A tabela 4x4 do jogo.

    Returns
    -------
    list[tuple[int, int]]
        Uma lista de índices, onde cada elemento é uma tupla de
        dois valores inteiros, representando linha e coluna, respectivamente.

    Examples
    --------
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [0, 2, 2, 0], [2, 0, 2, 0]]
    >>> _get_empty_indexes(table)
    [(0, 3), (1, 3), (2, 0), (2, 3), (3, 1), (3, 3)]
    """
    indexes: list[tuple[int, int]] = []

    for row_idx in range(4):
        for col_idx in range(4):
            if table[row_idx][col_idx] == 0:
                indexes.append((row_idx, col_idx))

    return indexes


def _horizontal_sum(table: list[list[int]], direction: str) -> int:
    """Algoritmo de soma do :push_table: para a somas horizontais.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo em si.

        .. note::
            A tabela é passada por referência.

    row: int
        A linha a ser afetada.

    direction: str
        Define a direção que o algoritmo deve somar.

        .. warning::
            Os parâmetros devem ser ``1`` para a direita ou
            ``-1`` para a esquerda.

    Returns
    -------
    int
        Retorna o total da soma da linha.

    Examples
    --------
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [2, 2, 2, 2], [0, 2, 2, 2]]
    >>> _horizontal_sum(table, "a")
    20
    >>> table
    [[4, 4, 0, 0], [4, 0, 2, 0], [4, 0, 4, 0], [0, 4, 0, 2]]
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [2, 2, 2, 2], [0, 2, 2, 2]]
    >>> _horizontal_sum(table, "d")
    20
    >>> table
    [[4, 0, 4, 0], [2, 0, 4, 0], [0, 4, 0, 4], [0, 2, 0, 4]]
    """
    assert direction in ("a", "d")

    sum = 0

    if direction == "a":
        idx_start, idx_end, iteration_factor = (0, 3, 1)
    else:
        idx_start, idx_end, iteration_factor = (3, 0, -1)

    for row in range(4):
        for idx in range(idx_start, idx_end, iteration_factor):
            last: int = table[row][idx]  # armazena o bloco mais recente

            # enquanto o :idx: permanece em um bloco fixo,
            # o :cursor: irá comear do próximo até o final.
            # O plano é somá-los, caso possível.
            for cursor in range(
                idx + iteration_factor, idx_end + iteration_factor, iteration_factor
            ):
                current: int = table[row][cursor]  # armazena o bloco atual.

                if current == 0:
                    pass
                elif current == last:
                    table[row][idx] *= 2
                    table[row][cursor] = 0
                    sum += table[row][idx]
                    break
                else:
                    break

    return sum


def _vertical_sum(table: list[list[int]], direction: str) -> int:
    """Algoritmo de soma do :push_table: para a somas verticais.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo em si.

        .. note::
            A tabela é passada por referência.

    col: int
        A coluna a ser afetada.

    direction: str
        Define a direção que o algoritmo deve somar.

        .. warning::
            Os parâmetros devem ser ``1`` para a cima ou
            ``-1`` para a baixo.

    Returns
    -------
    int
        Retorna o total da soma da linha.

    Examples
    --------
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [2, 2, 2, 2], [0, 2, 2, 2]]
    >>> _vertical_sum(table, "w")
    24
    >>> table
    [[4, 4, 4, 0], [4, 0, 0, 0], [0, 4, 4, 4], [0, 0, 0, 0]]
    >>> table = [[4, 2, 2, 0], [2, 2, 2, 0], [2, 2, 2, 2], [0, 2, 2, 2]]
    >>> _vertical_sum(table, "s")
    24
    >>> table
    [[4, 0, 0, 0], [0, 4, 4, 0], [4, 0, 0, 0], [0, 4, 4, 4]]
    """
    assert direction in ("w", "s")

    sum = 0

    if direction == "w":
        idx_start, idx_end, iteration_factor = (0, 3, 1)
    else:
        idx_start, idx_end, iteration_factor = (3, 0, -1)

    for col in range(4):
        for idx in range(idx_start, idx_end, iteration_factor):
            last: int = table[idx][col]  # armazena o bloco mais recente

            # enquanto o :idx: permanece em um bloco fixo,
            # o :cursor: irá comear do próximo até o final.
            # O plano é somá-los, caso possível.
            for cursor in range(
                idx + iteration_factor, idx_end + iteration_factor, iteration_factor
            ):
                current: int = table[cursor][col]  # armazena o bloco atual.

                if current == 0:
                    pass
                elif current == last:
                    table[idx][col] *= 2
                    table[cursor][col] = 0
                    sum += table[idx][col]
                    break
                else:
                    break

    return sum


def _horizontal_move(table: list[list[int]], direction: str) -> bool:
    """Algoritmo de movimento do :push_table: para a movimentos horizontais.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo em si.

        .. note::
            A tabela é passada por referência.

    row: int
        A linha a ser afetada.

    direction: str
        Define a direção que o algoritmo deve somar.

        .. warning::
            Os parâmetros devem ser ``1`` para a direita ou
            ``-1`` para a esquerda.

    Returns
    -------
    bool
        Retorna se houve movimento efetuado.

    Examples
    --------
    >>> table = [[4, 4, 0, 0], [4, 0, 2, 0], [4, 0, 4, 0], [0, 4, 0, 2]]
    >>> _horizontal_move(table, "a")
    True
    >>> table
    [[4, 4, 0, 0], [4, 2, 0, 0], [4, 4, 0, 0], [4, 2, 0, 0]]
    >>> table = [[4, 0, 4, 0], [2, 0, 4, 0], [0, 4, 0, 4], [0, 2, 0, 4]]
    >>> _horizontal_move(table, "d")
    True
    >>> table
    [[0, 0, 4, 4], [0, 0, 2, 4], [0, 0, 4, 4], [0, 0, 2, 4]]
    """
    assert direction in ("a", "d")

    movement = False

    if direction == "a":
        idx_start, idx_end, iteration_factor = (0, 3, 1)
    else:
        idx_start, idx_end, iteration_factor = (3, 0, -1)

    for row in range(4):
        for idx in range(idx_start, idx_end, iteration_factor):
            pivot: int = table[row][idx]  # usado como referência

            # Só trocamos a posição, caso o :pivot: seja 0.
            if pivot != 0:
                continue

            for cursor in range(
                idx + iteration_factor, idx_end + iteration_factor, iteration_factor
            ):
                # Se o :pivot: é 0 e o cursor, diferente, trocamo-os de posição.
                if table[row][cursor] != 0:
                    temp: int = table[row][idx]
                    table[row][idx] = table[row][cursor]
                    table[row][cursor] = temp
                    movement = True
                    break

    return movement


def _vertical_move(table: list[list[int]], direction: str) -> bool:
    """Algoritmo de movimento do :push_table: para a movimentos verticais.

    Parameters
    ----------
    table: list[list[int]]
        A tabela do jogo em si.

        .. note::
            A tabela é passada por referência.

    col: int
        A linha a ser afetada.

    direction: str
        Define a direção que o algoritmo deve somar.

        .. warning::
            Os parâmetros devem ser ``1`` para a cima ou
            ``-1`` para a baixo.

    Returns
    -------
    bool
        Retorna se houve movimento efetuado.

    Examples
    --------
    >>> table = [[4, 4, 4, 0], [4, 0, 0, 0], [0, 4, 4, 4], [0, 0, 0, 0]]
    >>> _vertical_move(table, "w")
    True
    >>> table
    [[4, 4, 4, 4], [4, 4, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    >>> table = [[4, 0, 0, 0], [0, 4, 4, 0], [4, 0, 0, 0], [0, 4, 4, 4]]
    >>> _vertical_move(table, "s")
    True
    >>> table
    [[0, 0, 0, 0], [0, 0, 0, 0], [4, 4, 4, 0], [4, 4, 4, 4]]
    """
    assert direction in ("w", "s")

    movement = False

    if direction == "w":
        idx_start, idx_end, iteration_factor = (0, 3, 1)
    else:
        idx_start, idx_end, iteration_factor = (3, 0, -1)

    for col in range(4):
        for idx in range(idx_start, idx_end, iteration_factor):
            pivot: int = table[idx][col]  # usado como referência

            # Só trocamos a posição, caso o :pivot: seja 0.
            if pivot != 0:
                continue

            for cursor in range(
                idx + iteration_factor, idx_end + iteration_factor, iteration_factor
            ):
                # Se o :pivot: é 0 e o cursor, diferente, trocamo-os de posição.
                if table[cursor][col] != 0:
                    temp: int = table[idx][col]
                    table[idx][col] = table[cursor][col]
                    table[cursor][col] = temp
                    movement = True
                    break

    return movement


# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
#  Interface do Usuário
# =~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~


def __clear_screen() -> None:
    """Limpa o terminal atual."""
    match os.name:
        case "nt":
            os.system("cls")
        case _:
            os.system("clear")


def _format_row(template: str, row: list[int]) -> str:
    """Dado um template, essa função remove os 0 de serem impressos.

    Parameters
    ----------
    template: str
        O template da linha.
    row: list[int]
        Os números a serem inseridos.

    Returns
    -------
    str
        A string já formatada.

    Examples
    --------
    >>> _format_row("|{0: ^4}|{1: ^4}|{2: ^4}|{3: ^4}|", [4, 2, 0, 8])
    '| 4  | 2  |    | 8  |'
    """
    a, b, c, d = row

    if not a:
        a = ""
    if not b:
        b = ""
    if not c:
        c = ""
    if not d:
        d = ""

    return template.format(a, b, c, d)


def _get_instructions(config: tuple[int, bool]) -> tuple[str, str]:
    """Retorna as instruções de partida e movimentação.

    Parameters
    ----------
    config: tuple[int, bool])
        Configuração do jogo: (language, ascii-mode).
        Afetará a linguagem e o modo de impressão.

    Returns
    -------
    tuple[str, str]
        0: Instruções da partida.
        1: Instruções da movimentação.
    """
    match config:
        case (1, True):
            return (
                "Game: R (restart) Q (menu)",
                "Movements: W (up) A (left) S (down) D (right)",
            )
        case (1, False):
            return (
                "Game: R (↺: restart) Q (x: menu)",
                "Movements: W (⇡) A (⇠) S (⇣) D (⇢)",
            )
        case (2, True):
            return (
                "Jogo: R (reiniciar) Q (menu)",
                "Movimentos: W (cima) A (esquerda) S (baixo) D (direita)",
            )
        case (2, False):
            return (
                "Jogo: R (↺: reiniciar) Q (x: menu)",
                "Movimentos: W (⇡) A (⇠) S (⇣) D (⇢)",
            )
        case _:
            return (
                "Game: R (restart) Q (menu)",
                "Movements: W (up) A (left) S (down) D (right)",
            )


def _vertical_align(menu_height: int) -> None:
    """Algoritmo que alinha verticalmente o jogo.

    Basicamente, imprime a quantidade faltante de linhas em branco
    antes do conteúdo para o alinhamento.
    """
    _, HEIGHT = terminal_size()
    padding = (HEIGHT - menu_height) // 2
    for _ in range(padding):
        print()


# Para testes unitários
if __name__ == "__main__":
    import doctest

    doctest.testmod()
