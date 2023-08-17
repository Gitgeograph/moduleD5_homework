from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Left


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.authorUser.username
    
    def update_rating(self):
        postRating = self.post_set.all().aggregate(pRating=Sum('rating'))
        postRat = 0
        postRat += postRating.get('pRating')

        commentRating = self.authorUser.comment_set.all().aggregate(cRating=Sum('rating'))
        comRat = 0
        comRat += commentRating.get('cRating')

        self.authorRating = postRat * 3
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique = True)

    def __str__(self) -> str:
        return self.categoryName


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    category_choises = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=category_choises, default= ARTICLE)
    creationData = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...' 
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
    


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()