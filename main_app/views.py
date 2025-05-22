from django.contrib import messages as django_messages
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import UserManager
from .forms import PostForm, PhotoForm
from django.http import HttpResponse
from .forms import UserPhotoForm  # ensure this import is at the top

from .models import Post, Photo, Comment, Like, User, UserDescription, Message, UserPhoto
from .forms import CommentForm

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'garageguru57'

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', { 'posts': posts })

@login_required
def messages(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'messages.html', {'messages': received_messages})

@login_required
def profile(request, user_id):
    posts = Post.objects.filter(user=user_id)
    user_profile = User.objects.filter(id = user_id).values()[0]
    if UserDescription.objects.filter(user_id=user_id).exists():
        bio = UserDescription.objects.filter(user_id=user_id).values()[0]
    else:
        bio = {
            'description': 'No User Bio'
        }
    if UserPhoto.objects.filter(user_id=user_id).exists():
        profile_photo = UserPhoto.objects.filter(user_id=user_id).values()[0]
    else:
        profile_photo = []
    return render(request, 'profile.html', {'posts': posts, 'user_profile': user_profile, 'bio': bio, 'profile_photo': profile_photo})

@login_required
def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    return render(request, 'posts/detail.html', { 'post': post, 'comment_form': comment_form })

@login_required
def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # If you use Cloudinary
        from cloudinary.uploader import upload
        result = upload(photo_file)
        url = result['secure_url']
        Photo.objects.create(image=url, post_id=post_id)  # Adjust this if your model uses FileField/ImageField!
        print("FILES RECEIVED:", request.FILES)
    return redirect('detail', post_id=post_id)



@login_required
def delete_photo(request, post_id, photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.delete()
    return redirect('detail', post_id=post_id)

@login_required
def search_by_hashtag(request, hashtag):
    posts = Post.objects.filter(description__icontains=f'#{hashtag}')
    context = {
        'hashtag': hashtag,
        'posts': posts,
    }
    return render(request, 'search_results.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def posts_create(request):
    error_message = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if form.is_valid() and photo_form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            photo = photo_form.save(commit=False)
            photo.post = post
            photo.save()
            return redirect('detail', post_id=post.id)
        else:
            error_message = 'Invalid new post'
    else:
        form = PostForm()
        photo_form = PhotoForm()
    context = {'form': form, 'photo_form': photo_form, 'error_message': error_message}
    return render(request, 'posts/create.html', context)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['description']
    success_url = '/'

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        content = request.POST['content']
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            django_messages.error(
                request, f'User with username {recipient_username} does not exist.')
            return redirect('send_message')
        message = Message(sender=request.user, recipient=recipient, content=content)
        message.save()
        django_messages.success(request, 'Message sent successfully!')
        return redirect('messages')
    return render(request, 'send_message.html')

@login_required
def add_comment(request, post_id, user_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.user_id = user_id
        new_comment.save()
    return redirect('detail', post_id=post_id)

@login_required
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('detail', post_id=post_id)

@login_required
def add_like(request, post_id, user_id):
    like_list = []
    idx = 0
    for x in Like.objects.filter(post_id=post_id):
        like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
        idx += 1

    if user_id in like_list:
        Like.objects.filter(post_id=post_id, user_id=user_id).delete()
    else:
        new_like = Like()
        new_like.post_id = post_id
        new_like.user_id = user_id
        new_like.save()

    return redirect('home')

def add_like_detail(request, post_id, user_id):
    like_list = []
    idx = 0
    for x in Like.objects.filter(post_id=post_id):
        like_list.append(Like.objects.filter(post_id=post_id).values("user_id")[idx]['user_id'])
        idx += 1

    if user_id in like_list:
        Like.objects.filter(post_id=post_id, user_id=user_id).delete()
    else:
        new_like = Like()
        new_like.post_id = post_id
        new_like.user_id = user_id
        new_like.save()

    return redirect('detail', post_id=post_id)

def likes_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'likes/detail.html', { 'post': post })

def username_update(request, user_id):
    return render(request, 'main_app/username_form.html')

def username_updated(request, user_id):
    this_user = User.objects.get(id=user_id)
    this_user.username = request.POST['username']
    for user in User.objects.values():
        if user['username'] == request.POST['username']:
            return redirect('username_update', user_id=user_id)
    this_user.save()
    return redirect('profile', user_id=user_id)

def bio_update(request, user_id):
    return render(request, 'main_app/bio_form.html')

def bio_updated(request, user_id):
    if not UserDescription.objects.filter(user_id=user_id).exists():
        this_user = UserDescription(description=request.POST['description'], user_id=user_id)
        this_user.save()
        return redirect('profile', user_id=user_id)
    else:
        this_user = UserDescription.objects.get(user_id=user_id)
        this_user.description = request.POST['description']
        this_user.save()
        return redirect('profile', user_id=user_id)


@login_required
def user_photo_update(request, user_id):
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_photo, created = UserPhoto.objects.get_or_create(user_id=user_id)
            user_photo.image = form.cleaned_data['image']
            user_photo.save()
        else:
            print(form.errors)  # Log errors to the Heroku logs
            # Optionally return errors as HTTP response for debugging
            return HttpResponse(form.errors, status=400)
    return redirect('profile', user_id=user_id)

@login_required
def user_photo_update(request, user_id):
    if request.method == 'POST':
        form = UserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            user_photo, created = UserPhoto.objects.get_or_create(user_id=user_id)
            user_photo.image = form.cleaned_data['image']
            user_photo.save()
            return redirect('profile', user_id=user_id)
    else:
        form = UserPhotoForm()
    return render(request, 'main_app/user_photo_form.html', {'form': form})
