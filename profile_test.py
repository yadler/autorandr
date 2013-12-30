import unittest
import profile

class ProfileTest(unittest.TestCase):

    def test_docking_station_yves(self):
        xrand_out = """Screen 0: minimum 320 x 200, current 1920 x 1080, maximum 32767 x 32767
                    LVDS1 connected (normal left inverted right x axis y axis)
                       1280x800       60.0 +   50.0  
                       1024x768       60.0  
                       800x600        60.3     56.2  
                       640x480        59.9  
                    VGA1 disconnected (normal left inverted right x axis y axis)
                    HDMI1 disconnected (normal left inverted right x axis y axis)
                    DP1 connected 1920x1080+0+0 (normal left inverted right x axis y axis) 521mm x 293mm
                       1920x1080      60.0*+   59.9  
                       1680x1050      59.9  
                       1280x1024      75.0     60.0  
                       1440x900       75.0     59.9  
                       1280x960       60.0  
                       1152x864       75.0  
                       1280x720       60.0     50.0     59.9  
                       1440x576       50.0  
                       1024x768       75.1     70.1     60.0  
                       832x624        74.6  
                       800x600        72.2     75.0     60.3     56.2  
                       720x576        50.0  
                       720x480        60.0     59.9  
                       640x480        75.0     72.8     66.7     60.0     59.9  
                       720x400        70.1  
                    VIRTUAL1 disconnected (normal left inverted right x axis y axis)"""
        result = profile.parse_xrandr_query(xrand_out)
        expected = {'LVDS1': {'default': '1280x800', 'connected': True}, 'DP1': {'default': '1920x1080', 'current': '1920x1080', 'connected': True}}
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()