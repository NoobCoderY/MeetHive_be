from drf_yasg import openapi

TENANT_ID_HEADER = openapi.Parameter(
    'X-Tenant-ID', openapi.IN_HEADER, description="Company ID", type=openapi.IN_HEADER
)

PROJECT_ID_HEADER = openapi.Parameter(
    'X-Project-ID', openapi.IN_HEADER, description="Project ID", type=openapi.IN_HEADER
)
