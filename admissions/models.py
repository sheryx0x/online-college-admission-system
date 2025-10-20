from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

class College(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default="General")
    is_open = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def __str__(self):
        return self.name

class FAApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, default='submitted')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_selection = models.CharField(max_length=100, default='FG College')
    program_selection = models.CharField(max_length=100, choices=[('Arts', 'Arts'), ('Humanities', 'Humanities')])


    QUOTA_CHOICES = [
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
        ('sports', 'Sports'),
    ]


    EMPLOYMENT_STATUS_CHOICES = [
        ('serving_armed_forces', 'Serving Armed Forces'),
        ('serving_fgei_employee', 'Serving FGEI Employee'),
        ('retired_armed_forces', 'Retired Armed Forces'),
        ('civilian', 'Civilian'),
        ('defence_paid', 'Defence Paid'),
        ('ward_of_shuhada', 'Ward of Shuhada'),
        
    ]
    employment_status = models.CharField(max_length=30, choices=EMPLOYMENT_STATUS_CHOICES)
    cnic = models.CharField(max_length=15)
    domicile = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    ssc_registration_number = models.CharField(max_length=20)
    last_school_attended = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()
    roll_no = models.CharField(max_length=20)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField()
    
    div_grade = models.CharField(max_length=5)
    board = models.CharField(max_length=50)
    quota = models.CharField(max_length=20, choices=QUOTA_CHOICES, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)

    
    attested_photocopy_hssc = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_father_mother_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_candidate_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    provisional_character_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    original_migration_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    passport_photographs = models.ImageField(upload_to='documents/', blank=True, null=True)
    proof_employment_status_parents = models.ImageField(upload_to='documents/', blank=True, null=True)
    affidavit_district_court = models.ImageField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return self.cnic





class FSCApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, default='submitted')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_selection = models.CharField(max_length=100, default='FG College')
    program_selection = models.CharField(max_length=100, choices=[
        ('Political Science', 'Political Science'),
        ('Computer Science', 'Computer Science'),
        ('medical', 'Medical')
    ])

    QUOTA_CHOICES = [
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
        ('sports', 'Sports'),
    ]



    employment_status = models.CharField(max_length=30, choices=FAApplication.EMPLOYMENT_STATUS_CHOICES)
    cnic = models.CharField(max_length=15)
    domicile = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    ssc_registration_number = models.CharField(max_length=20)
    last_school_attended = models.CharField(max_length=100)
    year_of_passing_ssc = models.IntegerField()
    ssc_roll_no = models.CharField(max_length=20)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField()
    
    ssc_div_grade = models.CharField(max_length=5)
    ssc_board = models.CharField(max_length=50)
    quota = models.CharField(max_length=20, choices=QUOTA_CHOICES, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)

    
    attested_photocopy_hssc = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_father_mother_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_candidate_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    provisional_character_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    original_migration_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    passport_photographs = models.ImageField(upload_to='documents/', blank=True, null=True)
    proof_employment_status_parents = models.ImageField(upload_to='documents/', blank=True, null=True)
    affidavit_district_court = models.ImageField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return self.cnic





class BSApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, default='submitted')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    college_selection = models.CharField(max_length=100, default='FG College')
    program_selection = models.CharField(max_length=100, choices=[
        ('BBA Hons', 'BBA Hons'),
        ('Political Science', 'Political Science'),
        ('Computer Science', 'Computer Science'),
        ('English', 'English')
    ])
    
    
    QUOTA_CHOICES = [
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
        ('sports', 'Sports'),
    ]


    employment_status = models.CharField(max_length=30, choices=FAApplication.EMPLOYMENT_STATUS_CHOICES)
    cnic = models.CharField(max_length=15)
    domicile = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    certificate_degree_level = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField()
    roll_no = models.CharField(max_length=100)
    board = models.CharField(max_length=100)
    major_subject = models.CharField(max_length=100)
    
    father_cnic = models.CharField(max_length=15)
    relationship_to_student = models.CharField(max_length=50, blank=True, null=True)
    father_profession = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    emergency_number = models.CharField(max_length=15, blank=True, null=True)
    father_whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    quota = models.CharField(max_length=20, choices=QUOTA_CHOICES, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)

    
    attested_photocopy_hssc = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_father_mother_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    attested_photocopy_candidate_cnic = models.ImageField(upload_to='documents/', blank=True, null=True)
    provisional_character_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    original_migration_certificate = models.ImageField(upload_to='documents/', blank=True, null=True)
    passport_photographs = models.ImageField(upload_to='documents/', blank=True, null=True)
    proof_employment_status_parents = models.ImageField(upload_to='documents/', blank=True, null=True)
    affidavit_district_court = models.ImageField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  
    def __str__(self):
        return self.cnic

    
    

class MeritList(models.Model):
    PROGRAM_CHOICES = [
        ('FA', 'FA'),
        ('FSC', 'FSC'),
        ('BS', 'BS'),
    ]
    QUOTA_CHOICES = [
        ('open', 'Open Merit'),
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
        ('sports', 'Sports'),
    ]

    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    subject = models.CharField(max_length=100, default="General")
    available_seats = models.PositiveIntegerField(default=10)
    list_type = models.CharField(max_length=20, choices=[('open', 'Open Merit'), ('quota', 'Quota Based')],default='open')
    quota = models.CharField(
    max_length=20, 
    choices=[
        ('army_retired', 'Army Retired'),
        ('hafiz_e_quran', 'Hafiz-e-Quran'),
        ('disabled', 'Disabled'),
        ('sports', 'Sports')
    ],
    blank=True,
    null=True  
)
    percentage_cutoff = models.DecimalField(
    max_digits=5, 
    decimal_places=2, 
    default=0.0
)
    fa_applications = models.ManyToManyField(FAApplication, blank=True)
    fsc_applications = models.ManyToManyField(FSCApplication, blank=True)
    bs_applications = models.ManyToManyField(BSApplication, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.program} {self.get_list_type_display()} Merit List - {self.percentage_cutoff}%"
    
    
    
class AdmissionStatus(models.Model):
    is_open = models.BooleanField(default=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Open" if self.is_open else "Closed"
    
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
