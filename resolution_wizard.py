class ResolutionWizard:
    INTERNAL_DISPLAYS = ['LVDS']
    EXTERNAL_DISPLAYS = ['DP', 'HDMI', 'DVI', 'VGA', 'S-video', 'TV']

    def __init__(self, display_list):
        self.display_list = sorted(display_list)

    def guess_primary(self):
        for internal_display in self.INTERNAL_DISPLAYS:
            for connected_display in self.display_list:
                if connected_display.startswith(internal_display):
                    return connected_display

        for external_display in self.EXTERNAL_DISPLAYS:
            for connected_display in self.display_list:
                if connected_display.startswith(external_display):
                    return connected_display
                    
        return None

