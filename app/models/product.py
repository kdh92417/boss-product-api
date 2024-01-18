from django.db import models


class SizeType(models.TextChoices):
    small = ("small",)
    large = ("large",)


class Product(models.Model):
    user = models.ForeignKey(
        to="app.User", verbose_name="사장님", on_delete=models.CASCADE
    )
    category = models.CharField("카테고리", max_length=100, db_index=True)
    barcode = models.CharField("제목", max_length=100, unique=True)
    price = models.PositiveIntegerField("가격")
    cost = models.PositiveIntegerField("원가")
    name = models.CharField("상품 이름", max_length=100, db_index=True)
    description = models.TextField("상품 설명")
    expiration_date = models.DateField("유통기한")

    size = models.CharField("사이즈", max_length=15, choices=SizeType.choices)

    created_at = models.DateTimeField("생성일시", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "상품"
