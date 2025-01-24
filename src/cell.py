class Cell:
    def __init__(self, cell_type: str, position):
        """
        Inicializa uma célula no ambiente.
        :param cell_type: Tipo da célula ('L' para livre, 'B' para bomba, 'T' para tesouro, 'F' para bandeira)
        :param position: Posição da célula na grade (linha, coluna)
        """
        self.type = cell_type  # Tipo da célula ('L', 'B', 'T', 'F')
        self.position = position  # Posição na grade
        self.is_discovered = False  # Indica se a célula foi descoberta
        self.is_consumed =  False  # Indica se o tesouro foi consumido (aplicável apenas para tesouros)
        self.is_destroyed = False  # Indica se a bomba foi destruída (aplicável apenas para bombas)
        self.is_flag_found = False # Indica se a bandeira foi encontrada (aplicável apenas para bandeiras)

    def discover(self):
        """
        Marca a célula como descoberta.
        """
        self.is_discovered = True

    def consume_treasure(self, consume_all):
        """
        Consome o tesouro da célula se aplicável.
        :param consume_all: Se verdadeiro, a célula se torna uma célula livre após ser consumida.
        :return: Verdadeiro se o tesouro foi consumido, falso caso contrário.
        """
        if self.type in 'T' and not self.is_consumed:
            self.is_consumed = True
            if consume_all:
                self.change_cell_type('L')
            return True
        return False

    def destroy_bomb(self):
        """
        Destrói a bomba na célula se aplicável.
        :return: Verdadeiro se a bomba foi destruída, falso caso contrário.
        """
        if self.type in 'B' and not self.is_destroyed:
            self.is_destroyed = True
            self.change_cell_type('L')
            return True
        return False

    def found_the_flag(self):
        """
        Marca a bandeira como encontrada.
        :return: Verdadeiro se a bandeira foi encontrada, falso caso contrário.
        """
        if self.type in 'F' and not self.is_flag_found:
            self.is_flag_found = True
            return True
        return False

    def change_cell_type(self, cell_type):
        """
        Altera o tipo da célula.
        :param cell_type: Novo tipo da célula ('L', 'B', 'T', 'F')
        """
        self.type = cell_type

    def display_color(self):
        """
        Retorna a cor associada ao tipo da célula para exibição.
        """
        if self.type == 'L': return "white"
        if self.type == 'B': return "light coral"
        if self.type == 'T': return "gold"
        if self.type == 'F': return "green"

    def __repr__(self):
        """
        Representação textual da célula para depuração.
        """
        status = "Descoberta" if self.is_discovered else "Não descoberta"
        consumed_status = ", Consumida" if self.is_consumed else ""
        return f"Cell({self.type}, {status}{consumed_status}, Posição={self.position})"
