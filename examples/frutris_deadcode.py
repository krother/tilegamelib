    def choose_next_music(self):
        letter, number = self.current_music
        number = 3 - number
        if len(self.players) >= 1:
            stack_size = self.players[0].get_stack_size()
            if stack_size <= 4:
                letter = 'a'
            elif stack_size <= 8:
                letter = 'b'
            else:
                letter = 'c'
        self.current_music = (letter, number)
        return 'music/%s%i.wav' % (letter, number)

    def update_music(self):
        return
        self.music_counter -= 1
        if self.music_counter == 0:
            self.music_counter = 50
            if check_music_status() == CLOSE_TO_END:
                next_music(self.choose_next_music())

    def new_game(self):
        play_music('music/a1.wav')
        if self.mode == 'one player game':
            self.status_box = StatusBox(self, array([500,100]), array([200,500]))
            self.status_box['player1_score'] = 0
            self.status_box['level'] = 1
            self.players.append(FrutrisBox(self, (250, 0)))
            self.delay = ONE_PLAYER_START_DELAY
            play_effect('menu_select_game_1')
        elif self.mode == 'two player game':
            self.status_box = StatusBox(self, array([300,100]), array([200,500]))
            self.status_box['player1_score'] = 0
            self.status_box['player2_score'] = 0
            self.players.append(FrutrisBox(self, (50, 0)))
            self.players.append(FrutrisBox(self, (500, 0)))
            self.delay = TWO_PLAYER_DELAY
            play_effect('menu_select_game_2')

    def terminate_game(self):
        #stop_music()
        play_effect('menu_select_quit')
        time.sleep(1)

    def message(self, sender, msg_type, *params):
        if msg_type == 'diamond_to_opponent'\
           and self.mode == 'two player game':
            opp = self.players[0]==sender and self.players[1] or self.players[0]
            opp.diamonds_queued += params[0]
        elif msg_type == 'add_points':
            field = 'player2_score'
            if sender == self.players[0]:
                field = 'player1_score'
            self.status_box[field] += params[0] * self.status_box.get('level',1)

    def _deadcode(self):
        """Check for game over."""
        if self.mode == 'one player game':
            if self.players[0].game_over:
                play_effect('game_over')
                self.show_game_over('GAME OVER!')
                play_effect('highscores_normal')
                self.show_highscores(self.status_box['player1_score'])
                self.terminate_game()
            else:
                self.level_counter -= 1
                if self.level_counter == 0:
                    self.status_box['level'] += 1
                    self.level_counter = LEVEL_COUNTER_INIT
                    if self.players[0].drop_delay > LEVEL_DROP_COUNTER_DECREASE:
                        self.players[0].drop_delay -= LEVEL_DROP_COUNTER_DECREASE
        elif self.mode == 'two player game':
            if self.players[0].game_over:
                play_effect('winner_second')
                self.show_game_over('Player 2 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player2_score'])
                self.terminate_game()
            elif self.players[1].game_over:
                play_effect('winner_first')
                self.show_game_over('Player 1 wins!',offset=self.settings.GAME_OVER_SHORT_OFFSET)
                #self.show_highscores(self.status_box['player1_score'])
                self.terminate_game()
        self.update_music()
