# Django Post API 文档

## 1. 项目简介

Django Post API 是一个基于 Django 框架的二次封装工具，旨在通过统一的 POST 请求方式实现常见的 CRUD 操作（增、删、改、查）。通过 `act` 参数指定操作类型，简化了 API 的设计和使用。默认支持以下操作：
- `get_page`：获取分页数据
- `get_all`：获取全部数据
- `get_detail`：获取详情数据
- `post`：新增数据
- `put`：修改数据
- `delete`：删除数据

## 2. 安装

通过以下命令安装 Django Post API：

```bash
pip install django_post_api
```

## 3. 使用方法

### 3.1 模型定义

在 `models.py` 中定义模型时，继承 `django_post_api.models.BaseModel` 以支持封装后的 API 功能。以下是一个示例：

```python
from django.db import models
from django_post_api.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=20)
    img = models.CharField(verbose_name="图片", max_length=20)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Grade(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=20)
    img = models.CharField(verbose_name="图片", max_length=20)
    tag = models.ForeignKey(Tag, verbose_name="标签", on_delete=models.DO_NOTHING, db_constraint=False)

    class Meta:
        verbose_name = "年级"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Teacher(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=20)
    grade = models.ManyToManyField(Grade, db_constraint=False, related_name="related_teacher_list")

    class Meta:
        verbose_name = "老师"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Student(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=20)
    age = models.IntegerField(verbose_name="年龄", null=True)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, db_constraint=False, related_name="related_student_list")

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Score(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="related_score_list")
    subject = models.CharField(verbose_name="科目", max_length=50)
    score = models.FloatField()

    class Meta:
        verbose_name = "分数"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Order(BaseModel):
    name = models.CharField(verbose_name="名称", max_length=200)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="related_order_detail_list")
    name = models.CharField(verbose_name="名称", max_length=200)

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name
        ordering = ("-id",)
```

### 3.2 视图定义

在 `views.py` 中定义视图类，继承 `django_post_api.views` 中的视图类，并配置相关参数。以下是一个示例：

```python
from django.db import models
from django.db.models import Q, Count, Case, When
from django_post_api.constants import QueryWayEnum
from django_post_api.fields import ModelField, ForeignKeyField, ManyToManyField, AnnotateField
from django_post_api.params import StrParam, DictParam, IntParam, ListParam
from django_post_api.returns import success_return
from django_post_api.views import APIGetAllView, APIGetPageView, APIGetDetailView, APIPostView, APIPutView, APIDeleteView

from index_app.models import Grade, Student, Tag, Teacher, Order, OrderDetail


class GradeView(APIGetAllView, APIGetPageView, APIGetDetailView, APIPostView, APIPutView):
    model = Grade

    page_field_list = [
        ModelField(model_field=Grade.name),
        ModelField(model_field=Grade.img),
        ForeignKeyField(model_field=Grade.tag, related_field_list=[
            ModelField(model_field=Tag.name),
        ]),
        ManyToManyField(model_field=Student.grade, reverse=True, related_field_list=[
            ModelField(model_field=Student.name),
            AnnotateField(name="pass_subject_count", label="及格科目数量",
                          annotate_func=lambda cls_self: Count(Case(
                              When(related_score_list__score__gte=60, then=1),  # 及格的科目计数
                              output_field=models.IntegerField()
                          )))
        ], limit_num=3),
        AnnotateField(
            name="teacher_count", label="教师数量",
            annotate_func=lambda cls_self: Count("related_teacher_list", distinct=True),
        ),
        AnnotateField(
            name="student_count", label="学生数量",
            annotate_func=lambda cls_self: Count("related_student_list", distinct=True),
        ),
    ]
    detail_field_list = [
        ForeignKeyField(model_field=Grade.tag, related_field_list=[
            ModelField(model_field=Tag.img),
        ]),
        ManyToManyField(model_field=Teacher.grade, reverse=True, related_field_list=[
            ModelField(model_field=Teacher.name),
        ]),
        ManyToManyField(model_field=Student.grade, reverse=True, related_field_list=[
            ModelField(model_field=Student.age),
        ]),
    ]

    page_query_params_list = [
        StrParam(model_field=Grade.name, query_fun=lambda param_self, v: Q(name=v) | Q(img=v)),
        StrParam(model_field=Grade.img,
                 query_fun=lambda param_self, v: {f"{param_self.name}__{QueryWayEnum.icontains.name}": v}),
        DictParam(model_field=Grade.tag, dict_key_list=[
            IntParam(name="id"),
            StrParam(model_field=Tag.name),
        ], is_foreign=True)
    ]

    post_params_list = [
        DictParam(model_field=Grade.tag, dict_key_list=[
            IntParam(name="id", not_allow_null=True),
        ], not_allow_null=True, is_foreign=True),
        StrParam(model_field=Grade.name),
        StrParam(model_field=Grade.img),
    ]
    put_params_list = post_params_list


class StudentView(APIGetPageView, APIGetAllView, APIPostView, APIPutView, APIGetDetailView, APIDeleteView):
    model = Student

    def test_api(self):
        return success_return()


class OrderView(APIGetPageView, APIPostView):
    model = Order
    page_field_list = [
        ModelField(model_field=Order.name),
        ManyToManyField(model_field=OrderDetail.order, reverse=True, related_field_list=[
            ModelField(model_field=OrderDetail.name),
        ])
    ]

    post_params_list = [
        StrParam(model_field=Order.name),
    ]
    post_related_many_to_many_params_list = [
        ListParam(
            model_field=OrderDetail.order, reverse=True,
            list_element=DictParam(dict_key_list=[
                StrParam(model_field=OrderDetail.name),
            ]), not_allow_null=True, min_length=1,
        ),
    ]
```

### 3.3 请求参数说明

#### 3.3.1 分页参数

- `offset`：分页偏移量，默认值为 0。
- `limit`：每页显示的数量，默认值为 10。

#### 3.3.2 查询参数

通过 `page_query_params_list` 配置查询参数，支持以下类型：
- `StrParam`：字符串类型参数。
- `IntParam`：整数类型参数。
- `DictParam`：字典类型参数，支持嵌套查询。
- `ListParam`：列表类型参数，支持多值查询。

#### 3.3.3 操作参数

通过 `act` 参数指定操作类型：
- `get_page`：获取分页数据。
- `get_all`：获取全部数据。
- `get_detail`：获取详情数据。
- `post`：新增数据。
- `put`：修改数据。
- `delete`：删除数据。

### 3.4 字段定义

#### 3.4.1 普通字段

使用 `ModelField` 定义普通字段，例如：

```python
ModelField(model_field=Grade.name)
```

#### 3.4.2 外键字段

使用 `ForeignKeyField` 定义外键字段，支持嵌套字段，例如：

```python
ForeignKeyField(model_field=Grade.tag, related_field_list=[
    ModelField(model_field=Tag.name),
])
```

#### 3.4.3 多对多字段

使用 `ManyToManyField` 定义多对多字段，支持反向查询，例如：

```python
ManyToManyField(model_field=Student.grade, reverse=True, related_field_list=[
    ModelField(model_field=Student.name),
])
```

#### 3.4.4 注解字段

使用 `AnnotateField` 定义注解字段，支持自定义聚合函数，例如：

```python
AnnotateField(
    name="teacher_count", label="教师数量",
    annotate_func=lambda cls_self: Count("related_teacher_list", distinct=True),
)
```

## 4. 示例请求

### 4.1 获取分页数据

请求方法：POST  
请求路径：`/grade/`  
请求参数：
```json
{
    "act": "get_page",
    "offset": 0,
    "limit": 10,
    "name": "测试年级",
    "tag": {
        "id": 1
    }
}
```

返回结果：
```json
{
    "code": 200,
    "message": "成功",
    "data": {
        "total": 100,
        "results": [
            {
                "id": 1,
                "name": "测试年级",
                "img": "test.jpg",
                "tag": {
                    "id": 1,
                    "name": "测试标签"
                },
                "teacher_count": 10,
                "student_count": 50
            }
        ]
    }
}
```

### 4.2 获取详情数据

请求方法：POST  
请求路径：`/grade/`  
请求参数：
```json
{
    "act": "get_detail",
    "id": 1
}
```

返回结果：
```json
{
    "code": 200,
    "message": "成功",
    "data": {
        "id": 1,
        "name": "测试年级",
        "img": "test.jpg",
        "tag": {
            "id": 1,
            "img": "tag.jpg"
        },
        "teachers": [
            {
                "id": 1,
                "name": "测试老师"
            }
        ],
        "students": [
            {
                "id": 1,
                "age": 18
            }
        ]
    }
}
```

### 4.3 新增数据

请求方法：POST  
请求路径：`/grade/`  
请求参数：
```json
{
    "act": "post",
    "name": "新年级",
    "img": "new.jpg",
    "tag": {
        "id": 1
    }
}
```

返回结果：
```json
{
    "code": 200,
    "message": "成功",
    "data": {
        "id": 101,
        "name": "新年级",
        "img": "new.jpg",
        "tag": {
            "id": 1
        }
    }
}
```

### 4.4 修改数据

请求方法：POST  
请求路径：`/grade/`  
请求参数：
```json
{
    "act": "put",
    "id": 101,
    "name": "修改后的年级",
    "img": "updated.jpg"
}
```

返回结果：
```json
{
    "code": 200,
    "message": "成功",
    "data": {
        "id": 101,
        "name": "修改后的年级",
        "img": "updated.jpg"
    }
}
```

### 4.5 删除数据

请求方法：POST  
请求路径：`/grade/`  
请求参数：
```json
{
    "act": "delete",
    "id": 101
}
```

返回结果：
```json
{
    "code": 200,
    "message": "成功",
    "data": null
}
```

## 5. 注意事项

1. **模型字段限制**：所有模型字段必须定义在 `models.py` 中，并继承 `BaseModel`。
2. **外键字段限制**：外键字段必须设置 `db_constraint=False`，以避免数据库级的约束限制。
3. **多对多字段限制**：多对多字段必须设置 `db_constraint=False`，并指定 `related_name`。
4. **查询参数限制**：查询参数必须通过 `page_query_params_list` 配置，支持多种查询方式。
5. **操作参数限制**：操作类型必须通过 `act` 参数指定，支持的操作类型包括 `get_page`、`get_all`、`get_detail`、`post`、`put`、`delete`。

## 6. 联系方式

如有问题或建议，请联系 [你的邮箱] 或提交 Issue 至 [项目地址]。

希望这份文档对你有所帮助！