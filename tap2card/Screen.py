from psychopy import core, visual, event
from os import listdir
from re import findall


class Screen(visual.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=[1., 1., 1.], allowGUI=False)
        self.mouse = event.Mouse(visible=False, win=self)
        self.frame_rate = self.getActualFrameRate()

        files = sorted(listdir('instructions'), key=lambda x: int(*findall(r'\d+', x)))
        self.pages = [visual.ImageStim(self, 'instructions/' + f) for f in files]

    def instructions(self):
        navigation_dict = {'left': -1,
                           'right': 1,
                           'return': 0,
                           'escape': 'quit'}

        i = 0
        while i < 9:
            self.pages[i].draw()
            self.flip()

            press = event.waitKeys()[0]
            if press in navigation_dict.keys():
                key = navigation_dict[press]

                if key is 'quit':
                    core.quit()

                elif key == i < 2:  # First 2 pages
                    i += 1

                elif 1 < i < 8:  # LR navigation
                    i += key

                elif i == 8:  # Last page
                    if key < 0:
                        i += key
                    elif key == 0:
                        i += 1

    def show_rhythm(self, trial_num, practice=False):
        i = 0
        if trial_num == 0:
            i = 9 if practice else 13
        elif trial_num == 1:
            i = 17 if practice else 18
        elif trial_num == 2:
            i = 20 if practice else 21

        # print('show', i)
        self.pages[i].draw()
        self.flip()
        # event.waitKeys()

    def stop(self, practice=False):
        i = 14 if practice else 19
        # print('stop', i)
        self.pages[i].draw()
        self.flip()
        # event.waitKeys()

    def finish(self):
        self.pages[-1].draw()
        self.flip()
        # event.waitKeys()

    def uneven_taps(self, trial_num):
        slide_map = {'0': 11,
                     '1': 21,
                     '2': 30}

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
