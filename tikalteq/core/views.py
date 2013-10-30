from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext

from core.models import CANDIDATE_TEQ_STATUS_PENDING
from models import Candidate, CandidateTeq, CandidateEntry, Entry, CANDIDATE_TEQ_STATUS_COMPLETED


def teq_form(request, uuid):
    candidate = Candidate.objects.get(uuid=uuid)

    if candidate is not None:
        candidate_teq = CandidateTeq.objects.get(candidate=candidate)
        if candidate_teq.status == CANDIDATE_TEQ_STATUS_COMPLETED:
            return HttpResponse('Your TEQ was already submitted')

        if request.method == 'GET':
            blocks = candidate.domain.blocks.all() #Block.objects.filter(domain=candidate.domain)#
            candidate_blocks = []

            for block in blocks:
                candidate_block = {'name':block.name, 'entries':[]}

                for entry in block.entries.all():
                    candidate_block['entries'].append(entry)

                candidate_blocks.append(candidate_block)

            template = loader.get_template('core/teq_form.html')
            context = RequestContext(request, {
                'candidate_blocks': candidate_blocks,
                'candidate': candidate
            })
            return HttpResponse(template.render(context))

        if request.method == 'POST':
            post_data = request.POST
            for key in post_data.keys():
                if key!='csrfmiddlewaretoken' and not key.endswith('_level'):

                    entry = Entry.objects.filter(name=key)[0]
                    if post_data[key] == None or post_data[key] == '' or not post_data[key].isdigit():
                        experience = 0
                    else:
                        experience = post_data[key]

                    CandidateEntry(entry=entry,yearsOfExperience=experience,candidate=candidate,level_of_knowledge=post_data[key+'_level'],teq=candidate_teq).save()
            candidate_teq.status = CANDIDATE_TEQ_STATUS_COMPLETED
            candidate_teq.save()
            return HttpResponse('Thank you')


def teq_report(request, uuid):
    candidate = Candidate.objects.get(uuid=uuid)

    if candidate is not None:
        candidate_teq = CandidateTeq.objects.get(candidate=candidate)
        if candidate_teq.status == CANDIDATE_TEQ_STATUS_PENDING:
            return HttpResponse('This user did not yet fill the TEQ from')
        else:
            blocks = candidate.domain.blocks.all() #Block.objects.filter(domain=candidate.domain)#
            candidate_blocks = []

            for block in blocks:
                candidate_block = {'name':block.name, 'entries':[]}

                for entry in block.entries.all():
                    candidate_entry = CandidateEntry.objects.get(entry=entry,candidate=candidate)
                    candidate_block['entries'].append({'name':entry.name,'years':candidate_entry,'level':candidate_entry.level_of_knowledge})

                candidate_blocks.append(candidate_block)

            template = loader.get_template('core/teq_report.html')
            context = RequestContext(request, {
                'candidate_blocks': candidate_blocks,
                'candidate': candidate
            })
            return HttpResponse(template.render(context))


def candidates(request):
    ret_candidates = []
    all_candidates = Candidate.objects.all()
    for can in all_candidates:
        candidate_teq = CandidateTeq.objects.get(candidate=can)
        if candidate_teq.status == CANDIDATE_TEQ_STATUS_COMPLETED:
            ret_teq = can.uuid
        else:
            ret_teq = 'UNAVAILABLE'
        ret_candidates.append({'first_name':can.first_name,'last_name':can.last_name,'teq':ret_teq})

    template = loader.get_template('core/candidates.html')
    context = RequestContext(request, {
        'candidates': ret_candidates
    })
    return HttpResponse(template.render(context))





