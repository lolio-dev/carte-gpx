from pathlib import Path

raw_wp = """
  <wpt lat="$lt$" lon="$lg$">
    <name>$name$</name>
  </wpt>
"""


def create_file(name: str, description: str):
	template = Path('template.gpx').read_text().replace('$name$', name).replace('$desc$', description)

	new_file = Path(f'{name}.gpx')
	new_file.touch()
	new_file.write_text(template)

	return new_file


def create_wp(lt: int, lg: int, label: str):
    return raw_wp.replace('$lt$', str(lt)).replace('$lg$', str(lg)).replace('$name$', str(label))


def add_wps(new_wps, file_name, file_description):
	wps = []
	for x, i in new_wps:
		wps.append(create_wp(i['latitude'], i['longitude'], i['emplacement']))

	print(''.join(wps))

	file = create_file(file_name, file_description)
	content = file.read_text()

	file.write_text(content.replace('$wpt$', ''.join(wps)))
