from psychopy import core, visual, event
from os import listdir
from re import findall


class Screen(visual.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=[1., 1., 1.])
        self.mouse = event.Mouse(visible=False, win=self)
        self.frame_rate = self.getActualFrameRate()

        # Fix number ordering with missing leading zeros
        files = sorted(listdir('instructions'), key=lambda x: int(*findall(r'\d+', x)))
        self.pages = [visual.ImageStim(self, 'instructions/' + f) for f in files]

    def instructions(self):
        last_page = 9
        navigation_dict = {'left': -1,
                           'right': 1,
                           'return': 0,
                           'escape': 'quit'}

        i = 0
        while i <= last_page:
            self.pages[i].draw()
            self.flip()

            press = event.waitKeys()[0]
            if press in navigation_dict.keys():
                key = navigation_dict[press]

                if key is 'quit':
                    core.quit()

                elif key == i < 2:  # First 2 pages
                    i += 1

                elif 1 < i < last_page:  # LR navigation
                    i += key

                elif i == last_page:  # Last page
                    if key < 0:
                        i += key
                    elif key == 0:
                        i += 1

    def main_experiment(self):
        self.pages[19].draw()
        self.flip()
        enter_to_continue()

    def trial_complete(self, trial_num):
        slide_map = {'0': 18,
                     '1': 28,
                     '2': 38}

        idx = str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()
        enter_to_continue()

    def show_rhythm(self, trial_num, practice=False):
        slide_map = {'p0': 10,
                     'r0': 16,
                     'p1': 20,
                     'r1': 26,
                     'p2': 29,
                     'r2': 35}

        idx = 'p' if practice else 'r'
        idx += str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()

    def stop(self, trial_num, practice=False):
        slide_map = {'p0': 15,
                     'r0': 17,
                     'p1': 25,
                     'r1': 27,
                     'p2': 34,
                     'r2': 36}

        idx = 'p' if practice else 'r'
        idx += str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()
        enter_to_continue()

    def uneven_taps(self, trial_num):
        slide_map = {'0': 11,
                     '1': 21,
                     '2': 30}

        idx = str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()

    def correct_rhythm(self, trial_num):
        slide_map = {'0': 38,
                     '1': 39,
                     '2': 40}

        idx = str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()

    def incorrect_rhythm(self, trial_num, short):
        slide_map = {'s0': 12,
                     'l0': 13,
                     's1': 22,
                     'l1': 23,
                     's2': 31,
                     'l2': 32}

        idx = 's' if short else 'l'
        idx += str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()

    def incorrect_metre(self, trial_num):
        slide_map = {'0': 14,
                     '1': 24,
                     '2': 33}

        idx = str(trial_num)
        self.pages[slide_map[idx]].draw()
        self.flip()

    def finished(self):
        self.pages[37].draw()
        self.flip()
        enter_to_continue()


def enter_to_continue():
    while True:
        press = event.waitKeys()[0]
        if press == 'return':
            return
        elif press == 'escape':
            core.quit()
        else:
            continue
