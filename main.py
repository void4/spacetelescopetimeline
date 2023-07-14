import datetime as dt
from dateutil.parser import parse, ParserError

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.collections import PolyCollection
from bs4 import BeautifulSoup


with open("List of space telescopes - Wikipedia.html") as f:
	soup = BeautifulSoup(f.read(), "html.parser")

data = []

colors = []

color = "black"

categories = ["Gamma ray", "X-ray", "Ultraviolet", "Visible light", "Infrared and submillimeter", "Microwave", "Radio", "Other (Particle det., Grav. waves)", "To be launched"]

catcolors = ["black", "pink", "violet", "green", "red", "blue", "yellow", "gray", "orange"]
catfirst = ["???", "Uhuru", "OAO-2 (Stargazer)", "Hipparcos", "IRAS", "Cosmic Background Explorer (COBE)", "Highly Advanced Laboratory for Communications and Astronomy (HALCA, VSOP or MUSES-B)", "Proton-1", "X-ray Polarimeter Satellite (XPoSat)"]

for tri, tr in enumerate(soup.find_all("tr")):
	tds = list(tr.find_all("td"))
	if len(tds) < 5:
		continue
	name = tds[1].text.strip()
	launch = tds[3].text.strip()
	terminated = tds[4].text.strip()
	
	if name in catfirst and tri > 5:
		color = catcolors[catfirst.index(name)]
	
	try:
		start = parse(launch, fuzzy=True, dayfirst=True)
		if terminated == "—":
			end = dt.datetime.now()
		else:
			end = parse(terminated, fuzzy=True, dayfirst=True)
			
	except ParserError:
		continue
	
	print(name, launch, terminated, start, end)
	data.append([start, end, name])
	colors.append(color)


verts = []

for di, d in enumerate(data):
    v =  [(mdates.date2num(d[0]), di-.4),
          (mdates.date2num(d[0]), di+.4),
          (mdates.date2num(d[1]), di+.4),
          (mdates.date2num(d[1]), di-.4),
          (mdates.date2num(d[0]), di-.4)]
    verts.append(v)

bars = PolyCollection(verts, facecolors=colors)




fig, ax = plt.subplots()
ax.add_collection(bars)
ax.autoscale()
loc = mdates.AutoDateLocator()#MinuteLocator(byminute=[0,15,30,45])
#ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

ax.set_yticks(list(range(len(data))))
ax.set_yticklabels([d[2] for d in data])
plt.yticks(fontsize=4)

[tl.set_color(colors[i]) for i, tl in enumerate(plt.gca().get_yticklabels())]


custom_lines = [Line2D([0], [0], color=color, lw=4) for color in catcolors]
ax.legend(custom_lines, categories, loc="lower right")
fig.set_size_inches(18.5, 10.5)
fig.suptitle("Timeline of Space Telescopes")
ax.set_title("(data from https://en.wikipedia.org/wiki/List_of_space_telescopes, most probably incomplete and perhaps incorrectly parsed)", fontsize=10)
plt.tight_layout()

plt.savefig("space_telescope_timeline.png", dpi=180)
#plt.show()
