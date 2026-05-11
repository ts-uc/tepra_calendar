from PIL import Image, ImageDraw, ImageFont
from japanera import EraDate
import calendar
import datetime
import jpholiday
import argparse

H = 96

class Draw:
    def __init__(self, w, h):
        self.font = read_font(19)
        self.img = Image.new("1", (w, h), 1)
        self.draw = ImageDraw.Draw(self.img)
    
    def draw_cell(self, x:int, y:int, w:int, h:int, text:str, reverse:bool):
        if reverse:
            self.draw.rectangle(
                (x, y, x + w - 1, y + h - 1),
                fill=0
            )
        bbox = self.draw.textbbox((0, 0), text, font=self.font)
        tx = x + (w - (bbox[2] - bbox[0])) // 2
        ty = y - (11 - h//2) 

        self.draw.text(
            (tx, ty),
            text,
            font=self.font,
            fill=1 if reverse else 0
        )

    def save(self, out:str):
        self.img.save(out)

def read_font(size) -> ImageFont:
    try:
        return ImageFont.truetype(
            "./fonts/Jersey10-Regular.ttf",
            size
        )
    except:
        return ImageFont.load_default()


def make_calendar(year, month):
    cell_w = 20
    day_h = 12
    date_h = 14
    width = cell_w * 7

    draw = Draw(width, H)

    # 曜日部分のグリッド
    weekdays = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]

    for c, text in enumerate(weekdays):
        x = c * cell_w
        y = 0

        reverse = (text == "SU")

        draw.draw_cell(
            x, y, cell_w, day_h, text, reverse
        )

    # 日付部分のグリッド
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(year, month)

    for r, row in enumerate(weeks):
        for c, day in enumerate(row):
            if day == 0:
                continue

            # 祝日判定
            d = datetime.date(year, month, day)
            reverse = (c == 0) or jpholiday.is_holiday(d)

            x = c * cell_w
            y = r * date_h + day_h

            text = str(day)

            draw.draw_cell(
                x, y, cell_w, date_h, text, reverse
            )

    # 年月表示
    d = EraDate.from_date(datetime.date(year, month, 1))
    text = f"{d.strftime("%Y(%-h%-Y)")}/{month}"
    # bbox = draw.textbbox((0, 0), text, font=f)
    # tx = width - (bbox[2] - bbox[0]) - 3
    # ty = 5 * date_h + day_h - 4

    # draw.text(
    #     (tx, ty),
    #     text,
    #     font=f,
    #     fill=0
    # )

    out = f"./calendars/{year:04}_{month:02}.png"
    draw.save(out)
    print(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("year", type=int)
    p.add_argument("month", type=int)
    a = p.parse_args()

    make_calendar(a.year, a.month)
