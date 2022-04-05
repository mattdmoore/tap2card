from psychopy import core, visual, event
from os import listdir
from re import findall


class Screen(visual.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=[1., 1., 1.], allowGUI=False)
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

    def uneven_taps(self):
        self.pages[10].draw()
        self.flip()

    def incorrect_rhythm(self):
        self.pages[11].draw()
        self.flip()

    def incorrect_metre(self):
        self.pages[12].draw()
        self.flip()

#     def rhythm_visualiser(self, rhythm, no_flip=False):
#
#         if isinstance(rhythm, list):
#             for i, r in enumerate(rhythm):
#                 boxes = self.box_notation(r, i)
#                 [b.draw() for b in boxes]
#
#         else:
#             boxes = self.box_notation(rhythm, 0)
#             [b.draw() for b in boxes]
#
#         if not no_flip:
#             self.flip()
#
#     def box_notation(self, rhythm, i):
#         box_size = .05
#         boxes = [visual.Rect(self,
#                              box_size, box_size,
#                              lineColor=None,
#                              fillColor='black' if r == 1 else 'white',
#                              pos=(x_position(j, box_size, len(rhythm)), i * box_size * 1.1))
#                  for j, r in enumerate(rhythm)]
#         return boxes
#
#
# def x_position(i, box_size, n):
#     return (i * box_size * 1.1) - (n * box_size * 1.1 / 2)
