from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch

from .forms import DonorIdForm, SelectForm, SubmitForm


class AddWindowsTest(TestCase):
    def test_add_windows(self):
        out = StringIO()
        call_command('add_windows', 'windows/static/windows/windows.tsv', stdout=out)
        self.assertIn('information on 75 windows', out.getvalue())


class TestWindowsForm(TestCase):
    def test_donor_id_good(self):
        form = DonorIdForm({
            'donor_id': "12d3a799-0ed3-498e-ad79-a5191d4e4caf"})
        self.assertTrue(form.is_valid())

    def test_donor_id_not_uuid(self):
        form = DonorIdForm({'donor_id': "bad"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'donor_id': ["'bad' is not a valid UUID."]})

    def test_donor_id_does_not_exist(self):
        form = DonorIdForm({'donor_id': "12d3a799-0ed3-498e-ad79-a5191d4e4cad"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'donor_id': ['Donor ID not found']})


class TestWindowViews(TestCase):
    fixtures = ['windows']

    def test_index_exists(self):
        response = self.client.get(reverse('windows:index'))
        self.assertEqual(response.status_code, 200)

    def test_donor_exists(self):
        response = self.client.get(
            reverse('windows:donor',
                    args=['12d3a799-0ed3-498e-ad79-a5191d4e4caf']))
        self.assertEqual(response.status_code, 200)

    def test_donor_does_not_exist(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('windows:donor', args=['meh']))

    def test_select_exists(self):
        response = self.client.get(
            reverse('windows:select',
                    args=['12d3a799-0ed3-498e-ad79-a5191d4e4caf']))
        self.assertEqual(response.status_code, 200)

    def test_confirm_exists(self):
        response = self.client.get(
            reverse('windows:confirm',
                    args=['12d3a799-0ed3-498e-ad79-a5191d4e4caf']))
        self.assertEqual(response.status_code, 200)

    def test_list_exists(self):
        response = self.client.get(reverse('windows:list'))
        self.assertEqual(response.status_code, 200)
