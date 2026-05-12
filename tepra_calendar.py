from PIL import Image, ImageDraw, ImageFont
import calendar
import datetime
import jpholiday
import argparse


class Draw:
    def __init__(self, w, h):
        self.font_j10 = read_font("./fonts/Jersey10-Regular.ttf", 19)
        self.img = Image.new("1", (w, h), 1)
        self.draw = ImageDraw.Draw(self.img)

    def draw_cell(self, x: int, y: int, w: int, h: int, text: str, reverse: bool = False):
        if reverse:
            self.draw.rectangle(
                (x, y, x + w - 1, y + h - 1),
                fill=0
            )
        bbox = self.draw.textbbox((0, 0), text, font=self.font_j10)
        tx = x + (w - (bbox[2] - bbox[0])) // 2
        ty = y - (11 - h//2)

        self.draw.text(
            (tx, ty),
            text,
            font=self.font_j10,
            fill=1 if reverse else 0
        )

    def save(self, out: str):
        self.img.save(out)


def read_font(path: str, size: int) -> ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()


def make_calendar(year, month):
    cell_w = 20
    width = cell_w * 7
    height = 96

    header_h = 12
    weekdays_h = 12
    date_h = 12

    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(year, month)

    if len(weeks) <= 5:
        weekdays_h = 14
        date_h = 14

    draw = Draw(width, height)

    # 年月表示
    text = f"{year:04}-{month:02}"
    draw.draw_cell(
        x=0,
        y=0,
        w=width,
        h=header_h,
        text=text
    )

    # 曜日部分のグリッド
    weekdays = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]

    for c, text in enumerate(weekdays):
        reverse = (c == 0)
        draw.draw_cell(
            x=c * cell_w,
            y=header_h,
            w=cell_w,
            h=weekdays_h,
            text=text,
            reverse=reverse
        )

    # 日付部分のグリッド

    for r, row in enumerate(weeks):
        for c, day in enumerate(row):
            if day == 0:
                continue

            # 祝日判定
            d = datetime.date(year, month, day)
            reverse = (c == 0) or jpholiday.is_holiday(d)

            draw.draw_cell(
                x=c * cell_w,
                y=r * date_h + header_h + weekdays_h,
                w=cell_w,
                h=date_h,
                text=str(day),
                reverse=reverse
            )

    out = f"./calendars/{year:04}_{month:02}.png"
    draw.save(out)
    print(out)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("year", type=int)
    p.add_argument("month", type=int)
    a = p.parse_args()

    make_calendar(a.year, a.month)
