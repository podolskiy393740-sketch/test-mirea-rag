# ============================================
# ПРОТОТИП ПОМОЩНИКА ПЕРВОКУРСНИКА
# Гибридный поиск (FTS + Векторный) через RRF
# ============================================

# ---------- ШАГ 1. НАША БАЗА ЗНАНИЙ (FAQ) ----------
# Здесь хранятся вопросы и ответы с сайта университета
# Добавь свои вопросы!

faq_database = [
    {
        "id": 1,
        "question": "Где находится главный корпус?",
        "answer": "Главный корпус находится по адресу ул. Ленина, д. 1.",
        "source": "university.ru/contacts"
    },
    {
        "id": 2,
        "question": "Как получить стипендию?",
        "answer": "Для получения стипендии необходимо сдать сессию на 'отлично' и подать заявление в деканате.",
        "source": "university.ru/scholarship"
    },
    {
        "id": 3,
        "question": "Когда начинаются пары?",
        "answer": "Пары начинаются в 8:30 утра, перерыв между парами 10 минут.",
        "source": "university.ru/schedule"
    },
    {
        "id": 4,
        "question": "Где находится деканат?",
        "answer": "Деканат находится на 3-м этаже главного корпуса, кабинет 305.",
        "source": "university.ru/dean"
    },
    {
        "id": 5,
        "question": "Как оформить академический отпуск?",
        "answer": "Для оформления академического отпуска нужно подать заявление в деканате и справку из медицинского учреждения (при необходимости).",
        "source": "university.ru/academic_leave"
    },
    {
        "id": 6,
        "question": "Где находится 7-й корпус?",
        "answer": "7-й корпус находится через дорогу от главного, переход по подземному переходу.",
        "source": "university.ru/campus"
    },
    {
        "id": 7,
        "question": "Когда сессия?",
        "answer": "Сессия обычно проходит в январе и июне. Точные даты смотри в расписании на сайте.",
        "source": "university.ru/schedule"
    },
    {
        "id": 8,
        "question": "Как получить студенческий билет?",
        "answer": "Студенческий билет выдают в деканате после зачисления. Нужно принести фото 3х4.",
        "source": "university.ru/student_card"
    },
    {
        "id": 9,
        "question": "Есть ли общежитие для иногородних?",
        "answer": "Да, общежитие предоставляется иногородним студентам. Нужно подать заявление в отдел по работе с общежитиями.",
        "source": "university.ru/dormitory"
    },
    {
        "id": 10,
        "question": "Во сколько работает библиотека?",
        "answer": "Библиотека работает с 9:00 до 18:00, перерыв с 13:00 до 14:00.",
        "source": "university.ru/library"
    },
    # ============================================
    # 🔥 ДОБАВЬ СВОИ ВОПРОСЫ НИЖЕ (минимум 30 штук)!
    # ============================================
    # {
    #     "id": 11,
    #     "question": "ТВОЙ ВОПРОС",
    #     "answer": "ТВОЙ ОТВЕТ",
    #     "source": "ССЫЛКА"
    # },
]


# ---------- ШАГ 2. ПОИСК ПО КЛЮЧЕВЫМ СЛОВАМ (FTS) ----------
def simple_search(query):
    """Ищет вопросы, в которых есть слова из запроса"""
    words = query.lower().split()
    results = []

    for record in faq_database:
        question_lower = record["question"].lower()
        matches = 0

        for word in words:
            if word in question_lower:
                matches += 1

        if matches > 0:
            results.append({
                "id": record["id"],
                "question": record["question"],
                "answer": record["answer"],
                "source": record.get("source", ""),
                "score": matches
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ---------- ШАГ 3. ВЕКТОРНЫЙ ПОИСК (ЭМУЛЯЦИЯ) ----------
# Настоящий векторный поиск использует нейросеть для поиска по смыслу.
# В прототипе мы используем синонимы, чтобы показать ту же идею.

def vector_search(query):
    """Эмуляция векторного поиска — ищет по смыслу через синонимы"""
    synonyms = {
        "корпус": ["здание", "учебный корпус", "факультет", "кафедра"],
        "стипендия": ["деньги", "выплата", "грант", "баллы"],
        "пары": ["занятия", "уроки", "лекции", "семинары"],
        "деканат": ["декан", "завкафедрой", "учебный отдел"],
        "сессия": ["экзамены", "зачеты", "экзамен"],
        "общежитие": ["общага", "студенческое общежитие", "комната"],
        "библиотека": ["читальный зал", "книги", "книгохранилище"],
        "студенческий": ["студбилет", "зачетка"],
        "стипендия": ["стипа", "стипуха"],
    }

    words = query.lower().split()
    results = []

    for record in faq_database:
        question = record["question"].lower()
        matches = 0
        found_words = []

        for word in words:
            # Точное совпадение
            if word in question:
                matches += 1
                found_words.append(word)
            # Синонимы
            if word in synonyms:
                for synonym in synonyms[word]:
                    if synonym in question:
                        matches += 0.5
                        found_words.append(synonym)
                        break

        if matches > 0:
            results.append({
                "id": record["id"],
                "question": record["question"],
                "answer": record["answer"],
                "source": record.get("source", ""),
                "score": matches
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


# ---------- ШАГ 4. RRF (ОБЪЕДИНЯЕМ РЕЗУЛЬТАТЫ) ----------
def rrf_hybrid_search(query):
    """Объединяет результаты двух поисков через RRF"""

    fts_results = simple_search(query)
    vector_results = vector_search(query)

    rrf_scores = {}

    def add_results(results_list):
        k = 60
        for rank, record in enumerate(results_list, 1):
            record_id = record["id"]
            if record_id not in rrf_scores:
                rrf_scores[record_id] = {
                    "id": record_id,
                    "question": record["question"],
                    "answer": record["answer"],
                    "source": record.get("source", ""),
                    "score": 0
                }
            rrf_scores[record_id]["score"] += 1 / (rank + k)

    add_results(fts_results)
    add_results(vector_results)

    final_results = sorted(
        rrf_scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return final_results


# ---------- ШАГ 5. ОБЩЕНИЕ С ПОЛЬЗОВАТЕЛЕМ ----------
def main():
    print("=" * 60)
    print("🎓 ПОМОЩНИК ПЕРВОКУРСНИКА (ПРОТОТИП)")
    print("Задайте вопрос о жизни в университете")
    print("Для выхода введите 'выход'")
    print("=" * 60)
    print(f"📚 В базе {len(faq_database)} вопросов-ответов")
    print("=" * 60)

    while True:
        query = input("\n🤔 Ваш вопрос: ").strip()

        if query.lower() in ["выход", "exit", "quit", "q"]:
            print("\nДо свидания! Удачи в учёбе! 🎓")
            break

        if not query:
            print("Пожалуйста, введите вопрос.")
            continue

        # Выполняем поиск
        results = rrf_hybrid_search(query)

        if not results:
            print("\n😕 Не нашёл ответ на ваш вопрос.")
            print("💡 Попробуйте переформулировать или использовать ключевые слова:")
            print("   Например: корпус, стипендия, сессия, общежитие, деканат")
            continue

        # Выводим результаты
        print(f"\n📚 Нашёл {len(results)} возможных ответов. ТОП-3:")
        print("-" * 50)

        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. {result['question']}")
            print(f"   ✅ {result['answer']}")
            if result.get('source'):
                print(f"   📎 Источник: {result['source']}")
            print(f"   📊 Рейтинг: {result['score']:.4f}")

        # Подсказка, если результат не очень точный
        if results and results[0]["score"] < 0.02:
            print("\n💡 Попробуйте уточнить вопрос. Используйте конкретные слова.")

        # Показываем, сколько всего нашлось
        if len(results) > 3:
            print(f"\n... и ещё {len(results) - 3} ответов (для просмотра измените код)")


# ---------- ЗАПУСКАЕМ ПРОГРАММУ ----------
if __name__ == "__main__":
    