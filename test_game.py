import unittest
from sudovanta import Game,count_solutions
class Tests(unittest.TestCase):
 def test_unique(self):
  for seed in range(10):g=Game(seed);self.assertEqual(count_solutions([r[:] for r in g.board]),1)
 def test_fixed(self):g=Game(0);r,c=next(iter(g.fixed));self.assertFalse(g.set(r,c,0))
 def test_win(self):g=Game(1);g.board=[r[:] for r in g.solution];self.assertTrue(g.won)
 def test_conflict(self):g=Game(1);g.board[0][0]=g.board[0][1]=2;self.assertTrue(g.conflict(0,0))
 def test_note(self):
  g=Game(1);r,c=next((r,c) for r in range(9) for c in range(9) if not g.board[r][c]);g.note(r,c,2);self.assertIn(2,g.notes[(r,c)]);g.note(r,c,2);self.assertNotIn(2,g.notes[(r,c)])
 def test_seed(self):self.assertEqual(Game(2).board,Game(2).board)
if __name__=='__main__':unittest.main()
