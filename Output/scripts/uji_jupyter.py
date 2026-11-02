#!/usr/bin/env python3
"""Menjalankan notebook praktik di antarmuka JupyterLab yang sebenarnya dan memotretnya.

Notebook dibuka di peramban tanpa jendela, seluruh sel dijalankan dari menu Run, lalu sel yang
ditentukan dipotret. Berkas notebook tidak disimpan ulang oleh skrip ini.

Pemakaian: python uji_jupyter.py <folder_data_praktik> <nama_notebook> <folder_foto> <batas_detik> <sel:nama> ...
Memerlukan: jupyterlab, playwright, dan Chromium. Mode windowing JupyterLab dimatikan lewat overrides.json
agar semua sel berada di halaman.
"""
import os
import socket
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright


def port_bebas():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    folder, nama, foto, batas = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    pilih = [a.split(':') for a in sys.argv[5:]]
    os.makedirs(foto, exist_ok=True)
    port = port_bebas()
    # sama seperti mengaktifkan venv: pastikan jupyter-lab dan kernel berasal dari lingkungan ini
    bin_venv = os.path.dirname(sys.executable)
    env = dict(os.environ, PATH=bin_venv + os.pathsep + os.environ['PATH'], VIRTUAL_ENV=os.path.dirname(bin_venv))
    srv = subprocess.Popen([os.path.join(bin_venv, 'jupyter-lab'), '--no-browser', f'--port={port}', '--ServerApp.token=', '--ServerApp.password=', '--ServerApp.disable_check_xsrf=True', f'--ServerApp.root_dir={folder}'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
    try:
        time.sleep(8)
        with sync_playwright() as p:
            br = p.chromium.launch(headless=True, executable_path=os.environ.get('CHROMIUM') or None)
            hal = br.new_page(viewport={'width': 1440, 'height': 900})
            hal.goto(f'http://127.0.0.1:{port}/lab/tree/{nama}', timeout=120000)
            hal.wait_for_selector('.jp-Notebook .jp-Cell', timeout=120000)
            time.sleep(5)
            hal.screenshot(path=os.path.join(foto, 'J01_notebook_terbuka.png'))
            # Run > Run All Cells
            hal.click('.lm-MenuBar-itemLabel:text-is("Run")')
            hal.click('.lm-Menu-itemLabel:text-is("Run All Cells")')
            mulai = time.time()
            time.sleep(5)
            while time.time() - mulai < batas:
                sibuk = hal.evaluate("() => { const n = document.querySelectorAll('.jp-Notebook .jp-InputPrompt'); let s = 0; n.forEach(e => { if (e.textContent.includes('*')) s++; }); return s; }")
                if sibuk == 0:
                    break
                time.sleep(3)
            durasi = time.time() - mulai
            galat = hal.evaluate("() => [...document.querySelectorAll('.jp-OutputArea-output[data-mime-type=\"application/vnd.jupyter.stderr\"]')].map(e => e.textContent.slice(0, 200))")
            kosong = hal.evaluate("() => [...document.querySelectorAll('.jp-Notebook .jp-CodeCell .jp-InputPrompt')].filter(e => !/\\d/.test(e.textContent)).length")
            jumlah = hal.evaluate("() => document.querySelectorAll('.jp-Notebook .jp-CodeCell').length")
            print(f'{nama}: {jumlah} sel kode, {kosong} belum berjalan, durasi {durasi:.0f} detik, keluaran stderr: {galat}')
            # JupyterLab merender sel saat terlihat, jadi gulir setiap sel lalu potret bagian yang diminta
            sel_sel = hal.locator('.jp-Notebook .jp-Cell')
            for i, (no, judul) in enumerate(pilih, start=2):
                # bagian bawah sel, tempat keluarannya berada, diselaraskan dengan bagian bawah layar
                sel_sel.nth(int(no)).evaluate("e => e.scrollIntoView({block: 'end'})")
                time.sleep(1.2)
                hal.screenshot(path=os.path.join(foto, f'J{i:02d}_{judul}.png'))
            br.close()
    finally:
        srv.terminate()


if __name__ == '__main__':
    main()
