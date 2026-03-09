from rest_framework.permissions import BasePermission

class PuedeFinalizarOrden(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("mantenimiento.puede_finalizar_orden")
    
class PuedeAprobarOrden(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("mantenimiento.puede_aprobar_orden")
    
class PuedeVerDashboard(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("mantenimiento.puede_ver_dashboard")
    

    
