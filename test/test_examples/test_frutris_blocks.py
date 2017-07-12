
from unittest import main
from unittest import TestCase

from blocks import Blocks
from blocks import DOWN
from blocks import DOWNLEFT
from blocks import DOWNRIGHT
from blocks import LEFT
from blocks import RIGHT
from blocks import UP
from blocks import UPLEFT
from blocks import UPRIGHT


class BlocksTests(TestCase):
    def setUp(self):
        self.blocks = Blocks()
        
    def test_get_set(self):
        self.blocks.set(box)
        self.assertEqual(self.blocks.get(), box)

    def test_get_set_with_moving(self):
        self.blocks.set(box_drop_after)
        self.assertEqual(self.blocks.get(), box_drop_after)

    def test_insert_new(self):
        self.blocks.set(box)
        self.blocks.insert_block("AE")
        self.assertEqual(self.blocks.get(), box_new_block)

    def test_insert_diamond(self):
        self.blocks.set(box)
        self.blocks.insert_diamond(1)
        self.assertEqual(self.blocks.get(), box_new_diamond)

    def test_drop(self):
        self.blocks.set(box_drop_before)
        self.blocks.drop()
        self.assertEqual(self.blocks.get(), box_drop_after)

    def test_drop_partial(self):
        self.blocks.set(box_drop_independent_before)
        self.blocks.drop()
        self.assertEqual(self.blocks.get(), box_drop_independent_after)

    def test_drop_result(self):
        self.blocks.set(box_drop_before)
        r = self.blocks.drop()
        self.assertEqual(r,[(3,0,'a',DOWN),(4,0,'e',DOWN)])
    
    def test_settle(self):
        self.blocks.set(box_settle_before)
        self.blocks.drop()
        self.assertEqual(self.blocks.get(), box_settle_after)

    def test_leftshift(self):
        self.blocks.set(box_shift_before)
        result = self.blocks.left_shift()
        self.assertEqual(self.blocks.get(), box_leftshift)
        self.assertTrue(result)
        
    def test_rightshift(self):
        self.blocks.set(box_shift_before)
        result = self.blocks.right_shift()
        self.assertEqual(self.blocks.get(), box_rightshift)
        self.assertTrue(result)

    def test_leftshift_return(self):
        self.blocks.set(box_shift_before)
        result = self.blocks.left_shift()
        self.assertEqual(result,[(3,1,'a',LEFT),(4,1,'e',LEFT)])

    def test_rightshift_return(self):
        self.blocks.set(box_shift_before)
        result = self.blocks.right_shift()
        self.assertEqual(result,[(3,1,'a',RIGHT),(4,1,'e',RIGHT)])

    def test_cannot_shift_without_moving(self):
        self.blocks.set(box)
        result = self.blocks.left_shift()
        self.assertFalse(result)
        self.assertEqual(self.blocks.get(), box)
        result = self.blocks.right_shift()
        self.assertFalse(result)
        self.assertEqual(self.blocks.get(), box)

    def test_cannot_leftshift(self):
        self.blocks.set(box_cannot_leftshift)
        result = self.blocks.left_shift()
        self.assertEqual(self.blocks.get(), box_cannot_leftshift)
        self.assertFalse(result)

    def test_cannot_rightshift(self):
        self.blocks.set(box_cannot_rightshift1)
        result = self.blocks.right_shift()
        self.assertEqual(self.blocks.get(), box_cannot_rightshift1)
        self.assertFalse(result)
        self.blocks.set(box_cannot_rightshift2)
        result = self.blocks.right_shift()
        self.assertFalse(result)
        self.assertEqual(self.blocks.get(), box_cannot_rightshift2)

    def test_rotate(self):
        self.blocks.set(box_rotate_1)
        for after in [box_rotate_2, box_rotate_3, box_rotate_4]:
            self.blocks.rotate()
            self.assertEqual(self.blocks.get(), after)

    def test_rotate_return(self):
        self.blocks.set(box_rotate_1)
        result = self.blocks.rotate()
        self.assertEqual(result, [(4,1,'e',DOWNLEFT)])

    def test_cannot_rotate(self):
        self.blocks.set(box_cannot_rotate)
        self.blocks.rotate()
        self.assertEqual(self.blocks.get(), box_cannot_rotate)

    def test_remove_single(self):
        self.blocks.set(box_remove_single_before)
        self.blocks.remove_multiplets()
        self.assertEqual(self.blocks.get(), box_remove_single_after)

    def test_remove_multi(self):
        self.blocks.set(box_remove_multi_before)
        self.blocks.remove_multiplets()
        self.assertEqual(self.blocks.get(), box_remove_multi_after)

    def test_drop_bricks(self):
        self.blocks.set(box_drop_bricks_before)
        result = self.blocks.drop_bricks()
        expected = [(2,2,'a',DOWN*2),(4,3,'b',DOWN*1),
                    (5,1,'e',DOWN*4),(5,0,'e',DOWN*4),
                    (6,4,'c',DOWN*1),(6,3,'d',DOWN*1)]
        self.assertEqual(self.blocks.get(), box_drop_bricks_after)
        for r,e in zip(result,expected):
            self.assertEqual(r[0],e[0])
            self.assertEqual(r[1],e[1])
            self.assertEqual(r[2],e[2])
            self.assertEqual(sum(r[3]==e[3]),2)
            

    def test_remove_and_drop(self):
        self.blocks.set(box_drop_remove_before)
        self.blocks.remove_multiplets()
        self.blocks.drop_bricks()
        self.assertEqual(self.blocks.get(), box_drop_remove_after)

    def test_remove_consecutive(self):
        self.blocks.set(box_remove_consecutive_before)
        self.blocks.remove_consecutive()
        self.assertEqual(self.blocks.get(), box_remove_consecutive_after)

    def test_box_overflow(self):
        self.blocks.set(box_game_over)
        self.assertTrue(self.blocks.box_overflow())
        self.blocks.set(box_not_game_over)
        self.assertFalse(self.blocks.box_overflow())

    def test_get_stack_size(self):
        """returns height of the pile"""
        self.blocks.set(box)
        self.assertEqual(self.blocks.get_stack_size(),5)
        self.blocks.set(box_drop_after)
        self.assertEqual(self.blocks.get_stack_size(),5)
        self.blocks.set(box_remove_multi_after)
        self.assertEqual(self.blocks.get_stack_size(),3)
        

        
box = """#......#
#......#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_new_block = """#..AE..#
#......#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_new_diamond = """#.X....#
#......#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_drop_before = box_new_block

box_drop_after = """#......#
#..AE..#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_drop_independent_before = """#......#
#......#
#......#
#....a.#
#..EAa.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_drop_independent_after = """#......#
#......#
#......#
#....a.#
#..e.a.#
#.bbAa.#
#ccddde#
#cbbbaa#
########"""

box_settle_before = """#......#
#......#
#......#
#....a.#
#...Aa.#
#.bbDa.#
#ccddde#
#cbbbaa#
########"""


box_settle_after = """#......#
#......#
#......#
#....a.#
#...aa.#
#.bbda.#
#ccddde#
#cbbbaa#
########"""

box_shift_before = box_drop_after

box_leftshift = """#......#
#.AE...#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_rightshift = """#......#
#...AE.#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_cannot_leftshift = """#......#
#AE....#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_cannot_rightshift1 = """#......#
#....AE#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_cannot_rightshift2 = """#......#
#......#
#......#
#..AEa.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_rotate_1 = box_drop_after

box_rotate_2 = """#......#
#..A...#
#..E...#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_rotate_3 = """#......#
#..EA..#
#......#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_rotate_4 = """#......#
#..E...#
#..A...#
#....a.#
#....a.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""

box_cannot_rotate = """#......#
#......#
#......#
#....a.#
#..AEa.#
#.bb.a.#
#ccddde#
#cbbbaa#
########"""


box_remove_multi_before = box_settle_after

box_remove_multi_after = """#......#
#......#
#......#
#......#
#......#
#.bb...#
#cc...e#
#cbbbaa#
########"""

box_drop_remove_before = box_remove_multi_after

box_drop_remove_after = """#......#
#......#
#......#
#......#
#......#
#.b....#
#ccb..e#
#cbbbaa#
########"""

box_remove_consecutive_before = box_remove_multi_before
box_remove_consecutive_after = """#......#
#......#
#......#
#......#
#......#
#......#
#cb...e#
#cc..aa#
########"""

box_remove_single_before = """#......#
#......#
#......#
#....a.#
#...aa.#
#.bbea.#
#ccddde#
#cbbbaa#
########"""

box_remove_single_after = """#......#
#......#
#......#
#......#
#......#
#.bbe..#
#ccddde#
#cbbbaa#
########"""

box_drop_bricks_before = """#....e.#
#....e.#
#.a....#
#...b.d#
#.....c#
#.bbe..#
#ccddde#
#cbbbaa#
########"""

box_drop_bricks_after = """#......#
#......#
#......#
#......#
#.a.bed#
#.bbeec#
#ccddde#
#cbbbaa#
########"""

box_not_game_over = box_drop_bricks_after

box_game_over = """#...c..#
#...c..#
#...c..#
#...b..#
#.a.b.d#
#.bbe.c#
#ccddde#
#cbbbaa#
########"""


if __name__ == '__main__':
    main()
