import requests
import json
import csv

# Код показника GDP per capita для Світового банку
INDICATOR = "NY.GDP.PCAP.CD"
YEAR = "2019"
COUNTRY = "all"

JSON_FILENAME = "gdp_per_capita_2019.json"
CSV_FILENAME = "gdp_per_capita_2019.csv"

# Формування URL-адреси запиту
URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}?date={YEAR}&format=json&per_page=500"


# 1. Функція одержання даних через API
def fetch_data(url):
    try:
        response = requests.get(url)
        # Перевірка на успішний статус відповіді
        response.raise_for_status()
        data = response.json()
        
        # Перевірка наявності даних у відповіді
        if not data or len(data) < 2 or not data[1]:
            print("Помилка: від API отримано порожні дані.")
            return None
        
        print("Дані успішно отримано з API Світового банку.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"Помилка під час виконання HTTP-запиту: {e}")
        return None


# 2. Функція збереження даних у JSON файл
def save_to_json(data, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Дані успішно збережено у файл '{filename}'.")
    except IOError as e:
        print(f"Помилка при записі у JSON-файл: {e}")


# 3. Функція перетворення та збереження даних у CSV файл
def convert_to_csv(data, filename):
    try:
        csv_data = []
        # Проходимо по отриманому списку записів
        for item in data[1]:
            # Відбираємо тільки записи, де є числове значення GDP
            if item.get("value") is not None:
                csv_data.append([
                    item["country"]["value"],
                    item["date"],
                    item["value"]
                ])
        
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Заголовки стовпчиків
            writer.writerow(["Country", "Year", "GDP per capita (current US$)"])
            writer.writerows(csv_data)
            
        print(f"Дані успішно збережено у CSV-файл '{filename}'.")
        return csv_data

    except (IOError, KeyError, IndexError) as e:
        print(f"Помилка при формуванні чи записі CSV-файлу: {e}")
        return []


# 4. Функція виведення результатів на екран
def display_results(data, csv_data):
    print("ЗМІСТ JSON-ФАЙЛУ (перші 3 записів):")
    for item in data[1][:3]:
        print(json.dumps(item, ensure_ascii=False, indent=4))

    print("ЗМІСТ CSV-ФАЙЛУ (перші 3 записів):")
    print("Country, Year, GDP per capita (current US$)")
    for row in csv_data[:3]:
        print(f"{row[0]}, {row[1]}, {row[2]}")


# Головна функція для запуску програми
def main():
    print("Запуск програми...")
    data = fetch_data(URL)
    
    if data:
        save_to_json(data, JSON_FILENAME)
        csv_data = convert_to_csv(data, CSV_FILENAME)
        display_results(data, csv_data)


if __name__ == "__main__":
    main()