        elif self.mode == 'two player game':
            if self.players[0].game_over:
                self.show_game_over('Player 2 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player2_score'])
                self.terminate_game()
            elif self.players[1].game_over:
                self.show_game_over('Player 1 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player1_score'])
                self.terminate_game()
        self.update_music()
