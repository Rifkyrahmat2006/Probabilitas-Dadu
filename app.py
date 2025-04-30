from flask import Flask, render_template, request

app = Flask(__name__)

# Simpan hanya dua lemparan terakhir
roll_history = []

def calculate_probability(roll):
    global roll_history
    
    # Tambahkan lemparan baru dan pastikan hanya menyimpan dua lemparan terakhir
    roll_history.append(roll)
    if len(roll_history) > 2:
        roll_history = roll_history[-2:]
    
    # Jika belum ada cukup data (kurang dari 2 lemparan)
    if len(roll_history) < 2:
        probability = 1/6  # Probabilitas dasar untuk dadu 6-sisi
        steps = [
            "Belum cukup data untuk perhitungan probabilitas lemparan ketiga.",
            "Dibutuhkan minimal 2 lemparan sebelumnya.",
            "Probabilitas dasar untuk dadu 6-sisi: P(x) = 1/6 = 0.1667."
        ]
        return round(probability, 4), steps
    
    # Hitung probabilitas berdasarkan dua lemparan terakhir
    first_roll = roll_history[0]
    second_roll = roll_history[1]
    
    # Penjelasan pola
    if first_roll == second_roll:
        probability = 1/5
        pola = "Dua lemparan terakhir SAMA ({} dan {}).".format(first_roll, second_roll)
        rumus = "P(lemparan ketiga sama) = 1/5"
        substitusi = f"P({first_roll} | dua sebelumnya {first_roll}) = 1/5 = 0.2"
        alasan = "Karena dua hasil sebelumnya sama, peluang munculnya angka yang sama pada lemparan ketiga diasumsikan lebih besar (misal, karena pola atau asumsi tertentu)."
    else:
        probability = 1/6
        pola = "Dua lemparan terakhir BERBEDA ({} dan {}).".format(first_roll, second_roll)
        rumus = "P(lemparan ketiga angka tertentu) = 1/6"
        substitusi = f"P(x | dua sebelumnya berbeda) = 1/6 = 0.1667"
        alasan = "Karena dua hasil sebelumnya berbeda, peluang setiap angka tetap sama besar."
    
    steps = [
        "Langkah 1: Catat dua lemparan terakhir:",
        f"  - Lemparan pertama: {first_roll}",
        f"  - Lemparan kedua: {second_roll}",
        "",
        "Langkah 2: Analisis Pola:",
        f"  - {pola}",
        "",
        "Langkah 3: Tentukan Rumus Peluang:",
        f"  - {rumus}",
        "",
        "Langkah 4: Substitusi Nilai:",
        f"  - {substitusi}",
        "",
        "Langkah 5: Penjelasan:",
        f"  - {alasan}",
        "",
        "Langkah 6: Hasil Akhir:",
        f"  - Probabilitas lemparan ketiga = {round(probability, 4)}"
    ]
    
    return round(probability, 4), steps

@app.route('/', methods=['GET', 'POST'])
def index():
    global roll_history
    probability = None
    steps = None
    if request.method == 'POST':
        try:
            roll = int(request.form['roll'])
            if 1 <= roll <= 6:  # Hanya menerima nilai 1-6 karena dadu 6-sisi
                probability, steps = calculate_probability(roll)
        except (ValueError, KeyError):
            pass
    return render_template('index.html', probability=probability, steps=steps, roll_history=roll_history)

if __name__ == '__main__':
    app.run(debug=True) 