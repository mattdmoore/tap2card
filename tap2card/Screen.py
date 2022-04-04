from psychopy import visual, event


class Screen(visual.Window):
    def __init__(self, size, backend='pyglet'):
        super().__init__(size, color=[0., 0., 0.], winType=backend, allowGUI=False)
        self.frame_rate = self.getActualFrameRate()

    def instructions(self):
        pass
        # TODO: Replace with Ece's image instructions instead?
        # task = visual.TextBox2(self,
        #                        'Task: tap your finger on the drum pad to produce the rhythm you see on the screen')
        # rules = visual.TextBox2(self,
        #                         'Please tap according to the following rules:\n'
        #                         '- Time goes from left to right\n'
        #                         '- Each box lasts the same amount of time\n'
        #                         '- Black means tap and white means wait\n'
        #                         '- Tap in a loop, meaning start from the beginning once you reach the end\n'
        #                         '   as if the first box follows the last box\n'
        #                         '- Stop only when the word stop is displayed on the screen\n')
        # rules.draw()
        # self.flip()

    def trial_feedback(self, ioi, strength):
        text = visual.TextBox2(self,
                               'IOI: {0:.1f}ms\nConfidence: {1:.1f}%'.format(ioi, strength * 100),
                               pos=(0, .2),
                               alignment='center')
        text.draw()

    def uneven_taps(self):
        text = visual.TextBox2(self,
                               'IOI: uneven taps\nConfidence: uneven taps',
                               pos=(0, .2),
                               alignment='center')
        text.draw()

    def rhythm_visualiser(self, rhythm, no_flip=False):

        if isinstance(rhythm, list):
            for i, r in enumerate(rhythm):
                boxes = self.box_notation(r, i)
                [b.draw() for b in boxes]

        else:
            boxes = self.box_notation(rhythm, 0)
            [b.draw() for b in boxes]

        if not no_flip:
            self.flip()

    def box_notation(self, rhythm, i):
        box_size = .05
        boxes = [visual.Rect(self,
                             box_size, box_size,
                             lineColor=None,
                             fillColor='black' if r == 1 else 'white',
                             pos=(x_position(j, box_size, len(rhythm)), i * box_size * 1.1))
                 for j, r in enumerate(rhythm)]
        return boxes


def x_position(i, box_size, n):
    return (i * box_size * 1.1) - (n * box_size * 1.1 / 2)
