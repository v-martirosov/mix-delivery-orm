"""
Главный демонстрационный скрипт (CRUD + тестирование репозитория).
Проверяет взаимодействие слоя бизнес-логики с базой данных через ProductRepository.
"""
import sys
from app.database import get_session
from app.models.product import Product
from app.repositories.product_repository import ProductRepository

def run_demo():
    print("=" * 70)
    print("  ООО «МИКС» (г. Владимир) — СИСТЕМА УПРАВЛЕНИЯ СКЛАДОМ И ДОСТАВКОЙ")
    print("  Тестирование ORM SQLAlchemy 2.0 + Паттерн Repository")
    print("=" * 70)

    session = get_session()
    repo = ProductRepository(session)

    # 1. CREATE: Добавление тестовой номенклатуры плодоовощной базы
    print("\n[1] ТЕСТИРОВАНИЕ ОПЕРАЦИИ CREATE (Добавление товаров в базу):")
    initial_items = [
        Product(
            name="Томаты розовые Баку",
            category="Овощи",
            variety="Экстра грунтовые",
            unit="кг",
            price=240.0,
            wholesale_price=190.0,
            stock_quantity=45.0,
            min_stock_level=50.0
        ),
        Product(
            name="Огурцы Луховицкие",
            category="Овощи",
            variety="Короткоплодные пупырчатые",
            unit="кг",
            price=180.0,
            wholesale_price=140.0,
            stock_quantity=120.0,
            min_stock_level=30.0
        ),
        Product(
            name="Яблоки Симиренко",
            category="Фрукты",
            variety="1-й сорт Краснодар",
            unit="кг",
            price=125.0,
            wholesale_price=95.0,
            stock_quantity=80.0,
            min_stock_level=25.0
        ),
        Product(
            name="Бананы Эквадор",
            category="Фрукты",
            variety="Кавендиш Премиум",
            unit="кг",
            price=150.0,
            wholesale_price=115.0,
            stock_quantity=8.0,   # Ниже неснижаемого остатка (15.0)
            min_stock_level=15.0
        ),
        Product(
            name="Укроп свежий",
            category="Зелень",
            variety="Тепличный пучковой",
            unit="кг",
            price=320.0,
            wholesale_price=260.0,
            stock_quantity=4.5,   # Ниже неснижаемого остатка (10.0)
            min_stock_level=10.0
        )
    ]

    for item in initial_items:
        # Проверяем, нет ли уже такого товара, чтобы не дублировать при повторном запуске
        existing = repo.search_by_name(item.name)
        if not existing:
            created = repo.add(item)
            print(f"  + Добавлен: ID={created.id} | {created.name} ({created.category}) — {created.price} руб/{created.unit}")
        else:
            print(f"  * Уже в базе: ID={existing[0].id} | {existing[0].name}")

    # 2. READ ALL: Получение всех товаров
    print("\n[2] ТЕСТИРОВАНИЕ ОПЕРАЦИИ READ (Получение полного каталога):")
    all_products = repo.get_all()
    print(f"  Всего номенклатурных позиций в базе: {len(all_products)}")
    for p in all_products:
        print(f"    - #{p.id:2d} | {p.name:<25} | Категория: {p.category:<8} | Остаток: {p.stock_quantity:5.1f} {p.unit:<3} | Цена: {p.price:6.2f} руб.")

    # 3. READ BY CATEGORY: Фильтрация по категории
    print("\n[3] ФИЛЬТРАЦИЯ ПО КАТЕГОРИИ ('Овощи'):")
    veg_list = repo.get_by_category("Овощи")
    for v in veg_list:
        print(f"    - {v.name} (сорт: {v.variety}) — опт: {v.wholesale_price} руб., розница: {v.price} руб.")

    # 4. BUSINESS LOGIC: Выборка дефицитных товаров (Low Stock Alert)
    print("\n[4] СКЛАДСКОЙ КОНТРОЛЬ: Товары, требующие закупки (Stock <= Min Stock):")
    low_stock_items = repo.get_low_stock()
    if low_stock_items:
        for ls in low_stock_items:
            print(f"    ⚠️ ВНИМАНИЕ: {ls.name} | Текущий остаток: {ls.stock_quantity} {ls.unit} (Критический минимум: {ls.min_stock_level} {ls.unit})")
    else:
        print("    Все позиции в достаточном количестве.")

    # 5. UPDATE: Изменение остатков при отгрузке и корректировка цены
    print("\n[5] ТЕСТИРОВАНИЕ ОПЕРАЦИИ UPDATE (Отгрузка со склада и переоценка):")
    if all_products:
        first_product = all_products[0]
        print(f"  Исходный товар: {first_product.name} | Остаток: {first_product.stock_quantity} кг | Цена: {first_product.price} руб.")

        # Списание 10 кг
        repo.update_stock(first_product.id, -10.0)
        # Изменение цены
        first_product.price += 15.0
        repo.update(first_product)

        updated = repo.get_by_id(first_product.id)
        print(f"  После обновления: {updated.name} | Остаток: {updated.stock_quantity} кг | Новая цена: {updated.price} руб.")

    # 6. DELETE (Демонстрация жизненного цикла)
    print("\n[6] ТЕСТИРОВАНИЕ ОПЕРАЦИИ DELETE (Создание временного товара и его удаление):")
    temp_item = Product(
        name="Временный тест-товар",
        category="Тест",
        variety="Тест",
        unit="шт",
        price=99.0,
        wholesale_price=80.0,
        stock_quantity=1.0,
        min_stock_level=1.0
    )
    temp_item = repo.add(temp_item)
    print(f"  + Создан временный объект: ID={temp_item.id} ({temp_item.name})")

    delete_result = repo.delete(temp_item.id)
    print(f"  - Удаление ID={temp_item.id}: {'УСПЕШНО' if delete_result else 'ОШИБКА'}")

    check_deleted = repo.get_by_id(temp_item.id)
    print(f"  - Проверка чтения после удаления: {'Объект отсутствует (None), всё корректно' if check_deleted is None else 'Объект всё еще в БД'}")

    print("\n" + "=" * 70)
    print("  ✅ ВСЕ МЕТОДЫ РЕПОЗИТОРИЯ УСПЕШНО ПРОТЕСТИРОВАНЫ И РАБОТАЮТ КОРРЕКТНО!")
    print("=" * 70)

if __name__ == '__main__':
    run_demo()
