import json
import random
import os

def split_json_array(
    input_file: str,
    train_file: str,
    eval_file: str,
    train_ratio: float = 0.8,
    seed: int = 42
):
    """
    将一个包含 JSON 对象数组的文件，按 train_ratio 切分成 train_file 和 eval_file。
    """
    # 1. 读取整个 JSON 数组
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert isinstance(data, list), "输入文件必须是一个 JSON 数组"

    # 2. 随机打乱
    random.seed(seed)
    random.shuffle(data)

    # 3. 切分下标
    n_train = int(len(data) * train_ratio)

    # 4. 写入 train / eval
    os.makedirs(os.path.dirname(train_file) or '.', exist_ok=True)
    with open(train_file, 'w', encoding='utf-8') as ft:
        json.dump(data[:n_train], ft, ensure_ascii=False, indent=2)
    with open(eval_file, 'w', encoding='utf-8') as fe:
        json.dump(data[n_train:], fe, ensure_ascii=False, indent=2)

    print(f"总样本数: {len(data)}, train: {n_train}, eval: {len(data)-n_train}")

if __name__ == '__main__':
    # 示例：对 24_sft.json 做 75/25 切分
    split_json_array(
        input_file  = '24_sft.json',
        train_file  = '24_sft_train.json',
        eval_file   = '24_sft_eval.json',
        train_ratio = 0.9,
        seed        = 0
    )
