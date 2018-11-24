from datetime import datetime

from django.db import models
from django.db.models import Sum

from apps.organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, unique=True, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree_choice = (
        ('low', '初级'),
        ('middle', '中级'),
        ('high', '高级'),
    )
    degree = models.CharField(max_length=6, choices=degree_choice, verbose_name='课程难度')
    learn_time = models.IntegerField(default=0, verbose_name='学习时长')
    student_num = models.IntegerField(default=0, verbose_name='学习人数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    image = models.ImageField(max_length=100, upload_to='image/%Y/%m', verbose_name='封面')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='后端开发', max_length=20, verbose_name='课程分类')
    you_need_know = models.TextField(default='', verbose_name='课程须知')
    teacher_tell_you = models.TextField(default='', verbose_name='老师告诉你')
    # tag = models.CharField(default='', max_length=20, verbose_name='课程标签')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_all_lessons(self):
        # 获取课程章节数
        return self.lesson_set.all()

    def get_all_students(self):
        # 获取所有学习该课程的学生
        return self.usercourse_set.all()[:5]

    def course_total_time(self):
        # 课程总时长
        lesson_obj = self.lesson_set.all()
        total_time = 0
        for lesson in lesson_obj:
            total_time += lesson.lesson_total_time()
        return total_time

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def lesson_total_time(self):
        # 章节总时长
        time_list = [int(item['video_time']) for item in self.video.values('video_time')]
        return sum(time_list)

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='video', verbose_name='章节')
    name = models.CharField(max_length=50, verbose_name='视频名')
    url = models.URLField(default='', verbose_name='课程链接')
    video_time = models.IntegerField(default=0, verbose_name='视频时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='附件名')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name='附件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '课程附件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
