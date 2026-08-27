from dotenv import dotenv_values
import sys
from pathlib import Path
import requests
import asyncio
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))
from models import Element

config = dotenv_values(".env")

def generate_description(path):
    # max 1024 characters
    desc = 'TEST'
    return desc

def remove_pdf(path):
    if path is not None:
        Path(path).unlink(missing_ok=True)

def save_pdf(config, uuid):
    url = f"http://{config['DOMAIN']}:{config['PROXY_PORT']}/files/{uuid}.pdf"
    path = Path(f'{uuid}.pdf').resolve()
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        print('File!')
        return path
    else:
        print('No file!')
        return None 

DATABASE_HOST = config.get("DOMAIN", "localhost")
DATABASE_PORT = config.get("POSTGRES_PORT", "5432")
DATABASE_URL = (
    f"postgresql+asyncpg://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{config['POSTGRES_DB']}"
)

async def async_main(element_uuid, path):
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with AsyncSession(engine) as session:
        query = (
            update(Element)
            .where(Element.uuid == element_uuid)
            .values(description=generate_description(path))
        )
        await session.execute(query)
        await session.commit()

    await engine.dispose()


def run_update():

    
    
    element_uuid = uuid_entry.get().strip()
    if not element_uuid:
        messagebox.showwarning("No UUID")
        return

    run_button.config(state=tk.DISABLED)

    def update_in_background():

        path = save_pdf(config, element_uuid)

        try:
            asyncio.run(async_main(element_uuid, path))
        except Exception as error:
            root.after(0, lambda: messagebox.showerror("Błąd", str(error)))
        else:
            root.after(0, lambda: messagebox.showinfo("Gotowe", "Opis został zmieniony."))
        finally:
            remove_pdf(path)
            root.after(0, lambda: run_button.config(state=tk.NORMAL))

    threading.Thread(target=update_in_background, daemon=True).start()


root = tk.Tk()
root.title("Zmiana opisu elementu")
root.resizable(False, False)

tk.Label(root, text="UUID elementu:").pack(padx=20, pady=(20, 5))
uuid_entry = tk.Entry(root, width=45)
uuid_entry.pack(padx=20, pady=5)
run_button = tk.Button(root, text="Run", command=run_update)
run_button.pack(pady=(5, 20))

root.mainloop()