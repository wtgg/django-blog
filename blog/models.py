# -*- coding: utf-8 -*-
# author: itimor

import datetime

from django.conf import settings
from django.db import models
from uuslug import slugify
from blog.storage import PathAndRename

BlogTypes = (
    ('l', '星辰大海'),
    ('j', '碎碎念'),
    ('w', '旅行'),
)


class Article(models.Model):
    name = models.CharField(u'标题', max_length=150, unique=True)
    slug = models.SlugField(u'链接', default='#', null=True, blank=True)
    cover = models.ImageField(upload_to=PathAndRename("cover"), blank=True, verbose_name=u'封面')
    type = models.CharField(max_length=1, choices=BlogTypes, default='l', verbose_name=u'类型')
    content = models.TextField(u'内容', )
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间')
    published = models.BooleanField(u'发布', default=True)
    publish_time = models.DateTimeField(u'发布时间', null=True)
    views = models.PositiveIntegerField(u'浏览量', default=0)
    tags = models.ManyToManyField('Tag', related_name='tags', null=True, blank=True, verbose_name=u'标签')

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'
        ordering = ['-update_time']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        modified = kwargs.pop("modified", True)
        if modified:
            self.update_time = datetime.datetime.utcnow()

        if self.published:
            self.publish_time = datetime.datetime.utcnow()

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/post/%s' % self.slug

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(u'名称', max_length=50, db_index=True, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name = u'标签'
        verbose_name_plural = u'标签'

    def __str__(self):
        return self.name


class Friend(models.Model):
    """
    友情链接
    """
    name = models.CharField(u'名称', max_length=100, default='')
    link = models.URLField(u'链接', default='')
    position = models.SmallIntegerField(u'位置', default=1)
    active = models.BooleanField(u'激活', default=True)

    class Meta:
        ordering = ['-position']
        verbose_name = u'友情链接'
        verbose_name_plural = '友情链接'

    def __str__(self):
        return self.name


class Social(models.Model):
    """
    社交网站
    """
    name = models.CharField(u'名称', max_length=10, unique=True)
    url = models.CharField(u'地址', max_length=50, unique=True)
    ico = models.ImageField(upload_to=PathAndRename("ico"), blank=True, verbose_name=u'图标')
    position = models.SmallIntegerField(u'位置', default=1)

    class Meta:
        ordering = ['position']
        verbose_name = u'社交网站'
        verbose_name_plural = u'社交网站'

    def __str__(self):
        return self.name
