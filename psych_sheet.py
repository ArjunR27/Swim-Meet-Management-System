import time


class PsychSheet:
    def __init__(self):
        self.dict_of_events = {'50YDButterfly': [], '100YDButterfly': [], '200YDButterfly': [],
                               '50YDBackstroke': [], '100YDBackstroke': [], '200YDBackstroke': [],
                               '50YDBreaststroke': [], '100YDBreaststroke': [], '200YDBreaststroke': [],
                               '50YDFreestyle': [], '100YDFreestyle': [], '200YDFreestyle': [],
                               '500YDFreestyle': [], '1000YDFreestyle': [], '1650YDFreestyle': [],
                               '100YDIM': [], '200YDIM': [], '400YDIM': []}

    def add(self, person):
        p_event = person[0]
        self.dict_of_events[p_event] += [person]

    def parser(self, input):
        global psych_sheet
        psych_sheet = PsychSheet()
        # Creates the dictionary, with all swimmers inside the events (unsorted)
        with open(input) as in_file:
            for line in in_file:
                line_list = line.split()
                event, f_name, l_name, team, seed_time = line_list[0], line_list[1], line_list[2], line_list[3], line_list[4]
                # If the entry time is set as 'NT' set it to an arbitrary time which is very large as to correct the
                # ordering
                if 'NT' in seed_time:
                    seed_time = self.get_seconds('90:00.00')
                elif ':' in seed_time:
                    seed_time = self.get_seconds(seed_time)
                else:
                    seed_time = float(seed_time)
                new_person = (event, f_name, l_name, team, seed_time)
                psych_sheet.add(new_person)
            # Sort the dictionary, via the times within each person tuple
            for event in psych_sheet.dict_of_events:
                n_list = psych_sheet.dict_of_events[event]
                n_list.sort(key=lambda x: x[4])

    def create_simple_psych(self, output):
        with open(output, 'w') as out_file:
            for event in psych_sheet.dict_of_events:
                n_list = psych_sheet.dict_of_events[event]
                for person in n_list:
                    out_file.write(person[0] + ' ' + person[1] + ' ' + person[2] + ' ' + person[3] + ' ' + self.reformat_to_time(
                        str(person[4])) + '\n')
                out_file.write('\n')

    def create_psych_sheet(self, output):
        # Creates the psych sheet, and writes to a python text file
        with open(output, 'w') as out_file:
            out_file.write('Psych Sheet: ' + '\n\n')
            count = 0
            for event in psych_sheet.dict_of_events:
                out_file.write('Event: ' + event + '\n')
                n_list = psych_sheet.dict_of_events[event]
                for person in n_list:
                    count += 1
                    out_file.write(str(count) + ')' + ' ' + person[1] + ' ' +
                                   person[2] + ' ' + person[3] + ' ' + self.reformat_to_time(str(person[4])) + '\n')
                out_file.write('\n')
                count = 0

    @staticmethod
    def get_seconds(time):
        # Converts the time format into a seconds representation of that time
        # gets the seconds for a time format in the form 00:00.00
        minutes = ''
        sec = ''
        milli = ''
        if len(time) < 8:
            minutes = time[0]
            sec = time[2:4]
            milli = time[5:]
        elif len(time) == 8:
            minutes = time[0:2]
            sec = time[3:5]
            milli = time[6:]
        return_time = 60 * float(minutes) + float(sec) + (float(milli) / 100)
        return round(float(return_time), 2)

    @staticmethod
    def reformat_to_time(time):
        # Reformat the seconds representation of the time into a minutes:seconds.milliseconds representation
        # time = '5400.0' is the default time that is set if someone is given an entry time of 'NT this feature is
        # implemented due to the fact that the ordering of the psych/heat sheet is based upon floating point numbers
        # since the entry 'NT' is a string, convert it into the floating point representation of a large time (90:00.00)
        if time == '5400.0':
            return 'NT'
        else:
            x = float(time)
            minutes = int(x) // 60
            seconds = int(x) % 60
            milliseconds = int((time.split('.', 1)[1]))
            if minutes >= 1:
                formatted_string = '{:d}:{:02d}.{:02d}'.format(minutes, seconds, milliseconds)
            else:
                formatted_string = '{:02d}.{:02d}'.format(seconds, milliseconds)
            return formatted_string


st = time.time()
p = PsychSheet()
p.parser('entries.txt')
p.create_psych_sheet('psych_sheet.txt')
p.create_simple_psych('example_simple_out.txt')
end = time.time()
print(end - st)