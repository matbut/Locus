import unittest

from common.url import is_valid


class UrlValidationTest(unittest.TestCase):

    def test_incorrect(self):
        urls = [
            'https://www.tvp.info/polska',
            'https://wiadomosci.radiozet.pl/Swiat',
            'https://fakty.interia.pl/autor/joanna-bercal',
            'https://www.tvn24.pl/wiadomosci-z-kraju,3',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid(url))

    def test_correct(self):
        urls = [
            'https://www.rmf.fm/magazyn/news,23722,szescioraczki-po-raz-pierwszy-urodzily-sie-w-polsce.html',
            'https://www.tvp.info/45572287/losowanie-grup-euro-2020-za-nami-wiemy-z-kim-zagraja-polacy',
            'https://fakty.interia.pl/swiat/news-uratowane-w-polsce-tygrysy-sa-w-drodze-do-azylu-w-villenie,nId,3364782',
            'https://www.tvn24.pl/poznan,43/afrykanski-pomor-swin-asf-w-zielonej-gorze-zakaz-wchodzenia-do-lasow,989759.html',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid(url))

    def test_none(self):
        url = 'https://eurosport.tvn24.pl/skoki-narciarskie,408/skoki-narciarskie-kuusamo-2019-kubacki-stoch-i-dolezal-komentarze-puchar-swiata,989831.html'
        self.assertTrue(is_valid(url))


if __name__ == '__main__':
    unittest.main()
