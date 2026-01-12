import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AppUser, Post

# ------------------------------
# Users
# ------------------------------

# GET all users
def get_users(request):
    try:
        users = list(AppUser.objects.values('id', 'username', 'email', 'created_at'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# POST create a new user
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Check if username and email exist in request
            if 'username' not in data or 'email' not in data:
                return JsonResponse({'error': 'Username and email are required'}, status=400)

            user = AppUser.objects.create(username=data['username'], email=data['email'])
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# ------------------------------
# Posts
# ------------------------------

# GET all posts
def get_posts(request):
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# POST create a new post
@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Make sure author exists
            author = AppUser.objects.get(id=data['author'])
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except AppUser.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)