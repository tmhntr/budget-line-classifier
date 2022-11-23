# test_label_classifier.py
#
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import ANY
from unittest.mock import mock_open


from description_labeler import DescriptionLabeler
from description_labeler import LabelClassifyFrame

class TestLabelClassifier(unittest.TestCase):
    def test_get_current_description(self):
        charge_description_list = ["a", "b", "c"]
        label_classifier = DescriptionLabeler(charge_description_list)
        self.assertEqual(label_classifier.get_current_description(), "a")

    def test_label(self):
        charge_description_list = ["a", "b", "c"]
        label_classifier = DescriptionLabeler(charge_description_list)
        label_classifier.label("label")
        self.assertEqual(label_classifier.get_labels(), ["label", "", ""])

    def test_get_categories(self):
        charge_description_list = ["a", "b", "c"]
        label_classifier = DescriptionLabeler(charge_description_list)
        self.assertEqual(label_classifier.get_categories(), [])

    def test_get_labels(self):
        charge_description_list = ["a", "b", "c"]
        label_classifier = DescriptionLabeler(charge_description_list)
        self.assertEqual(label_classifier.get_labels(), ["", "", ""])

    def test_get_labeled_descriptions(self):
        charge_description_list = ["a", "b", "c"]
        label_classifier = DescriptionLabeler(charge_description_list)
        self.assertEqual(label_classifier.get_labeled_descriptions(), [("", "a"), ("", "b"), ("", "c")])