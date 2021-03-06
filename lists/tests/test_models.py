from xml.dom import ValidationErr
from django.forms import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelsTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')
    
    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationErr):
            item.save()
            item.full_clean()


class ListModelsTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
    
    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='qwerty')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='qwerty')
            item.full_clean()
    
    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='qwerty')
        item = Item(list=list2, text='qwerty')
        item.full_clean()  # should not raise

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='L1')
        item2 = Item.objects.create(list=list1, text='L2')
        item3 = Item.objects.create(list=list1, text='L3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )
    
    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
