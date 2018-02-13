from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open

from iscraper import get_iplayer, download_history

class TestRunGetIplayer(TestCase):
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
    
class TestDownloadHistory(TestCase):
  def test_valid_history_file(self):
    download_data = [
      'ab1234|Some downl|oad data\n', 
      'cd5678|Some more d|ownload data\n',
      'ef9012|sdfgsd|dghghfgdf|fdgsdg',
    ]
    o = mock_open(read_data=''.join(download_data))
    o.return_value.__iter__ = lambda self: self
    o.return_value.__next__ = lambda self: next(iter(self.readline, ''))

    with patch('os.path.expanduser', 
               return_value='/home/user/.get_iplayer/download_history') \
        as mock_expanduser:
      with patch('builtins.open', o) as mock_file:
        self.assertEqual(['ab1234','cd5678','ef9012'],
          download_history())
        mock_file.assert_called_with('/home/user/.get_iplayer/download_history')
        mock_expanduser.assert_called_with('~/.get_iplayer/download_history')

