import curses,random
from ui import put,run

def candidates(board,r,c):
 return set(range(1,10))-set(board[r])-{board[i][c] for i in range(9)}-{board[i][j] for i in range(r//3*3,r//3*3+3) for j in range(c//3*3,c//3*3+3)}
def count_solutions(board,limit=2):
 best=None
 for r in range(9):
  for c in range(9):
   if not board[r][c]:
    choices=candidates(board,r,c)
    if not choices:return 0
    if best is None or len(choices)<len(best[2]):best=(r,c,choices)
 if best is None:return 1
 r,c,choices=best;total=0
 for n in choices:
  board[r][c]=n;total+=count_solutions(board,limit-total);board[r][c]=0
  if total>=limit:break
 return total
class Game:
 def __init__(self,seed=None):
  rng=random.Random(seed);bands=list(range(3));rng.shuffle(bands);rows=[];cols=[]
  for b in bands:
   inner=list(range(3));rng.shuffle(inner);rows.extend(b*3+i for i in inner)
  rng.shuffle(bands)
  for b in bands:
   inner=list(range(3));rng.shuffle(inner);cols.extend(b*3+i for i in inner)
  nums=list(range(1,10));rng.shuffle(nums);self.solution=[[nums[(r*3+r//3+c)%9] for c in cols] for r in rows];self.board=[row[:] for row in self.solution]
  cells=list(range(81));rng.shuffle(cells);removed=0
  for cell in cells:
   if removed>=38:break
   r,c=divmod(cell,9);old=self.board[r][c];self.board[r][c]=0
   if count_solutions([row[:] for row in self.board])!=1:self.board[r][c]=old
   else:removed+=1
  self.fixed={(r,c) for r in range(9) for c in range(9) if self.board[r][c]};self.notes={}
 def set(self,r,c,n):
  if (r,c) in self.fixed:return False
  if not 0<=n<=9:return False
  self.board[r][c]=n;self.notes.pop((r,c),None);return True
 def conflict(self,r,c):
  n=self.board[r][c]
  return bool(n and (any(self.board[r][i]==n for i in range(9) if i!=c) or any(self.board[i][c]==n for i in range(9) if i!=r) or any(self.board[i][j]==n for i in range(r//3*3,r//3*3+3) for j in range(c//3*3,c//3*3+3) if (i,j)!=(r,c))))
 @property
 def won(self):return self.board==self.solution
 def note(self,r,c,n):
  if (r,c) in self.fixed or self.board[r][c]:return
  notes=self.notes.setdefault((r,c),set());notes.remove(n) if n in notes else notes.add(n)
def loop(s):
 g=Game();r=c=0;pencil=False
 while True:
  h,w=s.getmaxyx();s.erase();put(s,1,2,'S U D O V A N T A',curses.A_BOLD)
  if h<26 or w<60:put(s,3,2,'Resize to60x26. Q exits.')
  else:
   cw=max(4,min(8,(w-8)//9));x=(w-cw*9)//2
   for i in range(9):
    for j in range(9):
     n=g.board[i][j];style=curses.color_pair(3 if g.conflict(i,j) else 1 if (i,j) in g.fixed else 2)
     if (i,j)==(r,c):style|=curses.A_REVERSE
     value=str(n) if n else '.'
     put(s,4+i*2,x+j*cw,value.center(cw-1),style)
     if j in (2,5):put(s,4+i*2,x+(j+1)*cw-1,'│')
    if i in (2,5):put(s,5+i*2,x,'─'*(cw*9-1))
   put(s,h-4,2,'Pencil mode: '+('ON' if pencil else 'OFF')+' | Cell notes: '+' '.join(map(str,sorted(g.notes.get((r,c),set())))))
   put(s,h-3,2,'Solved! N new puzzle.' if g.won else 'Numbers1-9 | 0 erase | P pencil | N new | Q quit')
   put(s,h-2,2,'Arrows/WASD move. Fixed clues cannot be changed.');
  s.refresh();k=s.getch()
  if k in (ord('q'),ord('Q')):return
  if h<26 or w<60:continue
  if k in (ord('n'),ord('N')):g=Game();r=c=0;continue
  if k in (ord('p'),ord('P')):pencil=not pencil;continue
  dr,dc={curses.KEY_UP:(-1,0),ord('w'):(-1,0),curses.KEY_DOWN:(1,0),ord('s'):(1,0),curses.KEY_LEFT:(0,-1),ord('a'):(0,-1),curses.KEY_RIGHT:(0,1),ord('d'):(0,1)}.get(k,(0,0));r=max(0,min(8,r+dr));c=max(0,min(8,c+dc))
  if ord('1')<=k<=ord('9'):
   if pencil:g.note(r,c,k-ord('0'))
   else:g.set(r,c,k-ord('0'))
  elif k in (ord('0'),curses.KEY_BACKSPACE,127):g.set(r,c,0)
if __name__=='__main__':raise SystemExit(run(loop))
