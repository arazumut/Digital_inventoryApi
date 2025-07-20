from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from categories.models import Category


class Item(models.Model):
    """Demirbaş/Envanter modeli."""
    
    STATUS_CHOICES = (
        ('available', _('Müsait')),
        ('assigned', _('Atanmış')),
        ('broken', _('Arızalı')),
        ('maintenance', _('Bakımda')),
        ('retired', _('Emekli')),
    )
    
    name = models.CharField(_('demirbaş adı'), max_length=255)
    serial_number = models.CharField(_('seri numarası'), max_length=100, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name=_('kategori')
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='assigned_items',
        verbose_name=_('atanan kullanıcı')
    )
    status = models.CharField(
        _('durum'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available'
    )
    purchase_date = models.DateField(_('satın alma tarihi'), null=True, blank=True)
    warranty_until = models.DateField(_('garanti bitiş tarihi'), null=True, blank=True)
    notes = models.TextField(_('notlar'), blank=True)
    created_at = models.DateTimeField(_('oluşturulma tarihi'), auto_now_add=True)
    updated_at = models.DateTimeField(_('güncellenme tarihi'), auto_now=True)

    class Meta:
        verbose_name = _('demirbaş')
        verbose_name_plural = _('demirbaşlar')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
