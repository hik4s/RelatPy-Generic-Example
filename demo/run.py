"""Run: python -m demo.run --inicio 2026-11-01 --fim 2026-11-03"""
import argparse
import asyncio
import copy
import json
from pathlib import Path

from playwright.async_api import async_playwright

from core import executor
from demo.site import DemoSite, REPORTS, validate_period


async def run_demo(start, end, output, headed=False):
    """One batch per process, matching the existing executor's global state model."""
    validate_period(start, end)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    previous = executor.PASTA_STATUS, executor.CAMINHO_STATUS, executor.SEMAFORO
    executor.PASTA_STATUS = str(output / 'status')
    executor.CAMINHO_STATUS = str(output / 'status/status.json')
    executor.SEMAFORO = asyncio.Semaphore(3)
    try:
        executor.inicializar_status([{'modulo': name} for name in REPORTS])
        with DemoSite() as site:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=not headed)
                try:
                    context = await browser.new_context(accept_downloads=True)
                    # Prevent the demonstration from sending requests beyond its local site.
                    async def local_only(route):
                        if route.request.url.startswith(site.url + '/'):
                            await route.continue_()
                        else:
                            await route.abort()
                    await context.route('**/*', local_only)

                    async def download(name):
                        page = await context.new_page()
                        page.set_default_timeout(10000)
                        try:
                            await page.goto(site.url + '/relatorio/' + name)
                            await page.get_by_label('Início', exact=True).fill(start)
                            await page.get_by_label('Fim', exact=True).fill(end)
                            async with page.expect_download() as pending:
                                await page.get_by_role('button', name='Baixar CSV').click()
                            item = await pending.value
                            if item.suggested_filename != name + '.csv':
                                raise ValueError('Download não corresponde ao relatório solicitado.')
                            target = output / (name + '.csv')
                            await item.save_as(target)
                            if not target.is_file() or not target.stat().st_size:
                                raise ValueError('Download vazio ou ausente.')
                            executor.atualizar_arquivo(name, str(target))
                            if name == 'vendas':
                                await page.screenshot(path=str(output / 'demo.png'), full_page=True)
                            return {'status': 'CONCLUIDO'}
                        finally:
                            await page.close()

                    results = await executor.executar_lote([
                        executor.executar_relatorio(download(name), name) for name in REPORTS
                    ])
                    errors = [result for result in results if isinstance(result, BaseException)]
                    if errors:
                        raise RuntimeError(f'{len(errors)} relatório(s) falharam; consulte status/status.json.') from errors[0]
                finally:
                    await browser.close()
        return copy.deepcopy(executor.STATUS)
    finally:
        executor.PASTA_STATUS, executor.CAMINHO_STATUS, executor.SEMAFORO = previous


def main():
    parser = argparse.ArgumentParser(description='RelatPy: três relatórios fictícios via navegador local.')
    parser.add_argument('--inicio', default='2026-11-01')
    parser.add_argument('--fim', default='2026-11-03')
    parser.add_argument('--output', type=Path, default=Path('demo-output'))
    parser.add_argument('--headed', action='store_true', help='Mostrar o Chromium durante a execução.')
    args = parser.parse_args()
    try:
        result = asyncio.run(run_demo(args.inicio, args.fim, args.output, args.headed))
    except (ValueError, RuntimeError) as error:
        parser.exit(1, f'Erro: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
