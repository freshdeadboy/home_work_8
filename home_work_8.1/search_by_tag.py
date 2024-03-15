import re
from mongoengine import connect
from models import Author, Quote

connect('Сluster0', host='mongodb+srv://zajchuk2014:GFnbFetD2EaVWVJh@cluster0.lxirfac.mongodb.net/')

def search_quotes(command):
    if command.startswith('name:') or command.startswith('author:'):
        author_name = re.search(r'name:(\w+)', command) or re.search(r'author:(\w+)', command)
        if author_name:
            author_name = author_name.group(1)
            author = Author.objects(fullname__icontains=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                print_quotes(quotes)
            else:
                print("Автор не знайдений.")
        else:
            print("Невірний формат команди.")
    elif command.startswith('tag:') or command.startswith('tags:'):
        tag_names = re.findall(r'tag:\s*(\w+)', command) or re.findall(r'tags:\s*(\w+(?:\s*,\s*\w+)*)', command)
        valid_tags = [tag.strip() for tag in tag_names]
        quotes = Quote.objects(tags__all=valid_tags)
        print_quotes(quotes)
    elif command == 'exit':
        return False
    else:
        print("Невірний формат команди.")
    return True

def print_quotes(quotes):
    for quote in quotes:
        print(f"Author: {quote.author.fullname}")
        print(f"Quote: {quote.quote}")
        print("")

print("Для пошуку цитат введіть команду в форматі:")
print("name:<ім'я_автора> або author:<ім'я_автора> — знайти всі цитати автора з вказаним ім'ям;")
print("tag:<тег> — знайти всі цитати з вказаним тегом;")
print("tags:<тег1>,<тег2>,... — знайти всі цитати з вказаними тегами (без пробілів);")
print("exit — завершити пошук.")
print()

while True:
    user_input = input("Введіть команду: ")
    if not search_quotes(user_input):
        break