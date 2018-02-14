from unittest import TestCase
from unittest.mock import MagicMock, patch

from iscraper import search_url, programme_id, episodes

class TestSearchURL(TestCase):
  def test_no_special_chars(self):
    self.assertEqual('https://www.bbc.co.uk/iplayer/search?q=Modus',
                     search_url('Modus'))

  def test_space(self):
    self.assertEqual('https://www.bbc.co.uk/iplayer/search?q=Hard+Sun',
                     search_url('Hard Sun'))

class TestProgrammesFromSearchPage(TestCase):
  def test_one_prog_none_linked_no_series_no_episode(self):
    with patch('urllib.request.urlopen', 
        return_value=open(
        'iscraper/test/BBC iPlayer - Search - julius caesar revealed.html')) \
        as mock_urlopen:
      self.assertEqual('b09s0mxj', programme_id('Julius Caesar Revealed'))
      mock_urlopen.assert_called_with(
          'https://www.bbc.co.uk/iplayer/search?q=Julius+Caesar+Revealed')

  def test_two_progs_one_page_two_linked(self):
    with patch('urllib.request.urlopen', 
        return_value=open(
        'iscraper/test/BBC iPlayer - Search - modus.html')) \
        as mock_urlopen:
      self.assertEqual('b0644tbl', programme_id('Modus'))
      mock_urlopen.assert_called_with(
          'https://www.bbc.co.uk/iplayer/search?q=Modus')

class TestEpisodeIds(TestCase):
  def test_multiple_episodes(self):
    with patch('urllib.request.urlopen', 
        return_value=open(
        'iscraper/test/BBC iPlayer - Modus.html')) \
        as mock_urlopen:
      self.assertEqual([{
        'pid': 'b09mktwz',
        'brand': 'Modus',
        'series': 2,
        'episode': 1,
        'episode_title': 'Episode 1',
      },{
        'pid': 'b09chwwq',
        'brand': 'Modus',
        'series': 2,
        'episode': 2,
        'episode_title': 'Episode 2',
      }], episodes('b0644tbl'))
      mock_urlopen.assert_called_with(
          'https://www.bbc.co.uk/iplayer/episodes/b0644tbl')

  def test_cbbc_danger_mouse(self):
    with patch('urllib.request.urlopen', 
        return_value=open(
        'iscraper/test/BBC iPlayer - Danger Mouse.html')) \
        as mock_urlopen:
      es = episodes('--DMPID--')
      self.assertEqual(36, len(es))
      self.assertEqual({
        'pid': 'b06jm5q8',
        'brand': 'Danger Mouse',
        'series': 1,
        'episode': 13,
        'episode_title': 'The Unusual Suspects',
      },es[0])  
      self.assertEqual({
        'pid': 'b09dc9l0',
        'brand': 'Danger Mouse',
        'series': 2,
        'episode': 23,
        'episode_title': 'The Scare Mouse Project',
      },es[-1])  
      #TODO: second page of results?
      mock_urlopen.assert_called_with(
          'https://www.bbc.co.uk/iplayer/episodes/--DMPID--')
