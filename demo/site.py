"""Small local report website. No corporate systems or credentials are used."""
import csv
from datetime import date
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import io
from threading import Thread
from urllib.parse import parse_qs, urlsplit

REPORTS = {'vendas': 'Vendas', 'estoque': 'Estoque', 'atendimentos': 'Atendimentos'}


def validate_period(start, end):
    first, last = date.fromisoformat(start), date.fromisoformat(end)
    if first > last:
        raise ValueError('A data inicial deve ser anterior ou igual à final.')
    return first, last


STYLE = '''body{font:17px system-ui;background:#101820;color:#edf2f7;margin:0}
main{max-width:850px;margin:60px auto;padding:24px}h1{font-size:36px}
a{color:#77d8bb}nav{display:flex;gap:24px;margin:32px 0}label{display:block;margin:20px 0}
input,button{font:inherit;padding:12px;border-radius:8px;border:1px solid #789}
button{background:#77d8bb;color:#101820;cursor:pointer}small{color:#bccbd7}
section{padding:24px;background:#1b2936;border-radius:16px}footer{margin-top:36px;color:#bccbd7}'''


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def send(self, status, body, kind='text/html; charset=utf-8', filename=None):
        data = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        if filename:
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlsplit(self.path)
        parts = url.path.strip('/').split('/')
        if parts[0] == 'download':
            if len(parts) != 2 or parts[1] not in REPORTS:
                return self.send(404, 'Relatório desconhecido.')
            try:
                params = parse_qs(url.query)
                start, end = validate_period(params['inicio'][0], params['fim'][0])
            except (KeyError, ValueError):
                return self.send(400, 'Período inválido.')
            output = io.StringIO(newline='')
            writer = csv.writer(output)
            writer.writerow(['id', 'data', 'relatorio', 'descricao', 'quantidade'])
            name = parts[1]
            for day in range(1, 4):
                current = date(2026, 11, day)
                if start <= current <= end:
                    writer.writerow([f'{name}-{day}', current.isoformat(), name,
                                     f'Registro fictício {day}', day * 10])
            return self.send(200, '\ufeff' + output.getvalue(), 'text/csv; charset=utf-8', name + '.csv')
        if url.path == '/':
            content = '<h1>RelatPy · ambiente de demonstração</h1><p>Escolha um relatório para testar a extração.</p>'
        elif len(parts) == 2 and parts[0] == 'relatorio' and parts[1] in REPORTS:
            name = parts[1]
            content = f'''<h1>{escape(REPORTS[name])}</h1><section>
<form action="/download/{name}" method="get">
<label>Início <input name="inicio" type="date" value="2026-11-01" required></label>
<label>Fim <input name="fim" type="date" value="2026-11-03" required></label>
<button type="submit">Baixar CSV</button></form></section>'''
        else:
            return self.send(404, 'Página não encontrada.')
        links = ''.join(f'<a href="/relatorio/{name}">{label}</a>' for name, label in REPORTS.items())
        self.send(200, f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>RelatPy · Demo</title>
<style>{STYLE}</style><main><small>DEMONSTRAÇÃO LOCAL · DADOS FICTÍCIOS</small>
<nav>{links}</nav>{content}<footer>Amostras: 1 a 3 de novembro de 2026.
Nenhum acesso a sistemas corporativos. Os filtros alteram as linhas do CSV.</footer></main></html>''')


class DemoSite:
    def __enter__(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'
        return self

    def __exit__(self, *_args):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


if __name__ == '__main__':
    import time
    with DemoSite() as site:
        print(site.url, flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
