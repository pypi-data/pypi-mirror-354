

def convert_english_to_urdu(text: str) -> str:
    """
    Convert English Number to Urdu
    """
    eng_to_urdu = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    return ''.join(eng_to_urdu.get(ch, ch) for ch in text)

def convert_urdu_to_english(text: str) -> str:
    """
    Convert Urdu Number to English
    """
    urdu_to_eng = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    return ''.join(urdu_to_eng.get(ch, ch) for ch in text)
