

def show(filename):
    import importlib.resources as pkg_resources
    from IPython.display import display, Image
    package = "theory"
    filename += '.png'
    try:
        with pkg_resources.path(package, filename) as file_path:
            img = Image(filename=str(file_path))
            display(img)
    except Exception as e:
        print(f'Неправильное имя файла: {e}')
    return filename


def show_pdf(filename):
    import importlib.resources as pkg_resources
    from IPython.display import display, IFrame
    package = "numpyp.theory"
    filename += '.pdf'
    try:
        with pkg_resources.path(package, filename) as file_path:
            # Создаем IFrame для отображения PDF
            pdf_iframe = IFrame(src=str(file_path), width=1000, height=800)
            display(pdf_iframe)
    except Exception as e:
        print(f'Неправильное имя файла: {e}')
    return filename

def info():
    print('info1() code 1-10')
    print('info2() code 11-20')
    print('info3() code 21-29')

    print('info4() theory 30-40')
    print('info5() theory 41-42')
    print('info6() theory 51-60')
    print('info7() theory 61-70')
    print('info8() theory 71-80')
    print('info9() theory 81-90')


def info1():
    print('p1() Метод половинного деления (бисекции)')


