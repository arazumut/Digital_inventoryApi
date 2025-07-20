from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from items.models import Item


class Assignment(models.Model):
    """İşlem Geçmişi modeli."""
    
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='assignments',
        verbose_name=_('demirbaş')
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='assignments',
        verbose_name=_('atanan kullanıcı')
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='assigned_by',
        verbose_name=_('atayan kullanıcı')
    )
    assigned_at = models.DateTimeField(_('atanma tarihi'), auto_now_add=True)
    returned_at = models.DateTimeField(_('iade tarihi'), null=True, blank=True)
    condition_on_return = models.TextField(_('iade durumu'), blank=True)
    
    class Meta:
        verbose_name = _('atama')
        verbose_name_plural = _('atamalar')
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.item} - {self.assigned_to} ({self.assigned_at.strftime('%d.%m.%Y')})"
