import unittest
from ..resolution_wizard import ResolutionWizard

class ResolutionWizardTest(unittest.TestCase):

    def test_guess_primary_dual_monitor(self):
        display_list = ['DP1', 'LVDS1']
        result = ResolutionWizard(display_list).guess_primary()
        self.assertEqual('LVDS1', result)

        display_list = ['HDMI1', 'LVDS1']
        result = ResolutionWizard(display_list).guess_primary()
        self.assertEqual('LVDS1', result)
        
        display_list = ['LVDS2', 'LVDS1']
        result = ResolutionWizard(display_list).guess_primary()
        self.assertEqual('LVDS1', result)

if __name__ == '__main__':
    unittest.main()