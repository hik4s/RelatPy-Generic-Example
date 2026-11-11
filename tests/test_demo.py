import asyncio
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from demo.site import DemoSite
from demo.run import run_demo, validate_period


class DemoTests(unittest.TestCase):
    def test_period_rejects_invalid_and_reversed_dates(self):
        for start, end in [('2026-13-01', '2026-11-03'), ('2026-11-03', '2026-11-01')]:
            with self.assertRaises(ValueError):
                validate_period(start, end)

    def test_site_download_is_filtered_and_unknown_reports_rejected(self):
        with DemoSite() as site:
            with urlopen(site.url + '/download/vendas?inicio=2026-11-02&fim=2026-11-02') as response:
                rows = list(csv.DictReader(io.StringIO(response.read().decode('utf-8-sig'))))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['data'], '2026-11-02')
            with self.assertRaises(HTTPError) as error:
                urlopen(site.url + '/download/desconhecido?inicio=2026-11-01&fim=2026-11-03')
            self.assertEqual(error.exception.code, 404)

    def test_bad_period_returns_400(self):
        with DemoSite() as site:
            with self.assertRaises(HTTPError) as error:
                urlopen(site.url + '/download/vendas?inicio=errado&fim=2026-11-03')
            self.assertEqual(error.exception.code, 400)

    def test_parallel_browser_downloads_match_reports_and_record_status(self):
        with tempfile.TemporaryDirectory() as temp:
            result = asyncio.run(run_demo('2026-11-01', '2026-11-03', Path(temp)))
            self.assertEqual(set(result), {'vendas', 'estoque', 'atendimentos'})
            for name, item in result.items():
                self.assertEqual(item['status'], 'CONCLUIDO')
                path = Path(item['arquivo_local'])
                self.assertEqual(path.name, name + '.csv')
                rows = list(csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))))
                self.assertEqual(len(rows), 3)
                self.assertEqual({row['relatorio'] for row in rows}, {name})
            saved = json.loads((Path(temp) / 'status/status.json').read_text(encoding='utf-8'))
            self.assertEqual(saved, result)


if __name__ == '__main__':
    unittest.main()
