from rest_framework import serializers
from blog.models import Post,Category,PostComment
from accounts.models import Profile

class PostCommentSerializer(serializers.ModelSerializer):
    absolute_api_url = serializers.SerializerMethodField()
    class Meta:
        model = PostComment
        fields = ['id','post','profile','user','subject','message','absolute_api_url','created_date','updated_date','approved']
        
    def get_absolute_api_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj)

    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class PostSerializer(serializers.ModelSerializer):
    # tags = serializers.SerializerMethodField()
    snippet = serializers.CharField(source='get_snippet',read_only=True)
    # category = serializers.SlugRelatedField(many=False,slug_field='name',read_only=False,queryset=Category.objects.all())
    # category = CategorySerializer()
    relative_url = serializers.URLField(source='get_relative_api_url',read_only=True)
    absolute_api_url = serializers.SerializerMethodField(method_name='abs_api_url')
    image_url = serializers.URLField(source='get_absolute_image_url',read_only=True)
    email = serializers.EmailField(source='author.user.email',read_only=True)
    name = serializers.CharField(source='author.first_name',read_only=True)
    class Meta:
        model = Post
        fields = ['id','image','image_url','author','name','email','title','snippet','content','category','counted_views','status','login_require','relative_url','absolute_api_url','published_date']
        read_only_fields = ['author','counted_views','snippet']
        # fields = '__all__'
    def get_tags(self, obj):
        return list(obj.tags.names())  # Convert tags to a list of tag names
    
    def abs_api_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)        
        # return request.build_absolute_uri(obj.get_relative_api_url())
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)        
        rep['category'] = CategorySerializer(instance.category,context={'request':request}).data
        rep['name'] = instance.author.first_name + ' ' + instance.author.last_name
        # rep['author'] = instance.author.user.email
        # rep['topic'] = instance.topic.name 
        
        if request.parser_context['kwargs'].get('pk'):
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_api_url', None)
            return rep
        rep.pop('content', None)      
        return rep
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)