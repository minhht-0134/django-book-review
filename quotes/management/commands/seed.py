from django.core.management.base import BaseCommand
from books.models import *
from quotes.models import *
import random

# python manage.py seed --mode=<SINGLE MODEL>

CLEAR_DATA = 'clear'
SINGLE_MODEL = ['Category', 'Book', 'Quote']
MODELS = [Category, Book, Quote]


class Command(BaseCommand):
    help = "seed database for testing and development."
    
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('Seeding done!')


def clear_data(modeli=None):
    if modeli == 'Category':
        print(f"Delete {modeli} instances")
        Category.objects.all().delete()
    elif modeli == 'Book':
        print(f"Delete {modeli} instances")
        Book.objects.all().delete()
    elif modeli == 'Quote':
        print(f"Delete {modeli} instances")
        Quote.objects.all().delete()
    else:
        print(f"Delete all data instances")
        for i in MODELS:
            i.objects.all().delete()

def create_quotes():
    print("Creating quotes")
    datas = [
      {
        "model": "quotes",
        "pk": 1,
        "fields": {
          "content": "If you only read the books that everyone else is reading, you can only think what everyone else is thinking.",
          "author": "Haruki Murakami"
        }
      },
      {
        "model": "quotes",
        "pk": 2,
        "fields": {
          "content": "Books are a uniquely portable magic.",
          "author": "Stephen King"
        }
      },  {
        "model": "quotes",
        "pk": 3,
        "fields": {
          "content": "Reading is important. If you know how to read then the whole world opens up to you.",
          "author": "Barack Obama"
        }
      },  {
        "model": "quotes",
        "pk": 4,
        "fields": {
          "content": "In books lies the soul of the whole past time.",
          "author": "Thomas Carlyle"
        }
      },  {
        "model": "quotes",
        "pk": 5,
        "fields": {
          "content": "The instruction we find in books is like fire. We fetch it from our neighbours, kindle it at home, communicate it to others, and it becomes the property of all.",
          "author": "Voltaire"
        }
      },  {
        "model": "quotes",
        "pk": 6,
        "fields": {
          "content": "You don’t have to burn books to destroy a culture. Just get people to stop reading them.",
          "author": "Mahatma Gandhi"
        }
      },  {
        "model": "quotes",
        "pk": 7,
        "fields": {
          "content": "A room without books is like a body without a soul.",
          "author": "Marcus Tullius Cicero"
        }
      },  {
        "model": "quotes",
        "pk": 8,
        "fields": {
          "content": "I think of life as a good book. The further you get into it, the more it begins to make sense.",
          "author": "Harold Kushner"
        }
      },  {
        "model": "quotes",
        "pk": 9,
        "fields": {
          "content": "Books are mirrors: you only see in them what you already have inside you.",
          "author": "Carlos Ruiz Zafón"
        }
      },  {
        "model": "quotes",
        "pk": 10,
        "fields": {
          "content": "There is a great deal of difference between an eager man who wants to read a book and the tired man who wants a book to read.",
          "author": "Gilbert K. Chesterton"
        }
      }
    ]
    quotes = None
    for data in datas:
        quotes = Quote(
            content=data.get('fields').get('content'),
            author=data.get('fields').get('author'),
        )
        quotes.save()
    print("Quotes created!")
    return quotes


def create_categories():
    print('Creating categories...')
    data_categories = [
        'Y Học- Sức Khỏe',
        'Tâm Lý - Kỹ Năng Sống',
        'Kinh Tế - Quản Lý',
        'Marketing - Bán hàng',
        'Y Học - Sức Khỏe',
        'Học Ngoại Ngữ',
        'Khoa Học - Kỹ Thuật',
        'Thể Thao - Nghệ Thuật',
        'Trinh Thám - Hình Sự',
        'Văn Hóa - Tôn Giáo',
        'Tử Vi - Phong Thủy',
        'Lịch Sử - Chính Trị',
        'Văn Học Việt Nam',
        'Truyện Ngắn - Ngôn Tình',
        'Truyện Cười - Tiếu Lâm',
        'Tiểu Thuyết Phương Tây',
        'Truyện Ma - Truyện Kinh Dị',
        'Huyền bí - Giả Tưởng',
        'Hồi Ký - Tuỳ Bút',
        'Phiêu Lưu - Mạo Hiểm',
        'Truyên Teen - Tuổi Học Trò',
        'Cổ Tích - Thần Thoại',
        'Triết Học',
        'Kiếm Hiệp - Tiên Hiệp',
        'Tiểu Thuyết Trung Quốc',
        'Kiến Trúc - Xây Dựng',
        'Nông - Lâm - Ngư',
        'Công Nghệ Thông Tin',
        'Tài Liệu Học Tập',
        'Ẩm thực - Nấu ăn',
        'Thư Viện Pháp Luật',
        'Truyện Tranh'
    ]
    category = None
    for data in data_categories:
        category = Category(name=data)
        category.save()
    print('Categories created!')
    return category


def create_books():
    print('Creating books...')
    data_books = [
        {
            'title': "Các Kiểu Kiến Trúc Trên Thế Giới",
            'image_url': 'https://sachvui.com/cover/2018/cac-kieu-kien-truc-tren-the-gioi.jpg',
            'author': 'Nguyễn Tứ',
            'book_url': 'https://sachvui.com/sachvui-686868666888/ebooks/2018/pdf/Sachvui.Com-cac-kieu-kien-truc-tren-the-gioi-nguyen-tu.pdf',
            'pages': 123
        },
        {
            'title': 'Con Trai Kẻ Khủng Bố',
            'image_url': 'https://sachvui.com/cover/2019/con-trai-ke-khung-bo.jpg',
            'author': 'Zak Ebrahim',
            'book_url': 'https://sachvui.com/sachvui-686868666888/ebooks/2019/pdf/Sachvui.Com-con-trai-ke-khung-bo-zak-ebrahim.pdf',
            'pages': 76
        },
        {
            'title': 'Từ Tơ Lụa Đến Silicon',
            'image_url': 'https://sachvui.com/cover/2019/tu-to-lua-den-silicon.jpg',
            'author': 'Jeffrey E. Garten',
            'book_url': 'https://sachvui.com/sachvui-686868666888/ebooks/2019/pdf/Sachvui.Com-tu-to-lua-den-silicon-jeffrey-e-garten.pdf',
            'pages': 76
        },
        {
            'title': 'Thơ Ngụ Ngôn La Fontaine',
            'image_url': 'https://sachvui.com/cover/2018/tho-ngu-ngon-la-fontaine.jpg',
            'author': 'Jean de la Fontaine',
            'book_url': 'https://sachvui.com/sachvui-686868666888/ebooks/2018/pdf/Sachvui.Com-tho-ngu-ngon-la-fontaine-jean-de-la-fontaine.pdf',
            'pages': 76
        },
    
        {
            'title': 'Lịch Sử Giao Thương: Thương Mại Định Hình Thế Giới Như Thế Nào?',
            'image_url': 'https://sachvui.com/cover/2019/lich-su-giao-thuong-thuong-mai-dinh-hinh-the-gioi-nhu-the-nao.jpg',
            'author': 'William J. Bernstein',
            'book_url': 'https://sachvui.com/sachvui-686868666888/ebooks/2019/pdf/Sachvui.Com-lich-su-giao-thuong-thuong-mai-dinh-hinh-the-gioi-nhu-the-nao-william-j-bernstein.pdf',
            'pages': 76
        },
    
        {
            'title': 'Hành Trình Của Linh Hồn',
            'image_url': 'https://sachvui.com/cover/2019/hanh-trinh-cua-linh-hon.jpg',
            'author': 'Michael Duff Newton',
            'book_url': 'https://sachvui.com/download/pdf/7354',
            'pages': 76
        },
    
        {
            'title': 'Đức Phật Và Phật Pháp',
            'image_url': 'https://sachvui.com/cover/2018/duc-phat-va-phat-phap.jpg',
            'author': 'Maha Thera',
            'book_url': 'https://sachvui.com/download/pdf/6965',
            'pages': 76
        },
    
        {
            'title': 'Sinh Ra Để Chạy',
            'image_url': 'https://sachvui.com/cover/2019/sinh-ra-de-chay.jpg',
            'author': 'Christopher McDougall',
            'book_url': 'https://sachvui.com/download/pdf/7360',
            'pages': 76
        },
    
        {
            'title': 'Tự Học Tiếng Anh Hiệu Quả',
            'image_url': 'https://sachvui.com/cover/2019/tu-hoc-tieng-anh-hieu-qua.jpg',
            'author': 'Nguyễn Thị Hà Bắc',
            'book_url': 'https://sachvui.com/download/pdf/7333',
            'pages': 76
        },
    
        {
            'title': 'Lối Sống Tối Giản Của Người Nhật',
            'image_url': 'https://sachvui.com/cover/2018/loi-song-toi-gian-cua-nguoi-nhat.jpg',
            'author': 'Sasaki Fumio',
            'book_url': 'https://sachvui.com/download/pdf/6790',
            'pages': 76
        },
    
        {
            'title': 'Dám Bị Ghét',
            'image_url': 'https://sachvui.com/cover/2018/dam-bi-ghet.jpg',
            'author': 'Koga Fumitake - Kishimi Ichiro',
            'book_url': 'https://sachvui.com/download/pdf/6740',
            'pages': 76
        },
    
        {
            'title': 'Công Nghệ Blockchain',
            'image_url': 'https://sachvui.com/cover/2018/cong-nghe-blockchain.jpg',
            'author': 'Nhiều tác giả',
            'book_url': 'https://sachvui.com/download/pdf/6715',
            'pages': 76
        },
    ]
    book = None
    ids = []
    categories = Category.objects.all()
    for i in categories:
        ids.append(i)
    for data in data_books:
        book = Book(
            title=data.get('title'),
            author=data.get('author'),
            pages=data.get('pages'),
            image_url=data.get('image_url'),
            book_url=data.get('book_url'),
            category=random.choice(ids),
            # category=ids[0],
        )
        book.save()
    print('Books created!')
    return book


def create(model):
    if model == SINGLE_MODEL[0]:
        create_categories()
    elif model == SINGLE_MODEL[1]:
        create_books()
    elif model == SINGLE_MODEL[2]:
        create_quotes()


def run_seed(self, mode):
    if not mode:
        print('----clear and create all data without mode---')
        clear_data()
        create_quotes()
        create_categories()
        create_books()
    elif mode == CLEAR_DATA:
        clear_data()
    elif mode not in SINGLE_MODEL:
        print('ERROR: mode invalid!')
        return
    
    for fmode in SINGLE_MODEL:
        if mode == fmode:
            clear_data(fmode)
            create(fmode)
            break
    return
