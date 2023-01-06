# Create your tests here.
from django.test import TestCase
import pytest
from django.urls import reverse, resolve
from django.test import TestCase


def test_home():
    # Check if at root "/" we get the home page
    path = reverse('/')
    print(path)
    assert resolve(path).view_name == "home"


def test_navigate_translate():
    # A simple test to check the CI
    assert 1 + 1 == 2
