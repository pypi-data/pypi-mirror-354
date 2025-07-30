"""
测试objects管理器的完整CRUD功能
演示所有新增、更新、查询、删除功能
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import asyncio
import logging
from asyncframe.models import Model
from asyncframe.fields import IntegerField, CharField, TextField, DateTimeField, BooleanField
from asyncframe.database import DatabaseConfig, db_manager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 定义测试模型
class User(Model):
    """用户模型"""
    __tablename__ = 'test_users'
    
    name = CharField(max_length=100, null=False)
    email = CharField(max_length=255, unique=True, null=False)
    age = IntegerField(null=True)
    is_active = BooleanField(default=True)
    bio = TextField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

async def test_objects_manager():
    """测试objects管理器的所有功能"""
    
    # 配置数据库
    database_config = DatabaseConfig(
        url="mysql://root:0716gzs.cn@localhost:3306/asyncframe_examples"
    )
    db_manager.add_database("default", database_config, is_default=True)
    
    try:
        # 连接数据库
        await db_manager.connect_all()
        print("✅ 数据库连接成功")
        
        # 创建表
        from asyncframe.models import create_tables
        await create_tables(User)
        print("✅ 数据表创建成功")
        
        # 清理旧数据
        await User.objects.filter().delete()
        print("✅ 清理旧数据完成")
        
        print("\n" + "="*60)
        print("🧪 测试 objects 管理器功能")
        print("="*60)
        
        # ==================== 测试新增数据 ====================
        print("\n📝 1. 测试新增数据功能")
        print("-" * 40)
        
        # 创建单个用户
        user1 = await User.objects.create(
            name="张三",
            email="zhangsan@example.com",
            age=25,
            bio="这是张三的简介"
        )
        print(f"✅ 创建单个用户: {user1.name} (ID: {user1.pk})")
        
        # 批量创建用户
        users_data = [
            {"name": "李四", "email": "lisi@example.com", "age": 30, "bio": "李四的简介"},
            {"name": "王五", "email": "wangwu@example.com", "age": 28, "bio": "王五的简介"},
            {"name": "赵六", "email": "zhaoliu@example.com", "age": 22, "bio": "赵六的简介"},
            {"name": "钱七", "email": "qianqi@example.com", "age": 35, "bio": "钱七的简介"}
        ]
        created_users = await User.objects.bulk_create(users_data)
        print(f"✅ 批量创建用户: {len(created_users)} 个")
        
        # get_or_create
        user_new, created = await User.objects.get_or_create(
            email="test@example.com",
            defaults={"name": "测试用户", "age": 20}
        )
        print(f"✅ get_or_create: {user_new.name} ({'新创建' if created else '已存在'})")
        
        # ==================== 测试查询数据 ====================
        print("\n🔍 2. 测试查询数据功能")
        print("-" * 40)
        
        # 查询所有用户
        all_users = await User.objects.all().all()
        print(f"✅ 查询所有用户: {len(all_users)} 个")
        
        # 根据条件查询单个用户
        user = await User.objects.get(email="zhangsan@example.com")
        print(f"✅ 查询单个用户: {user.name}")
        
        # 根据条件查询多个用户
        young_users = await User.objects.filter(age__lt=30).all()
        print(f"✅ 查询年龄小于30的用户: {len(young_users)} 个")
        
        # find_one (不存在时返回None)
        found_user = await User.objects.find_one(name="不存在的用户")
        print(f"✅ find_one 不存在的用户: {found_user}")
        
        # find_many 限制数量
        limited_users = await User.objects.find_many(limit=3, is_active=True)
        print(f"✅ find_many 限制3个活跃用户: {len(limited_users)} 个")
        
        # 搜索功能
        search_results = await User.objects.search("张", ["name", "bio"])
        print(f"✅ 搜索包含'张'的用户: {len(search_results)} 个")
        
        # 分页查询
        page_data = await User.objects.paginate(page=1, per_page=3)
        print(f"✅ 分页查询: 第{page_data['page']}页, 共{page_data['total_pages']}页, {len(page_data['items'])}条记录")
        
        # 统计功能
        count = await User.objects.count()
        print(f"✅ 用户总数: {count}")
        
        exists = await User.objects.filter(age__gt=100).exists()
        print(f"✅ 是否存在年龄大于100的用户: {exists}")
        
        # ==================== 测试更新数据 ====================
        print("\n📝 3. 测试更新数据功能")
        print("-" * 40)
        
        # 更新单个用户
        user1.age = 26
        await user1.save()
        print(f"✅ 更新单个用户年龄: {user1.name} -> {user1.age}")
        
        # 批量更新
        users_to_update = await User.objects.filter(age__lt=25).all()
        for user in users_to_update:
            user.is_active = False
        
        if users_to_update:
            updated_count = await User.objects.bulk_update(users_to_update, ['is_active'])
            print(f"✅ 批量更新用户状态: {updated_count} 个")
        
        # QuerySet 批量更新
        qs_updated = await User.objects.filter(age__gte=30).update(is_active=True)
        print(f"✅ QuerySet批量更新: {qs_updated} 个用户")
        
        # update_or_create
        updated_user, created = await User.objects.update_or_create(
            email="test@example.com",
            defaults={"name": "更新的测试用户", "age": 21}
        )
        print(f"✅ update_or_create: {updated_user.name} ({'新创建' if created else '已更新'})")
        
        # ==================== 测试聚合查询 ====================
        print("\n📊 4. 测试聚合查询功能")
        print("-" * 40)
        
        # 聚合统计
        stats = await User.objects.aggregate(
            avg_age='AVG(age)',
            max_age='MAX(age)',
            min_age='MIN(age)',
            total_count='COUNT(*)'
        )
        print(f"✅ 用户统计: 平均年龄={stats.get('avg_age', 0):.1f}, "
              f"最大年龄={stats.get('max_age', 0)}, "
              f"最小年龄={stats.get('min_age', 0)}, "
              f"总数={stats.get('total_count', 0)}")
        
        # 获取指定字段值
        user_names = await User.objects.values('name', 'email')
        print(f"✅ 获取用户名和邮箱: {len(user_names)} 条记录")
        for user_data in user_names[:3]:  # 只显示前3个
            print(f"   - {user_data['name']}: {user_data['email']}")
        
        # 获取值列表
        names_list = await User.objects.values_list('name', flat=True)
        print(f"✅ 获取用户名列表: {names_list}")
        
        # ==================== 测试删除数据 ====================
        print("\n🗑️  5. 测试删除数据功能")
        print("-" * 40)
        
        # 删除单个用户
        test_user = await User.objects.find_one(email="test@example.com")
        if test_user:
            await test_user.delete()
            print(f"✅ 删除单个用户: {test_user.name}")
        
        # 批量删除对象
        users_to_delete = await User.objects.filter(age__lt=25).all()
        if users_to_delete:
            deleted_count = await User.objects.bulk_delete(users_to_delete)
            print(f"✅ 批量删除用户: {deleted_count} 个")
        
        # QuerySet 批量删除
        qs_deleted = await User.objects.filter(is_active=False).delete()
        print(f"✅ QuerySet批量删除: {qs_deleted} 个用户")
        
        # ==================== 测试排序和条件查询 ====================
        print("\n🔄 6. 测试排序和条件查询")
        print("-" * 40)
        
        # 排序查询
        ordered_users = await User.objects.order_by('-age', 'name').all()
        print(f"✅ 按年龄降序、姓名升序: {len(ordered_users)} 个用户")
        for user in ordered_users:
            print(f"   - {user.name}: {user.age}岁")
        
        # 复杂条件查询
        complex_users = await User.objects.filter(
            age__gte=25,
            is_active=True
        ).exclude(
            name__icontains="测试"
        ).order_by('-created_at').limit(5).all()
        print(f"✅ 复杂条件查询: {len(complex_users)} 个用户")
        
        # 获取第一个和最后一个
        first_user = await User.objects.first()
        last_user = await User.objects.last()
        print(f"✅ 第一个用户: {first_user.name if first_user else 'None'}")
        print(f"✅ 最后一个用户: {last_user.name if last_user else 'None'}")
        
        # 最终统计
        final_count = await User.objects.count()
        print(f"\n📊 最终用户总数: {final_count}")
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db_manager.disconnect_all()
        print("✅ 数据库连接已断开")

if __name__ == "__main__":
    asyncio.run(test_objects_manager()) 