import subprocess
from collections import deque
def parse_xrandr_query(xrandr_output):
	xrandr_output_array = filter(None, xrandr_output.split('\n'))
	displays = {}
	current_display = None
	
	for line in xrandr_output_array:
		if ' connected ' in line:
			current_display = get_first_col(line)
			displays[current_display] = {'connected' : True }

		elif line.startswith('   ') and current_display is not None:
			if '+' in line:
				displays[current_display]['default'] = get_first_col(line)
			if '*' in line:
				displays[current_display]['current'] = get_first_col(line)

		else:
			current_display = None

	return displays

def get_first_col(line):
	return deque(line.strip().split(' ')).popleft()

def run_xrandr_query():
	process = subprocess.Popen('xrandr -q', shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	errcode = process.returncode
	return out

def current():
	xrandr_output_array = run_xrandr_query() 
	displays = parse_xrandr_query(xrandr_output_array)
	return displays

if __name__ == '__main__':
	print current()