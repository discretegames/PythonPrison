import io
import time
import multiprocessing as mp
from contextlib import redirect_stdout

class Executor:
	TIME_LIMIT = 2
	UNSET = -1
	SUCCESS = 0
	ERROR = 1
	TIMEOUT = 2

	process = None
	queue = None
	start_time: float = 0
	status: int = UNSET
	output: str = ''

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
			self.status = Executor.TIMEOUT
			self.output = ''
			return True

		# Otherwise the process is done.
		if not self.queue or self.queue.qsize() == 0:
			self.status = Executor.ERROR
			self.output = ''
		else:
			self.status, self.output = self.queue.get()
		self.queue.close()
		self.process = None
		self.queue = None
		return True

	# TODO use error message instead of status
	def worker(self, code):
		try:
			output = io.StringIO()
			with redirect_stdout(output):
				exec(code, {}, {})
			result = Executor.SUCCESS, output.getvalue()
		except:
			result = Executor.ERROR, ''
		self.queue.put(result)

if __name__ == "__main__":
	import code.game
	code.game.run_game()
