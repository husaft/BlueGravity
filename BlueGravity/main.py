import threading
import asyncio
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from os.path import join
from datetime import datetime
from core_input import save_json, load_json, create_dir
from core_meta import parse_person_data
from core_mass import find_bmi_range, calc_bmi
from core_table import write_table
from core_scan import init_scan, run_scan


class BlueWindow(Gtk.Window):
    def __init__(self, data_dir):
        super().__init__(title="Blue Gravity")

        self.person_j_file = join(data_dir, 'person.json')
        self.person = parse_person_data(load_json(self.person_j_file))
        self.measure_j_file = join(data_dir, 'measurement.json')
        self.measure_c_file = join(data_dir, 'measurement.csv')
        self.measurement = load_json(self.measure_j_file)
        self.current_packet = None

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.mframe = Gtk.Frame()
        self.mframe.set_label(" Measuring")
        self.box.add(self.mframe)

        self.mgrid = Gtk.Grid()
        self.mframe.add(self.mgrid)

        self.time_label = Gtk.Label()
        self.time_label.set_text("---")
        self.time_label.set_hexpand(True)
        self.mgrid.attach(self.time_label, 0, 0, 1, 1)

        self.weight_label = Gtk.Label()
        self.weight_label.set_text("---")
        self.weight_label.set_hexpand(True)
        self.mgrid.attach(self.weight_label, 0, 1, 1, 1)

        self.device_label = Gtk.Label()
        self.device_label.set_text("---")
        self.device_label.set_hexpand(True)
        self.mgrid.attach(self.device_label, 0, 2, 1, 1)

        self.signal_scale = Gtk.ProgressBar(show_text=True)
        self.signal_scale.set_text("Signal strength")
        self.signal_scale.set_hexpand(True)
        self.mgrid.attach(self.signal_scale, 0, 3, 1, 1)

        self.pframe = Gtk.Frame()
        self.pframe.set_label(" Person")
        self.box.add(self.pframe)

        self.pgrid = Gtk.Grid()
        self.pframe.add(self.pgrid)

        self.birth_label = Gtk.Label()
        self.birth_label.set_text("---")
        self.birth_label.set_hexpand(True)
        self.pgrid.attach(self.birth_label, 0, 0, 1, 1)

        self.age_label = Gtk.Label()
        self.age_label.set_text("---")
        self.age_label.set_hexpand(True)
        self.pgrid.attach(self.age_label, 0, 1, 1, 1)

        self.height_label = Gtk.Label()
        self.height_label.set_text("---")
        self.height_label.set_hexpand(True)
        self.pgrid.attach(self.height_label, 0, 2, 1, 1)

        self.iframe = Gtk.Frame()
        self.iframe.set_label(" Interpretation")
        self.box.add(self.iframe)

        self.igrid = Gtk.Grid()
        self.iframe.add(self.igrid)

        self.bmi_label = Gtk.Label()
        self.bmi_label.set_text("---")
        self.bmi_label.set_hexpand(True)
        self.igrid.attach(self.bmi_label, 0, 0, 1, 1)

        self.update_person()
        self.scan_thread = threading.Thread(target=self.do_loop, daemon=True)
        self.scan_thread.start()

    def update_person(self):
        birth = self.person['birthdate'].strftime("%A, %d %B %Y")
        self.birth_label.set_text(f"{birth}")

        height = self.person['height_m']
        self.height_label.set_text(f"{height} meters")

        age = self.person['age']
        self.age_label.set_text(f"{age['y']} years, {age['m']} months, {age['d']} days")

    def do_loop(self):
        scanner = init_scan(self.on_data)
        asyncio.run(run_scan(scanner))

    def update_view(self):
        signal_val = self.current_packet['s']
        signal_scale_val = 1.0 - (((signal_val * -1) - 20) / 100.0)
        self.signal_scale.set_fraction(signal_scale_val)

        is_final = self.current_packet['f']
        weight_val = self.current_packet['w']
        weight_val_txt = weight_val if is_final else f"~ {weight_val}"
        self.weight_label.set_markup(f"<big>{weight_val_txt}</big> kg")

        dev_name = self.current_packet['n']
        self.device_label.set_markup(f"{dev_name}")

        ts_value = self.current_packet['t']
        ts_date = datetime.fromisoformat(ts_value)
        ts_date_txt = ts_date.strftime("%A, %d %B %Y")
        self.time_label.set_markup(f"<i>{ts_date_txt}</i>")

        height_m = self.person['height_m']
        age_y = self.person['age']['y']
        bmi = calc_bmi(weight_val, height_m, age_y, new_exp=False)
        bmi_b = f"{bmi['b']:.02f}"
        bmi_c = bmi['c']

        rang = find_bmi_range(height_m, age_y, new_exp=False)
        r_lines = list()
        r_lines.append(f"Your BMI is {bmi_b}")
        r_lines.append(f"This is {bmi_c}." + '\n')
        bmi_c_target = rang[bmi_c]['min'] - 0.1
        bmi_c_loss = weight_val - bmi_c_target
        bmi_n = calc_bmi(bmi_c_target, height_m, age_y, new_exp=False)['c']
        r_lines.append(f"minus {bmi_c_loss:.02f} kg would be {bmi_n}...")
        r_text = '\n'.join(r_lines)
        self.bmi_label.set_text(r_text)

    def on_data(self, data):
        self.current_packet = data
        if data['f']:
            min_key = data['t'][:16]
            self.measurement[min_key] = data
            save_json(self.measurement, self.measure_j_file)
            write_table(self.measure_c_file, self.measurement)
        self.update_view()


def run_app(root):
    win = BlueWindow(root)
    win.set_default_size(460, 400)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    run_app(create_dir('data'))
