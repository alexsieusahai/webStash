import pandas as pd

from datetime import datetime

class WebData:
    def __init__(self, filename, link, html, screenshotLocation=None):
        self.timeScraped = datetime.utcnow()
        self.filename = filename
        self.link = link
        self.html = html

    def to_df(self):
        df = pd.DataFrame(columns=['TimeScraped', 'Filename', 'Html', 'Link'])
        df.loc[0, 'TimeScraped'] = self.timeScraped
        df.loc[0, 'Filename'] - self.filename
        df.loc[0, 'Html'] = self.html
        df.loc[0, 'Link'] = self.link
        return df

    def to_csv(self):
        self.to_df().to_csv(self.filename+'.csv', index=False)

    def to_json(self):
        self.to_df().to_json(self.filename+'.json')
