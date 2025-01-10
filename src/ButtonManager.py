class ButtonManager:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
        button.set_manager(self)

    def button_clicked(self, clicked_button):
        for button in self.buttons:
            if button != clicked_button:    # Desmarca todos os outros botões
                button.deselect()
        clicked_button.select()        # Seleciona o botão clicado
