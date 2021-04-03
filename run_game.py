import code.game
import sys

# Not bothering with pyinstaller exe since it makes the imports all wonky.

if __name__ == "__main__":
	min_version = 3, 9
	if sys.version_info[:2] < min_version:
		print("Python Prison expects Python {}.{} and may not work!".format(*min_version))
	print("Started game")
	code.game.run_game()
	print("Ended game")