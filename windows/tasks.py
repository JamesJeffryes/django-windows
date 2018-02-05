from background_task import background
from datetime import timedelta
from django.core.mail import send_mail, EmailMessage
from .models import Donor


def send_next_email():
    # cancel tasks

    next_donor = Donor.objects.filter(invited=False).order_by(
        '-donation_amount').first()
    if not next_donor:
        return
    msg = "Hello {} {}, \n Thank you for your generous donation to " \
          "rebuilding the windows" \
          " in the PIKE Iota Delta Chapter House at PIKE. As a thank you" \
          " for your donation, we invite you to add a dedication plaque " \
          "to one of the windows. To select a window, please follow this " \
          "link: localhost:8000/windows/{}. The windows " \
          "are selected on a first-come " \
          "first serve basis but you will have 24 hours from the receipt" \
          "of this email before we notify the next donor. Dont delay picking" \
          " out your window!\n In ppka,\n Iota Delta Alumni Association".format(
           next_donor.first_name, next_donor.last_name, next_donor.donor_id)
    html = "<p>Hello {} {},</p> <p>Thank you for your generous donation to " \
           "rebuilding the windows" \
           " in the PIKE Iota Delta Chapter House at PIKE. As a thank you" \
           " for your donation, we invite you to add a dedication plaque " \
           "to one of the windows. To select a window, please follow this " \
           "<a href='http://pike-windows.com/windows/{}'>link</a>. The windows " \
           "are selected on a first-come " \
           "first serve basis but you will have 24 hours from the receipt " \
           "of this email before we notify the next donor. Don't delay picking" \
           " out your window!</p> <p>In ppka,</p> <p>Iota Delta Alumni " \
           "Association</p>".format(
        next_donor.first_name, next_donor.last_name, next_donor.donor_id)
    send_mail('Select your window dedication at PIKE', msg,
              'alumnipresident@pi-kappa-alpha.net', [next_donor.email_address],
              html_message=html)
    next_donor.invited = True
    next_donor.save()


@background(schedule=timedelta(hours=24))
def delayed_email():
    send_next_email()

