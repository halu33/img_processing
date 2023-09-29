import cv2
import os

def estimate_oyster_length(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)
    if image is None:  # 画像の読み込みに失敗した場合
        print(f"{image_path} の読み込みに失敗しました。")
        return None

    # グレースケール化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二値化 (大津の二値化を使用)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 輪郭抽出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_length = 0
    for contour in contours:
        # 輪郭を囲む矩形を取得
        x, y, w, h = cv2.boundingRect(contour)
        # 体長として矩形の長い方を取得
        length = max(w, h)
        if length > max_length:
            max_length = length

    return max_length

if __name__ == "__main__":
    # このpyファイルと同じ階層にあるimgフォルダを指定
    img_dir = "img"

    # imgフォルダ内の全ての画像を取得
    image_files = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    image_files.sort()  # ファイル名順にソート

    for image_file in image_files:
        image_path = os.path.join(img_dir, image_file)
        estimated_length = estimate_oyster_length(image_path)
        if estimated_length is not None:
            print(f"{image_file}:  {estimated_length} ピクセルです。")
