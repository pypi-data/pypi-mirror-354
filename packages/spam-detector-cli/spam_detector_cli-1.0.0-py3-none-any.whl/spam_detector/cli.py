def main():
    print("Spam Detector CLI aktif")
    import pandas as pd
    import requests
    from io import StringIO
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import os, sys, csv, re

    print("CWD:", os.getcwd())
    print("FILE EXISTS:", os.path.exists("spam.csv"))

    # Load data
    df = pd.read_csv("spam.csv", encoding="latin-1", sep=',', skipinitialspace=True, usecols=[0, 1])
    df.columns = ['label', 'text']
    df.dropna(subset=['text'], inplace=True)
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})

    # Load data from api
    def load_csv_from_api(url):
        headers = {'Authorization': 'Bearer YOUR_API_TOKEN'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        csv_text = response.text
        df = pd.read_csv(StringIO(csv_text), usecols=[0, 1], encoding='latin-1')
        df.columns = ['label', 'text']
        df.dropna(subset=['text'], inplace=True)
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})
        return df

    def bersihkan(teks):
        teks = re.sub(r'\W+', ' ', teks)      # hapus tanda baca
        teks = re.sub(r'\d+', '', teks)       # hapus angka
        teks = teks.lower().strip()
        return teks.strip()

    
    #df = load_csv_from_api()
    df['text'] = df['text'].apply(bersihkan)

    # Vectorisasi & training
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    print("✅ Model dilatih. Akurasi:", accuracy_score(y_test, model.predict(X_test)))

    # Prediksi teks
    def prediksi_email(teks):
        vektorisasi = vectorizer.transform([teks])
        hasil = model.predict(vektorisasi)
        return "SPAM 🛑📧" if hasil[0] == 1 else "HAM"# Clear log
    def clear_log():
        if os.path.exists(logfile):
            with open(logfile, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["teks", "hasil"])
            print("🧹 Log prediksi berhasil dibersihkan.")
        else:
            print("📂 Belum ada file log untuk dibersihkan.")

    # Prediksi dari file
    def prediksi_dari_file(nama_file):
        if not os.path.exists(nama_file):
            print(f"❌ File '{nama_file}' tidak ditemukan.")
            return

        print(f"📂 Membaca dari: {nama_file}")
        hasil_prediksi = []

        try:
            with open(nama_file, 'r', encoding='utf-8') as f:
                for baris in f:
                    teks = baris.strip()
                    if teks:
                        hasil = prediksi_email(teks)
                        hasil_prediksi.append((teks, hasil))
                        print(f"- {hasil}: {teks}")

            # Simpan hasil ke log
            with open(logfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(hasil_prediksi)

            print(f"✅ {len(hasil_prediksi)} baris berhasil diprediksi & disimpan ke log.")

        except Exception as e:
            print("⚠️ Gagal membaca file:", e)


    # Logging prediksi
    logfile = "log_prediksi.csv"
    if not os.path.exists(logfile):
        with open(logfile, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["teks", "hasil"])

    # Loop CLI
    print("\n📩 CLI Spam Detector:")
    print("- Ketik isi email → akan diprediksi")
    print("- Ketik 'stats' → lihat statistik")
    print("- Ketik 'clear' → bersihkan log")
    print("- Ketik 'predictfile [namafile.txt]' → deteksi dari file")
    print("- Ketik 'exit' → keluar\n")

    def tampilkan_help():
        print("""
    📌 Panduan Perintah Spam Detector:

        Ketik kalimat email       → Deteksi SPAM / HAM
        stats                     → Lihat statistik deteksi
        clear                     → Hapus isi log prediksi
        predictfile namafile.txt → Deteksi SPAM dari banyak email dalam file
        exit                      → Keluar dari program
        --help atau -h            → Tampilkan panduan ini
    """)

    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        tampilkan_help()
        sys.exit(0)


    # Simpan model dan vectorizer
    joblib.dump(model, "app/model.joblib")
    joblib.dump(vectorizer, "app/vectorizer.joblib")
    print("💾 Model dan vectorizer disimpan ke 'app/model.joblib' dan 'app/vectorizer.joblib'")


    while True:
        teks = input("\nMasukkan perintah atau teks email: ").strip()
        if teks.lower() == "exit":
            print("👋 Keluar dari program. Sampai jumpa!")
            break
        elif teks.lower() == "stats":
            if os.path.exists(logfile):
                df_log = pd.read_csv(logfile)
                total = len(df_log)
                spam = len(df_log[df_log["hasil"] == "SPAM"])
                ham = len(df_log[df_log["hasil"] == "HAM"])
                print(f"\n📊 Total: {total}, SPAM: {spam}, HAM: {ham}")
            else:
                print("📂 Belum ada data log.")
        elif teks.lower() == "clear":
            clear_log()
        elif teks.lower().startswith("predictfile"):
            parts = teks.split()
            if len(parts) == 2:
                prediksi_dari_file(parts[1])
            else:
                print("⚠️ Format: predictfile namafile.txt")
        else:
            hasil = prediksi_email(teks)
            print("🔍 Hasil prediksi:", hasil)
            with open(logfile, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([teks, hasil])



if __name__ == "__main__":
    main()
