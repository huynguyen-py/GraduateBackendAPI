from django.contrib import admin
from .models import DiagnosisRecord


class DiagnosisRecordAdmin(admin.ModelAdmin):
    model = DiagnosisRecord
    list_display = ('author_mail', 'create_at','predict')
    list_filter = ('anatom_site_general_challenge', 'gender', 'create_at',)

    fieldsets = (
        (None, {'fields': ('author', 'image_record', 'gender'
        , 'anatom_site_general_challenge', 'age_approx','predict')}),
    )

    def author_mail(self, obj):
        return obj.author.email
    # To display only in list_display

    ordering = ['create_at', ]
    search_fields = ['author_mail']     # with direct foreign key no error but filtering not possible directly


admin.site.unregister(DiagnosisRecord)
admin.site.register(DiagnosisRecord, DiagnosisRecordAdmin)