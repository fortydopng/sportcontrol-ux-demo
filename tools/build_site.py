from pathlib import Path
from PIL import Image
import shutil, json

SRC = Path('/home/claude/site/frames'); WEB = Path('/home/claude/site/web'); IMG = WEB / 'img'
if WEB.exists(): shutil.rmtree(WEB)
IMG.mkdir(parents=True)

# crops in 1x coordinates of the frame (scale 2 in PNG)
CROPS = {
 'blank': [('Шапка бланка', (0, 0, 1122, 130)), ('Левая половина', (0, 90, 600, 760)), ('Правая половина', (520, 90, 1122, 760))],
 'entry': [('Шапка сеанса', (195, 90, 1440, 142)), ('Сетка, левая часть', (195, 148, 830, 560)), ('Сетка, правая часть', (760, 148, 1440, 560)), ('Подсказки и кнопки', (195, 560, 1440, 730))],
 'confirmed': [('Итог подтверждения', (195, 148, 1440, 196)), ('Сетка, левая часть', (195, 200, 830, 610)), ('Сетка, правая часть', (760, 200, 1440, 610)), ('Что требует внимания', (195, 665, 1440, 860))],
 'history': [('График', (195, 148, 1440, 440)), ('Справочные обстоятельства', (195, 440, 1440, 640)), ('Измерения', (195, 640, 1440, 870))],
 'report_params': [('Выбор показателей', (195, 90, 1000, 400)), ('Что ещё показать', (195, 400, 1000, 720))],
 'report_preview': [('Таблица отчёта', (320, 185, 1070, 600)), ('Комментарий врача', (320, 580, 1070, 700))],
}
manifest = {}
for name in CROPS:
    im = Image.open(SRC / f'{name}.png')
    im.save(IMG / f'{name}.png', optimize=True)
    manifest[name] = []
    for i, (title, (x0, y0, x1, y1)) in enumerate(CROPS[name], 1):
        c = im.crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2))
        fn = f'{name}_z{i}.png'; c.save(IMG / fn, optimize=True)
        manifest[name].append((title, fn))

def slide(frame, caption, more, alt):
    zooms = ''.join(f'<button class="zoom" type="button" data-src="img/{fn}" data-cap="{alt} — {t}">{t}</button>' for t, fn in manifest[frame])
    return f'''<li class="slide">
 <figure><button class="open" type="button" data-src="img/{frame}.png" data-cap="{alt}"><img src="img/{frame}.png" alt="{alt}" loading="lazy"></button>
 <figcaption>{caption}</figcaption></figure>
 <div class="zooms"><span>Крупнее:</span>{zooms}</div>
 <details class="more"><summary>Подробнее</summary>{more}</details>
</li>'''

def slider(sid, slides):
    dots = ''.join(f'<button type="button" aria-label="кадр {i+1}"></button>' for i in range(len(slides)))
    return f'''<div class="slider" id="{sid}">
 <div class="track"><ul class="slides">{"".join(slides)}</ul></div>
 <div class="ctrls"><button class="prev" type="button" aria-label="Предыдущий кадр">‹</button><div class="dots">{dots}</div><button class="next" type="button" aria-label="Следующий кадр">›</button></div>
</div>'''

S1 = slider('s1', [
 slide('blank', 'Бланк печатается из программы: те же люди и те же столбцы, что потом будут на экране. Записываете рукой, как привыкли.',
       '<p>Программа печатает бланк на выбранную группу и дату. Столбцы идут в том же порядке, что и на экране ввода, поэтому переносить цифры можно глазами по позиции, не ища строку. Пустая клетка «Подг.» — чтобы отметить, кому сделана пробоподготовка. Серый столбец расчётный, его заполнять не нужно.</p><p>Бланк остаётся частью вашей технологии. Фотографию заполненного листа потом можно приложить к сеансу, но это не обязательно.</p>',
       'Бланк переноса результатов'),
 slide('entry', 'Ввод идёт по столбцам: напечатали число, Enter, курсор ниже. Синее — набрано, но ещё не сохранено в базе.',
       '<p><b>Шапка</b> заполняется один раз на сеанс: дата, панель, группа. Фамилии и даты рождения уже в программе.</p><p><b>Сетка</b> повторяет бланк. Пустая клетка значит «записи нет» — программа не додумывает «не измерялось». Ноль надо напечатать явно. Значение вроде «&lt;5» так и записывается.</p><p><b>Опечатка</b> подсвечивается и попадает в список «Требует внимания» внизу. Никаких всплывающих окон на каждую клетку: вы продолжаете печатать, а к ошибке возвращаетесь, когда удобно.</p><p><b>Сохранность.</b> Пока не нажата «Сохранить черновики», всё набранное хранится на этом компьютере. Если закрыть окно или выключится свет, при следующем открытии сеанс продолжится с того же места. Ничего не задвоится.</p>',
       'Экран ввода сеанса во время набора'),
 slide('confirmed', 'После «Подтвердить сеанс» виден точный итог: что подтверждено, а что ждёт вашего решения.',
       '<p><b>Подтверждение</b> — это ваша сверка с бланком, знак «я проверил». Программа подтверждает каждую клетку отдельно, поэтому одна опечатка не мешает остальным ста девяноста значениям.</p><p>На картинке три случая. Опечатка «&lt;abc» — просто исправить и подтвердить одну клетку. Значение, которое изменили в другом окне после вашего сохранения, — программа покажет оба варианта и попросит выбрать. Клетка, по которой не пришёл ответ от базы, — программа сама проверит, записалось ли значение, и никогда не запишет его дважды.</p><p><b>Пробоподготовка</b> подтверждается отдельной кнопкой: это отдельная услуга, и она не возникает сама собой из числа анализов.</p>',
       'Экран ввода сеанса после подтверждения'),
])
S2 = slider('s2', [
 slide('history', 'Синяя линия — значения. Пунктир — границы нормы, которые действовали в тот период. Красная точка — ниже нормы на дату измерения.',
       '<p><b>Нормы на дату.</b> Каждое измерение сравнивается с той нормой, которая была в силе в тот день, а не с сегодняшней. Если лаборатория сменила интервал, график это помнит и показывает, где норма поменялась и где её не было вовсе. Старые результаты не переоцениваются задним числом.</p><p><b>Значения вроде «&lt;10»</b> показываются отдельным значком и не соединяются линией: это не число, а «ниже порога прибора». В средние они не попадают.</p><p><b>Справочные обстоятельства</b> — приём препаратов, индивидуальные особенности — лежат отдельной таблицей и нужны только для понимания картины. Выключите их, и ни одно число, ни одна норма, ни один подсчёт не изменится.</p><p><b>Таблица измерений</b> показывает, кто и когда подтвердил каждое значение и что исправлялось. Старое значение при исправлении не исчезает.</p>',
       'История показателя у спортсмена'),
])
S3 = slider('s3', [
 slide('report_params', 'Выбираете, какие показатели и что ещё показывать тренеру. Справочные обстоятельства по умолчанию в отчёт не попадают.',
       '<p>Отчёт собирается из уже подтверждённых значений за выбранный период. Вы отмечаете показатели галочками, решаете, печатать ли границы нормы и отметки «ниже» и «выше», и пишете комментарий — он печатается отдельно от цифр.</p><p>Что не включено, того в отчёте нет совсем: ни в скрытых столбцах, ни в примечаниях. Сначала «Предварительный просмотр», потом «Выпустить».</p>',
       'Параметры отчёта для тренера'),
 slide('report_preview', 'Предварительный просмотр, как в Access: печать, PDF, Excel. «Ниже» и «выше» подписаны словами, а не только цветом.',
       '<p>Нормы в отчёте — те, что действовали на дату измерения. «Ниже» и «выше» — это сравнение с нормой, не диагноз, и об этом написано внизу страницы.</p><p>После «Выпустить» программа сохраняет отчёт как документ с номером и датой. Если потом вы исправите значение в базе, выпущенный отчёт останется прежним, а исправление попадёт в новый выпуск. Всегда можно поднять, что именно отправили тренеру в прошлый раз.</p>',
       'Предварительный просмотр отчёта тренеру'),
])

def faq(q, a): return f'<details class="faq"><summary>{q}</summary><div>{a}</div></details>'

HTML = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light">
<title>СпортКонтроль — как это будет выглядеть</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#about">К содержанию</a>
<header class="top">
 <div class="wrap">
  <a class="brand" href="#about"><b>СпортКонтроль</b><span>как это будет выглядеть</span></a>
  <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><span></span></button>
  <nav class="menu" id="menu">
   <a href="#about">О программе</a><a href="#session">Сеанс</a><a href="#history">История</a><a href="#report">Отчёт тренеру</a><a href="#faq">Вопросы</a>
  </nav>
 </div>
</header>

<main class="wrap">
<section id="about" class="intro">
 <h1>Как будет выглядеть СпортКонтроль</h1>
 <p class="lead">Это рисунки будущих экранов программы — чтобы вместе обсудить, как ей будет удобно пользоваться. Все фамилии и цифры здесь выдуманы. Экраны нарисованы так, как их позволяет сделать Microsoft Access 2024, без лишних украшений.</p>
 <div class="two">
  <div class="card"><h2>Что останется как есть</h2><ul>
   <li><b>Бумажный бланк.</b> Вы по-прежнему записываете результаты рукой в распечатанную таблицу.</li>
   <li><b>Порядок строк и столбцов.</b> На экране они те же, что на бланке: перенос идёт глазами по позиции, не ища строку.</li>
   <li><b>Нормы — в отчётах.</b> При вводе цифр подсказки и нормы не мешают; они появляются там, где нужны: в истории и у тренера.</li>
  </ul></div>
  <div class="card"><h2>Что станет проще</h2><ul>
   <li><b>Без лишнего набора.</b> Фамилии, даты рождения и шапка таблицы уже в программе: вы выбираете группу и печатаете только цифры.</li>
   <li><b>История в один клик.</b> Все годы по любому спортсмену и показателю, с нормами, которые действовали в тот день.</li>
   <li><b>Отчёт тренеру за минуты.</b> И он больше не меняется после выпуска.</li>
   <li><b>Ничего не теряется молча.</b> Что внесено, что подтверждено, кто и когда исправил — всегда видно.</li>
  </ul></div>
 </div>
 <div class="cards">
  <a class="scard" href="#session"><span class="num">Сценарий 1</span><b>Лабораторный сеанс</b><span>Бланк, ввод по столбцам, подтверждение</span></a>
  <a class="scard" href="#history"><span class="num">Сценарий 2</span><b>История спортсмена</b><span>Динамика, нормы на дату, справочные обстоятельства</span></a>
  <a class="scard" href="#report"><span class="num">Сценарий 3</span><b>Отчёт тренеру</b><span>Что показать, предпросмотр, выпуск</span></a>
 </div>
</section>

<section id="session" class="scen">
 <h2><span class="num">Сценарий 1</span>Лабораторный сеанс</h2>
 <p class="lead">Забор, пробоподготовка, анализ — всё как сейчас. Меняется только последний шаг: вместо Excel вы переносите цифры в СпортКонтроль, и дальше он берёт на себя остальное.</p>
 {S1}
 <div class="notice"><h3>Что вы заметите</h3><ul>
  <li>Время переноса примерно как в Excel: те же цифры и тот же Enter. Прибавляется минута на подтверждение.</li>
  <li>Не нужно копировать шапку, фамилии и даты рождения. Колонки не разъезжаются, цифры не превращаются в «####».</li>
  <li>Исправить можно и после подтверждения. Старое значение останется в истории с пометкой, кто и когда исправил.</li>
 </ul></div>
 {faq('Что, если я ошибся в цифре уже после подтверждения?', '<p>Открываете клетку, вводите верное значение и причину — старое значение не исчезает, а остаётся в истории с пометкой, кто и когда исправил. В отчёты, выпущенные раньше, исправление задним числом не попадает: оно пойдёт в следующий выпуск.</p>')}
 {faq('Как записать «меньше 5» или «больше 300»?', '<p>Так и печатаете: «&lt;5» или «&gt;300». Программа сохранит это как написано и не будет считать такое значение числом в средних.</p>')}
 {faq('Что будет, если компьютер выключится посреди ввода?', '<p>Набранное хранится на этом компьютере по мере ввода. При следующем открытии программа предложит продолжить сеанс с того же места. Ничего не задвоится: если какое-то значение уже успело записаться, оно так и останется одним.</p>')}
 {faq('Нужно ли отмечать пробоподготовку каждому?', '<p>Отметка ставится только вручную, по вашему решению: программа никогда не считает подготовку выполненной сама по себе из числа анализов. Можно отметить всех одной кнопкой, но это тоже ваше действие.</p>')}
</section>

<section id="history" class="scen">
 <h2><span class="num">Сценарий 2</span>История спортсмена</h2>
 <p class="lead">Открыли спортсмена, выбрали показатель — и видите все годы сразу. Не нужно искать старые файлы по сезонам.</p>
 {S2}
 <div class="notice"><h3>Что вы заметите</h3><ul>
  <li>Нормы разных лабораторий и разных лет не путаются: у каждого измерения — своя.</li>
  <li>Видно, кто и когда подтвердил каждое значение и что исправлялось.</li>
  <li>Справочные обстоятельства можно включать и выключать: на числа это не влияет.</li>
 </ul></div>
 {faq('Почему на графике две разные нормы?', '<p>Потому что в разные годы анализы делали разные лаборатории с разными интервалами. Программа помнит, какая норма действовала в какой период, и сравнивает каждое измерение с ней. Так старые результаты не переоцениваются по сегодняшней норме.</p>')}
 {faq('Что такое «норма не известна» на графике?', '<p>Для этого периода в программе нет сведений, какая норма действовала. Значение сохраняется и показывается, но без оценки «в норме» или «ниже». Когда норма за тот период станет известна, оценку можно добавить — с пометкой, что она восстановлена позже.</p>')}
</section>

<section id="report" class="scen">
 <h2><span class="num">Сценарий 3</span>Отчёт тренеру</h2>
 <p class="lead">Вы выбираете, что тренеру видеть, смотрите результат и выпускаете. Выпущенный отчёт больше не меняется.</p>
 {S3}
 <div class="notice"><h3>Что вы заметите</h3><ul>
  <li>Отчёт за минуты, без ручного форматирования таблиц.</li>
  <li>Чего не включили, того в файле нет — даже в скрытых ячейках.</li>
  <li>Всегда можно поднять, что именно отправили тренеру в прошлый раз, с номером и датой выпуска.</li>
 </ul></div>
 {faq('Можно ли показать тренеру нормы, но скрыть лишнее?', '<p>Да. Границы нормы и отметки «ниже» и «выше» включаются галочками, а справочные обстоятельства по умолчанию не показываются. Ваш комментарий печатается отдельно от цифр.</p>')}
 {faq('Что, если после выпуска нашлась ошибка?', '<p>Исправляете значение в базе и делаете новый выпуск. Старый остаётся как был — так всегда видно, что именно получал тренер раньше.</p>')}
</section>

<section id="faq" class="scen">
 <h2>Частые вопросы</h2>
 {faq('Это уже готовая программа?', '<p>Нет. Это рисунки для обсуждения, чтобы договориться, как должны выглядеть и вести себя экраны. Они нарисованы в рамках того, что умеет Microsoft Access 2024, чтобы не обещать лишнего.</p>')}
 {faq('Откуда данные на картинках?', '<p>Все фамилии, даты и цифры выдуманы и подобраны так, чтобы показать типичные ситуации: опечатку, значение «меньше порога», смену нормы.</p>')}
 {faq('Можно ли будет работать без мыши?', '<p>Да. Ввод рассчитан на клавиатуру: цифры и Enter. Мышь понадобится только для кнопок «Сохранить», «Подтвердить» и перехода между экранами.</p>')}
 {faq('Как будет с лактатом?', '<p>У лактата свои этапы: исход, 3…18, финиш, восстановление — и условные единицы. Для него будет отдельный экран ввода по этапам; его нарисуем следующим.</p>')}
 {faq('Что дальше?', '<p>Обсудить эти экраны, собрать ваши замечания и уточнить, что должно быть иначе. Потом — рабочая версия экрана ввода на тестовой базе с выдуманными данными, чтобы проверить время и удобство переноса на практике.</p>')}
</section>
</main>

<footer class="wrap foot"><p>СпортКонтроль, демонстрационные эскизы. Данные вымышленные. Экраны ориентированы на возможности Microsoft Access 2024.</p></footer>

<dialog id="lb" aria-label="Увеличенное изображение"><button class="close" type="button" aria-label="Закрыть">✕</button><img alt=""><p></p></dialog>
<script src="app.js"></script>
</body>
</html>'''

CSS = '''*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;font-family:"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#1F2A2E;background:#FAFAF9;line-height:1.5;font-size:17px}
a{color:#2F5496}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px;top:8px;background:#fff;padding:6px 10px}
.skip:focus{left:8px}
.top{position:sticky;top:0;z-index:20;background:#fff;border-bottom:1px solid #E3E6E5}
.top .wrap{display:flex;align-items:center;gap:20px;height:60px}
.brand{text-decoration:none;color:#1F2A2E;display:flex;flex-direction:column;line-height:1.1}
.brand b{font-size:19px}.brand span{font-size:12.5px;color:#5B6B70}
.menu{margin-left:auto;display:flex;gap:4px}
.menu a{text-decoration:none;color:#1F2A2E;padding:8px 12px;border-radius:6px;font-size:15.5px}
.menu a:hover{background:#F0F3F2}.menu a.on{background:#E7ECF7;color:#1F3864}
.burger{display:none;margin-left:auto;width:42px;height:42px;border:1px solid #D6DBDA;background:#fff;border-radius:6px;position:relative}
.burger span,.burger span::before,.burger span::after{content:'';position:absolute;left:11px;width:20px;height:2px;background:#1F2A2E;top:20px}
.burger span::before{top:-6px;left:0}.burger span::after{top:6px;left:0}
main{padding-top:10px}
section{padding:36px 0 10px;border-bottom:1px solid #E3E6E5;scroll-margin-top:70px}
section:last-of-type{border-bottom:0}
h1{font-size:34px;line-height:1.15;margin:12px 0 10px;font-weight:650}
h2{font-size:26px;margin:6px 0 10px;font-weight:650;display:flex;flex-direction:column;gap:2px}
h3{font-size:18px;margin:0 0 6px;font-weight:650}
.num{font-size:13.5px;color:#5B6B70;font-weight:500}
.lead{font-size:18.5px;color:#2B3A3F;max-width:70ch;margin:0 0 18px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:8px 0 22px}
.card{background:#fff;border:1px solid #E3E6E5;border-radius:10px;padding:16px 20px}
.card h2{font-size:19px;margin:0 0 6px}
.card ul{margin:0;padding-left:20px}.card li{margin:6px 0}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:10px}
.scard{display:flex;flex-direction:column;gap:3px;background:#fff;border:1px solid #E3E6E5;border-left:4px solid #2F5496;border-radius:10px;padding:14px 16px;text-decoration:none;color:#1F2A2E}
.scard b{font-size:17px}.scard span:last-child{font-size:14px;color:#5B6B70}
.slider{margin:14px 0 18px}
.track{overflow:hidden;border-radius:10px}
.slides{display:flex;margin:0;padding:0;list-style:none;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;gap:0}
.slides::-webkit-scrollbar{display:none}
.slide{flex:0 0 100%;scroll-snap-align:start;background:#fff;border:1px solid #E3E6E5;border-radius:10px;padding:14px 16px 12px}
.slide figure{margin:0}
.open{display:block;width:100%;padding:0;border:1px solid #D6DBDA;background:#fff;border-radius:6px;cursor:zoom-in;overflow:hidden}
.open img{display:block;width:100%;height:auto}
figcaption{font-size:16.5px;margin:10px 0 0;color:#1F2A2E}
.zooms{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:10px 0 0;font-size:14px;color:#5B6B70}
.zoom{border:1px solid #CFD6D4;background:#F6F8F7;border-radius:999px;padding:4px 11px;font-size:14px;color:#1F2A2E;cursor:zoom-in}
.zoom:hover{background:#E7ECF7;border-color:#9FB2DA}
.more{margin-top:10px;border-top:1px solid #EEF1F0;padding-top:8px}
.more summary,.faq summary{cursor:pointer;font-weight:600;color:#1F3864;padding:4px 0;list-style:none}
.more summary::before,.faq summary::before{content:'▸';display:inline-block;width:18px;color:#2F5496;transition:transform .15s}
details[open]>summary::before{transform:rotate(90deg)}
summary::-webkit-details-marker{display:none}
.more p,.faq p{margin:8px 0}
.ctrls{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:10px}
.ctrls .prev,.ctrls .next{width:40px;height:40px;border-radius:50%;border:1px solid #CFD6D4;background:#fff;font-size:22px;line-height:1;cursor:pointer;color:#1F2A2E}
.ctrls .prev:disabled,.ctrls .next:disabled{opacity:.35;cursor:default}
.dots{display:flex;gap:8px}
.dots button{width:11px;height:11px;border-radius:50%;border:1px solid #9FB2DA;background:#fff;padding:0;cursor:pointer}
.dots button.on{background:#2F5496;border-color:#2F5496}
.notice{background:#F2F6F4;border:1px solid #D9E5DF;border-radius:10px;padding:14px 18px;margin:10px 0 14px}
.notice ul{margin:0;padding-left:20px}.notice li{margin:5px 0}
.faq{background:#fff;border:1px solid #E3E6E5;border-radius:8px;padding:8px 14px;margin:8px 0}
.foot{padding:26px 20px 40px;color:#5B6B70;font-size:14px}
dialog#lb{border:0;padding:0;background:#111;max-width:100vw;max-height:100vh;width:100vw;height:100vh;margin:0;color:#fff}
dialog#lb::backdrop{background:#000}
dialog#lb[open]{display:flex;align-items:center;justify-content:center}
dialog#lb img{max-width:100vw;max-height:calc(100vh - 70px);width:auto;height:auto;display:block;margin:0 auto;touch-action:pinch-zoom}
dialog#lb p{margin:0;padding:10px 60px 10px 16px;font-size:15px;position:fixed;left:0;right:0;bottom:0;background:rgba(0,0,0,.65)}
dialog#lb .close{position:fixed;right:12px;top:12px;width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.5);background:rgba(0,0,0,.6);color:#fff;font-size:20px;cursor:pointer;z-index:2}
@media (max-width:860px){
 .two,.cards{grid-template-columns:1fr}
 .burger{display:block}
 .menu{display:none;position:absolute;left:0;right:0;top:60px;background:#fff;border-bottom:1px solid #E3E6E5;flex-direction:column;padding:8px 12px 12px}
 .menu.open{display:flex}
 .menu a{padding:12px 10px;font-size:17px}
 body{font-size:16.5px}
 h1{font-size:27px}h2{font-size:22px}.lead{font-size:17px}
 .slide{padding:10px 10px 10px}
 .open{cursor:pointer}
}
'''

JS = r'''(function(){
 var lb=document.getElementById('lb'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('p');
 function show(src,cap){lbImg.src=src;lbImg.alt=cap;lbCap.textContent=cap;if(typeof lb.showModal==='function'){lb.showModal();}else{lb.setAttribute('open','');}}
 document.querySelectorAll('.open,.zoom').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.src,b.dataset.cap);});});
 lb.querySelector('.close').addEventListener('click',function(){lb.close();});
 lb.addEventListener('click',function(e){if(e.target===lb||e.target===lbImg){lb.close();}});
 lb.addEventListener('close',function(){lbImg.src='';});
 var burger=document.querySelector('.burger'),menu=document.getElementById('menu');
 burger.addEventListener('click',function(){var o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o?'true':'false');});
 menu.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){menu.classList.remove('open');burger.setAttribute('aria-expanded','false');});});
 var links=menu.querySelectorAll('a');
 var secs=Array.prototype.map.call(links,function(a){return document.querySelector(a.getAttribute('href'));});
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id);});}});},{rootMargin:'-40% 0px -50% 0px'});secs.forEach(function(s){if(s)io.observe(s);});}
 document.querySelectorAll('.slider').forEach(function(sl){
  var ul=sl.querySelector('.slides'),slides=ul.querySelectorAll('.slide'),dots=sl.querySelectorAll('.dots button'),prev=sl.querySelector('.prev'),next=sl.querySelector('.next'),n=slides.length,i=0,t=null;
  if(n<2){sl.querySelector('.ctrls').style.display='none';return;}
  function paint(){dots.forEach(function(d,k){d.classList.toggle('on',k===i);d.setAttribute('aria-current',k===i?'true':'false');});prev.disabled=(i===0);next.disabled=(i===n-1);}
  function go(k,instant){i=Math.max(0,Math.min(n-1,k));paint();ul.scrollTo({left:i*ul.clientWidth,behavior:instant?'auto':'smooth'});}
  prev.addEventListener('click',function(){go(i-1);});
  next.addEventListener('click',function(){go(i+1);});
  dots.forEach(function(d,k){d.addEventListener('click',function(){go(k);});});
  ul.addEventListener('scroll',function(){clearTimeout(t);t=setTimeout(function(){var k=Math.max(0,Math.min(n-1,Math.round(ul.scrollLeft/ul.clientWidth)));if(k!==i){i=k;paint();}},120);});
  window.addEventListener('resize',function(){ul.scrollTo({left:i*ul.clientWidth,behavior:'auto'});});
  sl.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){e.preventDefault();go(i-1);}if(e.key==='ArrowRight'){e.preventDefault();go(i+1);}});
  sl.tabIndex=0;paint();
 });
})();'''

(WEB / 'index.html').write_text(HTML, encoding='utf-8')
(WEB / 'style.css').write_text(CSS, encoding='utf-8')
(WEB / 'app.js').write_text(JS, encoding='utf-8')
(WEB / '.nojekyll').write_text('', encoding='utf-8')
(WEB / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
(WEB / 'README.md').write_text('# СпортКонтроль — демонстрационные эскизы\n\nСайт для обсуждения будущих экранов программы: https://fortydopng.github.io/sportcontrol-ux-demo/\n\nВсе данные на эскизах вымышленные. Экраны ориентированы на возможности Microsoft Access 2024.\n', encoding='utf-8')
total = sum(f.stat().st_size for f in WEB.rglob('*') if f.is_file())
print('files', len(list(WEB.rglob('*'))), 'bytes', total)