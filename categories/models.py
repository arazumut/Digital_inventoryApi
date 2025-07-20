from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Kategori modeli."""
    name = models.CharField(_('kategori adı'), max_length=100)
    description = models.TextField(_('açıklama'), blank=True)
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('kategori')
        verbose_name_plural = _('kategoriler')
        ordering = ['name']

    def __str__(self):
        return self.name
