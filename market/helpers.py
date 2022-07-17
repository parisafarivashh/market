

def fa_to_eng_number(number):
    if number is None:
        return number
    farsi = '۰۱۲۳۴۵۶۷۸۹'
    english = '0123456789'
    farsi_to_english = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9'
    }
    standard_number = ''
    for i in number:
        if i in farsi:
            standard_number += farsi_to_english[i]
        elif i in english:
            standard_number += i
    return standard_number

