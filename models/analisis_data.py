import models.data as dataset

def analisis_data():
    import pandas as pd

    # Membaca data harga saham dari CSV
    data = dataset.read_data()
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=False)

    # Menghitung SMA-20
    sma_period = 20
    data['SMA-20'] = data['close'].rolling(window=sma_period).mean()

    # Menghitung Bollinger Bands
    std_dev = 2  # Deviasi standar
    data['Upper BB'] = data['SMA-20'] + (std_dev * data['close'].rolling(window=sma_period).std())
    data['Lower BB'] = data['SMA-20'] - (std_dev * data['close'].rolling(window=sma_period).std())

    # Inisialisasi kolom "Sinyal" dengan "Tidak Ada Sinyal"
    data['signal'] = 'Tidak Ada Sinyal'

    # Mendeteksi sinyal "Beli" dan "Jual"
    for i in range(sma_period, len(data)):
        if data['close'][i] > data['SMA-20'][i] and data['close'][i] > data['Upper BB'][i]:
            data.at[data.index[i], 'signal'] = '1' # beli
        elif data['close'][i] < data['SMA-20'][i] and data['close'][i] < data['Lower BB'][i]:
            data.at[data.index[i], 'signal'] = '0' # jual

    # Hapus baris dengan "Tidak Ada Sinyal"
    data = data[data['signal'] != 'Tidak Ada Sinyal']

    # Tampilkan DataFrame dengan sinyal
    data.to_csv('./static/data/dataset.csv', index=False)


