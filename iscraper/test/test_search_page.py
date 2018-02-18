from unittest import TestCase
from unittest.mock import MagicMock, patch, call

import urllib.parse

from iscraper import search_url, programme_id, episodes, programme_from_title,\
  films

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
          
class TestProgrammeFromTitle(TestCase):
  def test_title_series_episode(self):
    self.assertEqual({
      'series': 2,
      'episode': 1,
      'episode_title': 'Episode 1',
    }, programme_from_title('Series 2: Episode 1'))

  def test_title_episode(self):
    self.assertEqual({
      'series': 1,
      'episode': 5,
      'episode_title': 'Beat Feet',
    }, programme_from_title('5. Beat Feet'))
    
class TestFilms(TestCase):
  def test_all_films_multiple_pages(self):
    with patch('urllib.request.urlopen',
        side_effect=(open('iscraper/test/BBC iPlayer - Films.html'),
                     open('iscraper/test/BBC iPlayer - Films 2.html'),
                     open('iscraper/test/BBC iPlayer - Films 3.html'))) \
        as mock_urlopen:
        fs = films()
        self.assertEqual(24, len(fs))
        self.assertEqual({
            'pid': 'b04jj2zn',
            'title': 'Before the Winter Chill',
          },fs[1])
        # Query strings
        self.assertEqual([{
            'sort': ['atoz'],
            'page': ['1'],
          },{
            'sort': ['atoz'],
            'page': ['2'],
          },{
            'sort': ['atoz'],
            'page': ['3'],
          }
        ],[urllib.parse.parse_qs(urllib.parse.urlparse(args[0]).query) 
            for name, args, kwargs in mock_urlopen.mock_calls])
        # Pages
        self.assertEqual([
          ('https', 'www.bbc.co.uk', '/iplayer/categories/films/all', {
            'sort': ['atoz'],
            'page': ['1'],
          }),
          ('https', 'www.bbc.co.uk', '/iplayer/categories/films/all', {
            'sort': ['atoz'],
            'page': ['2'],
          }),
          ('https', 'www.bbc.co.uk', '/iplayer/categories/films/all', {
            'sort': ['atoz'],
            'page': ['3'],
          })
        ],[(u.scheme, u.netloc, u.path, urllib.parse.parse_qs(u.query)) 
            for u in [urllib.parse.urlparse(args[0])
              for name, args, kwargs in mock_urlopen.mock_calls]])
          
