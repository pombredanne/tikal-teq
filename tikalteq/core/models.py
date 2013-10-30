from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from util import make_uuid, send_candidate_mail
from django.db.models import signals


CANDIDATE_TEQ_STATUS_PENDING    = 0
CANDIDATE_TEQ_STATUS_COMPLETED  = 1

CANDIDATE_LEVEL_BASIC = 1
CANDIDATE_LEVEL_DEVELOPER = 2
CANDIDATE_LEVEL_BASIC = 1
##
# an entry in a knowledge block (MySQL, Writing Java Classes, Maven, Multithreading)
##
class Entry(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=300,default='')

    def __unicode__(self):
        return self.name

##
# A knwoldge block in Tikal (Java Language, Databases)
##
class Block(models.Model):
    name = models.CharField(max_length=50)
    entries = models.ManyToManyField(Entry)

    def __unicode__(self):
        return self.name

##
# A domain of knowledge in Tikal (ALM, Java, JavaScript)
##
class Domain(models.Model):
    name = models.CharField(max_length=50)
    blocks = models.ManyToManyField(Block)

    def __unicode__(self):
        return self.name

##
# A candidate in Tikal's system
##
class Candidate(AbstractBaseUser):
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    username = models.CharField(max_length=40, db_index=True)
    email = models.CharField(max_length=50)
    domain = models.ForeignKey(Domain)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username


def notify_new_candidate_email(sender, instance, created, **kwargs):
    if created:
        CandidateTeq(candidate=instance,domain=instance.domain).save()
        send_candidate_mail(instance)

signals.post_save.connect(notify_new_candidate_email, sender=Candidate)
##
# A Candidate TEQ results
##
class CandidateTeq(models.Model):
    candidate = models.ForeignKey(Candidate)
    domain = models.ForeignKey(Domain)
    status = models.IntegerField(default=CANDIDATE_TEQ_STATUS_PENDING)

    #@classmethod
    #def create(cls, id):
    #  candidate = Candidate.objects.get(uuid=id)
    #  return cls(candidate_id=id, domain=candidate.domain.id, status=CANDIDATE_TEQ_STATUS_PENDING)

    def __unicode__(self):
        return 'TEQ:'+self.candidate.first_name


##
# An entry in a candidate's TEQ
##
class CandidateEntry(models.Model):
    teq = models.ForeignKey(CandidateTeq)
    entry = models.ForeignKey(Entry)
    candidate = models.ForeignKey(Candidate)
    yearsOfExperience = models.IntegerField(default=0)
    level_of_knowledge = models.IntegerField(default=0)

    def __unicode__(self):
        return self.candidate.first_name+' '+self.candidate.last_name+':'+self.entry.name