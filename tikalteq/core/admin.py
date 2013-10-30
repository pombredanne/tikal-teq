from django.contrib import admin
import models as core


class CandidateAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'domain']

admin.site.register(core.Entry)
admin.site.register(core.Block)
admin.site.register(core.Domain)
admin.site.register(core.Candidate)
admin.site.register(core.CandidateEntry)
admin.site.register(core.CandidateTeq)

