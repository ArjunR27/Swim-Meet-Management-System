from src import heat_sheet, psych_sheet


class Tester:
    # Tests the arbitrary entries file and creates a psych sheet and heat sheet for it.
    def test1(self):
        p = psych_sheet.PsychSheet()
        p.parser('entries.txt')
        p.create_psych_sheet('psych_sheet.txt')
        p.create_simple_psych('example_simple_out.txt')

        hs = heat_sheet.HeatSheet()
        hs.parser('example_simple_out.txt')
        hs.create_heat_sheet('heat_sheet.txt')
