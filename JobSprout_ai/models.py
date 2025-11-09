"""
JobPilot AI - Complete Database Models
Handles resumes, jobs, applications, and outreach tracking
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Candidate(models.Model):
    """Multi-user candidate profiles"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, default='Bengaluru')
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Preferences
    target_roles = models.JSONField(default=list)  # ["Software Engineer", "Backend Dev"]
    preferred_locations = models.JSONField(default=list)
    salary_expectation = models.IntegerField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    auto_apply_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Resume(models.Model):
    """Resume storage and version management"""
    RESUME_STATUS = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('draft', 'Draft'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200)
    
    # File storage
    original_file = models.FileField(upload_to='resumes/original/')
    firebase_url = models.URLField(blank=True)
    
    # Extracted data
    skills = models.JSONField(default=list)  # ["Python", "Django", "AI/ML"]
    experience_years = models.FloatField(default=0)
    education = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    
    # Metadata
    summary = models.TextField(blank=True)
    key_achievements = models.JSONField(default=list)
    domain = models.CharField(max_length=100, blank=True)  # "Backend Dev", "AI/ML"
    
    # Status
    status = models.CharField(max_length=20, choices=RESUME_STATUS, default='active')
    version = models.IntegerField(default=1)
    is_primary = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']
        unique_together = ['candidate', 'version']
    
    def __str__(self):
        return f"{self.candidate.full_name} - {self.title} (v{self.version})"


class Job(models.Model):
    """Job postings from various sources"""
    JOB_STATUS = [
        ('new', 'New'),
        ('matched', 'Matched'),
        ('applied', 'Applied'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Job Details
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=200)
    company_website = models.URLField(blank=True)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, default='Full-time')  # Full-time, Contract, etc.
    
    # Description
    description = models.TextField()
    requirements = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    # Extracted Info
    required_skills = models.JSONField(default=list)
    preferred_skills = models.JSONField(default=list)
    experience_required = models.CharField(max_length=50, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    
    # Source
    source = models.CharField(max_length=50)  # "LinkedIn", "Naukri", etc.
    source_url = models.URLField()
    posted_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=JOB_STATUS, default='new')
    is_active = models.BooleanField(default=True)
    
    # Tracking
    scraped_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scraped_at']
        indexes = [
            models.Index(fields=['company', 'title']),
            models.Index(fields=['status', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class JobMatch(models.Model):
    """AI-powered job-resume matching"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='matches')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='matches')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='job_matches')
    
    # Match Score
    match_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Analysis
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    strength_areas = models.JSONField(default=list)
    improvement_areas = models.JSONField(default=list)
    ai_recommendation = models.TextField(blank=True)
    
    # Decision
    is_recommended = models.BooleanField(default=False)
    apply_priority = models.IntegerField(default=0)  # 1=High, 2=Medium, 3=Low
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-match_score', '-created_at']
        unique_together = ['job', 'resume']
    
    def __str__(self):
        return f"{self.job.title} - {self.candidate.full_name} ({self.match_score}%)"


class CustomizedResume(models.Model):
    """ATS-optimized custom resumes per job"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_match = models.ForeignKey(JobMatch, on_delete=models.CASCADE, related_name='custom_resumes')
    original_resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    
    # Customized Content
    customized_summary = models.TextField()
    customized_skills = models.JSONField(default=list)
    customized_experience = models.JSONField(default=list)
    keywords_added = models.JSONField(default=list)
    
    # File
    file_path = models.FileField(upload_to='resumes/customized/')
    firebase_url = models.URLField(blank=True)
    
    # ATS Score
    ats_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    ats_analysis = models.JSONField(default=dict)
    
    # Metadata
    generation_time = models.FloatField(default=0)  # seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-ats_score', '-created_at']
    
    def __str__(self):
        return f"Custom Resume - {self.job_match.job.title} ({self.ats_score}%)"


class Application(models.Model):
    """Track all job applications"""
    APPLICATION_STATUS = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('offered', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    APPLICATION_METHOD = [
        ('auto_apply', 'Auto Apply'),
        ('email_recruiter', 'Email to Recruiter'),
        ('manual', 'Manual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_match = models.ForeignKey(JobMatch, on_delete=models.CASCADE, related_name='applications')
    customized_resume = models.ForeignKey(CustomizedResume, on_delete=models.SET_NULL, null=True)
    
    # Application Details
    method = models.CharField(max_length=20, choices=APPLICATION_METHOD)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    
    # Tracking
    applied_at = models.DateTimeField(null=True, blank=True)
    response_received_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Automation
    auto_follow_up = models.BooleanField(default=True)
    follow_up_count = models.IntegerField(default=0)
    last_follow_up = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.job_match.job.title} - {self.status}"


class RecruiterContact(models.Model):
    """Recruiter and hiring manager contacts"""
    CONTACT_TYPE = [
        ('recruiter', 'Recruiter'),
        ('hr', 'HR Manager'),
        ('hiring_manager', 'Hiring Manager'),
        ('team_lead', 'Team Lead'),
        ('cto', 'CTO'),
        ('founder', 'Founder'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='contacts')
    
    # Contact Info
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Type
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE)
    title = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    # Source
    found_via = models.CharField(max_length=50, default='Hunter.io')
    confidence_score = models.FloatField(default=0)
    
    # Tracking
    is_contacted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']
        unique_together = ['job', 'email']
    
    def __str__(self):
        return f"{self.name} ({self.contact_type}) - {self.job.company}"


class OutreachMessage(models.Model):
    """Track recruiter outreach emails"""
    MESSAGE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('replied', 'Replied'),
        ('bounced', 'Bounced'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='outreach_messages')
    recruiter = models.ForeignKey(RecruiterContact, on_delete=models.CASCADE, related_name='messages')
    
    # Message Content
    subject = models.CharField(max_length=300)
    body = models.TextField()
    attachments = models.JSONField(default=list)  # Resume URLs
    
    # Status
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS, default='draft')
    
    # Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    # Response
    response_text = models.TextField(blank=True)
    sentiment = models.CharField(max_length=20, blank=True)  # positive, neutral, negative
    
    # Follow-up
    is_follow_up = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Gmail
    gmail_message_id = models.CharField(max_length=200, blank=True)
    gmail_thread_id = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.recruiter.email} ({self.status})"


class AutomationLog(models.Model):
    """System automation logs"""
    LOG_TYPE = [
        ('job_scrape', 'Job Scraping'),
        ('resume_match', 'Resume Matching'),
        ('resume_customize', 'Resume Customization'),
        ('auto_apply', 'Auto Apply'),
        ('email_sent', 'Email Sent'),
        ('follow_up', 'Follow-up'),
        ('sync', 'Data Sync'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    log_type = models.CharField(max_length=30, choices=LOG_TYPE)
    
    # Details
    message = models.TextField()
    details = models.JSONField(default=dict)
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Execution
    execution_time = models.FloatField(default=0)  # seconds
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['log_type', 'timestamp']),
            models.Index(fields=['success', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.log_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"