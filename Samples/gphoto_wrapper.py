class GPhoto(Wrapper):
    """ A class which wraps calls to the external gphoto2 process. """

    def __init__(self, subprocess):
        Wrapper.__init__(self, subprocess)
        self._CMD = 'gphoto2'
        self._shutter_choices = None
        self._iso_choices = None

    def get_camera_date_time(self):
        code, out, err = self.call(self._CMD + " --get-config /main/status/datetime")
        if code != 0:
            raise Exception(err)
        timestr = None
        for line in out.split('\n'):
            if line.startswith('Current:'):
                timestr = line[line.find(':'):]
        if not timestr:
            raise Exception('No time parsed from ' + out)
        stime = time.strptime(timestr, ": %Y-%m-%d %H:%M:%S")
        return stime


    def capture_image_and_download(self):
        code, out, err = self.call(self._CMD + " --capture-image-and-download")
        if code != 0:
            raise Exception(err)
        filename = None
        for line in out.split('\n'):
            if line.startswith('Saving file as '):
                filename = line.split('Saving file as ')[1]
        return filename

    def get_shutter_speeds(self):
        code, out, err = self.call([self._CMD + " --get-config /main/settings/shutterspeed"])
        if code != 0:
            raise Exception(err)
        choices = {}
        current = None
        for line in out.split('\n'):
            if line.startswith('Choice:'):
                choices[line.split(' ')[2]] = line.split(' ')[1]
            if line.startswith('Current:'):
                current = line.split(' ')[1]
        self._shutter_choices = choices
        return current, choices

    def set_shutter_speed(self, secs=None, index=None):
        code, out, err = None, None, None
        if secs:
            if self._shutter_choices == None:
                self.get_shutter_speeds()
            code, out, err = self.call([self._CMD + " --set-config /main/settings/shutterspeed=" + str(self._shutter_choices[secs])])
        if index:
            code, out, err = self.call([self._CMD + " --set-config /main/settings/shutterspeed=" + str(index)])

    def get_isos(self):
        code, out, err = self.call([self._CMD + " --get-config /main/settings/iso"])
        if code != 0:
            raise Exception(err)
        choices = {}
        current = None
        for line in out.split('\n'):
            if line.startswith('Choice:'):
                choices[line.split(' ')[2]] = line.split(' ')[1]
            if line.startswith('Current:'):
                current = line.split(' ')[1]
        self._iso_choices = choices
        return current, choices

    def set_iso(self, iso=None, index=None):
        code, out, err = None, None, None
        if iso:
            if self._iso_choices == None:
                self.get_isos()
            code, out, err = self.call([self._CMD + " --set-config /main/settings/iso=" + str(self._iso_choices[iso])])
        if index:
            code, out, err = self.call([self._CMD + " --set-config /main/settings/iso=" + str(index)])
