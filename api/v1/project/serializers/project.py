from rest_framework import serializers
from api.v1.project.models import Project, ProjectRole, ProjectUser
from api.v1.company.serializers import CompanyListItemSerializer

class ProjectRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectRole model
    """
    class Meta:
        model = ProjectRole
        fields = ['id', 'name']
        read_only_fields = fields


class ProjectRoleWithPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectRole model
    """
    class Meta:
        model = ProjectRole
        fields = ['id', 'name', 'permissions']
        read_only_fields = fields


class ProjectUserSerializer(serializers.ModelSerializer):
    """
    Serializer for ProjectUser model
    """
    role = ProjectRoleSerializer()

    class Meta:
        model = ProjectUser
        fields = ['id', 'user', 'role']
        read_only_fields = fields


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model
    """
    users = ProjectUserSerializer(many=True)
    company = CompanyListItemSerializer()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status',
            'created_by', 'updated_by', 'company',
            'users','created_at', 'updated_at'
        ]
        read_only_fields = fields


class ProjectListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']
        read_only_fields = fields


class ProjectCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['id', 'user', 'project', 'role']
        read_only_fields = fields

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": f"{instance.user.user.get_name()}",
        }
