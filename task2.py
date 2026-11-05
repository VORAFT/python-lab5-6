import csv

input_file = "gdp_per_capita_2019.csv"
output_file = "search_results.csv"

# 1. Читання початкового CSV-файлу з обробкою помилок
try:
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
except FileNotFoundError:
    print(f"Помилка: Файл '{input_file}' не знайдено! Переконайся, що він у цій же папці.")
    exit()
except IOError as e:
    print(f"Помилка відкриття файлу: {e}")
    exit()

# 2. Введення назв країн користувачем з перевіркою
user_input = input("Введіть назви країн для пошуку через кому (наприклад: Ukraine, Poland, Germany): ").strip()
while not user_input:
    user_input = input("Помилка! Введіть хоча б одну назву країни: ").strip()

# Перетворюємо введені назви в нижній регістр для зручного порівняння
search_countries = [country.strip().lower() for country in user_input.split(",")]

# 3. Пошук відповідних рядків у даних
found_rows = []
for row in data:
    country_name = row.get("Country", "").strip().lower()
    # Якщо якась із введених країн входить у назву країни з файлу
    if any(target in country_name for target in search_countries):
        found_rows.append(row)

# 4. Збереження знайдених результатів у новий CSV-файл
if found_rows:
    try:
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Country", "Year", "GDP per capita (current US$)"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(found_rows)
            
        print(f"\nЗнайдено записів: {len(found_rows)}")
        print(f"Результати збережено у файл '{output_file}'.\n")
        
        # Виведення результату у консоль для скріншота звіту
        print("Знайдені дані:")
        for row in found_rows:
            print(f"{row['Country']} ({row['Year']}): ${row['GDP per capita (current US$)']}")
            
    except IOError as e:
        print(f"Помилка при збереженні файлу: {e}")
else:
    print("\nЗа вашим запитом нічого не знайдено.")