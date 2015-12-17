#--------------------------------------------------------------------------------------
# Test Case 1 (Step 2)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from planner.models import Planner, Category, Event

user = User.objects.get(username = 'admin')
# Create two categories, the second of which has the same name of the first
categoryOne = Category.objects.create_category(user, "Category", "1", "0")
categoryId = categoryOne.id
# This second call will cause a validation error to be raised and the program will fail
Category.objects.create_category(user, "Category", "1", "0")
Category.objects.delete_category(user, categoryId)
#--------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------
# Test Case 1 (Step 3)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from planner.models import Planner, Category, Event

user = User.objects.get(username = 'admin')
# Create 10 categories
cat1 = Category.objects.create_category(user, "Category1", "1", "0")
cat2 = Category.objects.create_category(user, "Category2", "1", "0")
cat3 = Category.objects.create_category(user, "Category3", "1", "0")
cat4 = Category.objects.create_category(user, "Category4", "1", "0")
cat5 = Category.objects.create_category(user, "Category5", "1", "0")
cat6 = Category.objects.create_category(user, "Category6", "1", "0")
cat7 = Category.objects.create_category(user, "Category7", "1", "0")
cat8 = Category.objects.create_category(user, "Category8", "1", "0")
cat9 = Category.objects.create_category(user, "Category9", "1", "0")
cat10 = Category.objects.create_category(user, "Category10", "1", "0")

cat1 = cat1.id
cat2 = cat2.id
cat3 = cat3.id
cat4 = cat4.id
cat5 = cat5.id
cat6 = cat6.id
cat7 = cat7.id
cat8 = cat8.id
cat9 = cat9.id
cat10 = cat10.id
# The creation of an 11th category will cause a validation error to be raised and the program will fail
Category.objects.create_category(user, "Category11", "1", "0")

Category.objects.delete_category(user, cat1)
Category.objects.delete_category(user, cat2)
Category.objects.delete_category(user, cat3)
Category.objects.delete_category(user, cat4)
Category.objects.delete_category(user, cat5)
Category.objects.delete_category(user, cat6)
Category.objects.delete_category(user, cat7)
Category.objects.delete_category(user, cat8)
Category.objects.delete_category(user, cat9)
Category.objects.delete_category(user, cat10)
#--------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------
# Test Case 1 (Step 3)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from planner.models import Planner, Category, Event

user = User.objects.get(username = 'admin')
# Create 10 categories
Category.objects.create_category(user, "Category1", "1", "0")
# The category is persisted and we have access to all of its attributes 
# We will retreive the category by name then list its values
category = Category.objects.get_category_by_name(user, "Category1")
category.get_name()
category.get_color_forHTML()
category.get_order()
categoryId = category.id
Category.objects.delete_category(user, categoryId)
#--------------------------------------------------------------------------------------



