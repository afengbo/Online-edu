from datetime import datetime

from django.db import models

from apps.users.models import UserProfile
from apps.courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    telephone = models.CharField(max_length=11, verbose_name='手机号')
    course_name = models.CharField(max_length=50, verbose_name='咨询课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)" % (self.name, self.telephone)


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comments = models.TextField(verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)" % (self.user.username, self.course.name)


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据ID')
    fav_type_choice = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师'),
    )
    fav_type = models.IntegerField(default=0, choices=fav_type_choice, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接收用户')   # 默认为0时表示发给所有用户
    message = models.TextField(verbose_name='消息内容')
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '学习课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%s)" % (self.user.username, self.course.name)
