#!/usr/bin/env python
# coding: utf-8

# In[21]:


import sqlite3
from PIL import Image, ImageOps, ImageDraw
import time


# In[22]:


sqlite_connection = sqlite3.connect("units.db")
cursor = sqlite_connection.cursor()
tier_image = Image.open("system/tier.png")
elite_image = Image.open("system/plus.png")
p_immune = Image.open("system/immune-p.png")
m_immune = Image.open("system/immune-m.png")
empty_unit = Image.open("system/empty_unit.png")

star_image = {
	1: Image.open("system/1-star.png"),
	2: Image.open("system/2-star.png"),
	3: Image.open("system/3-star.png"),
	4: Image.open("system/4-star.png"),
	5: Image.open("system/5-star.png"),
	6: Image.open("system/6-star.png"),
	7: Image.open("system/7-star.png")
}

for i, val in star_image.items():
	star_image[i] = val.convert("RGBA")

gen_time = 0
lang = "en"


# In[23]:


def sql(fetch: str) -> str:
	cursor.execute(fetch)
	return cursor.fetchall()


# In[24]:


def ceildiv(a, b):
    return -(a // -b)


# In[25]:


def name2short(name: str) -> str:
	return sql(f"SELECT short FROM units WHERE name = '{name}' LIMIT 1")[0][0]


# In[26]:


def short2name(short: str, translate: bool = False) -> str:
	global lang
	lowershort = short.lower()
	capsshort = short.title()
	prefix = ""

	if lang != "en" and translate:
		prefix += lang + "_"

	data = sql(f"SELECT {prefix}name FROM units WHERE (short = '{lowershort}' or alt_short = '{lowershort}' or alt_short_2 = '{lowershort}' or name = '{capsshort}') LIMIT 1")

	if not data:
		raise SystemExit(f"Unknown abbreviation: {short}")

	return data[0][0]


# In[27]:


def short2star(short: str) -> int:
	lowershort = short.lower()
	capsshort = short.title()
	return int(sql(f"SELECT star FROM units WHERE (short = '{lowershort}' or alt_short = '{lowershort}' or alt_short_2 = '{lowershort}' or name = '{capsshort}') LIMIT 1")[0][0])


# In[28]:


def splitSolution(solution: str) -> list:

	solution = solution.strip()

	if solution.find(" or ") != -1:
		raise SystemExit("Or expressions are not supported yet")

	solution = solution.replace(",", "")

	tmp_units = solution.split(' ')

	units = []

	for unit in tmp_units:
		tmp_unit = {}
		mult = False
		short = unit
		folder = ''
		tier = 0
		immune = False
		elite = 0

		tiered = unit.find("T1") == 0 or unit.find("T2") == 0 or unit.find("T3") == 0 or unit.find("T4") == 0 or unit.find("T5") == 0 or unit.find("T6") == 0
		senior = unit.find("Sr") == 0

		if tiered or senior:
			senior = True
			folder = "senior"
		else:
			folder = "normal"

		if unit.find("*") != -1:
			tmp_unit["count"] = int(unit.split('*')[1])
			mult = 1
		else:
			tmp_unit["count"] = 1

		if senior:
			if tiered:
				tier = int(short[1])
			short = short[2:]

		if mult:
			short = short[:short.find('*')]

		if short.find("(MI)") != -1:
			short = short.replace("(MI)", "")
			immune = "M"
			
		if short.find("(PI)") != -1:
			short = short.replace("(PI)", "")
			immune = "P"

		if tier > 3:
			elite = tier - 3
			tier = 3

		tmp_unit["name"] = short2name(short, True)
		tmp_unit["star"] = short2star(short) + senior
		tmp_unit["senior"] = senior
		tmp_unit["tier"] = tier
		tmp_unit["immune"] = immune
		tmp_unit["elite"] = elite
		tmp_unit["image"] = f"{folder}/{short2name(short)}.png"

		units += [tmp_unit]
		
	return units


# In[29]:


def return_and_add (*number: float, add: float) -> float:
	number += add
	return number - add


# In[30]:


def repeat_to_array(item: any, count: int):
	items = []
	for i in range(count):
		items.append(item)
	return items


# In[31]:


def make_elite(image: Image, elite: int) -> Image:
	global elite_image
	for i in range(elite):
		size_mult = 1.3
		elite_image = elite_image.resize(size=(int(10*size_mult), int(11*size_mult)))
		elite_image = elite_image.convert("RGBA")
		image.alpha_composite(
			elite_image, (image.size[0] - elite_image.size[0] - 2 - i*12, 5))
	return image


# In[32]:


def make_immune(image: Image, immune: str) -> Image:
	global p_immune, m_immune
	immune_image = False
	if immune:
		if immune == "P":
			immune_image = p_immune
		if immune == "M":
			immune_image = m_immune
		size_mult = 1.3
		immune_image = immune_image.resize(
			size=(int(10*size_mult), int(10*size_mult)))
		immune_image = immune_image.convert("RGBA")
		image.alpha_composite(
			immune_image, (3, image.size[1] - immune_image.size[1] - 5))
	return image


# In[33]:


def log_generation(units: str):
	global gen_time
	units = splitSolution(units)
	print(f"Image generation done in {round(time.time() - gen_time, 2)}s")
	print("Units:")
	for unit in units:
		senior, plus, immune = "", "", ""
		if unit["senior"]: senior = "Sr "
		if unit["elite"]: plus = "+" * unit['elite'] + " "
		if unit["immune"] == "M": immune = "(MI) "
		if unit["immune"] == "P": immune = "(PI) "
		print(
			f"T{unit['tier']} {senior}«{unit['name']}» {plus}{immune}x{unit['count']}")


# In[34]:


def gen_image(units: str, border: int = 0, add_empty: bool = True) -> Image:
	star_colors = {
		1: (131, 132, 130, 255), #838482
		2: (100, 139, 21, 255),  #648b15
		3: (69, 146, 221, 255),  #4592dd
		4: (192, 52, 191, 255),  #c034c0
		5: (224, 57, 15, 255),   #e0390f
		6: (219, 142, 27, 255),  #db8e1b
		7: (245, 2, 145, 255)    #f50291
	}
	
	units = splitSolution(units)

	images = []

	for unit in units:
		for i in range(unit["count"]):
			tmp_img = Image.open(unit["image"])
			tmp_img = tmp_img.convert("RGBA")
			tmp_img = make_tier(tmp_img, unit["tier"])
			tmp_img = make_elite(tmp_img, unit["elite"])
			tmp_img = make_immune(tmp_img, unit["immune"])
			tmp_img = make_bg(tmp_img, unit["star"])
			images += [tmp_img]

	return image_grid(images, border, add_empty)


# In[35]:


def make_tier(image: Image, tier: int) -> Image:
	global tier_image
	for i in range(tier):
		size_mult = 1.3
		tier_image = tier_image.resize(size=(int(10*size_mult), int(14*size_mult)))
		tier_image = tier_image.convert("RGBA")
		image.alpha_composite(tier_image, (1, 2 + 10*i))
	return image


# In[36]:


def make_bg(image: Image, star: int) -> Image:
	global star_image
	bg_box = star_image[star].copy()
	move = int((bg_box.size[0] - image.size[0]) / 2)

	bg_box.alpha_composite(image, (move, move))

	return bg_box


# In[37]:


def image_grid(imgs: list, border: int = 0, add_empty: bool = True) -> Image:

	cols = 6
	rows = ceildiv(len(imgs), cols)

	gap = 7

	toadd = rows*cols - len(imgs)

	if len(imgs) < 6 and not add_empty:
		cols = len(imgs)
		
	bg_color = (22, 22, 22, 255) #161616

	if add_empty:
		for i in range(toadd):
			imgs += [empty_unit]

	w, h = imgs[0].size

	gap_add_w = (cols - 1) * gap
	gap_add_h = (rows - 1) * gap

	grid = Image.new('RGBA', (cols*w + gap_add_w + border*2, rows*h + gap_add_h + border*2), bg_color)
	grid_w, grid_h = grid.size
	for i, img in enumerate(imgs):
		grid.alpha_composite(img, (i % cols*w + (i % cols * gap) + border, i // cols * h + (i // cols * gap) + border))
	return grid


# In[38]:


def all_units():
	all = [i[0] + " Sr" + i[0] for i in sql('SELECT short FROM units')]
	units = ' '.join(all)
	return units


# In[39]:


gen_time = time.time()

lang = "en"

# units = all_units()
# units = "T3OH OAU*4 T3OHU T3SW T3Frost"
units = input("Units: ")

image = gen_image(units, 10, False)

log_generation(units)

image.show()

