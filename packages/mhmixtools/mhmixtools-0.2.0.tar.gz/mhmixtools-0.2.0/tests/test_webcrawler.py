import unittest
from unittest.mock import patch, Mock
import requests
import mhmixtools.webcrawler as webcrawler

class TestWebcrawler(unittest.TestCase):

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_internal_links(self, mock_get):
        html = '''
        <html>
            <body>
                <a href="/about">About</a>
                <a href="https://example.com/contact">Contact</a>
                <a href="https://external.com/page">External</a>
            </body>
        </html>
        '''
        mock_get.return_value = Mock(status_code=200, text=html)
        url = 'https://example.com'
        links = webcrawler.get_internal_links(url)
        self.assertIn('https://example.com/about', links)
        self.assertIn('https://example.com/contact', links)
        self.assertNotIn('https://external.com/page', links)

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_internal_links_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        links = webcrawler.get_internal_links('https://example.com')
        self.assertEqual(links, [])

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_external_links(self, mock_get):
        html = '''
        <html>
            <body>
                <a href="https://external.com/page">External</a>
                <a href="/internal">Internal</a>
            </body>
        </html>
        '''
        mock_get.return_value = Mock(status_code=200, text=html)
        url = 'https://example.com'
        links = webcrawler.get_external_links(url)
        self.assertIn('https://external.com/page', links)
        self.assertNotIn('https://example.com/internal', links)

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_external_links_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        links = webcrawler.get_external_links('https://example.com')
        self.assertEqual(links, [])

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_image_links(self, mock_get):
        html = '''
        <html>
            <body>
                <img src="/img1.png"/>
                <img src="https://example.com/img2.jpg"/>
                <img src="https://external.com/img3.gif"/>
            </body>
        </html>
        '''
        mock_get.return_value = Mock(status_code=200, text=html)
        url = 'https://example.com'
        links = webcrawler.get_image_links(url)
        self.assertIn('https://example.com/img1.png', links)
        self.assertIn('https://example.com/img2.jpg', links)
        self.assertIn('https://external.com/img3.gif', links)

    @patch('mhmixtools.webcrawler.requests.get')
    def test_get_image_links_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        links = webcrawler.get_image_links('https://example.com')
        self.assertEqual(links, [])

    @patch('mhmixtools.webcrawler.get_internal_links')
    def test_crawl_site(self, mock_internal_links):
        # Simulate a small site graph
        mock_internal_links.side_effect = [
            ['https://example.com/about', 'https://example.com/contact'],
            [],
            []
        ]
        links = webcrawler.crawl_site('https://example.com', depth=1)
        self.assertIn('https://example.com/about', links)
        self.assertIn('https://example.com/contact', links)

    @patch('mhmixtools.webcrawler.requests.get')
    def test_check_broken_pages(self, mock_get):
        # First URL is OK, second is 404, third raises exception
        mock_get.side_effect = [
            Mock(status_code=200),
            Mock(status_code=404),
            requests.RequestException("Timeout")
        ]
        urls = ['https://ok.com', 'https://notfound.com', 'https://timeout.com']
        broken = webcrawler.check_broken_pages(urls)
        self.assertIn(('https://notfound.com', 404), broken)
        self.assertTrue(any(url == 'https://timeout.com' for url, _ in broken))

    @patch('mhmixtools.webcrawler.crawl_site')
    @patch('mhmixtools.webcrawler.get_external_links')
    @patch('mhmixtools.webcrawler.get_image_links')
    @patch('mhmixtools.webcrawler.check_broken_pages')
    def test_generate_site_report(self, mock_broken, mock_images, mock_external, mock_crawl):
        mock_crawl.return_value = ['https://example.com', 'https://example.com/about']
        mock_external.side_effect = [['https://ext.com'], []]
        mock_images.side_effect = [['https://example.com/img.png'], []]
        mock_broken.return_value = [('https://example.com/about', 404)]
        report = webcrawler.generate_site_report('https://example.com', depth=1)
        self.assertIn('internal_links', report)
        self.assertIn('external_links', report)
        self.assertIn('image_links', report)
        self.assertIn('broken_pages', report)
        self.assertIn('https://example.com', report['internal_links'])
        self.assertIn('https://ext.com', report['external_links'])
        self.assertIn(('https://example.com/about', 404), report['broken_pages'])

    def test_print_site_report(self):
        # Just ensure it prints without error
        report = {
            'internal_links': ['https://example.com'],
            'external_links': ['https://ext.com'],
            'image_links': ['https://example.com/img.png'],
            'broken_pages': [('https://example.com/about', 404)]
        }
        webcrawler.print_site_report(report)

    @patch('builtins.open')
    @patch('json.dump')
    def test_save_site_report_json(self, mock_json_dump, mock_open):
        report = {'internal_links': [], 'external_links': [], 'image_links': [], 'broken_pages': []}
        webcrawler.save_site_report(report, filename='test.json', format='json')
        mock_open.assert_called_once_with('test.json', 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()

    @patch('builtins.open')
    @patch('csv.writer')
    def test_save_site_report_csv(self, mock_csv_writer, mock_open):
        mock_writer = Mock()
        mock_csv_writer.return_value = mock_writer
        report = {
            'internal_links': ['https://example.com'],
            'external_links': ['https://ext.com'],
            'image_links': ['https://example.com/img.png'],
            'broken_pages': [('https://example.com/about', 404)]
        }
        webcrawler.save_site_report(report, filename='test.csv', format='csv')
        mock_open.assert_called_once_with('test.csv', 'w', newline='', encoding='utf-8')
        self.assertTrue(mock_writer.writerow.called)

    @patch('mhmixtools.webcrawler.logging')
    def test_save_site_report_invalid_format(self, mock_logging):
        report = {'internal_links': [], 'external_links': [], 'image_links': [], 'broken_pages': []}
        webcrawler.save_site_report(report, filename='test.txt', format='txt')
        mock_logging.error.assert_called_with("Unsupported format. Use 'json' or 'csv'.")

if __name__ == '__main__':
    unittest.main()