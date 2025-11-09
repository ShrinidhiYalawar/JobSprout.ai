from django.contrib import admin
from .models import (
    Candidate,
    Resume,
    Job,
    JobMatch,
    CustomizedResume,
    Application,
    RecruiterContact,
    OutreachMessage,
    AutomationLog,
)

# Simple registrations (for quick admin view)
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "location", "is_active", "auto_apply_enabled", "created_at")
    search_fields = ("full_name", "email", "location")
    list_filter = ("is_active", "auto_apply_enabled", "location")
    ordering = ("-created_at",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "candidate", "status", "version", "is_primary", "created_at")
    list_filter = ("status", "is_primary", "domain")
    search_fields = ("title", "candidate__full_name", "domain")
    ordering = ("-created_at",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "source", "status", "is_active", "scraped_at")
    list_filter = ("source", "status", "is_active", "job_type")
    search_fields = ("title", "company", "location", "source_url")
    ordering = ("-scraped_at",)


@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ("job", "candidate", "match_score", "is_recommended", "apply_priority", "created_at")
    list_filter = ("is_recommended", "apply_priority")
    search_fields = ("job__title", "candidate__full_name")
    ordering = ("-match_score",)


@admin.register(CustomizedResume)
class CustomizedResumeAdmin(admin.ModelAdmin):
    list_display = ("job_match", "ats_score", "generation_time", "created_at")
    search_fields = ("job_match__job__title",)
    ordering = ("-ats_score",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job_match", "method", "status", "applied_at", "follow_up_count", "auto_follow_up")
    list_filter = ("method", "status", "auto_follow_up")
    search_fields = ("job_match__job__title", "notes")
    ordering = ("-created_at",)


@admin.register(RecruiterContact)
class RecruiterContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "contact_type", "job", "is_contacted", "confidence_score")
    list_filter = ("contact_type", "is_contacted", "is_verified", "found_via")
    search_fields = ("name", "email", "job__company")
    ordering = ("-confidence_score",)


@admin.register(OutreachMessage)
class OutreachMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "recruiter", "status", "sent_at", "opened_at", "replied_at")
    list_filter = ("status", "is_follow_up")
    search_fields = ("subject", "recruiter__email")
    ordering = ("-created_at",)


@admin.register(AutomationLog)
class AutomationLogAdmin(admin.ModelAdmin):
    list_display = ("log_type", "success", "timestamp", "execution_time")
    list_filter = ("log_type", "success")
    search_fields = ("message",)
    ordering = ("-timestamp",)
