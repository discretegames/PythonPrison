import io
import time
import multiprocessing as mp
from contextlib import redirect_stdout

class Executor:
	TIME_LIMIT = 2

	def __init__(self):
		self.process = None
		self.queue = None
		self.start_time = 0
		self.error = None
		self.output = ''

	# Kills any current exec_process and starts it again running code.
	def execute(self, code):
		if self.process: # and self.process.is_alive():
			self.process.kill() # Seems ok to always call kill just in case.
		if self.queue:
			self.queue.close()

		self.queue = mp.Queue()
		self.process = mp.Process(target=self.worker, args=(code,))
		self.start_time = time.time()
		self.process.start()

	def is_done(self): # Sloppy since I'm no expert at multiprocessing.
		if not self.process:
			return False # Doesn't make sense to be done if there's no process.

		if self.process.is_alive():
			if time.time() - self.start_time < Executor.TIME_LIMIT:
				return False # Still running within the time limit.
			# Otherwise timed out.
			self.process.kill()
			self.queue.close()
			self.process = None
			self.queue = None
			self.error = 'timed out'
			self.output = ''
			return True

		# Otherwise the process is done.
		if not self.queue or self.queue.qsize() == 0:
			self.error = 'queue error' # should never happen
			self.output = ''
		else:
			self.error, self.output = self.queue.get()
		self.queue.close()
		self.process = None
		self.queue = None
		return True

	def worker(self, code):
		try:
			output = io.StringIO()
			with redirect_stdout(output):
				exec(code, {}, {})
			result = None, output.getvalue()
		except Exception as e:
			error = str(e)
			cut = error.find(' (')
			if cut != -1:
				error = error[:cut]
			result = error, ''
		self.queue.put(result)

if __name__ == "__main__":
	import code.game
	code.game.run_game()