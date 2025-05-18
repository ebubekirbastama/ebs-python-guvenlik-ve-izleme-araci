import subprocess
import shutil
import re
import customtkinter as ctk
from tkinter import filedialog
import tkinter.ttk as ttk

# Temayı ayarla
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ana pencere
app = ctk.CTk()
app.geometry("1000x700")
app.title("🛡️ Güvenlik & İzleme Aracı")

# Sekmeler
notebook = ctk.CTkTabview(app)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

sec_general = notebook.add("🗂️ Genel")
sec_process = notebook.add("⚙️ Process")
sec_startup = notebook.add("🚀 Başlangıç")
sec_scan = notebook.add("🔍 Taramalar")

# Treeview widget'ları
general_tree = ttk.Treeview(sec_general, show='headings')
general_tree.pack(fill="both", expand=True, padx=10, pady=5)

process_tree = ttk.Treeview(sec_process, show='headings')
process_tree.pack(fill="both", expand=True, padx=10, pady=5)

startup_tree = ttk.Treeview(sec_startup, show='headings')
startup_tree.pack(fill="both", expand=True, padx=10, pady=5)

scan_tree = ttk.Treeview(sec_scan, show='headings')
scan_tree.pack(fill="both", expand=True, padx=10, pady=5)

# PowerShell komutunu çalıştırıp Treeview'a yazan fonksiyon
def run_command(command, treeview=None):
    powershell_path = shutil.which("powershell") or r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    try:
        result = subprocess.run(
            [powershell_path, "-Command", command],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        output = result.stdout if result.stdout else result.stderr
        if treeview:
            # Treeview temizle
            treeview.delete(*treeview.get_children())

            lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
            if not lines:
                treeview.insert("", "end", values=("Çıktı boş.",))
                return

            # Başlıkları ayır (tab veya 2+ boşluk ile)
            headers = re.split(r'\t|\s{2,}', lines[0])
            headers = [h.strip() for h in headers if h.strip()]
            if not headers:
                headers = ["Çıktı"]

            treeview["columns"] = headers
            for col in headers:
                treeview.heading(col, text=col)
                treeview.column(col, width=200, anchor="w")

            for line in lines[1:]:
                row = re.split(r'\t|\s{2,}', line)
                row = [c.strip() for c in row]
                # Hücre sayısını başlık sayısına eşitle
                if len(row) < len(headers):
                    row += [""] * (len(headers) - len(row))
                elif len(row) > len(headers):
                    row = row[:len(headers)]
                treeview.insert("", "end", values=row)
        else:
            print(output)
    except Exception as e:
        if treeview:
            treeview.delete(*treeview.get_children())
            treeview.insert("", "end", values=(f"Hata: {str(e)}",))
        else:
            print(f"Hata: {str(e)}")

# --- Genel Sekme Fonksiyonları ---

def list_hidden_files():
    folder = filedialog.askdirectory(title="Gizli Dosyaların Olduğu Klasörü Seçin")
    if folder:
        cmd = f'Get-ChildItem -Path "{folder}" -Force | Where-Object {{ $_.Attributes -match "Hidden" }} | Select-Object Name, FullName'
        run_command(cmd, general_tree)

def clean_file_attributes():
    file = filedialog.askopenfilename(title="Silinmeyen Dosyayı Seçin", filetypes=[("Executable Files", "*.exe"), ("Tüm Dosyalar", "*.*")])
    if file:
        cmd = f'attrib -S -H -R "{file}"'
        # Temizleme komutu çıktı üretmez, bilgilendirme için tabloyu güncelle
        run_command(f'"{cmd}"', general_tree)
        general_tree.delete(*general_tree.get_children())
        general_tree.insert("", "end", values=(f"{file} dosyasının Sistem, Gizli ve Salt Okunur özellikleri kaldırıldı.",))

ctk.CTkButton(sec_general, text="🗂️ Gizli Dosyaları Listele", command=list_hidden_files).pack(pady=5)
ctk.CTkButton(sec_general, text="🧹 Silinmeyen Dosyayı Temizle", command=clean_file_attributes).pack(pady=5)

# --- Process Sekme Fonksiyonları ---

def list_processes():
    cmd = 'Get-Process | Select-Object Name, Id'
    run_command(cmd, process_tree)

def find_process_path():
    dlg = ctk.CTkInputDialog(text="Process adı girin (örnek: notepad):", title="Process Dizin Bul")
    pname = dlg.get_input()
    if pname:
        cmd = f'Get-Process {pname} | Select-Object Id, Path, ProcessName'
        run_command(cmd, process_tree)
    else:
        process_tree.delete(*process_tree.get_children())
        process_tree.insert("", "end", values=("Process adı boş bırakıldı.",))

def kill_process():
    dlg = ctk.CTkInputDialog(text="Durdurmak istediğiniz Process ID'sini girin:", title="Process Durdur")
    pid = dlg.get_input()
    if pid and pid.isdigit():
        cmd = f'Stop-Process -Id {pid} -Force'
        run_command(cmd)
        process_tree.delete(*process_tree.get_children())
        process_tree.insert("", "end", values=(f"Process ID {pid} durduruldu.",))
    else:
        process_tree.delete(*process_tree.get_children())
        process_tree.insert("", "end", values=("Geçersiz veya boş Process ID girdiniz.",))

def file_hash():
    file = filedialog.askopenfilename(title="Hash alınacak dosyayı seçin", filetypes=[("Executable Files", "*.exe"), ("Tüm Dosyalar", "*.*")])
    if file:
        cmd = f'Get-FileHash "{file}" -Algorithm MD5 | Select-Object Algorithm, Hash, Path'
        run_command(cmd, process_tree)

ctk.CTkButton(sec_process, text="📋 Tüm Processleri Listele", command=list_processes).pack(pady=5)
ctk.CTkButton(sec_process, text="📌 Process Dizin Bul", command=find_process_path).pack(pady=5)
ctk.CTkButton(sec_process, text="🛑 Process Durdur", command=kill_process).pack(pady=5)
ctk.CTkButton(sec_process, text="🔑 Dosya Hash Al", command=file_hash).pack(pady=5)

# --- Başlangıç Sekme Fonksiyonları ---

def list_run_registry():
    cmd = 'Get-ItemProperty "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" | Select-Object *'
    run_command(cmd, startup_tree)

def scan_scheduled_tasks():
    dlg = ctk.CTkInputDialog(text="1) Tüm Zamanlayıcıları Listele\n2) İsimle Ara\nSeçiminiz (1 veya 2):", title="Zamanlayıcı Tara")
    choice = dlg.get_input()
    if choice == "1":
        cmd = 'Get-ScheduledTask | Select-Object TaskName, State, LastRunTime, NextRunTime'
        run_command(cmd, startup_tree)
    elif choice == "2":
        dlg2 = ctk.CTkInputDialog(text="Aramak istediğiniz görev adını yazın:", title="Görev Adı")
        name = dlg2.get_input()
        if name:
            cmd = f'Get-ScheduledTask | Where-Object {{ $_.TaskName -like "*{name}*" }} | Select-Object TaskName, State, LastRunTime, NextRunTime'
            run_command(cmd, startup_tree)
        else:
            startup_tree.delete(*startup_tree.get_children())
            startup_tree.insert("", "end", values=("Görev adı boş bırakıldı.",))
    else:
        startup_tree.delete(*startup_tree.get_children())
        startup_tree.insert("", "end", values=("Geçersiz seçim.",))

ctk.CTkButton(sec_startup, text="📝 Run Kayıtlarını Listele", command=list_run_registry).pack(pady=5)
ctk.CTkButton(sec_startup, text="⏰ Zamanlayıcıları Tara", command=scan_scheduled_tasks).pack(pady=5)

# --- Taramalar Sekme Fonksiyonları ---

def scan_directory():
    folder = filedialog.askdirectory(title="Tarama için klasör seçin")
    if folder:
        cmd = f'Get-ChildItem -Path "{folder}" -Recurse | Select-Object Name, FullName'
        run_command(cmd, scan_tree)

def list_services():
    cmd = 'Get-Service | Select-Object Name, Status, DisplayName'
    run_command(cmd, scan_tree)

ctk.CTkButton(sec_scan, text="📁 Klasördeki Dosyaları Tara", command=scan_directory).pack(pady=5)
ctk.CTkButton(sec_scan, text="🔧 Çalışan Servisleri Listele", command=list_services).pack(pady=5)

# Uygulamayı çalıştır
app.mainloop()
