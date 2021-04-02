import io
import time
import multiprocessing as mp
from contextlib import redirect_stdout

class Executor:
	TIME_LIMIT = 5
	UNSET = -1
	SUCCESS = 0
	ERROR = 1
	TIMEOUT = 2

	process = None
	queue = None
	start_time: float = 0
	status: int = UNSET
	output: str = ''

	def worker(self, code):
		print('WORKING')
		#out['status'] += 1
		out = Executor.SUCCESS, 'hello'
		self.queue.put(out)

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

	def is_done(self):
		if not self.process:
			return False # Doesn't make sense to be done if there's no process.

		if self.process.is_alive():
			if time.time() - self.start_time > Executor.TIME_LIMIT: # Timed out.
				self.process.kill()
				self.queue.close()
				self.process = None
				self.queue = None
				self.status = Executor.TIMEOUT
				self.output = ''
				return True
			else: # Still running within the time limit.
				return False

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

	# TODO combine
	def test(self, code='print(hi")'):
		f = io.StringIO()
		with redirect_stdout(f):
			try:
				exec(code, {}, {})
			except Exception as e:
				print('[ERROR]')
		output = f.getvalue()
		return output

if __name__ == "__main__":
	import code.game
	code.game.run_game()
