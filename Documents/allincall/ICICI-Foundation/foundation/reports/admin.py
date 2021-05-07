from django.contrib import admin
from .models import *



admin.site.register(Sourcing)
admin.site.register(SourcingReportStatus)

admin.site.register(FollowUpsReportStatus)

admin.site.register(FollowUps)


admin.site.register(EnrollmentReportStatus)
admin.site.register(Enrollments)


admin.site.register(Trainee)
admin.site.register(Batch)

admin.site.register(BatchFollowups)

admin.site.register(BatchFollowUpsRecord)

admin.site.register(UserBatchFollowups)

admin.site.register(Certificate)

admin.site.register(SessionImages)
admin.site.register(FinancialOrganization)
admin.site.register(CertificateTemplates)
admin.site.register(FinancialSession)

admin.site.register(ImpactBox)
admin.site.register(ImpactBoxUpload)

admin.site.register(Policies)
