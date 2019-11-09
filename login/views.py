import hashlib
import datetime

from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import User, ConfirmString
from . import forms


def hash_code(s, slat="mysite"):
    s += slat
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_mail(email, code):
    sub_object, from_mail, to_mail = "来自www.liujiang.com的注册确认邮件", "15950568268@sina.cn", "190381929@qq.com"
    text_context = "感谢注册www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！/" \
                   "如果你看到这个内容，表明你的邮箱不支持HTML连接功能，请联系管理员！"
    html_context = "<p>感谢注册<a href = 'http://{}/confirm/?code={}' target=blank>www.liujiangblog.com</a>，/" \
                   "这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>" \
                   "<p>请点击此链接完成注册却</p>" \
                   "<p>此链接有效期为{}天</p>".format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(sub_object, text_context, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_context, "text/html")
    msg.send()


def index(request):
    if not request.session.get("is_login", None):
        return redirect("/login/")
    return render(request, "login/index.html")


def login(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查输入的格式"
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            try:
                user = User.objects.get(name=username)
            except:
                message = "用户不存在"
                return render(request, "login/login.html", locals())

            if not user.has_confirmed:
                message = "该用户未经过邮件确认"
                return render(request, "login/login.html", locals())

            if user.password == hash_code(password):
                request.session["is_login"] = True
                request.session["user_id"] = user.id
                request.session["user_name"] = user.name
                return redirect("/index/")
            else:
                message = "密码错误"
                return render(request, "login/login.html", locals())
        else:
            return render(request, "login/login.html", locals())
    login_form = forms.UserForm()
    return render(request, "login/login.html", locals())


def logout(request):
    if not request.session.get("is_login", None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def register(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "POST":
        register_forms = forms.RegisterForm(request.POST)
        message = "请检查输入的格式"
        if register_forms.is_valid():
            username = register_forms.cleaned_data.get("username")
            password1 = register_forms.cleaned_data.get("password1")
            password2 = register_forms.cleaned_data.get("password2")
            email = register_forms.cleaned_data.get("email")
            sex = register_forms.cleaned_data.get("sex")

            if password1 != password2:
                message = "两次输入的密码不同"
                return render(request, "login/register.html", locals())
            else:
                if User.objects.filter(name=username).exists():
                    message = "用户名已存在"
                    return render(request, "login/register.html", locals())
                if User.objects.filter(email=email).exists():
                    message = "邮箱已注册"
                    return redirect("/register/")

                new_user = User.objects.create(name=username, password=hash_code(password1), email=email, sex=sex)

                code = make_confirm_string(new_user)
                send_mail(email, code)

                return redirect("/login/")
        else:
            return render(request, "login/register.html", locals())
    register_form = forms.RegisterForm()
    return render(request, "login/register.html", locals())


def user_confirm(request):
    code = request.GET.get("code", None)
    message = ""

    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求"
        return render(request, "login/confirm.html", locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > datetime.timedelta(settings.CONFIRM_DAYS) + c_time:
        confirm.user.delete()
        message = "注册邮件已经超过期限，请重新注册"
        return render(request, "login/confirm.html", locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢注册，请登录"
        return render(request, "login/confirm.html", locals())
