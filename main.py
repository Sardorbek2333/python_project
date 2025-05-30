from product_db import ProductDB

# Ma'lumotlar bazasiga ulanish
db = ProductDB(db_name="your_db", user="your_user", password="your_password")

# Mahsulot qo‘shish
db.add_product("Apple", 1.50, 100)

# Barcha mahsulotlarni ko‘rish
print(db.get_all_products())

# Nomi bo‘yicha qidirish
print(db.search_by_name("app"))

# Narx oralig‘i bo‘yicha filtrlash
print(db.filter_by_price(1.0, 2.0))

# Ma'lumotlarni JSON formatida eksport qilish
db.export_to_json()

# Bazani yopish
db.close()
