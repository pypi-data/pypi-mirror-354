from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from garpix_utils.managers import AvailableManager
from polymorphic.managers import PolymorphicManager

from ...mixins import CloneMixin
from ...models import BasePage
from polymorphic.models import PolymorphicModel
from ...serializers import get_components_serializer


class PageComponent(models.Model):
    component = models.ForeignKey("BaseComponent", on_delete=models.CASCADE, verbose_name='Компонент')
    page = models.ForeignKey("BasePage", on_delete=models.CASCADE, verbose_name='Страница')
    view_order = models.IntegerField(default=1, verbose_name='Порядок отображения')

    def __str__(self):
        return ''

    class Meta:
        unique_together = (('component', 'page'),)
        ordering = ('view_order', )
        verbose_name = 'Компонент страницы | Page component'
        verbose_name_plural = 'Компоненты страницы | Pages components'


class BaseComponent(CloneMixin, PolymorphicModel):
    """
    Базовый компонент
    """
    title = models.CharField(max_length=255, verbose_name='Название')
    is_deleted = models.BooleanField(default=False, verbose_name='Запись удалена')
    is_active = models.BooleanField(default=True, verbose_name='Включено')
    html_id = models.CharField(
        max_length=255,
        verbose_name='HTML ID',
        blank=True,
        default='',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\-_]*$',
                message='Допустимы только латинские буквы, цифры, дефисы и знаки подчеркивания',
                code='invalid'
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    pages = models.ManyToManyField(BasePage, blank=True, related_name='components', through='PageComponent',
                                   verbose_name='Страницы для отображения')

    text_title = models.CharField(blank=True, default='', max_length=128, verbose_name='Заголовок')
    template = 'garpix_page/components/default.html'

    searchable_fields = ('title',)
    serializer = None
    objects = PolymorphicManager()
    active_objects = AvailableManager()

    class Meta:
        verbose_name = 'Компонент | Component'
        verbose_name_plural = 'Компоненты | Components'
        ordering = ('created_at', 'title',)

    def __str__(self):
        return self.title

    @property
    def get_html_id(self):
        return format_html(f'id="{self.html_id}"') if self.html_id else ''

    def get_context(self, request):
        context = {
            'object': self,
            "component_model": self.__class__.__name__,
            'admin_edit_url': self.get_admin_url_edit_object(),
            'html_id': self.get_html_id
        }
        return context

    def get_template(self):
        return self.template

    def model_name(self):
        real_instance = self.get_real_instance_class()
        if real_instance:
            return real_instance._meta.verbose_name  # noqa
        return '- нет -'

    model_name.short_description = 'Тип'

    @classmethod
    def is_for_component_view(cls):
        return True

    @property
    def admin_link_to_change(self):
        link = reverse("admin:garpix_page_basecomponent_change",
                       args=[self.id])
        return format_html('<a class="inlinechangelink" href="{0}">{1}</a>', link, self.title)

    def get_context_data(self, request):
        context = self.get_context(request)

        context.update({
            'template': self.get_template()
        })
        return context

    def get_api_context_data(self, request):
        context = self.get_context(request)
        for k, v in context.items():
            if hasattr(v, 'is_for_component_view'):
                model_serializer_class = get_components_serializer(v.__class__)
                context[k] = model_serializer_class(v, context={"request": request}).data
        return context

    def get_serializer(self):
        return None

    def get_admin_url_edit_object(self):
        url = reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])
        return url

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()
