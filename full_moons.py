# some code edited from https://github.com/mareuter/pylunar/

# https://rhodesmill.org/pyephem/quick
# pip install ephem
import ephem
import numpy as np
import inspect
from datetime import datetime as dt

def get_default_args(func):
	# gets default parameters for a function
	# ie for use if I make a web app and want to display defaults
	signature = inspect.signature(func)
	return {
		k: v.default
		for k, v in signature.parameters.items()
		if v.default is not inspect.Parameter.empty
	}
#end get_default_args()

# 57.91394844089449, -4.616350110930627 near Croick in Scottish Highlands
hogwarts_coords = ((56, 54, 50), (-4, 36, 59))
hogwarts_elev = 400 # m above sea level
hogwarts_timezone = "GMT" # ????


moon_file_path = "/content/drive/MyDrive/Past_Years_etc/etc/moon_file.txt"
first_year = dt(1971, 9, 1) # 1st Sept 1971
that_night = dt(1981, 10, 31)
sirius_birth_year = 1959

test_start_date = dt(1976, 1, 1)
test_end_date = dt(1976, 12, 31)

def is_new_school_year(d):
	return (d.month == 9)

def get_marauders_school_year_string(d, printbool=False):
	## NB calculates years pre/post Hogwarts with turnover on 1st july (ie end of school year)
	school_year_start = d.year
	if d.month < 7: ## ie jan to june
		# school year started last calendar year
		school_year_start = school_year_start - 1
	marauder_school_year = (school_year_start - first_year.year) + 1
	if printbool: print(d.year, "-", d.month, " -> ", school_year_start, " -> ", marauder_school_year)

	msy_s = "\n"
	if d.month is 7 or d.month is 8: # ie july/august
		msy_s = "Summer before "

	if marauder_school_year >= 4 and marauder_school_year <= 7:
		msy_s = msy_s + (str(marauder_school_year) + "th Year")
	elif marauder_school_year is 1:
		msy_s = msy_s + "1st Year"
	elif marauder_school_year is 2:
		msy_s = msy_s + "2nd Year"
	elif marauder_school_year is 3:
		msy_s = msy_s + "3rd Year"
	# pre/post hogwarts write over 'summer before ' string
	elif marauder_school_year < 1:
		msy_s = ("\n" + str(abs(marauder_school_year)) + " years pre-Hogwarts")
	else:
		msy_s = ("\n" + str(marauder_school_year-7) + " years post-Hogwarts")

	m_age = school_year_start - sirius_birth_year # earliest birth year ie Sirius's
	msy_s = msy_s + (" (aged " + str(m_age-1) + "-" + str(m_age) +")\n")
	# eg. first year: 1971-1959 = 12 => "(aged 11-12)"
	if printbool: print(msy_s)
	return msy_s
#end get_school_year()

def dt_pretty_print(d, printbool=False):
	year_s = d.strftime("%Y")
	month_s = d.strftime("%b")
	day_s = d.strftime("%d")
	if d.day < 10:
		day_s = day_s.replace("0", " ")
	weekday_s = d.strftime("%a")
	date_s = ("    " + year_s + " " + month_s + " " + day_s + " (" + weekday_s + " night)\n")
	if printbool: print("full moon: ", d, "\n", date_s, "\n")
	return date_s
#end dt_prettyprint()

def clear_file(path):
	f = open(path, "w")
	f.write("")
	f.close()
	return
#end clear_file()

"""
def create_hogwarts_observer():
	ob = ephem.Observer()
	ob.lon = (":").join(hogwarts_coords[0])
	ob.lat = (":").join(hogwarts_coords[1])
	ob.elevation = hogwarts_elev
	return ob
"""

def write_full_moons(start_date=first_year, end_date=that_night, file_path=moon_file_path, printbool=False, over_write=True):
	if over_write: clear_file(file_path)
	moon_file = open(file_path, "a")
	#if observer is None:
	#    observer = create_hogwarts_observer()
	moon = ephem.Moon()

	current_date = start_date
	i = 0
	while (current_date < end_date):
		if printbool:
			print(i, ": ", current_date)
			i = i+1
		moon_ed = ephem.next_full_moon(current_date)
		moon_dt = moon_ed.datetime()
		moon_s = ""
		if is_new_school_year(moon_dt):
			moon_s = get_marauders_school_year_string(moon_dt, printbool=printbool)
		moon_s = moon_s + dt_pretty_print(moon_dt, printbool=printbool)
		moon_file.write(moon_s)

		current_date = moon_dt
	#end while


	moon_file.close()
	return
#end write_full_moons()

"""
>>> from datetime import date, datetime
>>> print(ephem.Date(datetime(2005, 4, 18, 22, 15)))
2005/4/18 22:15:00
>>> d = ephem.Date('2000/12/25 12:41:16')
>>> d.datetime()
datetime.datetime(2000, 12, 25, 12, 41, 15, 999999)
In those last two commands, note that slight round-off error has
"""
def main():
	#print(get_default_args(write_full_moons))
	write_full_moons(start_date=test_start_date, end_date=test_end_date, printbool=True)
#end main()

if __name__ == "__main__":
	main()
