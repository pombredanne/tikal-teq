import uuid
from django.contrib.sites.models import get_current_site, Site
from django.core.mail import send_mail
import models as core_models

FROM_EMAIL                  = 'no-reply@tikalk.com'
BASE_CANDIDATE_TEQ_URL      = '/teq/teq_form/%s/'
CANDIDATE_MAIL_SUBJECT      = '%s - Tikal would like to learn more about you'
CANDIDATE_MAIL_MESSAGE      = '%s, we would like to learn some more about your experience in order to find your next job, please follow the link below ' \
                         'and answer a few questions regarding your experience with different technologies. \n %s'


def make_uuid():
    return str(uuid.uuid1().int>>64)

def send_candidate_mail(candidate):
    email = candidate.email
    name = candidate.first_name
    subject = CANDIDATE_MAIL_SUBJECT % name
    url = 'http://'+Site.objects.get_current().domain + BASE_CANDIDATE_TEQ_URL  % candidate.uuid
    message = CANDIDATE_MAIL_MESSAGE % (name,url)

    send_mail(subject,message,FROM_EMAIL,[email],True)


#set up
def set_up():
    create_entries('Java','Java Language',['Developing Java Classes','Using threads'])
    create_entries('Java','Database',['SQL','Designing Database Schema','Creating ERD','Writing SQL Statements','Implementing Data Access Classes','Optimization and Tuning'])
    create_entries('Java', 'BigData',['NoSQL Database (MongoDB, CouchDB, Cassandra, Redis, BigTable, HBase)','MapReduce (Hadoop, Hive)','Servers (EC2, GAE)','Processing (Solr/Lucene ElasticSearch)'])
    create_entries('Java', 'Spring & Hibernate',['Spring','Hibernate'])
    create_entries('Java', 'EJB / EJB', ['EJB / EJB 3','JPA','JDBC'])
    create_entries('Java', 'Clientside - Java Web Framewroks', ['JSP & TagLib' ,'MyFaces' ,'RichFaces', 'Struts / Struts2', 'GWT', 'Wicket', 'Grails'])
    create_entries('Java', 'Rich Client' ,['Eclipse/RCP' 'Swing'])
    create_entries('Java', 'Flex' ,['Flex Data Driven-data visualization components (Grids, lists) forms, charts, data collections','Flex Media Driven-media servers', 'video,sound, gaming', 'Action Script' ,'Flash'])
    create_entries('Java', 'Javascript/Ajax' ,['Ajax', 'HTML&JavaScript' ,'Dojo', 'ExtJS', 'Prototype', 'jQuery'])
    create_entries('Java', 'MySQL' ,['MySQL' ,'Clustering', 'Performance', 'Tuning'])
    create_entries('Java', 'JBoss&Tomcat', ['JBoss' ,'Tomcat', 'Clustering','Performance', 'Tuning'])
    create_entries('Java', 'CM',['Bugzilla','Subversion','Git', 'Luntbuild', 'Hudson'])
    create_entries('Java', 'Ant&Maven',['ANT', 'Maven2','Make', 'Shell Script'])



def create_entries(domain_name,block_name,list):
    #entries = []
    block = core_models.Block.objects.get_or_create(name=block_name)[0]
    domain = core_models.Domain.objects.get_or_create(name=domain_name)[0]
    for name in list:
        e = core_models.Entry.objects.get_or_create(name=name)[0]
        block.entries.add(e)

    block.save()
    domain.blocks.add(block)

