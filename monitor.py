#!python3

"""
- Abrir o arquivo passando como argumento o nome da tabela a ser monitorada
- Criar um laço infinito que rode a cada X segundos
- Conectar com o banco e fazer a consulta
- Utilizar o curses para exibir os resultados ao vivo
"""

import sys, configparser, time, psycopg2, curses


class Postgre():

	def __init__(self, config):
		try:
			self.conn = psycopg2.connect(
				host = config['host'],
				port = config['port'],
				user = config['user'],
				password = config['password'],
				database = config['database']
			)
			self.cursor = self.conn.cursor()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def __del__(self):
		if self.conn is not None:
			self.conn.close()

	def consult_table(self, table):
		sql = 'SELECT * FROM {}'.format(table)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()

		return result

class Curses():

	def __init__(self):
		self.screen = curses.initscr()
		self.animation = True
		# Ocultar o cursor
		curses.curs_set(0)

		# Inicializar as cores
		curses.start_color()
		curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
		curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	def __del__(self):
		curses.endwin()

	def set_title(self, title):
		self.table_name = title

	def update_data(self, data):
		self.data = data

	def refresh_screen(self):
		self.screen.clear()
		# Pegar o tamanho da tela aqui ao inves do init,
		# para que o terminal fique adaptativo.
		self.height, self.width = self.screen.getmaxyx()

		# Título da tela
		title = 'Database monitor'
		self.screen.addstr(0, 0, title, curses.color_pair(1))

		# Render status bar
		self.screen.attron(curses.color_pair(3))
		text = '>> {}'.format(self.table_name)
		self.screen.addstr(1, 0, text)
		self.screen.addstr(1, len(text), " " * (self.width - len(text)))
		self.screen.attroff(curses.color_pair(3))

		# Count columns
		columns = len(self.data[0])
		space_between_columns = self.width / columns
		space_between_columns = int(space_between_columns)

		# Render data
		line_number = 2
		for result in self.data:
			cursor = 0

			for text in result:
				text = str(text)
				text = text[:space_between_columns]
				self.screen.addstr(line_number, cursor, text)
				cursor += space_between_columns

			line_number += 1

		# Render status bar
		self.screen.attron(curses.color_pair(3))
		self.screen.addstr(line_number, 0, " " * (self.width))
		self.screen.attroff(curses.color_pair(3))

		# Piscar um quadradinho vermelho para indicar que está vivo
		if self.animation:
			self.screen.attron(curses.color_pair(2))
			self.screen.addstr(1, self.width - 2, " ")
			self.screen.attroff(curses.color_pair(2))
			self.animation = not self.animation
		else:
			self.animation = not self.animation

		self.screen.refresh()


def get_config():
	config = configparser.ConfigParser()
	config.read('config.ini')

	return config['DATABASE']

def check_changes():
	return True

def main():
	if len(sys.argv) < 2:
		raise Exception('Informe o nome da tabela como argumento')

	table_name = sys.argv[1]
	config = get_config()
	db = Postgre(config)
	screen = Curses()
	screen.set_title(table_name)

	while True:
		table_content = db.consult_table(table_name)
		screen.update_data(table_content)
		screen.refresh_screen()

		if check_changes():
			# TODO play sound on changes
			pass

		time.sleep(1)


if __name__ == '__main__':
	main()

