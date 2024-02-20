def check_avalable_data():
    import os
    
    file_path = './static/data/dataset.csv'
    if os.path.getsize(file_path) != 0:
        return True
    else:
        return False

def read_data():
    if check_avalable_data() :
        import pandas as pd
        
        return pd.read_csv('./static/data/dataset.csv');