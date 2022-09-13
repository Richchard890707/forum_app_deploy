
from django.shortcuts import redirect, render, get_object_or_404
from matplotlib.style import context
from .models import Author, Category, Post, Comment,Reply
from .utils import update_views
from .forms import PostForm,CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #使用 Paginator 实现分页功能
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Congratuations for' + user + 'to success register, have fun!') # ignored
            return redirect('login')
    context = {'form':form}
    return render(request,'register.html',context)

def loginPage(request):
    context = {}
    return render(request,'login.html',context)

def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "last_post": last_post,
        "num_users":num_users,
        "num_categories":num_categories,
        "title": "OZONE forum app"
    }
    return render(request, "forums.html", context)

# def detail(request,slug):
#     post = get_object_or_404(Post, slug=slug) #What do you think about Django?
#     context = {"post":post}
#     update_views(request, post)
#     return render(request, 'detail.html',context)
def detail(request, slug): #以SLUG 當條件查詢
    post = get_object_or_404(Post,slug=slug)
    # print('aaaa,',request.POST)
    # if request.user.is_authenticated:
    author = Author.objects.get(user=request.user) #回傳請求者
    # if "comment-form" in request.POST: #如果comment-form發生上傳了
    if request.POST.get("comment-form"): #同上
        comment = request.POST.get("comment") #獲取剛上傳的新回覆
        print("comment:",comment) #comment: I agree.
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        print("new_comment:",new_comment)
        print('created:',created) #BOOL:True/False
        post.comments.add(new_comment.id)
    if "reply-form" in request.POST:
        reply = request.POST.get("reply")# words in textarea
        print('reply:',reply)
        commenr_id = request.POST.get('comment-id') #input's name
        print('commenr_id:',commenr_id)
        comment_obj = Comment.objects.get(id=commenr_id)#驗證 id 是否存在於數據庫中
        print('comment_obj:',comment_obj)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        print('new_reply:',new_reply)
        print('created:',created)
        comment_obj.replies.add(new_reply.id)
    context = {'post': post,"title": "OZONE: "+post.title,}
    update_views(request, post)
    return render(request, "detail.html", context)
# def detail(request, slug):
#     post = get_object_or_404(Post, slug=slug)
#     if request.user.is_authenticated:
#         author = Author.objects.get(user=request.user)

#     if "comment-form" in request.POST:
#         comment = request.POST.get("comment")
#         new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
#         post.comments.add(new_comment.id)

#     if "reply-form" in request.POST:
#         reply = request.POST.get("reply")
#         commenr_id = request.POST.get("comment-id")
#         comment_obj = Comment.objects.get(id=commenr_id)
#         new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
#         comment_obj.replies.add(new_reply.id)


#     context = {
#         "post":post,
#         "title": "OZONE: "+post.title,
#     }
#     update_views(request, post)

#     return render(request, "detail.html", context)
# HERE~~~~~~~~~~~~~~~~~~~~~~~~
def posts(request,slug):
    category = get_object_or_404(Category, slug=slug)
    print('category:',category)
    posts = Post.objects.filter(approved=True, categories=category)
    print('posts:',posts)
    # if Post.objects.exists(): #是否存在任何對象相關的搜索
    #     print('there is at least one object in post.')
    paginator = Paginator(posts,5) #實例化分頁對象 object_list, per_page
    page_number = request.GET.get("page",1) #獲取頁碼
    print('postssss:',page_number)
    page_obj = paginator.get_page(page_number)

    # try:
    #     posts = paginator.page(page_number) #獲取某頁對應的紀錄
    #     print('1try')
    # except PageNotAnInteger:
    #     posts = paginator.page(1)#If page is not an integer, deliver first page.
    #     print('1except')
    # except EmptyPage:#If page is out of range, Delivery last page of results
    #     posts = paginator.page(paginator.num_pages) #如果使用者請求的頁碼號超過了最大頁碼號，顯示最後一頁
    #     print('2except')
    context = { "posts":page_obj.object_list,"forum":category,'paginator':paginator,'page_number':page_number,"title":"OZONE:Posts"}
    # context = { "posts":posts,"forum":category,"title":"OZONE:Posts"}
    return render(request, 'posts.html',context)

@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({"form":form,"title":"OZONE: Create New Post"})
    return render(request, "create_post.html", context)

def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "OZONE: Latest 10 Posts"
    }
    return render(request, "latest-posts.html",context)

def search_result(request):
    # if request.method == "GET":
    post_name = request.GET.get("q")
    print("post_name:",post_name)
    posts = Post.objects.filter(Q(title__icontains=post_name))

        # objects.all().filter(title='python')
    print("status:",posts.count())
    query = posts.count()
    return render(request,"search.html",{'posts':posts,'query':query})

# def searchFunction(request):
#     search_context = {}
#     posts = Post.objects.all()
#     if "search" in request.GET:
#         query = request.GET.get("q")
#         #Filter starts here
#         search_box = request.GET.get("search-box")
#         if search_box == "Descriptions":
#             objects = posts.filter(content__icontains=query)
#         else:
#             objects = posts.filter(title__icontains=query)
#         #ends here
#         search_context = {
#             "objects":objects,
#             "query":query,
#         }
#     return search_context

