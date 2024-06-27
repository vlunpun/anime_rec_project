import unittest
from unittest.mock import patch, MagicMock
from animesketch import get_anime_by_title, get_similar_anime

class TestAnimeRecommendations(unittest.TestCase):

    @patch('requests.get')
    def test_get_anime_by_title(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [{'mal_id': 20, 'title': 'Naruto', 'url': 'https://api.jikan.moe/v4/anime/20'}]}
        mock_get.return_value = mock_response

        anime_title = 'Naruto'
        result = get_anime_by_title(anime_title)

        self.assertEqual(result['mal_id'], 20)
        self.assertEqual(result['title'], 'Naruto')
        self.assertEqual(result['url'], 'https://api.jikan.moe/v4/anime/20')

    @patch('requests.get')
    def test_get_similar_anime(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': [{'entry': {'mal_id': 20, 'title': 'Naruto', 'url': 'https://api.jikan.moe/v4/anime/20'}}]}
        mock_get.return_value = mock_response

        anime_id = 20
        result = get_similar_anime(anime_id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['entry']['mal_id'], 20)
        self.assertEqual(result[0]['entry']['title'], 'Naruto')
        self.assertEqual(result[0]['entry']['url'], 'https://api.jikan.moe/v4/anime/20')


if __name__ == '__main__':
    unittest.main()