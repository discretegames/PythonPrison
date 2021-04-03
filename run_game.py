import sys
import code.game

if __name__ == "__main__":
	min_version = 3, 9
	if sys.version_info[:2] < min_version:
		print("Python Prison expects Python {}.{} and may not work!".format(*min_version))
	print("If the game window is too big or too small try editing WINDOW_SIZE at the top of the /code/constants.py file")
	code.game.run_game()