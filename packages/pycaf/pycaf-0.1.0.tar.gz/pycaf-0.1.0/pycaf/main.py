import g4f
import re
import argparse
import sys
import os

def get_response_with_retries(prompt, model="gpt-4", max_attempts=3):
    attempts = max_attempts
    while attempts > 0:
        response = g4f.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        if "Status: 403" not in response:
            return response
        attempts -= 1
    raise RuntimeError("Failed to get valid response after multiple attempts due to Status 403.")

def extract_python_code(text):
    pattern = r"```python\s+(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    if matches:
        return "\n\n".join(match.strip() for match in matches)
    else:
        return None  # Код не найден

def main():
    parser = argparse.ArgumentParser(description="pycaf — Python Code Assistant Free")
    parser.add_argument("filename", type=str, help="Имя файла для записи/редактирования кода")
    parser.add_argument("--command", type=str, required=True, help="Запрос к GPT-4, описание программы или изменение")
    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        question = f"Напиши приложение на python: {args.command}"
    else:
        with open(args.filename, "r", encoding="utf-8") as f:
            existing_code = f.read().strip()
        question = (f"{existing_code}\n\n"
                    f"— внеси в этот код изменения по следующему запросу: {args.command}")

    print(f"INFO: Запрос принят. Ваш запрос: {args.command}.")

    try:
        response = get_response_with_retries(question)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print("INFO: Генерация кода окончена")

    code = extract_python_code(response)

    if code is None or code.strip() == "":
        print("INFO: Не удалось сгенерировать код по вашему запросу")
        sys.exit(0)

    with open(args.filename, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"INFO: Код записан в файл {args.filename}")

if __name__ == "__main__":
    main()
