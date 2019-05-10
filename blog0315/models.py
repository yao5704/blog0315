from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from ckeditor.fields import RichTextField
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    nickname = models.CharField('昵称', max_length=16  ,blank=True)
    """昵称"""

    logo = models.CharField('个性签名', max_length=16,blank=True)
    """个性签名"""

    telephone = models.CharField('电话', max_length=50,blank=True)
    """电话"""

    mod_date = models.DateTimeField('Last modified', auto_now=True)
    """最后修改日期"""

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname,self.user.username)


class Category(models.Model):
    '''
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    '''
    name = models.CharField(max_length=100)

    def get_category_count(self):
        return self.article_set.all().count()

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''标签'''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    '''文章'''
    # 文章标题

    title = models.CharField(max_length=70)
    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #阅读数量计数！！！
    def read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    #用户名称
    def author_name(self):
        try:
            return self.author.profile.nickname
        except exceptions.ObjectDoesNotExist:
            return self.author.username

    def __str__(self):
        return self.title


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    article = models.OneToOneField(Article,on_delete=models.DO_NOTHING)


class Testfiled(models.Model):
    content = RichTextField(config_name ='comment_ckeditor')


class Testnum(models.Model):
    name = models.TextField(max_length=20)
    test_num = models.PositiveIntegerField(default=0)
    testnum = models.IntegerField(default=220)

    def __str__(self):
        return self.name

#python manage.py makemigrations
#python manage.py migrate