import re
import psycopg2
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from difflib import SequenceMatcher
from difflib import get_close_matches
from sqlalchemy import create_engine, text
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# mengambil data dari PostgreSQL
def get_data_from_postgres():
    conn = psycopg2.connect(
        dbname="replikasipdj-bigdata",
        user="postgres",
        password="2lNyRKW3oc9kan8n",
        host="103.183.92.158",
        port="5432"
    )

    schemas = input("Masukkan nama Schemas: ").strip()
    tables = input("Masukkan nama Tables: ").strip()

    cursor = conn.cursor()
    query = f"SELECT * FROM {schemas}.{tables};"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=columns)

    # kapitalisasi, hapus spasi berlebih, ubah underscore ke spasi
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.upper().str.replace('_', ' ', regex=False)

    return df, schemas, tables

# mengubah format kolom periode_update
def periode_update(periode_str):
    month_mapping = {
        'JANUARI': '01', 'FEBRUARI': '02', 'MARET': '03', 'APRIL': '04',
        'MEI': '05', 'JUNI': '06', 'JULI': '07', 'AGUSTUS': '08',
        'SEPTEMBER': '09', 'OKTOBER': '10', 'NOVEMBER': '11', 'DESEMBER': '12'
    }

    triwulan_mapping = {'I': 'Q1', 'II': 'Q2', 'III': 'Q3', 'IV': 'Q4'}
    caturwulan_mapping = {'I': 'C1', 'II': 'C2', 'III': 'C3'}
    semester_mapping = {'I': 'S1', 'II': 'S2'}

    if not isinstance(periode_str, str):
        return periode_str

    periode_str = periode_str.strip().upper()

    # hapus tanggal
    if periode_str and periode_str.split()[0].isdigit():
        parts = periode_str.split(maxsplit=1)
        if len(parts) > 1:
            periode_str = parts[1]

    parts = periode_str.strip().split()

    if len(parts) == 2:
        if parts[0] == 'TAHUN':
            return parts[1]
        elif parts[0] in month_mapping:
            bulan = month_mapping[parts[0]]
            return f"{parts[1]}-{bulan}"
    elif len(parts) == 3:
        tipe = parts[0]
        nomor = parts[1]
        tahun = parts[2]

        if tipe == 'SEMESTER' and nomor in semester_mapping:
            return f"{tahun}-{semester_mapping[nomor]}"
        elif tipe == 'TRIWULAN' and nomor in triwulan_mapping:
            return f"{tahun}-{triwulan_mapping[nomor]}"
        elif tipe == 'CATURWULAN' and nomor in caturwulan_mapping:
            return f"{tahun}-{caturwulan_mapping[nomor]}"

    return periode_str

# mendeteksi tingkat wilayah berdasarkan kolom
def jenis_wilayah(df):
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_similarity_scores(cols):
        target = ['nama_provinsi', 'nama_kabupaten', 'nama_kecamatan', 'desa_kelurahan']
        return {
            key: max(((col, similarity(key, col)) for col in cols), key=lambda x: x[1])
            for key in target
        }

    # deteksi eksplisit kolom
    kolom = [col.lower() for col in df.columns]
    kelurahan = any(k in kolom for k in ['nama_kelurahan/desa', 'nama_kelurahan', 'nama_desa', 'kelurahan', 'desa'])
    kecamatan = any(k in kolom for k in ['nama_kecamatan', 'kecamatan'])
    kabupaten = any(k in kolom for k in ['nama_kabupaten', 'kabupaten', 'kabupaten_kota'])
    provinsi = any(k in kolom for k in ['nama_provinsi', 'provinsi'])

    if provinsi and not (kabupaten or kecamatan or kelurahan):
        return 'data_provinsi'
    elif kelurahan:
        return 'data_kelurahan'
    elif kecamatan:
        return 'data_kecamatan'
    elif kabupaten:
        return 'data_kabupaten'

    # similarity jika struktur tidak dikenali
    scores = get_similarity_scores(df.columns.tolist())
    np, nk, nc, nd = scores['nama_provinsi'][1], scores['nama_kabupaten'][1], scores['nama_kecamatan'][1], scores['desa_kelurahan'][1]

    if np > 0.75 and nk <= 0.75 and nc <= 0.75 and nd <= 0.75:
        return 'data_provinsi'
    elif np > 0.75 and nk > 0.75 and nc <= 0.75 and nd <= 0.75:
        return 'data_kabupaten'
    elif np > 0.75 and nk > 0.75 and nc > 0.75 and nd <= 0.75:
        return 'data_kecamatan'
    elif np > 0.75 and nk > 0.75 and nc > 0.75 and nd > 0.75:
        return 'data_kelurahan'
    else:
        return 'data_unknown'

def jenis_data(df):
    while True:
        jenis = input(
            "Pilih jenis data (transaksi/agregat). Ketik (t) untuk transaksi, ketik (a) untuk agregat, atau (t/a): ").strip().lower()

        if jenis in ['t', '0']:
            jenis_text = 'transaksi'
            df = transaksi(df)
            break
        elif jenis in ['a', '1']:
            jenis_text = 'agregat'
            df = agregat(df)
            break
        else:
            print("Jenis data tidak dikenali. Ketik (t) untuk transaksi, (a) untuk agregat, atau (t/a)")

    return df, jenis_text

def kabupaten(df):
        # koneksi ke database PostgreSQL
        conn_b = psycopg2.connect(
            dbname="result_cleansing",
            user="postgres",
            password="2lNyRKW3oc9kan8n",
            host="103.183.92.158",
            port="5432"
        )

        # data master kabupaten
        schemas_b = "masterdata"
        tables_b = "masterkabupaten"
        cursor_b = conn_b.cursor()
        query_b = f"SELECT * FROM {schemas_b}.{tables_b};"
        cursor_b.execute(query_b)
        rows_b = cursor_b.fetchall()
        columns = [desc[0] for desc in cursor_b.description]
        cursor_b.close()
        conn_b.close()

        data_kabupaten = pd.DataFrame(rows_b, columns=columns)

        # rename kolom jika menggunakan nama 'kab_kota'
        if 'kab_kota' in df.columns and 'kabupaten_kota' not in df.columns:
            df = df.rename(columns={'kab_kota': 'kabupaten_kota'})

        if 'kabupaten_kota' in df.columns:
            # pastikan string dan normalisasi huruf besar
            df['kabupaten_kota'] = df['kabupaten_kota'].astype(str).str.strip().str.upper()

            # normalisasi berbagai format 'kabupaten'
            df['kabupaten_kota'] = df['kabupaten_kota'].str.replace(r'^KAB[\./\s\-]*', 'KABUPATEN ', regex=True)
            df['kabupaten_kota'] = df['kabupaten_kota'].str.replace(r'^KOTA[\./\s\-]*', 'KOTA ', regex=True)

            # jika belum diawali 'KOTA ' atau 'KABUPATEN ', tambahkan awalan 'KABUPATEN '
            df['kabupaten_kota'] = df['kabupaten_kota'].apply(
                lambda x: 'KABUPATEN ' + x if not x.startswith('KOTA ') and not x.startswith('KABUPATEN ') else x)

            # join ke master kabupaten
            df = df.merge(
                data_kabupaten[['kode_kabupaten_kota', 'nama_kabupaten_kota']],
                left_on='kabupaten_kota',
                right_on='nama_kabupaten_kota',
                how='left'
            )

            # drop kolom kabupaten_kota
            df = df.drop(columns=['kabupaten_kota'])

        return df

def kecamatan(df):
    # koneksi ke database PostgreSQL
    conn_c = psycopg2.connect(
        dbname="result_cleansing",
        user="postgres",
        password="2lNyRKW3oc9kan8n",
        host="103.183.92.158",
        port="5432"
    )

    # data master kabupaten
    schemas_c = "masterdata"
    tables_c = "masterkecamatan"
    cursor_c = conn_c.cursor()
    query_c = f"SELECT * FROM {schemas_c}.{tables_c};"
    cursor_c.execute(query_c)
    rows_c = cursor_c.fetchall()
    columns = [desc[0] for desc in cursor_c.description]
    cursor_c.close()
    conn_c.close()

    data_kecamatan = pd.DataFrame(rows_c, columns=columns)

    # normalisasi
    df["kecamatan"] = df["kecamatan"].str.replace(r"(?i)\bkecamatan\b", "", regex=True).str.strip()

    # join ke master desa
    df = df.merge(data_kecamatan[['bps_kode_kecamatan', 'bps_nama_kecamatan', 'kode_kabupaten_kota', 'nama_kabupaten_kota']],
              left_on='kecamatan',
              right_on='bps_nama_kecamatan',
              how='left')

    # drop kolom kecamatan
    df = df.drop(columns=['kecamatan'])

    return df

def kelurahan(df, status, col, special_case=None, preference='kemendagri'):
    # koneksi master desa
    def conn_d():
        conn_d = psycopg2.connect(
            dbname="result_cleansing",
            user="postgres",
            password="2lNyRKW3oc9kan8n",
            host="103.183.92.158",
            port="5432"
        )
        cursor_d = conn_d.cursor()
        query = "SELECT * FROM masterdata.masterdesa;"
        cursor_d.execute(query)
        rows_d = cursor_d.fetchall()
        columns_d = [desc[0] for desc in cursor_d.description]
        cursor_d.close()
        conn_d.close()
        return pd.DataFrame(rows_d, columns=columns_d)

    # preprocessing lokasi
    def prepare_location_columns(df, kelurahan_col, kecamatan_col, kabupaten_col, prefix=''):
        df = df.copy()
        df = df.apply(lambda x: x.str.upper() if x.dtype == "object" else x)
        df[f'kabupaten_{prefix}'] = df[kabupaten_col].str.replace("KAB.", "KABUPATEN", regex=False).apply(lambda x: f"KABUPATEN {x}" if " " not in x else x)
        for colname, newname in zip([kelurahan_col, kecamatan_col], [f'kelurahan_{prefix}', f'kecamatan_{prefix}']):
            df[newname] = (df[colname]
                .str.replace(" ", "", regex=False)
                .str.replace(r'[^\w\s]', '', regex=True)
                .str.replace(r'[\'\"\`]', '', regex=True)
                .str.replace(r'[\n\r\t]', '', regex=True)
                .str.strip())
        df[f'lokasi_{prefix}_desa'] = df[[f'kelurahan_{prefix}', f'kecamatan_{prefix}', f'kabupaten_{prefix}']].fillna('').agg(', '.join, axis=1)
        return df

    # TF-IDF Matching
    def match_locations_tfidf(df_target, df_reference, col_target, col_reference, output_col, score_col, preference):
        texts_target = df_target[col_target].fillna('').tolist()
        texts_reference = df_reference[col_reference].fillna('').tolist()
        all_text = texts_target + texts_reference
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_text)
        tfidf_target = tfidf_matrix[:len(texts_target)]
        tfidf_ref = tfidf_matrix[len(texts_target):]
        cosine_sim = cosine_similarity(tfidf_target, tfidf_ref)
        best_matches = cosine_sim.argmax(axis=1)
        match_scores = cosine_sim.max(axis=1)
        df_target[f'kelurahan_{preference}'] = [df_reference.iloc[i][f'kelurahan_{preference}'] for i in best_matches]
        df_target[f'kecamatan_{preference}'] = [df_reference.iloc[i][f'kecamatan_{preference}'] for i in best_matches]
        df_target['kabupaten_master'] = [df_reference.iloc[i]['nama_kabupaten_kota'] for i in best_matches]
        df_target[output_col] = [texts_reference[i] for i in best_matches]
        df_target[score_col] = match_scores
        return df_target

    # fix berdasarkan special case
    def fix_inconsistent_case(df, tfidf_threshold=0.99):
        matched = df[df['tfidf_score'] > tfidf_threshold][[special_case, f'lokasi_edit_desa', f'lokasi_{preference}_desa']]
        mapping = matched.drop_duplicates(special_case).set_index(special_case).to_dict(orient='index')
        def fix(row):
            if row[special_case] in mapping and row['tfidf_score'] < tfidf_threshold:
                row[f'lokasi_edit_desa'] = mapping[row[special_case]][f'lokasi_edit_desa']
                row[f'lokasi_{preference}_desa'] = mapping[row[special_case]][f'lokasi_{preference}_desa']
                row['tfidf_score'] = tfidf_threshold
            return row
        return df.apply(fix, axis=1)

    # koreksi kecamatan/kelurahan
    def correct_kecamatan_kelurahan(kabupaten, kecamatan, kelurahan, master_df, preference, cutoff=0.6):
        df_kec = master_df[(master_df['nama_kabupaten_kota'].str.upper() == kabupaten.upper()) &
                           (master_df[f'kelurahan_{preference}'].str.upper() == kelurahan.upper())]
        kecamatan_baru = kecamatan
        if not df_kec.empty:
            match = get_close_matches(kecamatan.upper(), [k.upper() for k in df_kec[f'kecamatan_{preference}'].unique()], n=1, cutoff=cutoff)
            if match:
                kecamatan_baru = next(k for k in df_kec[f'kecamatan_{preference}'].unique() if k.upper() == match[0])
        df_kel = master_df[(master_df['nama_kabupaten_kota'].str.upper() == kabupaten.upper()) &
                           (master_df[f'kecamatan_{preference}'].str.upper() == kecamatan_baru.upper())]
        kelurahan_baru = kelurahan
        if not df_kel.empty:
            match = get_close_matches(kelurahan.upper(), [k.upper() for k in df_kel[f'kelurahan_{preference}'].unique()], n=1, cutoff=cutoff)
            if match:
                kelurahan_baru = next(k for k in df_kel[f'kelurahan_{preference}'].unique() if k.upper() == match[0])
        return kecamatan_baru, kelurahan_baru, f"{kelurahan_baru}, {kecamatan_baru}, {kabupaten}"

    # proses data desa
    masterdesa = conn_d()

    df_preprocess = prepare_location_columns(df, col['desa_kelurahan'], col['nama_kecamatan'], col['kabupaten_kota'], prefix='edit')
    masterdesa = prepare_location_columns(masterdesa, "kemendagri_nama_desa_kelurahan", "kemendagri_nama_kecamatan", "nama_kabupaten_kota", prefix=preference)

    df_preprocess = match_locations_tfidf(df_preprocess, masterdesa, f'lokasi_edit_desa', f'lokasi_{preference}_desa', f'lokasi_{preference}_desa', 'tfidf_score', preference)

    if special_case:
        df_preprocess = fix_inconsistent_case(df_preprocess)

    df_unmatch = df_preprocess[df_preprocess['tfidf_score'] < 0.99]
    df_unmatch[['kecamatan_masterdesa_fix', 'kelurahan_masterdesa_fix', 'lokasi_masterdesa_fix_desa']] = df_unmatch.apply(
        lambda x: correct_kecamatan_kelurahan(x['kabupaten_edit'], x['kecamatan_edit'], x['kelurahan_edit'], masterdesa, preference), axis=1, result_type='expand'
    )

    df_unmatch = match_locations_tfidf(df_unmatch, masterdesa, 'lokasi_masterdesa_fix_desa', f'lokasi_{preference}_desa', f'lokasi_{preference}_desa', 'tfidf_score', preference)

    df_match = df_preprocess[df_preprocess['tfidf_score'] >= 0.99]
    df_isi = pd.concat([df_match, df_unmatch[df_unmatch['tfidf_score'] >= 0.99]]).sort_values(by='id').reset_index(drop=True)

    df_isi_merge = df_isi[list(df.columns) + [f'lokasi_{preference}_desa']].merge(
        masterdesa.drop(columns=['kode_provinsi', 'nama_provinsi'], errors='ignore'),
        on=f'lokasi_{preference}_desa',
        how='left'
    )

    df_kosong = df_unmatch[df_unmatch['tfidf_score'] < 0.99].copy()
    df_kosong[col['kabupaten_kota']] = df_kosong[col['kabupaten_kota']].str.replace("KAB.", "KABUPATEN", regex=False).apply(lambda x: f"KABUPATEN {x}" if " " not in x else x)
    df_kosong.rename(columns={
        col['kabupaten_kota']: 'nama_kabupaten_kota',
        col['nama_kecamatan']: 'kemendagri_nama_kecamatan',
        col['desa_kelurahan']: 'kemendagri_nama_desa_kelurahan'
    }, inplace=True)

    df_concat = pd.concat([df_isi_merge, df_kosong], ignore_index=True).sort_values(by='id').reset_index(drop=True)
    df_concat = df_concat.fillna('0')

    kolom_buang = [
        'provinsi', 'kabupaten', 'kecamatan', 'kelurahan',
        f'lokasi_{preference}_desa', 'kabupaten_master',
        'tfidf_score', 'lokasi_edit_desa',
        'kabupaten_edit', 'kelurahan_edit', 'kecamatan_edit',
        'kecamatan_masterdesa_fix', 'kelurahan_masterdesa_fix',
        'lokasi_masterdesa_fix_desa', 'kabupaten_kemendagri',
        'kecamatan_kemendagri', 'kelurahan_kemendagri'
    ]
    df_concat = df_concat.drop(columns=[col for col in kolom_buang if col in df_concat.columns])

    return df_concat

def agregat(df):
    # membuat kolom 'periode_update' jika belum ada
    if 'periode_update' not in df.columns:
        if 'periode' in df.columns:
            df['periode_update'] = pd.to_datetime(df['periode'], errors='coerce')
        elif 'tahun' in df.columns:
            df['periode_update'] = pd.to_datetime(df['tahun'].astype(str) + '-01-01', errors='coerce')

    # membuat kolom 'tahun' jika belum ada
    if 'tahun' not in df.columns and 'periode_update' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['periode_update']):
            df['tahun'] = df['periode_update'].dt.year.astype(str)
        else:
            df['tahun'] = df['periode_update'].astype(str).str[:4]

    # drop kolom tak terpakai
    drop = ['kategori', 'jumlah', 'periode', 'bulan', 'tanggal']
    df = df.drop(columns=[col for col in drop if col in df.columns], errors='ignore')

    # daftar kolom yang akan dilewati saat transpose
    skip_cols = [
        'id_index', 'id',
        'kode_provinsi', 'nama_provinsi',
        'kode_kabupaten_kota', 'nama_kabupaten_kota',
        'bps_kode_kecamatan', 'bps_nama_kecamatan',
        'bps_kode_desa_kelurahan', 'bps_nama_desa_kelurahan',
        'kemendagri_kode_kecamatan', 'kemendagri_nama_kecamatan',
        'kemendagri_kode_desa_kelurahan', 'kemendagri_nama_desa_kelurahan',
        'periode_update', 'satuan', 'tahun'
    ]

    # mengambil semua kolom selain yang di-skip
    other_cols = [col for col in df.columns if col not in skip_cols]

    # deteksi kolom numerik termasuk yang object tapi isinya >= 60% numerik
    num_cols = [
        col for col in other_cols
        if pd.api.types.is_numeric_dtype(df[col])
        or pd.to_numeric(df[col].fillna(0), errors='coerce').notna().mean() >= 0.6
    ]

    # konversi num_cols ke numeric, isi NaN dengan 0
    df[num_cols] = df[num_cols].apply(lambda col: pd.to_numeric(col, errors='coerce').fillna(0))

    # ubah float yang bisa menjadi int secara utuh
    df = df.apply(lambda col: col.apply(lambda x: int(x) if isinstance(x, (int, float)) and x == int(x) else x))

    # kolom yang benar-benar bertipe int setelah konversi
    value_columns = [
        col for col in num_cols
        if pd.api.types.is_integer_dtype(df[col]) and col not in skip_cols
    ]

    if not value_columns:
        print("❌ Tidak ditemukan kolom integer untuk ditranspose.")
        return df

    print("✅ Kolom yang akan ditranspose:", value_columns)

    # kolom identitas (id_vars) = semua kolom selain value_columns + selain kolom hasil melt
    id_vars = [col for col in df.columns if col not in value_columns and col not in ['kategori', 'jumlah']]

    df_melted = df.melt(
        id_vars=id_vars,
        value_vars=value_columns,
        var_name='kategori',
        value_name='jumlah'
    )

    # normalisasi kolom object
    for col in df_melted.select_dtypes(include='object').columns:
        df_melted[col] = (
            df_melted[col]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace('_', ' ', regex=False)
            .apply(lambda x: re.sub(r'\b(\w+)\s+\1\b', r'\1-\1', x))
        )

    # buat urutan untuk tampil selang-seling berdasarkan kategori
    df_melted['_order'] = df_melted.groupby('kategori').cumcount()
    df_melted = df_melted.sort_values('_order').drop(columns=['_order']).reset_index(drop=True)

    # isi NaN di kolom 'jumlah' dengan 0
    if 'jumlah' in df_melted.columns:
        df_melted['jumlah'] = df_melted['jumlah'].fillna(0)

    return df_melted

def transaksi(df):
    # cek dan buat kolom 'periode_update' jika belum ada berdasarkan kolom 'periode' atau 'tahun'
    if 'periode_update' not in df.columns:
        if 'periode' in df.columns:
            df['periode_update'] = pd.to_datetime(df['periode'])
        elif 'tahun' in df.columns:
            df['periode_update'] = pd.to_datetime(df['tahun'].astype(str) + '-01-01')

    # cek dan buat kolom 'tahun' jika belum ada berdasarkan kolom periode_update
    if 'tahun' not in df.columns and 'periode_update' in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df['periode_update']):
            df['tahun'] = df['periode_update'].dt.year.astype(str)
        else:
            df['tahun'] = df['periode_update'].astype(str).str[:4]

    # daftar kolom yang di drop
    drop = ['kategori', 'jumlah', 'periode', 'bulan', 'tanggal']

    # hanya drop kolom yang terdaftar di dataframe
    df = df.drop(columns=[col for col in drop if col in df.columns])

    return df

def id_index(df):
    # buat 'id_index' dari nomor urut + id (keduanya sebagai string)
    df['id_index'] = (df.index + 1).astype(str) + df['id'].astype(str)

    # konversi kembali ke integer
    df['id_index'] = df['id_index'].astype(int)

    # pindahkan 'id_index' ke kolom pertama
    cols = ['id_index'] + [col for col in df.columns if col != 'id_index']
    df = df[cols]

    return df

def final(df):
    final_columns = [
        'id_index',
        'id',
        'kode_provinsi',
        'nama_provinsi',
        'kode_kabupaten_kota',
        'nama_kabupaten_kota',
        'bps_kode_kecamatan',
        'bps_nama_kecamatan',
        'bps_kode_desa_kelurahan',
        'bps_nama_desa_kelurahan',
        'kemendagri_kode_kecamatan',
        'kemendagri_nama_kecamatan',
        'kemendagri_kode_desa_kelurahan',
        'kemendagri_nama_desa_kelurahan',
        'kolom x',
        'periode_update',
        'kategori',
        'jumlah',
        'satuan',
        'tahun',
        'jenis_data'
    ]

    # kolom yang ada di df dan ada di final_columns
    recognized = [col for col in final_columns if col in df.columns]
    # kolom tidak dikenal yang ada di df tapi tidak ada di final_columns
    kolom_x = [col for col in df.columns if col not in final_columns]

    # isi NaN di kolom_x
    for col in kolom_x:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna('-')

    x = []
    for col in final_columns:
        if col == 'kolom x':
            x.extend(kolom_x)
        elif col in recognized:
            x.append(col)

    # jika 'kolom x' tidak ada di referensi akan sisipkan di akhir
    if 'kolom x' not in final_columns:
        x.extend(kolom_x)

    return df[x]

def preview_data(df):
    print("\nPreview akhir:", flush=True)
    print(tabulate(df.head(10), headers='keys', tablefmt='psql'), flush=True)

    while True:
        keputusan = input("\nApakah data sudah sesuai dan ingin disimpan? Ketik (y) yes/setuju, ketik (n) no/tidak setuju. (y/n): ").strip().lower()
        if keputusan in ['y', 'n']:
            break
        print("Input tidak dikenali, ketik (y) yes/setuju, ketik (n) no/tidak setuju. (y/n)", flush=True)

    return keputusan == 'y'

def simpan(df, schemas, tables, level_wilayah):
    primary_key = "id_index"
    index_col = None

    # deteksi nama kolom index berdasarkan level wilayah
    if level_wilayah == "data_kabupaten":
        index_col = "nama_kabupaten_kota"
    elif level_wilayah == "data_kecamatan":
        index_col = "bps_nama_kecamatan"
    elif level_wilayah == "data_kelurahan":
        index_col = "bps_nama_desa_kelurahan"

    # buat schema jika belum ada
    conn = psycopg2.connect(
        dbname="result_cleansing",
        user="postgres",
        password="2lNyRKW3oc9kan8n",
        host="103.183.92.158",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schemas};")
    conn.commit()
    cursor.close()
    conn.close()

    engine = create_engine(f'postgresql://postgres:2lNyRKW3oc9kan8n@103.183.92.158:5432/result_cleansing')

    # simpan data, replace jika tabel sudah ada
    df.to_sql(
        tables,
        engine,
        schema=schemas,
        if_exists='replace',
        index=False
    )

    # generate nama primary key constraint secara dinamis
    parts = tables.split('_')
    with engine.connect() as conn:
        for i in range(3, len(parts) + 1):
            candidate = '_'.join(parts[:i])
            constraint_name = f"{candidate}_pkey"
            check = conn.execute(
                text("""
                    SELECT 1 FROM information_schema.table_constraints
                    WHERE constraint_schema = :schema AND constraint_name = :name
                """), {"schema": schemas, "name": constraint_name}
            ).fetchone()
            if not check:
                pk_constraint_name = candidate
                break
        else:
            pk_constraint_name = '_'.join(parts)

    # tambahkan PRIMARY KEY
    with engine.connect() as connection:
        try:
            connection.execute(
                text(f"""
                    ALTER TABLE {schemas}.{tables}
                    ADD CONSTRAINT {pk_constraint_name}_pkey PRIMARY KEY ({primary_key});
                """)
            )
            connection.commit()
        except Exception as e:
            print(f"⚠️ Gagal menambahkan PRIMARY KEY: {e}")

    # cek keberhasilan primary key
    with engine.connect() as connection:
        result = connection.execute(
            text(f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_schema = :schema
                  AND tc.table_name = :table
                  AND tc.constraint_type = 'PRIMARY KEY';
            """), {"schema": schemas, "table": tables}
        ).fetchall()

    if result:
        print(f"✅ Primary key kolom: {result[0][0]}")
    else:
        print("⚠️ Tidak ada primary key ditemukan.")

    # buat index jika ada kolom yang cocok
    if index_col:
        with engine.connect() as connection:
            connection.execute(
                text(f"""
                    CREATE INDEX IF NOT EXISTS idx_{tables}_{index_col}
                    ON {schemas}.{tables} ({index_col});
                """)
            )
            connection.commit()
        print(f"✅ Index dibuat pada kolom: {index_col}")
    else:
        print(f"ℹ️ Tidak ada index dibuat (level wilayah: {level_wilayah})")

    print("✅ Data berhasil disimpan ke result_cleansing.")

def masterdata(schemas, tables, jenis_data):    
    # konversi input ke string
    if jenis_data == 0:
        jenis_text = 'transaksi'
    elif jenis_data == 1:
        jenis_text = 'agregat'
    elif jenis_data in ['transaksi', 'agregat']:
        jenis_text = jenis_data
    else:
        raise ValueError(f"Jenis data tidak dikenali: {jenis_data}")
    
    tanggal = datetime.now().date()

    # koneksi
    conn = psycopg2.connect(
        dbname="result_cleansing",
        user="postgres",
        password="2lNyRKW3oc9kan8n",
        host="103.183.92.158",
        port="5432"
    )
    cursor = conn.cursor()

    # pastikan struktur tabel
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS masterdata;
        CREATE TABLE IF NOT EXISTS masterdata.master_jenis_data (
            id INTEGER PRIMARY KEY,
            nama_schema TEXT,
            nama_table TEXT,
            jenis_data TEXT,
            modified_date DATE
        );
    """)
    conn.commit()

    # cek apakah data duplikat
    cursor.execute("""
        SELECT id FROM masterdata.master_jenis_data
        WHERE nama_schema = %s AND nama_table = %s;
    """, (schemas, tables))
    existing = cursor.fetchone()

    if existing:
        print("🔁 Duplikat ditemukan: replace dan reset seluruh ID...")

        # ambil seluruh data kecuali yang duplikat
        df = pd.read_sql("""
            SELECT * FROM masterdata.master_jenis_data
            WHERE NOT (nama_schema = %s AND nama_table = %s);
        """, conn, params=(schemas, tables))

        # menambahkan data baru
        new_row = {
            'nama_schema': schemas,
            'nama_table': tables,
            'jenis_data': jenis_text,
            'modified_date': datetime.now().date()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # reset id
        df = df.reset_index(drop=True)
        df['id'] = df.index + 1

        # truncate dan insert ulang
        cursor.execute("TRUNCATE masterdata.master_jenis_data;")
        conn.commit()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO masterdata.master_jenis_data (id, nama_schema, nama_table, jenis_data, modified_date)
                VALUES (%s, %s, %s, %s, %s);
            """, (row['id'], row['nama_schema'], row['nama_table'], row['jenis_data'], row['modified_date']))

        conn.commit()
        print(f"✅ Data duplikat di replace. Metadata disimpan ke masterdata.master_jenis_data: {len(df)}, {schemas}, {tables}, {jenis_text}, {tanggal}.")

    else:
        # ambil ID terakhir
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM masterdata.master_jenis_data;")
        next_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO masterdata.master_jenis_data (id, nama_schema, nama_table, jenis_data, modified_date)
            VALUES (%s, %s, %s, %s, %s);
        """, (next_id, schemas, tables, jenis_text, tanggal))
        conn.commit()
        print(f"✅ Metadata disimpan ke masterdata.master_jenis_data: ({next_id}, {schemas}, {tables}, {jenis_text}, {tanggal}).")

    cursor.close()
    conn.close()

def eksekusi():
    # mengambil data awal dari PostgreSQL
    df, schemas, tables = get_data_from_postgres()

    # mengolah kolom 'periode_update' jika tersedia
    if 'periode_update' in df.columns:
        df['periode_update'] = df['periode_update'].apply(periode_update)

    # deteksi tingkat wilayah
    wilayah = jenis_wilayah(df)

    # transformasi berdasarkan tingkat wilayah
    if wilayah == 'data_kabupaten':
        df = kabupaten(df)
    elif wilayah == 'data_kecamatan':
        df = kecamatan(df)
    elif wilayah == 'data_kelurahan':
        kolom = {
            'kabupaten_kota': 'kabupaten',
            'nama_kecamatan': 'kecamatan',
            'desa_kelurahan': 'kelurahan'
        }
        df = kelurahan(df, status=wilayah, col=kolom, special_case='kelurahan', preference='kemendagri')

    # tingkat wilayah data
    print(f"Tingkat wilayah: {wilayah}", flush=True)

    # preview awal
    print("\nPreview awal:", flush=True)
    print(tabulate(df.head(), headers='keys', tablefmt='psql'), flush=True)

    # input jenis data (transaksi/agregat)
    df, jenis = jenis_data(df)

    # menambahkan kolom id_index dan finalisasi data
    df = id_index(df)
    df = final(df)

    # preview akhir dan konfirmasi simpan
    if preview_data(df):
        simpan(df, schemas, tables, level_wilayah=wilayah)
        masterdata(schemas, tables, jenis)
    else:
        print("⛔ Proses dibatalkan.")

if __name__ == "__main__":
    eksekusi()