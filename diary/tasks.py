# coding: utf-8

import datetime
from django.utils.translation import ugettext as _
from celery.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail, EmailMessage
from diary.models import Post
from django.template.loader import get_template
from django.template import Context

@periodic_task(run_every = crontab(hour="*", minute="*", day_of_week="*"))
def process_mails():
	print('Sending mails…')

	mail_template = get_template('mails/post.txt')

	# Change to years = 1 in production
	searched_date = datetime.date.today() - datetime.timedelta(days = 0)

	posts = Post.objects.filter(date = searched_date, sent = False)

	print('Found {} mail(s) to send'.format(len(posts)))

	for post in posts:
		print('Sending mail for post #{} ({})'.format(post.id, post))

		mail = EmailMessage(
			_('Your shortdiary post from {0}').format(post.date),
			mail_template.render(Context({'post': post})),
			['shortdiary <team@shortdiary.me>'],
			[post.author.email])

		mail.attach(post.image.name, post.image.read(), post.image.content_type)
		mail.send()

		post.sent = True
		post.save()