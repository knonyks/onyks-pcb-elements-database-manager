import os
import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def database_config():
	return {
		"host": os.getenv("DB_HOST", "localhost"),
		"port": os.getenv("DB_PORT", os.getenv("POSTGRES_PORT", "5432")),
		"dbname": os.getenv("DB_NAME", os.getenv("POSTGRES_DB")),
		"user": os.getenv("DB_USER", os.getenv("POSTGRES_USER")),
		"password": os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD")),
	}


def add_user():
	login = login_var.get().strip()
	password = password_var.get()
	email = email_var.get().strip()
	rank = rank_var.get().strip()

	if not all((login, password, email, rank)):
		messagebox.showwarning("Brak danych", "Uzupełnij wszystkie pola.")
		return

	config = database_config()
	missing = [key for key in ("dbname", "user", "password") if not config[key]]
	if missing:
		messagebox.showerror(
			"Brak konfiguracji",
			"Brak zmiennych w .env: "
			+ ", ".join(
				{
					"dbname": "POSTGRES_DB",
					"user": "POSTGRES_USER",
					"password": "POSTGRES_PASSWORD",
				}[key]
				for key in missing
			),
		)
		return

	connection = None
	try:
		connection = psycopg2.connect(**config)
		with connection.cursor() as cursor:
			cursor.execute(
				"""
				INSERT INTO private.users (login, password, email, rank)
				VALUES (%s, crypt(%s, gen_salt('bf')), %s, %s)
				""",
				(login, password, email, rank),
			)
		connection.commit()
		messagebox.showinfo("Sukces", f"Użytkownik {login!r} został dodany.")
		login_var.set("")
		password_var.set("")
		email_var.set("")
	except psycopg2.Error as error:
		if connection:
			connection.rollback()
		messagebox.showerror("Błąd bazy danych", str(error).strip())
	except Exception as error:
		messagebox.showerror("Błąd", str(error))
	finally:
		if connection:
			connection.close()


root = tk.Tk()
root.title("Dodaj użytkownika")
root.resizable(False, False)

frame = ttk.Frame(root, padding=16)
frame.grid()

login_var = tk.StringVar()
password_var = tk.StringVar()
email_var = tk.StringVar()
rank_var = tk.StringVar(value="editor")

fields = (
	("Login", login_var, False),
	("Hasło", password_var, True),
	("E-mail", email_var, False),
	("Ranga", rank_var, False),
)
for row, (label, variable, secret) in enumerate(fields):
	ttk.Label(frame, text=label + ":").grid(row=row, column=0, sticky="w", pady=4)
	ttk.Entry(frame, textvariable=variable, show="*" if secret else "", width=32).grid(
		row=row, column=1, pady=4, padx=(10, 0)
	)

ttk.Button(frame, text="Dodaj użytkownika", command=add_user).grid(
	row=len(fields), column=0, columnspan=2, pady=(12, 0)
)

root.mainloop()