import json
import os
import random
import time

# --- KONFIGURASI ---
DB_FILE = "database_ilmu.json"
APP_NAME = "KOULEGH LITERASI"
VERSI = "1.0.0"

# --- UTILITIES ---
def bersihkan_layar():
    """Membersihkan terminal agar tampilan rapi."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    bersihkan_layar()
    print("="*50)
    print(f"   🧠  {APP_NAME} v{VERSI}")
    print("       Build Your Second Brain via CLI")
    print("="*50)

# --- FUNGSI DATABASE ---
def muat_database():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {} # Handle jika file rusak

def simpan_database(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print("✅ Data berhasil disimpan! (Auto-saved)")
    time.sleep(1)

# --- FITUR UTAMA ---
def tambah_ilmu(data):
    banner()
    print("✍️  TAMBAH CATATAN BARU\n")
    istilah = input("🔤 Masukkan Istilah/Kata Kunci : ").strip().title()
    
    if not istilah: return # Cegah input kosong

    if istilah in data:
        print(f"\n⚠️  Istilah '{istilah}' sudah ada di database!")
        input("\nTekan Enter untuk kembali...")
        return

    kategori = input("🏷️  Masukkan Kategori (cth: Aset): ").strip()
    definisi = input("📝 Masukkan Penjelasan         : ").strip()
    
    data[istilah] = {
        "definisi": definisi,
        "kategori": kategori,
        "tanggal": time.strftime("%Y-%m-%d") # Fitur baru: Tanggal
    }
    simpan_database(data)

def cari_ilmu(data):
    banner()
    print("🔍  PENCARIAN SMART\n")
    keyword = input("Ketik kata kunci: ").strip().lower()
    
    found = False
    print("-" * 50)
    for key, info in data.items():
        if keyword in key.lower() or keyword in info['definisi'].lower():
            print(f"📌 {key.upper()} ({info['kategori']})")
            print(f"   💡 {info['definisi']}")
            print("-" * 50)
            found = True
    
    if not found:
        print("❌ Tidak ditemukan data yang cocok.")
    
    input("\nTekan Enter untuk kembali...")

def mode_flashcard(data):
    banner()
    if not data:
        print("❌ Database kosong. Tambah ilmu dulu dong!")
        input("\nTekan Enter untuk kembali...")
        return

    print("🧠  MODE FLASHCARD (Uji Ingatan)\n")
    keys = list(data.keys())
    
    while True:
        soal = random.choice(keys)
        print(f"Jelaskan konsep: 👉  [{soal.upper()}]")
        print("(Kategori: " + data[soal]['kategori'] + ")")
        
        input("\n... Tekan [ENTER] untuk melihat kunci jawaban ...")
        
        print(f"\n✅ JAWABAN: {data[soal]['definisi']}")
        print("=" * 50)
        
        lagi = input("Lanjut? (y/n): ").lower()
        if lagi != 'y':
            break
        print("-" * 50)

def lihat_semua(data):
    banner()
    print(f"📚 TOTAL DATABASE: {len(data)} ILMU\n")
    
    # Sortir berdasarkan abjad biar rapi
    for i, key in enumerate(sorted(data.keys()), 1):
        print(f"{i}. {key} [{data[key]['kategori']}]")
    
    input("\nTekan Enter untuk kembali...")

# --- MENU UTAMA ---
def main():
    data_ilmu = muat_database()
    
    while True:
        banner()
        print("1. ➕ Tambah Catatan Baru")
        print("2. 🔍 Cari Ilmu")
        print("3. 🧠 Mode Ujian (Flashcard)")
        print("4. 📂 Lihat Semua List")
        print("5. 🚪 Keluar")
        print("-" * 50)
        
        pilihan = input("Pilih menu [1-5]: ")
        
        if pilihan == "1": tambah_ilmu(data_ilmu)
        elif pilihan == "2": cari_ilmu(data_ilmu)
        elif pilihan == "3": mode_flashcard(data_ilmu)
        elif pilihan == "4": lihat_semua(data_ilmu)
        elif pilihan == "5": 
            print("👋 Keep Learning, Stay Foolish!")
            break

if __name__ == "__main__":
    main()
