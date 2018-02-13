from unittest import TestCase
from unittest.mock import MagicMock, patch

from iscraper import get_iplayer

class TestGetIplayer(TestCase):
  @patch('subprocess.call')
  def test_valid_programme(self, subprocess_call):
    prog = {
      'pid': 'ab1234',
      'brand': 'The Brand',
      'series': 6,
      'episode': 12,
      'episode_title': 'The Last One',
    }

    get_iplayer(prog, 'the/output/dir')

    subprocess_call.assert_called_with([
      '/usr/bin/get-iplayer',
      '--type', 'tv',
      '--pid', 'ab1234',
      '--file-prefix', 'The Brand-s06e12-The Last One',
      '--output', 'the/output/dir',
    ])
    
