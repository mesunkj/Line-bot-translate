import asyncio
import time
from googletrans import Translator
from langdetect import detect, LangDetectException
import re
import json

# --- Prerequisites ---
# pip install googletrans==4.0.0rc1 langdetect

# --- Configuration ---
CHAR_LIMIT_FOR_SEGMENTATION = 15000
SOURCE_LANG_ZH = "zh-tw"
DEST_LANG_VI = "vi"

# --- 1. 文本處理與分段 ---
def segment_long_text(text: str) -> list[str]:
    """
    將長文本依據標點符號分割成多個短句，以處理超長文本翻譯。
    """
    sentences = re.split(r'([。！？.!?])', text)
    segments = []
    current_segment = ""
    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        if i + 1 < len(sentences):
            sentence += sentences[i+1]
        
        if len(current_segment) + len(sentence) <= CHAR_LIMIT_FOR_SEGMENTATION:
            current_segment += sentence
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = sentence
    if current_segment:
        segments.append(current_segment)
    return segments

# --- 2. 語言偵測與備援機制 ---
def detect_language_with_fallback(text: str) -> str:
    """
    偵測語言，並實作中/越文的備援邏輯。
    """
    try:
        lang = detect(text)
        if lang == 'vi':
            return 'vi'
        else:
            # 備援機制：如果不是越南文，預設為中文
            return 'zh-tw'
    except LangDetectException:
        # 處理無法偵測的情況，也預設為中文
        return 'zh-tw'

# --- 3. 翻譯核心模組 (非同步) ---
async def translate_text_part(translator: Translator, text: str, source_lang: str, dest_lang: str) -> str:
    """
    非同步地翻譯單一文本片段，使用 asyncio.to_thread 來處理同步翻譯。
    """
    try:
        # 使用 asyncio.to_thread 來包裝同步的 translator.translate() 呼叫
        translated = await asyncio.to_thread(translator.translate, text, src=source_lang, dest=dest_lang)
        return translated.text
    except Exception as e:
        print(f"翻譯錯誤 '{text[:20]}...': {e}")
        return text

async def execute_translation_flow(text: str) -> dict:
    """
    執行完整的翻譯流程，並測量時間。
    """
    start_time = time.time()
    
    if not text:
        return {
            "original_text": "",
            "translated_text": "",
            "execution_time": 0.0,
            "original_lang": "",
            "translated_lang": ""
        }

    if len(text) > CHAR_LIMIT_FOR_SEGMENTATION:
        text_parts = segment_long_text(text)
    else:
        text_parts = [text]

    source_lang = detect_language_with_fallback(text)
    dest_lang = DEST_LANG_VI if source_lang == SOURCE_LANG_ZH else SOURCE_LANG_ZH

    translator = Translator()
    tasks = [translate_text_part(translator, part, source_lang, dest_lang) for part in text_parts]
    translated_parts = await asyncio.gather(*tasks)
    translated_text = "".join(translated_parts)
    
    end_time = time.time()
    
    return {
        "original_text": text,
        "original_lang": source_lang,
        "translated_text": translated_text,
        "translated_lang": dest_lang,
        "execution_time": end_time - start_time
    }

# --- 4. 測試劇本與驗證邏輯 ---
async def run_validation_mode():
    """
    執行內建的測試劇本，並輸出詳細驗證報告。
    """
    test_cases_json = """
    [
        {
            "chinese": "李老師，您好。我是您的學生小蘭，很高興能和您進行這次視訊會議。",
            "vietnamese": "Chào thầy Lý. Em là Lan, học trò của thầy, rất vui được gặp thầy trong cuộc họp trực tuyến này."
        },
        {
            "chinese": "小蘭你好，我也很高興。你提交的關於水墨畫的報告我已經看過了，寫得很不錯。",
            "vietnamese": "Chào Lan, thầy cũng rất vui. Thầy đã đọc báo cáo của em về tranh thủy mặc rồi, viết rất tốt."
        },
        {
            "chinese": "謝謝老師的肯定。我想請教一下，報告中提到的「留白」技巧，我理解得還不夠深入。",
            "vietnamese": "Em cảm ơn lời khen của thầy. Em muốn hỏi về kỹ thuật 'để trắng' (liú bái) trong báo cáo, em cảm thấy mình hiểu chưa sâu."
        },
        {
            "chinese": "這是個很好的問題。留白不僅僅是留出空白，它其實是一種構圖和意境的表達。它讓觀者有想像的空間，也是中國畫講求「虛實相生」的精髓。",
            "vietnamese": "Đó là một câu hỏi rất hay. Để trắng không chỉ là chừa khoảng trống, nó thực ra là một cách diễn đạt về bố cục và ý cảnh. Nó cho phép người xem có không gian để tưởng tượng, và cũng là tinh hoa của triết lý 'hư thực tương sinh' trong hội họa Trung Quốc."
        },
        {
            "chinese": "原來如此。我原本只當作是未畫之處。",
            "vietnamese": "Thì ra là vậy. Trước đây em chỉ nghĩ đó là những phần chưa vẽ."
        },
        {
            "chinese": "是的，要掌握這種技巧，需要多觀察自然，將情感融入筆墨中，才能達到「此時無聲勝有聲」的境界。",
            "vietnamese": "Đúng vậy, để nắm vững kỹ thuật này, em cần quan sát thiên nhiên nhiều hơn và lồng cảm xúc vào từng nét bút, để đạt đến cảnh giới 'lúc này không có tiếng nói, còn hơn có tiếng nói'."
        },
        {
            "chinese": "老師您說的太好了。我會努力練習的。另外，我有一點點困惑。",
            "vietnamese": "Thầy nói hay quá. Em sẽ cố gắng luyện tập. Ngoài ra, em có một chút băn khoăn."
        },
        {
            "chinese": "請說，不用客氣。",
            "vietnamese": "Em cứ nói đi, đừng ngại."
        },
        {
            "chinese": "就是關於「點苔」這個技巧，我看您在第17號範例圖上示範過，但我自己嘗試的時候，總覺得不太自然。",
            "vietnamese": "Đó là về kỹ thuật 'chấm rêu' (diǎn tái). Em thấy thầy đã minh họa trong ví dụ số 17, nhưng khi tự mình thử, em cảm thấy nó không được tự nhiên cho lắm."
        },
        {
            "chinese": "點苔的筆法需要輕快、靈動，不能太過刻意。你試著用筆尖蘸少量的墨，以點擊的方式輕輕落在畫面上，而不是畫一個圓點。",
            "vietnamese": "Kỹ pháp chấm rêu cần nhẹ nhàng, linh hoạt, không nên quá cố ý. Em hãy thử dùng đầu cọ chấm một chút mực, dùng cách chấm nhẹ nhàng lên mặt giấy, chứ không phải vẽ một hình tròn."
        },
        {
            "chinese": "好的，我會記住的。我這份報告還需要修改嗎？",
            "vietnamese": "Vâng, em sẽ ghi nhớ. Báo cáo này của em có cần sửa đổi gì không ạ?"
        },
        {
            "chinese": "整體結構很好，內容也很豐富。但你可以嘗試在結論部分，加入你對中越兩國山水畫風格異同的一些個人見解，會讓報告更有深度。",
            "vietnamese": "Cấu trúc tổng thể rất tốt và nội dung cũng rất phong phú. Nhưng em có thể thử thêm một vài nhận định cá nhân về sự khác biệt và tương đồng giữa phong cách tranh sơn thủy của Trung Quốc và Việt Nam vào phần kết luận, điều đó sẽ làm cho báo cáo có chiều sâu hơn."
        },
        {
            "chinese": "哇，這是一個非常有創意的建議！我之前都沒想到這個角度。",
            "vietnamese": "Ồ, đây là một gợi ý rất sáng tạo! Trước đây em chưa từng nghĩ đến góc độ này."
        },
        {
            "chinese": "嗯，多思考、多比較，這是學習藝術的必經之路。藝術沒有標準答案，只有不斷的探索。",
            "vietnamese": "Ừm, suy nghĩ nhiều, so sánh nhiều, đó là con đường tất yếu trong học tập nghệ thuật. Nghệ thuật không có đáp án chuẩn, chỉ có sự khám phá không ngừng."
        },
        {
            "chinese": "我明白了，老師。謝謝您的教導！",
            "vietnamese": "Em đã hiểu rồi, thưa thầy. Em cảm ơn thầy đã chỉ bảo!"
        },
        {
            "chinese": "不客氣。另外，下週三下午兩點有一場關於書法的講座，你感興趣嗎？",
            "vietnamese": "Không có gì. Ngoài ra, chiều thứ Tư tuần sau lúc hai giờ có một buổi tọa đàm về thư pháp, em có quan tâm không?"
        },
        {
            "chinese": "太好了！我很感興趣！",
            "vietnamese": "Hay quá ạ! Em rất quan tâm!"
        },
        {
            "chinese": "好的，那我會請助教將連結發到你郵箱。講座的課程編號是20250819。",
            "vietnamese": "Được rồi, vậy thầy sẽ nhờ trợ giảng gửi đường link vào email của em. Mã số lớp học của buổi tọa đàm là 20250819."
        },
        {
            "chinese": "好的，老師，我收到了。對了，今天您看起來氣色很好。",
            "vietnamese": "Vâng, thưa thầy, em đã nhận được. À, hôm nay thầy trông có vẻ rất khỏe."
        },
        {
            "chinese": "哈哈，謝謝你。最近天氣不錯，心情也跟著好了起來。",
            "vietnamese": "Haha, cảm ơn em. Gần đây thời tiết rất đẹp, tâm trạng của thầy cũng tốt hơn."
        },
        {
            "chinese": "是的，台北最近也很舒服。",
            "vietnamese": "Vâng, Đài Bắc gần đây cũng rất dễ chịu ạ."
        },
        {
            "chinese": "嗯，小蘭，你的中文口語進步很快，發音也越來越標準了。",
            "vietnamese": "Ừm, Lan, khả năng nói tiếng Trung của em tiến bộ rất nhanh, phát âm cũng ngày càng chuẩn hơn rồi."
        },
        {
            "chinese": "真的嗎？謝謝老師！我每天都會花一個小時練習。",
            "vietnamese": "Thật ạ? Em cảm ơn thầy! Em dành một giờ mỗi ngày để luyện tập."
        },
        {
            "chinese": "堅持下去，你一定會取得更大的進步。",
            "vietnamese": "Hãy kiên trì, em chắc chắn sẽ đạt được tiến bộ lớn hơn nữa."
        },
        {
            "chinese": "我會的！老師，那我就不打擾您了。",
            "vietnamese": "Em sẽ làm vậy! Thưa thầy, vậy em xin phép không làm phiền thầy nữa."
        },
        {
            "chinese": "好，再見。",
            "vietnamese": "Được, tạm biệt."
        },
        {
            "chinese": "老師再見！",
            "vietnamese": "Chào thầy!"
        },
        {
            "chinese": "啊，對了，小蘭。",
            "vietnamese": "À, đúng rồi, Lan."
        },
        {
            "chinese": "是的，老師？",
            "vietnamese": "Vâng, thưa thầy?"
        },
        {
            "chinese": "別忘了去圖書館借閱那本《中國畫技法解析》，對你的報告很有幫助。",
            "vietnamese": "Đừng quên đến thư viện mượn cuốn 'Phân tích kỹ pháp hội họa Trung Quốc', nó sẽ rất hữu ích cho báo cáo của em đó."
        },
        {
            "chinese": "好的，謝謝老師的提醒！",
            "vietnamese": "Vâng, em cảm ơn lời nhắc của thầy!"
        }
    ]
    """
    test_cases_data = json.loads(test_cases_json)
    test_cases = []
    
    # 建立雙向測試案例
    for case in test_cases_data:
        test_cases.append({"original_text": case["chinese"], "expected_translation": case["vietnamese"]})
        test_cases.append({"original_text": case["vietnamese"], "expected_translation": case["chinese"]})

    total_tests = len(test_cases)
    passed_tests = 0
    
    print("--- 啟動翻譯可靠度驗證模式 ---")
    
    for i, case in enumerate(test_cases):
        print(f"\n--- 測試案例 {i+1}/{total_tests} ---")
        
        result = await execute_translation_flow(case["original_text"])
        
        is_passed = (result["translated_text"] == case["expected_translation"])
        
        print(f"原始文本: {result['original_text']}")
        print(f"偵測語言: {result['original_lang']}")
        print(f"翻譯結果: {result['translated_text']}")
        print(f"預期結果: {case['expected_translation']}")
        print(f"執行時間: {result['execution_time']:.4f} 秒")
        print(f"結果: {'PASS' if is_passed else 'FAIL'}")
        
        if is_passed:
            passed_tests += 1
    
    print("\n--- 測試總結 ---")
    print(f"總測試數: {total_tests}")
    print(f"通過: {passed_tests}")
    print(f"失敗: {total_tests - passed_tests}")
    print("-" * 50)

# --- 5. 程式主入口 ---
async def main_entry(text_to_translate: str = None, run_validation: bool = False):
    """
    程式主入口。可選擇執行單一翻譯流程或測試驗證模式。
    
    Args:
        text_to_translate (str): 欲翻譯的文字。
        run_validation (bool): 如果為 True，則忽略 text_to_translate，執行測試劇本。
    """
    if run_validation:
        await run_validation_mode()
    else:
        if text_to_translate is None:
            print("請提供要翻譯的文字。")
            return

        print("--- 啟動正式翻譯模式 ---")
        result = await execute_translation_flow(text_to_translate)
        print("\n--- 翻譯結果 ---")
        print(f"原始文本: {result['original_text']}")
        print(f"偵測語言: {result['original_lang']}")
        print(f"翻譯結果: {result['translated_text']}")
        print(f"執行時間: {result['execution_time']:.4f} 秒")
        print("-" * 50)

def main_entry_sync(text: str) -> str:
    """
    提供一個同步的入口，用於從 Flask 這樣的同步框架中調用。
    它會啟動一個非同步迴圈來執行翻譯流程，並返回翻譯結果。
    """
    result = asyncio.run(execute_translation_flow(text))
    return result['translated_text']

if __name__ == "__main__":
    # 範例：執行正式翻譯流程
    text_for_translation = "這個程式非常棒，可以同時處理長文本和短文本的翻譯，而且速度很快！"
    # 這裡的程式碼被修改為呼叫同步入口，以確保在所有環境下都能運行
    translated_text = main_entry_sync(text_for_translation)
    print(f"正式流程範例翻譯結果: {translated_text}")

    # 範例：執行測試驗證模式
    # asyncio.run(main_entry(run_validation=True))