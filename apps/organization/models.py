from datetime import datetime

from django.db import models

class City(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    category_choice = (
        ('org','培训机构'),
        ('per','个人'),
        ('edu','高校'),
    )
    category = models.CharField(max_length=3, choices=category_choice, default='org', verbose_name='机构类型')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(max_length=200, upload_to='org/%Y/%m', verbose_name='机构logo')
    address = models.CharField(max_length=200, verbose_name='地址')
    city = models.ForeignKey(City, verbose_name='所在城市')
    tag = models.CharField(default='全国知名', max_length=20, verbose_name='机构标签')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    courses = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def get_teacher_num(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=20, verbose_name='教师名')
    age = models.IntegerField(default=23, verbose_name='年龄')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=100, verbose_name='就职公司')
    work_position = models.CharField(max_length=20, verbose_name='公司职位')
    image = models.ImageField(max_length=100, upload_to='teacher/%Y/%m', verbose_name='头像', null=True, blank=True)
    points = models.CharField(max_length=100, verbose_name='教学特点')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
