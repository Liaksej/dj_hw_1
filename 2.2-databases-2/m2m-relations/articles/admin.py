from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag


class ScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        is_mains = []
        for form in self.forms:
            is_main = form.cleaned_data.get('is_main')
            if is_main == 1:
                is_mains.append(is_main)
        if len(is_mains) > 1:
            raise ValidationError('Основным тегом может быть только один тег')
        elif len(is_mains) == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Tag.articles.through
    extra = 1
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ScopeInline,
    ]
    list_display = ['id', 'title']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
