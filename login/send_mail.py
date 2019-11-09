import os

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


if __name__ == "__main__":
    # send_mail(
    #     '来自www.liujiang.com的博客的邮件',
    #     '欢迎访问',
    #     '15950568268@sina.cn',
    #     ['190381929@qq.com'],
    # )
    sub_object, from_mail, to_mail = "来自www.liujiang.com的博客的邮件", "15950568268@sina.cn", "190381929@qq.com"
    text_context = "欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！"
    html_context = '<p>欢迎访问<a href = "http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，' \
                   '这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(sub_object, text_context, from_mail, [to_mail])
    msg.attach_alternative(html_context, "text/html")
    msg.send()

