from models.data import read_data

def show_visual():
    import matplotlib.pyplot as plt
    import pandas as pd
    
    data = read_data()
    
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    # plot grafik
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['close'], label='Harga Penutupan')
    plt.plot(data.index, data['SMA-20'], label='SMA-20', linestyle='--')
    plt.plot(data.index, data['Upper BB'], label='Upper BB')
    plt.plot(data.index, data['Lower BB'], label='Lower BB')
    plt.legend()
    plt.title('Grafik Harga Saham dengan SMA-20 dan Bollinger Bands')
    plt.xlabel('Tanggal')
    plt.ylabel('Harga')
    plt.savefig('./static/assets/plot/ta-plot.png')
    plt.close()
