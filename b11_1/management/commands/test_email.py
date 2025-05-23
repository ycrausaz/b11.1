from django.core.management.base import BaseCommand
from b11_1.utils.email_utils import send_simple_email, send_template_email

class Command(BaseCommand):
    help = 'Test email functionality'

    def add_arguments(self, parser):
        parser.add_argument('--recipient', type=str, required=True, help='Recipient email address')

    def handle(self, *args, **options):
        recipient = options['recipient']
        
        self.stdout.write(self.style.WARNING('Sending test email...'))
        
        # Send a simple email
        result = send_simple_email(
            subject="Test Email from Django App",
            message="This is a test email sent from your Django application using Mailgun.",
            recipient_list=[recipient]
        )
        
        if result:
            self.stdout.write(self.style.SUCCESS(f'Simple test email sent to {recipient}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to send simple test email'))
        
        # Send a template email
        result = send_template_email(
            subject="Test Template Email",
            template_name="emails/welcome_email",
            context={
                'name': 'Test User',
                'app_name': 'Your Django App'
            },
            recipient_list=[recipient]
        )
        
        if result:
            self.stdout.write(self.style.SUCCESS(f'Template test email sent to {recipient}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to send template test email'))
