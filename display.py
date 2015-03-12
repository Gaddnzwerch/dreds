import subprocess

class Display():

    def display(self, a_list):
        self.clear()
        m_format = '{:' + chr(9472) + '^51}'
        print(chr(9484) + m_format.format('') + chr(9488))
        for m_row in a_list:
            m_string = ""
            for m_value in m_row:
                m_string += m_value
            print(chr(9474) + m_string + chr(9474))
        print(chr(9492) + m_format.format('') + chr(9496))

    def clear(self):
        subprocess.call( "cls" , shell=True)
