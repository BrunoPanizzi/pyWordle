from random import choice
from curses import wrapper
import curses

words = []
with open('words.txt', 'r') as f:
  for word in f:
    if len(word) == 6:
      words.append(word.replace('\n', ''))

allowed_keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']



def center_message(height, max_w, message, stdscr):
  pos = int(max_w / 2 - len(message) / 2) 
  stdscr.addstr(height, pos, message)

def welcome(stdscr): 
  _, width = stdscr.getmaxyx()

  stdscr.clear()
  center_message(3, width, 'Welcome to Wordle!', stdscr)
  center_message(4, width, 'press any key to start', stdscr)
  stdscr.refresh()
  stdscr.getch()
  main(stdscr)

def winscr(stdscr, word):
  stdscr.addstr(f'YOU GUESSED IT!!\nThe word was {word}')
  stdscr.addstr('Press enter to play again or esc to quit')

  key = stdscr.getch()
  stdscr.addstr(str(key))
  stdscr.getch()
  if key == 27:
    curses.endwin()
  elif key == 10:
    main(stdscr)

def main(stdscr):
  # COLORS
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
  green_bg = curses.color_pair(1)
  yellow_bg = curses.color_pair(2)
  black_bg = curses.color_pair(3)

  stdscr.clear()

  str_word = choice(words)
  word = list(str_word)
  guesses = 0
  user_word = ['' for _ in range(5)]
  win = False
  
  stdscr.clear()
  stdscr.addstr('Try to guess the wordle in 6 tries \n\n')
  stdscr.addstr(str_word)
  
  while guesses < 6 and not win:
    key = stdscr.getch()
    cursor_y, cursor_x = stdscr.getyx()
    
    if key in range(97, 123) and cursor_x < 5:
      for _ in range(6, 99):
        stdscr.delch(cursor_y, 6)

      character = allowed_keys[key - 97]
      user_word[cursor_x] = character
      stdscr.addstr(cursor_y, cursor_x, character)

    elif key == 260: # move left
      if cursor_x != 0:
        stdscr.move(cursor_y ,cursor_x - 1)

    elif key == 261: # move right
      if cursor_x < 5:
        stdscr.move(cursor_y ,cursor_x + 1)

    elif key == 8: # delete
      if cursor_x > 0:
        prev_index = cursor_x - 1
        stdscr.addstr(cursor_y, prev_index, ' ')
        stdscr.move(cursor_y, prev_index)
        user_word[prev_index] = ''

    elif key == 10: # enter
      if all(user_word):
        if ''.join(user_word) in words:
          guesses += 1

          stdscr.deleteln()
          stdscr.move(cursor_y, 0)
          for i, letter in enumerate(user_word):
            color = black_bg
            if letter in word:
              color = green_bg if word[i] == letter else yellow_bg
            stdscr.addstr(cursor_y, i, letter, color)
            

          stdscr.move(cursor_y + 1, 0)

          if user_word == word: # win
            win = True
            stdscr.addstr('\n')

          user_word = ['' for _ in range(5)]
        else: 
          stdscr.addstr(cursor_y, 7, 'invalid word')
          stdscr.move(cursor_y, 0)  
      else: 
        stdscr.addstr(cursor_y, 7, 'short word')
        stdscr.move(cursor_y, 0)

  if win:
    winscr(stdscr, str_word)
  else: 
    stdscr.addstr(cursor_y + 2, 0, f'Not this time...\nThe word was {str_word}')
  stdscr.getch()

if __name__ == '__main__': 
  wrapper(welcome)
