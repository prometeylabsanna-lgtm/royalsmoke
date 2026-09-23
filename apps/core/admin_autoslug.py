from __future__ import annotations

SLUG_HELP = 'Заповнюється автоматично з назви. Можна залишити порожнім.'


class AutoSlugAdminMixin:
    """Slug не обовʼязковий у формі — генерується в model.save()."""

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'slug' and formfield is not None:
            formfield.required = False
            if not formfield.help_text:
                formfield.help_text = SLUG_HELP
        return formfield
