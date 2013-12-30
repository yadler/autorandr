import unittest
from unittest_data_provider import data_provider
from ..resolution_wizard import ResolutionWizard

class ResolutionWizardTest(unittest.TestCase):
    displays = lambda: (
        ( 'LVDS1', ['DP1', 'LVDS1']   ),
        ( 'LVDS1', ['HDMI1', 'LVDS1'] ),
        ( 'LVDS1', ['LVDS2', 'LVDS1'] ),
        ( 'LVDS2', ['LVDS2', 'DP1'] ),
        ( 'DP1'  , ['HDMI1', 'DP1']   )
    )

    @data_provider(displays)
    def test_guess_primary(self, expected, display_list):
        result = ResolutionWizard(display_list).guess_primary()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()