from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post

User = get_user_model()


class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='AuthorPass123')
        self.post = Post.objects.create(
            title='Initial Post',
            body='This is the first post body.',
            author=self.user,
        )
        self.home_url = reverse('home')
        self.detail_url = reverse('post_detail', args=[self.post.id])
        self.create_url = reverse('post_new')
        self.edit_url = reverse('post_edit', args=[self.post.id])
        self.delete_url = reverse('post_delete', args=[self.post.id])

    def test_blog_list_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertTemplateUsed(response, 'home.html')

    def test_blog_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.body)
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_blog_create_view(self):
        response = self.client.post(
            self.create_url,
            {
                'title': 'Created Post',
                'body': 'This post was created in a test.',
                'author': self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Created Post').exists())

    def test_blog_update_view(self):
        response = self.client.post(
            self.edit_url,
            {
                'title': 'Updated Title',
                'body': 'Updated body text.',
                'author': self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_blog_delete_view(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
