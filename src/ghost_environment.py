class GhostEnvironment:
    def __init__(self):
        """
        Inicializa o ambiente fantasma com células desconhecidas ('?').
        """
        self.rows = 10
        self.cols = 10
        self.ghost_env = [['?' for _ in range(self.cols)] for _ in range(self.rows)]

    def initialize_ghost_environment(self, agent_positions):
        """
        Inicializa o ambiente fantasma com agentes posicionados como 'L'.
        :param agent_positions: Lista de posições dos agentes.
        """
        for x, y in agent_positions:
            self.ghost_env[x][y] = 'L'

    def update_ghost_environment(self, x, y, value):
        """
        Atualiza o ambiente fantasma na posição (x, y) com o valor fornecido.
        :param x: Coordenada da linha.
        :param y: Coordenada da coluna.
        :param value: Novo valor da célula.
        """
        self.ghost_env[x][y] = value

    def get_cell_value(self, x, y):
        """
        Retorna o valor da célula na posição (x, y), garantindo que esteja dentro dos limites.
        :param x: Coordenada da linha.
        :param y: Coordenada da coluna.
        :return: Valor da célula ou '-' se estiver fora dos limites.
        """
        if 0 <= x < len(self.ghost_env) and 0 <= y < len(self.ghost_env[0]):
            return self.ghost_env[x][y]
        else:
            return "-"

    def print_ghost_environment(self):
        """
        Exibe o ambiente fantasma de forma legível no terminal.
        """
        for row in self.ghost_env:
            print("  ".join(row))
