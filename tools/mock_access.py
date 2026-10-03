import random, datetime as dt
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path('/home/claude/site/frames'); OUT.mkdir(parents=True, exist_ok=True)

CSS = r"""
*{box-sizing:border-box}
body{margin:0;font-family:Carlito,'Liberation Sans',sans-serif;font-size:14.5px;color:#000;background:#D6D6D6}
.win{width:1440px;height:960px;background:#F3F3F3;display:flex;flex-direction:column;overflow:hidden}
.tbar{height:34px;background:#fff;display:flex;align-items:center;padding:0 10px;font-size:13px;color:#333;border-bottom:1px solid #E1E1E1}
.tbar .qat{display:flex;gap:12px;color:#444;font-size:13px;margin-right:18px}
.tbar .ttl{flex:1;text-align:center;color:#333}
.tbar .wc{display:flex;gap:26px;color:#333;font-size:13px;margin-left:18px}
.tabs{height:30px;background:#fff;display:flex;align-items:flex-end;padding-left:8px;gap:2px;border-bottom:1px solid #D0D0D0;font-size:13.5px}
.tabs span{padding:5px 11px 7px;color:#222}
.tabs span.file{background:#A4373A;color:#fff;padding:5px 14px 7px;margin-right:4px}
.tabs span.on{border:1px solid #D0D0D0;border-bottom:1px solid #fff;margin-bottom:-1px;background:#fff;color:#A4373A}
.tabs .rb{margin-left:auto;padding:5px 12px 7px;color:#666;font-size:12px}
.ribbon{background:#fff;border-bottom:1px solid #D0D0D0;display:flex;padding:6px 10px 4px;gap:0;font-size:12px;color:#222;height:92px}
.ribbon .g{display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:0 12px;border-right:1px solid #E6E6E6}
.ribbon .g .b{display:flex;gap:8px}
.ribbon .g .b div{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:50px;padding:2px 4px}
.ribbon .g .b i{width:30px;height:30px;border:1px solid #BFBFBF;background:#F7F7F7;border-radius:3px;display:block}
.ribbon .g .b i.big{width:36px;height:36px}
.ribbon .g .n{color:#555;margin-top:4px}
.doctabs{height:28px;background:#E9E9E9;display:flex;align-items:flex-end;padding-left:28px;gap:2px;font-size:13.5px}
.doctabs span{background:#D9D9D9;padding:4px 12px;border:1px solid #C9C9C9;border-bottom:0;color:#333}
.doctabs span.on{background:#fff;color:#000}
.doctabs span.on::after{content:'  ✕';color:#666;font-size:11px}
.body{flex:1;display:flex;min-height:0;background:#fff}
.navbar{width:20px;background:#F3F3F3;border-right:1px solid #C9C9C9;position:relative}
.navbar span{position:absolute;left:17px;top:60px;transform:rotate(90deg);transform-origin:left top;white-space:nowrap;font-size:12.5px;color:#444}
.navbar b{position:absolute;left:4px;top:6px;color:#444;font-size:12px}
.form{flex:1;display:flex;min-width:0}
.menu{width:190px;background:#F7F7F7;border-right:1px solid #D0D0D0;padding:12px 10px;display:flex;flex-direction:column;gap:6px}
.menu .mb{height:34px;border:1px solid #ADADAD;background:#F0F0F0;display:flex;align-items:center;padding:0 10px;font-size:14px}
.menu .mb.on{background:#DCE6F2;border-color:#7A9CC6;font-weight:700}
.menu .mf{margin-top:auto;font-size:12px;color:#555;line-height:1.3}
.canvas{flex:1;display:flex;flex-direction:column;min-width:0;padding:12px 14px 8px}
.sbar{height:22px;background:#F3F3F3;border-top:1px solid #D0D0D0;display:flex;align-items:center;padding:0 10px;font-size:12px;color:#333}
.sbar .r{margin-left:auto;display:flex;gap:16px;color:#333}
.hdr{display:flex;gap:16px;align-items:flex-end;margin-bottom:10px}
.ctl label{display:block;font-size:13px;color:#222;margin-bottom:2px}
.tb{border:1px solid #ABADB3;background:#fff;height:26px;padding:3px 6px;font-size:14.5px;white-space:nowrap;display:flex;align-items:center}
.cb{display:flex} .cb .tb{border-right:0} .cb .dd{width:19px;height:26px;border:1px solid #ABADB3;background:#E8E8E8;display:flex;align-items:center;justify-content:center;font-size:9px;color:#000}
.btn{height:30px;border:1px solid #ADADAD;background:#F0F0F0;padding:0 14px;font-size:14px;display:inline-flex;align-items:center;white-space:nowrap}
.btn.pri{background:#2F5496;border-color:#1F3864;color:#fff}
.btn.dis{color:#8A8A8A;border-color:#C9C9C9;background:#F7F7F7}
.chk{display:inline-flex;align-items:center;gap:6px;font-size:14px}
.chk i{width:14px;height:14px;border:1px solid #333;background:#fff;display:inline-block;position:relative}
.chk i.on::after{content:'✓';position:absolute;left:1px;top:-4px;font-size:14px;font-weight:700}
.sub{border:1px solid #ABADB3;display:flex;flex-direction:column;background:#fff}
.sub .cap{font-size:13px;color:#222;padding:4px 6px;background:#F5F5F5;border-bottom:1px solid #D4D4D4}
table.ds{border-collapse:collapse;table-layout:fixed;width:100%}
table.ds th{background:#F2F2F2;font-weight:400;font-size:13.5px;text-align:center;border-right:1px solid #D4D4D4;border-bottom:1px solid #C0C0C0;padding:2px 2px;height:38px;line-height:1.1;vertical-align:middle}
table.ds th small{display:block;font-size:11px;color:#444}
table.ds th.sel{width:18px;background:#F2F2F2}
table.ds td{border-right:1px solid #D4D4D4;border-bottom:1px solid #D4D4D4;height:25px;padding:0 5px;text-align:right;font-size:14.5px;white-space:nowrap;overflow:hidden;position:relative;font-variant-numeric:tabular-nums}
table.ds tr:nth-child(even) td{background:#F2F2F2}
table.ds td.sel{background:#F2F2F2;text-align:center;color:#000;font-size:12px;padding:0;border-right:1px solid #C0C0C0}
table.ds td.t{text-align:left}
table.ds td.loc{color:#1F4E99}
table.ds td.dr{color:#7F7F7F;font-style:italic}
table.ds td.err{background:#F8CBAD !important;color:#C00000}
table.ds td.con{background:#FFE699 !important}
table.ds td.unk{background:#E7E6E6 !important;color:#595959}
table.ds td.calc{color:#7F7F7F}
table.ds td.cur{box-shadow:inset 0 0 0 1.5px #000;background:#fff !important}
table.ds td.cur::before{content:'';position:absolute;right:8px;top:5px;width:1px;height:15px;background:#000}
table.ds td.chkc{text-align:center}
table.ds td.chkc i{width:13px;height:13px;border:1px solid #333;background:#fff;display:inline-block;position:relative;vertical-align:-2px}
table.ds td.chkc i.on::after{content:'✓';position:absolute;left:1px;top:-5px;font-size:13px;font-weight:700}
table.ds td.okg{color:#548235;font-weight:700;text-align:center}
.recnav{height:24px;background:#F5F5F5;border-top:1px solid #C9C9C9;display:flex;align-items:center;gap:8px;padding:0 6px;font-size:12.5px;color:#222}
.recnav .n{border:1px solid #ABADB3;background:#fff;padding:1px 6px;min-width:52px;text-align:center}
.recnav .f{border:1px solid #ABADB3;background:#fff;padding:1px 6px;color:#777;width:150px}
.legend{display:flex;gap:18px;margin:8px 0 0;font-size:12.5px;color:#222;align-items:center;flex-wrap:wrap}
.legend .k{display:inline-block;width:22px;height:15px;border:1px solid #BFBFBF;vertical-align:-3px;margin-right:5px;text-align:center;font-size:11px;line-height:13px}
.cf{border:1px solid #ABADB3;margin-top:8px;background:#fff}
.cf .cap{font-size:13px;color:#222;padding:4px 6px;background:#F5F5F5;border-bottom:1px solid #D4D4D4;display:flex;gap:10px}
.cf .row{display:grid;grid-template-columns:150px 90px 1fr 190px;gap:8px;align-items:center;padding:5px 8px;border-bottom:1px solid #E1E1E1;font-size:14px}
.cf .row:last-child{border-bottom:0}
.cf .row .ac{text-align:right}
.foot{display:flex;align-items:center;gap:10px;margin-top:10px}
.foot .cnt{display:flex;gap:18px;font-size:13.5px;color:#222}
.foot .cnt b{font-size:15px}
.foot .sp{flex:1}
.note{font-size:12.5px;color:#444}
.msg{border:1px solid #ABADB3;background:#FFF9E6;padding:7px 10px;font-size:14px;display:flex;gap:12px;align-items:center;margin-bottom:8px}
"""

def tabs(on='Главная', extra=None):
    names = ['Главная', 'Создать', 'Внешние данные', 'Работа с базами данных', 'Справка']
    if extra: names = [extra] + names
    s = '<div class="tabs"><span class="file">Файл</span>'
    for n in names:
        s += f'<span class="{"on" if n == on else ""}">{n}</span>'
    s += '<span class="rb">▲</span></div>'
    return s

def ribbon_preview():
    return """<div class="ribbon">
<div class="g"><div class="b"><div><i class="big"></i>Печать</div></div><div class="n">Печать</div></div>
<div class="g"><div class="b"><div><i></i>Размер</div><div><i></i>Поля</div><div><i></i>Книжная</div><div><i></i>Альбомная</div></div><div class="n">Размер страницы</div></div>
<div class="g"><div class="b"><div><i></i>Масштаб</div><div><i></i>Одна</div><div><i></i>Две</div></div><div class="n">Масштаб</div></div>
<div class="g"><div class="b"><div><i class="big"></i>PDF или XPS</div><div><i class="big"></i>Excel</div><div><i class="big"></i>Эл. почта</div></div><div class="n">Данные</div></div>
<div class="g" style="border-right:0"><div class="b"><div><i class="big"></i>Закрыть<br>просмотр</div></div><div class="n">Закрыть</div></div>
</div>"""

def window(doc_on, doc_tabs, body, mode='Режим формы', tab_on='Главная', ribbon='', extra_tab=None, menu_on=None, with_menu=True):
    dts = ''.join(f'<span class="{"on" if d == doc_on else ""}">{d}</span>' for d in doc_tabs)
    menu = ''
    if with_menu:
        items = ['Сегодня', 'Ввод сеанса', 'Спортсмены', 'События и команды', 'Заявки и исполнение', 'Отчёты', 'Справочники']
        menu = '<div class="menu">' + ''.join(f'<div class="mb {"on" if i == menu_on else ""}">{i}</div>' for i in items) + \
               '<div class="mf">Учебная база<br>вымышленные данные</div></div>'
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="win">
<div class="tbar"><div class="qat">💾 ↶ ↷ ▾</div><div class="ttl">СпортКонтроль : база данных- C:\\SportControl\\SportControl.accdb (формат файла Access 2007 - 2016) - Access</div><div class="wc">—&nbsp;&nbsp;&nbsp;▢&nbsp;&nbsp;&nbsp;✕</div></div>
{tabs(tab_on, extra_tab)}{ribbon}
<div class="doctabs">{dts}</div>
<div class="body"><div class="navbar"><b>»</b><span>Область навигации</span></div><div class="form">{menu}<div class="canvas">{body}</div></div></div>
<div class="sbar">{mode}<div class="r"><span>Num Lock</span><span>▦ ▤ ▥</span></div></div>
</div></body></html>"""

IND = [('Hb', 'г/л', (128, 166), 0), ('Эр', '10¹²/л', (4.2, 5.6), 2), ('Hct', '%', (38, 49), 1),
       ('Ферр', 'нг/мл', (18, 140), 0), ('Жел', 'мкмоль/л', (10, 30), 1), ('Глю', 'ммоль/л', (3.8, 5.9), 1),
       ('Моч', 'ммоль/л', (3.5, 8.5), 1), ('Креат', 'мкмоль/л', (70, 115), 0), ('АЛТ', 'Ед/л', (12, 45), 0),
       ('АСТ', 'Ед/л', (15, 45), 0), ('КФК', 'Ед/л', (120, 520), 0), ('Белок', 'г/л', (64, 82), 0),
       ('Корт', 'нмоль/л', (250, 650), 0), ('Тест', 'нмоль/л', (12, 32), 1), ('Т/К', 'расчёт', None, None),
       ('ЛДГ', 'Ед/л', (140, 260), 0)]
CALC = 14
ROWS = [f'Спортсмен {i:02d}' for i in range(1, 14)]
rnd = random.Random(20261003)
def fmt(v, d): return f'{v:.{d}f}'.replace('.', ',')
VAL = [[None] * len(IND) for _ in ROWS]; NUM = [[None] * len(IND) for _ in ROWS]
for r in range(len(ROWS)):
    for c, (n, u, rng, d) in enumerate(IND):
        if rng is None: continue
        v = rnd.uniform(*rng); NUM[r][c] = v; VAL[r][c] = fmt(v, d)
    NUM[r][CALC] = NUM[r][13] / NUM[r][12] * 100; VAL[r][CALC] = fmt(NUM[r][CALC], 1)
VAL[4][3] = '&lt;5'; VAL[6][3] = '&lt;abc'
EMPTY = {(9, 1), (12, 13)}

def ds_head():
    h = '<tr><th class="sel"></th><th style="width:150px;text-align:left;padding-left:6px">Спортсмен</th>'
    for c, (n, u, rng, d) in enumerate(IND):
        h += f'<th style="width:54px">{n}<small>{u}</small></th>'
    h += '<th style="width:44px">Подг.</th><th style="width:118px;text-align:left;padding-left:6px">Строка</th></tr>'
    return h

def session_hdr(prim_label=None):
    return """<div class="hdr">
<div class="ctl"><label>Дата сеанса</label><div class="tb">03.10.2026</div></div>
<div class="ctl"><label>Панель</label><div class="cb"><div class="tb" style="width:230px">Лабораторная базовая, версия 3</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Группа и порядок как на бланке</label><div class="cb"><div class="tb" style="width:220px">Группа А, 13 спортсменов</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Исполнитель</label><div class="cb"><div class="tb" style="width:90px">Врач</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Enter переходит</label><div class="cb"><div class="tb" style="width:130px">вниз по столбцу</div><div class="dd">▼</div></div></div>
<div style="flex:1"></div><span class="btn">Печать бланка</span></div>"""

LEGEND = """<div class="legend"><span><span class="k" style="color:#1F4E99">12</span>набрано, ещё не сохранено</span>
<span><span class="k" style="color:#7F7F7F;font-style:italic">12</span>сохранено как черновик</span>
<span><span class="k">12</span>подтверждено</span>
<span><span class="k" style="background:#F8CBAD;color:#C00000">12</span>ошибка</span>
<span><span class="k" style="background:#FFE699">12</span>изменено в другом окне</span>
<span><span class="k" style="background:#E7E6E6;color:#595959">12</span>ответ не получен</span>
<span>Пустая ячейка — записи нет. Значения со знаком &lt; или &gt; остаются как записаны.</span></div>"""

def recnav(cur, total, nf='Нет фильтра'):
    return f'<div class="recnav">Запись: <span>|◄</span><span>◄</span><span class="n">{cur} из {total}</span><span>►</span><span>►|</span><span>►*</span><span style="margin-left:10px">▽ {nf}</span><span class="f">Поиск</span></div>'

def frame_entry():
    rows = ''; typed = 0
    for r, name in enumerate(ROWS):
        cur = (r == 11)
        sel = '✎' if cur else ''
        tr = f'<tr><td class="sel">{sel}</td><td class="t">{name}</td>'
        for c in range(len(IND)):
            cls, txt = '', ''
            if c == CALC: cls = 'calc'
            elif c <= 6 or (c == 7 and r <= 10):
                if (r, c) not in EMPTY: cls, txt = 'loc', VAL[r][c]; typed += 1
            if (r, c) == (6, 3): cls = 'err'
            if (r, c) == (11, 7): cls = 'cur'
            tr += f'<td class="{cls}">{txt}</td>'
        chk = '<td class="chkc"><i class="on"></i></td>' if r <= 10 else '<td class="chkc"><i></i></td>'
        st = '<td class="t" style="color:#C00000">1 ошибка</td>' if r == 6 else '<td class="t" style="color:#1F4E99">набирается</td>'
        rows += tr + chk + st + '</tr>'
    rows += '<tr><td class="sel">*</td><td class="t"></td>' + '<td></td>' * (len(IND) + 2) + '</tr>'
    total = len(ROWS) * (len(IND) - 1)
    body = session_hdr() + f"""<div class="sub"><div class="cap">Результаты сеанса</div><table class="ds">{ds_head()}{rows}</table>{recnav(12, 13)}</div>
{LEGEND}
<div class="cf"><div class="cap">Требует внимания <span style="color:#555">1</span></div>
<div class="row"><span>Спортсмен 07</span><span>Ферр</span><span>«&lt;abc» не сохранится: после знака &lt; нужно число, например «&lt;5»</span><span class="ac"><span class="btn">Перейти к ячейке</span></span></div></div>
<div class="foot"><div class="cnt"><span><b>{typed}</b> набрано из {total}</span><span><b>0</b> в базе</span><span><b>11</b> подготовок отмечено</span></div><div class="sp"></div>
<span class="note">Набранное хранится на этом компьютере, пока вы не сохраните черновики</span>
<span class="btn">Проверить</span><span class="btn pri">Сохранить черновики</span><span class="btn dis">Подтвердить сеанс</span></div>"""
    return window('Ввод сеанса', ['Сегодня', 'Ввод сеанса'], body, menu_on='Ввод сеанса')

def frame_confirmed():
    rows = ''; done = 0; nd = 0; vals = 0
    for r, name in enumerate(ROWS):
        tr = f'<tr><td class="sel">{"▶" if r == 6 else ""}</td><td class="t">{name}</td>'
        for c in range(len(IND)):
            cls, txt = '', VAL[r][c]
            if c == CALC:
                cls = 'calc'
                if (r, 12) in EMPTY or (r, 13) in EMPTY: txt = ''
            elif (r, c) in EMPTY: txt = ''
            else:
                vals += 1
                if (r, c) == (6, 3): cls = 'err'; nd += 1
                elif (r, c) == (10, 12): cls = 'con'; nd += 1
                elif (r, c) == (3, 10): cls = 'unk'; nd += 1
                else: done += 1
            tr += f'<td class="{cls}">{txt}</td>'
        chk = '<td class="okg">✓</td>' if r <= 10 else '<td></td>'
        if r == 6: st = '<td class="t" style="color:#C00000">1 ошибка</td>'
        elif r == 10: st = '<td class="t" style="color:#7F6000">1 изменение</td>'
        elif r == 3: st = '<td class="t" style="color:#595959">проверяется</td>'
        else: st = '<td class="t" style="color:#548235">подтверждено</td>'
        rows += tr + chk + st + '</tr>'
    rows += '<tr><td class="sel">*</td><td class="t"></td>' + '<td></td>' * (len(IND) + 2) + '</tr>'
    body = session_hdr() + f"""<div class="msg"><b>Подтверждено {done} значений из {vals}.</b> Ещё {nd} ждут вашего решения — они в списке ниже. На остальные ячейки это не влияет.<div style="flex:1"></div><span class="btn">Повторить для неподтверждённых</span></div>
<div class="sub"><div class="cap">Результаты сеанса</div><table class="ds">{ds_head()}{rows}</table>{recnav(7, 13)}</div>
{LEGEND}
<div class="cf"><div class="cap">Требует внимания <span style="color:#555">{nd}</span></div>
<div class="row"><span>Спортсмен 07</span><span>Ферр</span><span>«&lt;abc» не сохранено. Сверьтесь с бланком, исправьте и подтвердите ячейку.</span><span class="ac"><span class="btn">Перейти к ячейке</span></span></div>
<div class="row"><span>Спортсмен 11</span><span>Корт</span><span>Значение изменили в другом окне после вашего сохранения. Сравните и подтвердите заново.</span><span class="ac"><span class="btn">Сравнить значения</span></span></div>
<div class="row"><span>Спортсмен 04</span><span>КФК</span><span>Ответ от базы не пришёл. Программа проверит, записалось ли значение; двойной записи не будет.</span><span class="ac"><span class="btn">Проверить запись</span></span></div></div>
<div class="foot"><div class="cnt"><span><b>{done}</b> подтверждено</span><span><b>{nd}</b> требуют внимания</span><span><b>11</b> подготовок подтверждено</span></div><div class="sp"></div>
<span class="btn">Приложить фото бланка</span><span class="btn">Подтвердить подготовки</span><span class="btn pri">Подтвердить сеанс</span></div>"""
    return window('Ввод сеанса', ['Сегодня', 'Ввод сеанса'], body, menu_on='Ввод сеанса')

BLANK_CSS = r"""*{box-sizing:border-box}body{margin:0;background:#D9DEDC;font-family:Carlito,'Liberation Sans',sans-serif;color:#111}
.sheet{width:1122px;height:794px;background:#fff;margin:0 auto;padding:34px 38px;display:flex;flex-direction:column}
.top{display:flex;align-items:flex-end;gap:28px;border-bottom:2px solid #111;padding-bottom:8px}.top h1{font-size:22px;margin:0;font-weight:700}
.top .m{font-size:13.5px}.top .m b{font-size:15px}.top .r{margin-left:auto;text-align:right;font-size:12px;color:#444}
table{border-collapse:collapse;margin-top:12px;table-layout:fixed;width:100%}
th{border:1.2px solid #222;font-size:12.5px;padding:3px 1px;font-weight:700;height:40px;line-height:1.1}th small{display:block;font-weight:400;font-size:10px;color:#333}th.c{background:#EEE;color:#555}
td{border:1px solid #444;height:44px}td.n{text-align:left;padding-left:6px;font-size:13px;white-space:nowrap}
td.c{background:repeating-linear-gradient(135deg,#F4F4F4 0 6px,#E9E9E9 6px 7px)}td.p{text-align:center}td.p span{display:inline-block;width:14px;height:14px;border:1.3px solid #222}
.foot{margin-top:auto;display:flex;gap:30px;font-size:12px;color:#333;align-items:flex-end}.foot .sig{margin-left:auto;font-size:13px;color:#111}"""

def frame_blank():
    head = '<tr><th style="width:24px">№</th><th style="width:118px;text-align:left;padding-left:6px">Спортсмен</th>'
    for c, (n, u, rng, d) in enumerate(IND):
        head += f'<th{" class=c" if c == CALC else ""}>{n}<small>{u}</small></th>'
    head += '<th style="width:40px">Подг.</th></tr>'
    rows = ''
    for r, name in enumerate(ROWS):
        rows += f'<tr><td style="text-align:center;font-size:12px">{r+1}</td><td class="n">{name}</td>' + ''.join('<td class="c"></td>' if c == CALC else '<td></td>' for c in range(len(IND))) + '<td class="p"><span></span></td></tr>'
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{BLANK_CSS}</style></head><body><div class="sheet">
<div class="top"><h1>Бланк переноса результатов</h1><div class="m">Дата сеанса <b>03.10.2026</b></div><div class="m">Панель <b>Лабораторная базовая, версия 3</b></div><div class="m">Группа <b>А</b></div><div class="r">Напечатано из СпортКонтроль<br>Экземпляр 2026-10-03-01</div></div>
<table>{head}{rows}</table>
<div class="foot"><span>Строки и столбцы в том же порядке, что на экране «Ввод сеанса».<br>Серый столбец программа считает сама. Служебная форма, не медицинский отчёт.</span><span class="sig">Врач ____________________</span></div></div></body></html>"""

def frame_history():
    W, H = 1180, 268; x0, x1, yT, yB = 54, W - 16, 14, H - 30
    d0, d1 = dt.date(2023, 1, 1), dt.date(2026, 11, 1); vmax = 320
    Y = lambda v: yB - v / vmax * (yB - yT)
    X = lambda d: x0 + (d - d0).days / (d1 - d0).days * (x1 - x0)
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Carlito,Liberation Sans" font-size="12">']
    s.append(f'<rect x="{x0}" y="{yT}" width="{x1-x0}" height="{yB-yT}" fill="#fff" stroke="#D9D9D9"/>')
    for v in (0, 50, 100, 150, 200, 250, 300):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#E6E6E6"/><text x="{x0-6}" y="{Y(v)+4:.1f}" text-anchor="end" fill="#595959">{v}</text>')
    for yr in (2023, 2024, 2025, 2026):
        xx = X(dt.date(yr, 1, 1)); s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{yT}" y2="{yB}" stroke="#E6E6E6"/><text x="{xx+4:.1f}" y="{yB+16}" fill="#595959">{yr}</text>')
    def step(points, color, dash):
        pts = ' '.join(f'{X(d):.1f},{Y(v):.1f}' for d, v in points)
        s.append(f'<polyline fill="none" stroke="{color}" stroke-width="1.6" stroke-dasharray="{dash}" points="{pts}"/>')
    r1a, r1b, r2a = dt.date(2023, 1, 1), dt.date(2024, 6, 1), dt.date(2024, 9, 1)
    step([(r1a, 300), (r1b, 300)], '#7F7F7F', '5 4'); step([(r1a, 30), (r1b, 30)], '#7F7F7F', '5 4')
    step([(r2a, 250), (d1, 250)], '#7F7F7F', '5 4'); step([(r2a, 20), (d1, 20)], '#7F7F7F', '5 4')
    s.append(f'<text x="{X(r1a)+6:.1f}" y="{Y(300)-5:.1f}" fill="#595959">норма 30–300 (лаборатория А, версия 1)</text>')
    s.append(f'<text x="{X(r2a)+6:.1f}" y="{Y(250)-5:.1f}" fill="#595959">норма 20–250 (лаборатория Б, версия 2)</text>')
    s.append(f'<text x="{(X(r1b)+X(r2a))/2:.1f}" y="{yT+16}" text-anchor="middle" fill="#595959" font-size="11">норма</text><text x="{(X(r1b)+X(r2a))/2:.1f}" y="{yT+29}" text-anchor="middle" fill="#595959" font-size="11">не известна</text>')
    pts = [(dt.date(2023, 2, 14), 64), (dt.date(2023, 5, 20), 88), (dt.date(2023, 9, 11), 52), (dt.date(2024, 1, 22), 41), (dt.date(2024, 4, 15), 27), (dt.date(2024, 7, 8), None), (dt.date(2024, 10, 2), 15), (dt.date(2025, 1, 20), 33), (dt.date(2025, 4, 14), 58), (dt.date(2025, 7, 7), 96), (dt.date(2025, 10, 6), 81), (dt.date(2026, 1, 19), 70), (dt.date(2026, 4, 13), 64), (dt.date(2026, 7, 6), 59), (dt.date(2026, 10, 3), 47)]
    seg = []; paths = []
    for d, v in pts:
        if v is None:
            if seg: paths.append(seg); seg = []
        else: seg.append((X(d), Y(v)))
    if seg: paths.append(seg)
    for p in paths: s.append('<polyline fill="none" stroke="#2F5496" stroke-width="2" points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in p) + '"/>')
    for d, v in pts:
        if v is None:
            x, y = X(d), Y(10); s.append(f'<path d="M{x-6:.1f},{y-6:.1f} L{x+6:.1f},{y-6:.1f} L{x:.1f},{y+5:.1f} Z" fill="#fff" stroke="#2F5496" stroke-width="1.5"/><text x="{x+9:.1f}" y="{y-2:.1f}" fill="#2F5496">&lt;10</text>'); continue
        low = (d < r1b and v < 30) or (d >= r2a and v < 20)
        s.append(f'<circle cx="{X(d):.1f}" cy="{Y(v):.1f}" r="4.5" fill="{"#C00000" if low else "#2F5496"}"/>')
        if d == dt.date(2026, 10, 3): s.append(f'<text x="{X(d)-8:.1f}" y="{Y(v)+22:.1f}" text-anchor="end" fill="#000" font-weight="700">47 (03.10.2026)</text>')
    s.append(f'<g font-size="12" fill="#333"><circle cx="{x0+14}" cy="{H-8}" r="4" fill="#2F5496"/><text x="{x0+24}" y="{H-4}">значение</text><circle cx="{x0+110}" cy="{H-8}" r="4" fill="#C00000"/><text x="{x0+120}" y="{H-4}">ниже нормы на дату измерения</text><line x1="{x0+330}" x2="{x0+360}" y1="{H-8}" y2="{H-8}" stroke="#7F7F7F" stroke-dasharray="5 4" stroke-width="1.6"/><text x="{x0+368}" y="{H-4}">границы нормы, которая действовала в тот период</text></g>')
    s.append('</svg>')
    chart = ''.join(s)
    body = f"""<div class="hdr"><div class="ctl"><label>Спортсмен</label><div class="cb"><div class="tb" style="width:180px">Спортсмен 04</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Показатель</label><div class="cb"><div class="tb" style="width:170px">Ферритин, нг/мл</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Период</label><div class="cb"><div class="tb" style="width:210px">с 01.01.2023 по 03.10.2026</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>&nbsp;</label><span class="chk"><i class="on"></i>Показывать справочные обстоятельства</span></div><div style="flex:1"></div><span class="btn">Открыть отчёт</span></div>
<div class="sub" style="padding:4px 6px"><div class="cap" style="margin:-4px -6px 4px">Динамика показателя</div>{chart}</div>
<div style="display:flex;flex-direction:column;gap:8px;margin-top:8px">
<div class="sub"><div class="cap">Справочные обстоятельства</div><table class="ds">
<tr><th class="sel"></th><th style="width:260px;text-align:left;padding-left:6px">Что</th><th style="width:200px;text-align:left;padding-left:6px">Откуда известно</th><th style="width:100px">С</th><th style="width:100px">По</th><th style="text-align:left;padding-left:6px">Примечание</th></tr>
<tr><td class="sel"></td><td class="t">Препарат железа X</td><td class="t">со слов</td><td>10.10.2024</td><td>15.01.2025</td><td class="t">курс окончен</td></tr>
<tr><td class="sel"></td><td class="t">Препарат железа X</td><td class="t">подтверждено документом</td><td>01.03.2025</td><td>30.06.2025</td><td class="t">курс окончен</td></tr>
<tr><td class="sel"></td><td class="t">Витамин D</td><td class="t">со слов</td><td>01.11.2025</td><td></td><td class="t">принимал по сообщению на 01.02.2026, дальше сведений нет</td></tr>
<tr><td class="sel"></td><td class="t">Индивидуальная особенность</td><td class="t">со слов</td><td></td><td></td><td class="t">без даты, сообщена врачу</td></tr>
<tr><td class="sel">*</td><td></td><td></td><td></td><td></td><td></td></tr></table>{recnav(1, 4)}</div>
<div class="sub"><div class="cap">Измерения</div><table class="ds">
<tr><th class="sel"></th><th style="width:110px">Дата</th><th style="width:90px">Значение</th><th style="width:300px;text-align:left;padding-left:6px">Относительно нормы на ту дату</th><th style="text-align:left;padding-left:6px">Кто и когда подтвердил</th></tr>
<tr><td class="sel"></td><td>03.10.2026</td><td>47</td><td class="t">в норме</td><td class="t">Врач, 03.10.2026</td></tr>
<tr><td class="sel"></td><td>06.07.2026</td><td>59</td><td class="t">в норме</td><td class="t">Врач, 06.07.2026</td></tr>
<tr><td class="sel"></td><td>02.10.2024</td><td>15</td><td class="t" style="color:#C00000">ниже</td><td class="t">Врач, 05.10.2024, исправлено</td></tr>
<tr><td class="sel"></td><td>08.07.2024</td><td>&lt;10</td><td class="t">норма не известна</td><td class="t">перенос из архива</td></tr>
<tr><td class="sel">*</td><td></td><td></td><td></td><td></td></tr></table>{recnav(1, 15)}</div></div>
<div class="note" style="margin-top:8px">Справочные обстоятельства — только для понимания картины. Выключите их — значения, нормы и подсчёты не изменятся.</div>"""
    return window('Спортсмен 04', ['Сегодня', 'Спортсмены', 'Спортсмен 04'], body, menu_on='Спортсмены')

def frame_report_params():
    cks = ''.join(f'<span class="chk" style="width:150px;margin:3px 0"><i class="{"on" if c in (0,3,7,10,12,13) else ""}"></i>{IND[c][0]}, {IND[c][1]}</span>' for c in range(len(IND)) if c != CALC)
    body = f"""<div style="max-width:760px"><div style="font-size:18px;margin:4px 0 12px">Отчёт для тренерского штаба</div>
<div class="hdr"><div class="ctl"><label>Группа</label><div class="cb"><div class="tb" style="width:160px">Группа А</div><div class="dd">▼</div></div></div>
<div class="ctl"><label>Измерения с</label><div class="tb" style="width:110px">01.09.2026</div></div><div class="ctl"><label>по (включительно)</label><div class="tb" style="width:110px">03.10.2026</div></div>
<div class="ctl"><label>Шаблон</label><div class="cb"><div class="tb" style="width:180px">Тренерский, версия 2</div><div class="dd">▼</div></div></div></div>
<div class="sub" style="padding:8px 10px"><div class="cap" style="margin:-8px -10px 8px">Какие показатели включить</div><div style="display:flex;flex-wrap:wrap;gap:4px 10px">{cks}</div></div>
<div class="sub" style="padding:8px 10px;margin-top:10px"><div class="cap" style="margin:-8px -10px 8px">Что ещё показать тренеру</div>
<div style="display:flex;flex-direction:column;gap:6px;font-size:14px"><span class="chk"><i class="on"></i>Границы нормы под названием показателя</span><span class="chk"><i class="on"></i>Отметки «ниже» и «выше» нормы</span><span class="chk"><i></i>Справочные обстоятельства (по умолчанию не показываются)</span><span class="chk"><i></i>Фамилии полностью (иначе — как в списке группы)</span></div></div>
<div class="ctl" style="margin-top:10px"><label>Комментарий врача (печатается отдельно от цифр)</label><div class="tb" style="height:56px;align-items:flex-start;padding-top:4px">Группе рекомендован повторный контроль ферритина через месяц.</div></div>
<div class="foot"><span class="note">Сначала посмотрите, как выглядит отчёт. Выпуск сохраняет его как есть: позже цифры в этом документе уже не изменятся.</span><div class="sp"></div><span class="btn pri">Предварительный просмотр</span><span class="btn">Отмена</span></div></div>"""
    return window('Отчёт тренеру', ['Сегодня', 'Отчёты', 'Отчёт тренеру'], body, menu_on='Отчёты')

def frame_report_preview():
    sel = [0, 3, 7, 10, 12, 13]; refs = {0: '130–160', 3: '20–250', 7: '62–115', 10: 'до 400', 12: '170–540', 13: '8,6–29'}
    limits = {0: (130, 160), 3: (20, 250), 7: (62, 115), 10: (0, 400), 12: (170, 540), 13: (8.6, 29)}
    head = '<tr><th style="text-align:left">Спортсмен</th>' + ''.join(f'<th>{IND[c][0]}<small>{IND[c][1]}<br>норма {refs[c]}</small></th>' for c in sel) + '</tr>'
    rows = ''
    for r, name in enumerate(ROWS):
        rows += f'<tr><td class="nm">{name}</td>'
        for c in sel:
            v = NUM[r][c]; txt = VAL[r][c]
            if (r, c) == (4, 3): rows += '<td>&lt;5 <span class="mk">ниже</span></td>'; continue
            if (r, c) == (6, 3): txt = '31'; v = 31
            lo, hi = limits[c]; mk = ''
            if v > hi: mk = '<span class="mk">выше</span>'
            if v < lo: mk = '<span class="mk">ниже</span>'
            rows += f'<td>{txt} {mk}</td>'
        rows += '</tr>'
    css_extra = """<style>.pv{flex:1;background:#8C8C8C;display:flex;justify-content:center;padding:14px;overflow:hidden;margin:-12px -14px -8px}
.page{background:#fff;width:800px;padding:28px 34px;box-shadow:0 0 6px rgba(0,0,0,.4);font-family:Carlito,'Liberation Sans',sans-serif}
.page h2{font-size:20px;margin:0 0 2px}.page .sub2{font-size:13px;color:#333;margin-bottom:12px}
.page table{border-collapse:collapse;width:100%;font-size:13px}.page th{border:1px solid #666;background:#F2F2F2;padding:4px;font-size:12.5px;line-height:1.15}
.page th small{display:block;font-weight:400;font-size:10.5px;color:#444}.page td{border:1px solid #999;padding:3px 6px;text-align:right;white-space:nowrap}
.page td.nm{text-align:left}.page .mk{font-size:10.5px;border:1px solid #C00000;color:#C00000;padding:0 3px;margin-left:3px}
.page .note{font-size:11.5px;color:#444;margin-top:10px;line-height:1.4}.page .concl{margin-top:12px;border:1px solid #999;padding:8px 10px;font-size:13px}
.page .concl b{display:block;margin-bottom:4px}.page .ft{margin-top:14px;font-size:11px;color:#555;display:flex;justify-content:space-between}</style>"""
    body = f"""{css_extra}<div class="pv"><div class="page"><h2>Лабораторный контроль, группа А</h2><div class="sub2">Измерения с 01.09.2026 по 03.10.2026. Для тренерского штаба.</div>
<table>{head}{rows}</table>
<div class="note">Границы нормы — те, что действовали на дату измерения. «Ниже» и «выше» — сравнение с нормой, не медицинское заключение.</div>
<div class="concl"><b>Комментарий врача</b>Группе рекомендован повторный контроль ферритина через месяц.</div>
<div class="ft"><span>СпортКонтроль, предварительный просмотр</span><span>Страница 1 из 1</span></div></div></div>"""
    return window('Отчёт тренеру', ['Сегодня', 'Отчёты', 'Отчёт тренеру'], body, mode='Предварительный просмотр', tab_on='Предварительный просмотр', ribbon=ribbon_preview(), extra_tab='Предварительный просмотр', with_menu=False)

FRAMES = [('blank', frame_blank(), (1122, 794)), ('entry', frame_entry(), (1440, 960)), ('confirmed', frame_confirmed(), (1440, 960)),
          ('history', frame_history(), (1440, 960)), ('report_params', frame_report_params(), (1440, 960)), ('report_preview', frame_report_preview(), (1440, 960))]

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, (w, h) in FRAMES:
        (OUT / f'{name}.html').write_text(html, encoding='utf-8')
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2)
        pg.set_content(html); pg.wait_for_timeout(120)
        pg.screenshot(path=str(OUT / f'{name}.png')); pg.close()
    b.close()
print('ok')