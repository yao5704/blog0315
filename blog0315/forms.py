from django import forms
from .models import Article
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from .models import Category,Tag


class ArticleForm(forms.Form):
    title = forms.CharField(label='标题',error_messages={'required': '我想要个名字QAQ'})
    body = forms.CharField(label='正文',widget=CKEditorWidget(config_name='article_ckeditor'),
                           error_messages={'required': '要给窝喂食哟'})
    # tags = forms.CharField(label='标签',widget=forms.Select())
    #标签
    tags_model = Tag.objects.all()
    # 我定义一个空列表
    tags_list = []
    # 循环我我的model对象
    for i in tags_model:
        # 定一个接收id和name的列表
        test = []
        test.append(i.id)
        test.append(i.name)
        # 添加到空列表
        tags_list.append(test)
    tags = forms.MultipleChoiceField(label='标签', choices=tags_list, widget=forms.CheckboxSelectMultiple(),
                                     required=False)

    #分类
    category_model = Category.objects.all()
    # 我定义一个空列表
    category_list = []
    # 循环我我的model对象
    for i in category_model:
        # 定一个接收id和name的列表
        test = []
        test.append(i.id)
        test.append(i.name)
        # 添加到空列表
        category_list.append(test)
    category = forms.CharField(widget=forms.Select(choices=category_list, attrs={'class': 'form-control'}),
                               error_messages={'required': '给我整一个！'})
    # text = forms.CharField(widget=forms.Textarea)
    # def clean(self):
    #     # 判断用户是否登录
    #     if self.user.is_authenticated:
    #         self.cleaned_data['user'] = self.user
    #     else:
    #         raise forms.ValidationError('用户尚未登录')
    # class Meta:
    #     model = Article
    #     fields = ['title','body','tags','category']
    #     #labels = {'tags':''}