from psychopy import visual


class Screen(visual.Window):
    def __init__(self, size, backend='pyglet'):
        super().__init__(size, color=[0., 0., 0.], winType=backend, allowGUI=False)
        self.frame_rate = self.getActualFrameRate()

    def instructions(self):
        pass

    def trial_feedback(self):
        pass
