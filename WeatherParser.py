__author__ = 'AbbyTheRat'

class weather_parser():
    """
    translate XML into a object.

    Allows for translating tags into the correct word. Most likely a better way to do this but eh, AbbyTheRat is new to
    Python. At least this make it easier to create a new lang map for translating at least the weather part into another
    language.

    Maybe another day, I'll refactor this to share lang_map across all the objects and share get get_unit function.
    Possible this is better as a single class. This works fine for me.
    """
    def __init__(self, xml_root):

        xml_loc = xml_root.find('loc')
        xml_cc = xml_root.find('cc')
        xml_units = xml_root.find('head')

        ob_units = weather_units(xml_units)
        ob_loc = weather_loc(xml_loc)
        ob_currentconditions = weather_cc(xml_cc)


class weather_units():
    """
        Defines basic infomation about the data received, such as unit.
    """
    lang_map = {'locale': 'locale', 'form': 'form', 'head':'units', 'ut': 'temperature', 'ud': 'distance', 'us': 'speed',
                'up': 'pressure', 'ur': 'rainfall'}
    data_map = None

    def __init__(self, xml_units):
        self.create_units(xml_units)

    def create_units(self, xml_units):
        #TODO - check tags
        for units in xml_units:
            self.data_map = {units.tag: units.text}
            print self.get_unit(units.tag)

    def get_unit(self, tag):
        #TODO check tags - raise exception for invalid tags(missing from lang_map), or display tags missing data
        arr_tag = []
        if tag in self.lang_map:
            arr_tag.append(self.lang_map[tag])
        else:
            arr_tag.append('tag: ' + tag)  # if no tags in lang_map - print tag
        if tag in self.data_map:
            arr_tag.append(self.data_map[tag])
        else:
            arr_tag.append('Missing data')

        return arr_tag

class weather_cc():
    """
        Defines current conditions(cc). Such as current temperature, wind speed and humidity
    """

    data_map = None
    lang_map = {'cc': 'current conditions', 'lsup': 'last updated', 'obst': 'weather station', 'tmp': 'temperature',
                'flik': 'feels like', 't': 'text', 'icon': 'icon', 'bar': 'barometer', 'r': 'reading', 'd': 'direction',
                'wind': 'wind', 's': 'speed', 'gust': 'gusting', 'hmid': 'humidity', 'vis': 'visibility',
                'uv': 'UV', 'i': 'index', 'dewp': 'dew point', 'moon': 'moon phase'}

    def __init__(self, xml_cc):
        self.create_cc(xml_cc)

    def create_cc(self, xml_cc):
        for cc in xml_cc:
            if len(cc) > 0:
                for nested_cc in list(cc):
                    self.data_map = {cc.tag + '_' + nested_cc.tag: nested_cc.text}
                    print self.get_cc(nested_cc.tag, cc.tag)

            self.data_map = {cc.tag: cc.text}
            print self.get_cc(cc.tag)

    def get_cc(self, tag, parent_tag=None):

        arr_tag = []
        if parent_tag is not None:
            pparent_tag = parent_tag + '_' + tag
        else :
            pparent_tag = tag

        if tag in self.lang_map:
            arr_tag.append(self.lang_map[tag])
        else:
            arr_tag.append('tag: ' + tag)

        if pparent_tag in self.data_map:
            arr_tag.append(self.data_map[pparent_tag])
        else:
            arr_tag.append('Missing data')

        if parent_tag is not None:
            arr_tag.append(parent_tag)

        return arr_tag


class weather_loc():
    """
        Defines infomation about the location of the weather. Such as timezone, longitude/latitude, sunset/rise times.

    """
    lang_map = {'loc': 'location id', 'dnam': 'name', 'tm': 'time', 'lat': 'latitude', 'lon': 'longitude',
                'sunr': 'sunrise', 'suns': 'sunset', 'zone': 'timezone'}
    data_map = None

    def __init__(self, xml_loc):
        self.create_loc(xml_loc)

    def create_loc(self, xml_loc):
        for loc in xml_loc:
            if loc == 'loc':
                self.data_map = {loc.tag: loc.attrib}
            else:
                self.data_map = {loc.tag: loc.text}

            print self.get_loc(loc.tag)

    def get_loc(self, tag):
        arr_tag = []
        if tag in self.lang_map:
            arr_tag.append(self.lang_map[tag])
        else:
            arr_tag.append('tag: ' + tag) #if no tags in lang_map - print tag
        if tag in self.data_map:
            arr_tag.append(self.data_map[tag])
        else:
            arr_tag.append('Missing data')

        return arr_tag