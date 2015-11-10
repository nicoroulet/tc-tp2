import curses

COL_PADDING = 2

def start_display(step, start_state):
	scr = curses.initscr()
	scr.addstr(0, 0, "LE MONITOR.\n\n")

	state = start_state

	try:
		while True:
			title, rows, state = step(state)

			scr.clear()
			scr.addstr(0, 0, title + "\n\n")

			col_width = COL_PADDING + max(len(word) for row in data for word in row)

			for row in rows:
				scr.addstr("".join(str(word).ljust(col_width) for word in row) + "\n")

			scr.refresh()

	except KeyboardInterrupt:
		pass

	finally:
		curses.endwin()

# vim: noet ts=4
