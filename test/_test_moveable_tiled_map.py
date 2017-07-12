# class MoveableTiledMapTests(TestCase):

#     def setUp(self):
#         frame = Frame(TEST_GAME_CONTEXT.screen, Rect(90, 50, 160, 160))
#         self.tm = TiledMap(frame, TEST_GAME_CONTEXT.tile_factory)

#     def move_tiles(self):
#         while self.tm.is_map_moving():
#             self.tm.update()
#             self.tm.draw()
#             pygame.display.update()
#             time.sleep(SHORT_DELAY)

#     @showdoc
#     def test_move_map_tile(self):
#         """Moves two tiles right and up, then moves one tile back."""
#         self.tm.set_map(TEST_MAP)
#         self.tm.move_tile(Move(Vector(3,1), DOWNLEFT, 3, 2))
#         self.tm.move_tile(Move(Vector(1,2), UP, 1, 1))
#         self.move_tiles()
#         # move one piece back
#         self.tm.move_tile(Move(Vector(0,0), DOWN, 1, 4))
#         self.tm.move_tile(Move(Vector(0,4), UPRIGHT, 3, 2))
#         self.move_tiles()

#     @showdoc
#     def test_queued_moves(self):
#         """Two 2+1 moves across the map shown."""
#         self.tm.set_map(TEST_MAP)
#         self.tm.add_queued_moveset(
#                 [Move(Vector(0,0), DOWN, 3, 2),
#                  Move(Vector(2,1), UPLEFT, 1, 4)])
#         self.tm.add_queued_moveset([Move(Vector(3,3), LEFT, 2, 1)])
#         self.move_tiles()
