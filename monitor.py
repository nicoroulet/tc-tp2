import curses
from common import title

COL_SEP = '  '

def my_str(x):
	if isinstance(x, float):
		return str('{:.4f}'.format(x))
	else:
		return str(x)

def monitor(header, step, start_state):
	"""
	Recibe una funcion `step` que a partir de un estado inicial genera
	un titulo y filas de datos para mostrar en pantalla en un loop.
	"""

	# Inicializa la pantalla
	scr = curses.initscr()
	scr.addstr(0, 0, title + '\n\n')
	scr.refresh()

	# Inicializa variables de estado
	state = start_state
	col_widths = []

	try:
		while True:
			# Obtiene lo proximo a mostrar en pantalla.
			rows, state = step(state)

			# Pone el cursor al principio e imprime el titulo
			scr.clear()
			scr.addstr(0, 0, title + '\n\n')

			# Calcula el ancho de las columnas para que este alineado
			for i, row in enumerate(rows):
				for j, col in enumerate([i+1] + row):
					try:
						col_widths[j] = max(col_widths[j], len(my_str(col)))
					except IndexError:
						col_widths.append(len(my_str(col)))

			# Imprime header
			if header:
				for j, col in enumerate([''] + header):
					try:
						col_widths[j] = max(col_widths[j], len(col))
					except IndexError:
						col_widths.append(len(col))

				scr.addstr(
					COL_SEP.join(col.ljust(col_widths[j]) for j, col in enumerate([''] + header))
				)
				scr.addstr('\n')

			# Imprime cada fila
			for i, row in enumerate(rows):
				scr.addstr(COL_SEP.join(
					my_str(col).ljust(col_widths[j]) for j, col in enumerate([i+1] + row)
				))
				scr.addstr('\n')

			scr.refresh()

	except KeyboardInterrupt:
		# Ctrl-C
		pass

	finally:
		# Necesario para volver la terminal a la normalidad
		curses.endwin()

	return state
